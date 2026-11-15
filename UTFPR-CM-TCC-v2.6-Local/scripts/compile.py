#!/usr/bin/env python3
"""Self-contained TeX build runner. Requires only Python 3.9+ and OS tools."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / 'build-config.json').read_text(encoding='utf-8'))
DEFAULT_IMAGE = 'texlive/texlive:latest'
SKIP_DIRS = {'.git','.build','build','__MACOSX','.venv','venv','node_modules','__pycache__','.pytest_cache'}
SKIP_SUFFIXES = {'.aux','.log','.bbl','.blg','.fls','.fdb_latexmk','.synctex.gz','.toc','.lof','.lot','.out','.idx','.ilg','.ind','.nlo','.nls','.acn','.acr','.gls','.glo','.glg','.mw','.xmpi','.run.xml','.bcf','.dvi','.xdv','.fns','.maf','.mtc','.lol','.loa','.alg','.acn2','.acn3','.acr2','.acr3','.glg2','.glg3','.bak'}


def say(msg):
    print(msg, flush=True)


def cmd_exists(cmd):
    return shutil.which(cmd) is not None


def short_id(source: Path, name: str) -> str:
    if source.resolve() == ROOT.resolve():
        return 'default'
    slug = re.sub(r'[^a-zA-Z0-9_.-]+', '-', source.name).strip('-')[:35] or 'project'
    digest = hashlib.sha256(str(source.resolve()).encode('utf-8')).hexdigest()[:8]
    return f'{slug}-{digest}'


def copy_worktree(src: Path, dst: Path):
    """Use a private copy so nested TeX \\include/*.aux files remain writable."""
    if dst.exists():
        shutil.rmtree(dst)
    def ignore(directory, names):
        ignored = []
        for name in names:
            path = Path(directory) / name
            if path.is_dir() and (name in SKIP_DIRS or name.startswith('.git')):
                ignored.append(name)
            elif path.is_file() and (name == '.DS_Store' or name.startswith('._') or path.suffix in SKIP_SUFFIXES or name.endswith('.synctex.gz')):
                # Real .pdf figures must be kept; generated top-level main.pdf is excluded below.
                ignored.append(name)
        return ignored
    shutil.copytree(src, dst, ignore=ignore)
    # Exclude only the selected main's old output, never figure/source PDFs.
    if (dst / 'main.pdf').exists():
        (dst / 'main.pdf').unlink()


def resolve_project(argument: str | None, main_name: str):
    if argument is None:
        project = ROOT
    else:
        selected = Path(argument).expanduser().resolve()
        if selected.is_file():
            main_name = selected.name
            project = selected.parent
        elif selected.is_dir():
            project = selected
        else:
            raise RuntimeError(f'LaTeX project not found: {selected}')
    m = Path(main_name)
    if m.is_absolute() or '..' in m.parts:
        raise RuntimeError('The --main argument must be a relative .tex path inside the project.')
    if not (project / m).is_file():
        raise RuntimeError(f'Main document not found: {project / m}')
    return project, m


class CommandRunner:
    def __init__(self, log: Path, cwd: Path, docker_prefix: list[str] | None, image: str, work: Path):
        self.log = log
        self.cwd = cwd
        self.docker_prefix = docker_prefix
        self.image = image
        self.work = work
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text('', encoding='utf-8')

    def execute(self, args: list[str], label: str, ignore_errors=False):
        command = list(args)
        if self.docker_prefix is not None:
            command = self.docker_prefix + [
                'run', '--rm', '--mount', f'type=bind,source={self.work.resolve()},target=/workspace',
                '-w', '/workspace',
            ] + self._container_user() + [self.image] + args
        say(f'[{label}] {" ".join(args)}')
        with self.log.open('a', encoding='utf-8', errors='replace') as out:
            out.write(f'\n===== {label}: {" ".join(command)} =====\n'); out.flush()
            try:
                result = subprocess.run(command, cwd=self.cwd, stdout=out, stderr=subprocess.STDOUT, check=False)
            except OSError as exc:
                out.write(f'COMMAND FAILED TO START: {exc}\n')
                raise RuntimeError(f'{label} could not start: {exc}') from exc
            out.write(f'\n===== EXIT CODE {result.returncode} =====\n');out.flush()
        if result.returncode != 0 and not ignore_errors:
            raise RuntimeError(f'{label} failed (exit {result.returncode}); see {self.log}')
        return result.returncode

    @staticmethod
    def _container_user():
        if os.name != 'nt' and sys.platform != 'darwin' and hasattr(os, 'getuid'):
            # Linux bind mounts must not create root-owned generated files.
            return ['--user', f'{os.getuid()}:{os.getgid()}','-e','HOME=/tmp']
        return []


def pick_bibtex(docker: bool):
    if docker: return 'bibtex8'
    if cmd_exists('bibtex8'):return 'bibtex8'
    if cmd_exists('bibtex'):return 'bibtex'
    raise RuntimeError('Neither bibtex8 nor bibtex is installed.')


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def stable_snapshot(work: Path, stem: str):
    files = [work / f'{stem}.{ext}' for ext in ('aux','toc','lof','lot','out')]
    # Changes in nested include aux files also need another pass.
    files += [p for p in work.rglob('*.aux') if p.parent != work]
    return {p.relative_to(work).as_posix(): checksum(p) for p in files}


def arrange_logs(work: Path, logs_dir: Path, stem: str):
    for ext in ('log','blg','ilg','nlg','alg','fls'):
        p = work / f'{stem}.{ext}'
        if p.is_file():
            shutil.copy2(p, logs_dir / f'{stem}.{ext}')


def build(args):
    source, main = resolve_project(args.project, args.main)
    project_id = short_id(source, main.name)
    work = ROOT / '.build' / 'work' / project_id
    output = ROOT / 'build' / ('output' if project_id == 'default' else f'output-{project_id}')
    logs = ROOT / 'build' / 'logs' / project_id
    logs.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    log_file = logs / 'build.log'
    # Ensure that even preflight failures preserve a build log.
    log_file.write_text('UTFPR Local Build -- build preflight\n', encoding='utf-8')
    try:
        import setup_tools
        use_docker = CONFIG['mode'] == 'docker'
        if use_docker:
            docker_prefix = setup_tools.ensure_docker(args.no_install, args.yes)
            image = args.image or os.environ.get('TEXLIVE_IMAGE', CONFIG.get('docker_image', DEFAULT_IMAGE))
            setup_tools.ensure_image(docker_prefix, image, refresh=args.refresh_image)
        else:
            setup_tools.ensure_native(args.no_install, args.yes)
            docker_prefix = None
            image = ''
        say(f'Project: {source}\nMain: {main}\nEngine: {"Docker / " + image if use_docker else "native TeX"}')
        copy_worktree(source, work)
        cwd = work
        runner = CommandRunner(log_file, cwd, docker_prefix, image, work)
        # Generate outputs in the working root, avoiding TeX -output-directory
        # and broken nested \\include auxiliary paths.
        stem = main.stem
        base_flags = ['-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder']
        if not use_docker and sys.platform == 'win32':
            # MiKTeX supports installing missing packages on demand.
            version = subprocess.run(['pdflatex','--version'],capture_output=True,text=True,check=False)
            if 'miktex' in version.stdout.lower(): base_flags += ['--enable-installer']
        # Strictly optional shell escape: not needed for included PDF/PNG/EPS source files.
        if args.shell_escape:
            base_flags.append('-shell-escape')
        runner.execute(['pdflatex'] + base_flags + [main.as_posix()], 'pdflatex pass 1')
        aux_file = work / (stem + '.aux')
        if not aux_file.exists():
            raise RuntimeError(f'Expected auxiliary file not created: {aux_file}')
        aux_text = aux_file.read_text(encoding='utf-8', errors='replace')
        if '\\bibdata{' in aux_text:
            bib_cmd = pick_bibtex(use_docker)
            # TeX Live needs the -8 argument for UTF-8-preserving BibTeX8.
            if bib_cmd == 'bibtex8':
                runner.execute([bib_cmd,'-8',stem], 'BibTeX8 references')
            else:
                runner.execute([bib_cmd,stem], 'BibTeX references')
        if (work / (stem + '.idx')).exists() and (work / (stem + '.idx')).stat().st_size > 0:
            runner.execute(['makeindex', stem + '.idx'], 'MakeIndex')
        if (work / (stem + '.nlo')).exists() and (work / (stem + '.nlo')).stat().st_size > 0:
            runner.execute(['makeindex', stem+'.nlo', '-s','nomencl.ist','-o',stem+'.nls'], 'Nomenclature')
        previous = None
        converged = False
        for pass_number in range(2, args.max_passes+1):
            runner.execute(['pdflatex'] + base_flags + [main.as_posix()], f'pdflatex pass {pass_number}')
            now = stable_snapshot(work,stem)
            if now == previous and pass_number >= 3:
                converged = True
                say(f'Auxiliary files converged at pass {pass_number}.')
                break
            previous = now
        else:
            say(f'NOTICE: {args.max_passes} passes completed; convergence not established.')
        pdf = work / (stem+'.pdf')
        if not pdf.is_file() or pdf.stat().st_size < 200:
            raise RuntimeError(f'No valid PDF generated: {pdf}')
        dest = output / pdf.name
        tmp = output / (pdf.name + '.new')
        shutil.copy2(pdf,tmp);tmp.replace(dest)
        if project_id == 'default':
            # Convenience copy for beginner users. Only update after a successful build.
            convenience = ROOT / pdf.name
            tmp_root = ROOT / (pdf.name + '.new')
            shutil.copy2(pdf,tmp_root);tmp_root.replace(convenience)
        arrange_logs(work, logs, stem)
        diagnostic = (work / (stem+'.log')).read_text(encoding='utf-8', errors='replace')
        warning_lines = [line.strip() for line in diagnostic.splitlines() if ('Warning:' in line or line.startswith('Overfull \\') or line.startswith('Underfull \\'))]
        report = {'project':str(source),'main':main.as_posix(),'mode':CONFIG['mode'],'image':image or None,'pdf':str(dest),'warnings':warning_lines,'warning_count':len(warning_lines),'aux_converged':converged}
        (logs/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        say(f'SUCCESS: PDF: {dest}\nFULL LOG: {log_file}\nTEX LOG: {logs / (stem + ".log")}\nReported warnings: {len(warning_lines)} (see report.json)')
        if args.strict and warning_lines:
            raise RuntimeError('Strict mode: PDF built, but warnings remain; see report.json')
        return 0
    except Exception as exc:
        logs.mkdir(parents=True,exist_ok=True)
        with log_file.open('a',encoding='utf-8') as stream:
            stream.write(f'\nBUILD FAILED: {exc}\n'+traceback.format_exc()+'\n')
        if work.exists():
            arrange_logs(work,logs,main.stem)
        say(f'ERROR: {exc}\nFULL LOG: {log_file}')
        return 1


def doctor(args):
    import setup_tools
    say(f'Project: {ROOT}\nMode: {CONFIG["mode"]}\nPlatform: {sys.platform}\nPython: {sys.version.split()[0]}')
    cmds = ['docker'] if CONFIG['mode']=='docker' else ['pdflatex','bibtex8','bibtex','makeindex']
    for cmd in cmds:
        say(f'{cmd}: {shutil.which(cmd) or "not found"}')
    return 0


def clean(args):
    build_dir = ROOT / '.build'
    if build_dir.exists():shutil.rmtree(build_dir)
    say('Removed the private compilation workspace (.build). Exported PDF and logs are preserved.')
    return 0


def setup(args):
    import setup_tools
    if CONFIG['mode']=='docker':
        docker_prefix=setup_tools.ensure_docker(args.no_install,args.yes)
        image=args.image or os.environ.get('TEXLIVE_IMAGE',CONFIG.get('docker_image',DEFAULT_IMAGE))
        setup_tools.ensure_image(docker_prefix,image,refresh=args.refresh_image)
    else:
        setup_tools.ensure_native(args.no_install,args.yes)
    say('Prerequisites are ready.')
    return 0


def main():
    parser=argparse.ArgumentParser(description='UTFPR-CM LaTeX compiler (native or Docker).')
    parser.add_argument('action',nargs='?',choices=['compile','doctor','setup','clean'],default='compile')
    parser.add_argument('--project','-p',help='Project directory or .tex file (default: this repository).')
    parser.add_argument('--main',default='main.tex',help='Main document path relative to project (default: main.tex).')
    parser.add_argument('--yes','-y',action='store_true',help='Approve supported prerequisite installation (OS prompts may still appear).')
    parser.add_argument('--no-install',action='store_true',help='Never attempt to install software.')
    parser.add_argument('--image',help='Override Docker image.')
    parser.add_argument('--refresh-image',action='store_true',help='Pull selected Docker image even when cached.')
    parser.add_argument('--shell-escape',action='store_true',help='Explicitly allow TeX shell-escape for trusted projects.')
    parser.add_argument('--max-passes',type=int,default=5,choices=range(3,11),metavar='3..10')
    parser.add_argument('--strict',action='store_true',help='Fail if final LaTeX log reports warnings.')
    args=parser.parse_args()
    if args.action=='compile':return build(args)
    if args.action=='doctor':return doctor(args)
    if args.action=='clean':return clean(args)
    if args.action=='setup':return setup(args)
    return 2


if __name__=='__main__':
    sys.exit(main())
