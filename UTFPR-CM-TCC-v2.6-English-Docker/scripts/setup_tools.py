#!/usr/bin/env python3
"""Best-effort OS-native prerequisite installation with explicit consent."""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def say(message): print('[setup] '+message, flush=True)


def has(tool): return shutil.which(tool) is not None


def run(args, description, *, env=None):
    say(description+': '+' '.join(map(str,args)))
    try:
        subprocess.run(args, check=True, env=env)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f'{description} failed with exit code {exc.returncode}') from exc
    except FileNotFoundError as exc:
        raise RuntimeError(f'Required installer not found: {args[0]}') from exc


def consent(message, auto_yes, no_install):
    if no_install:
        raise RuntimeError(message+' Automatic installation disabled (--no-install).')
    say(message)
    if auto_yes: return
    if not sys.stdin.isatty():
        raise RuntimeError('Installation requires a user decision. Run in a terminal or supply --yes.')
    answer=input('Install the missing prerequisite? [y/N] ').strip().lower()
    if answer not in ('y','yes','s','sim'):
        raise RuntimeError('Installation declined. No system changes made.')


def elevate_prefix():
    if os.name=='nt':return []
    if hasattr(os,'geteuid') and os.geteuid()==0:return []
    if has('sudo'):return ['sudo']
    raise RuntimeError('Administrator rights are required to install system packages; sudo was not found.')


def linux_package_manager():
    if has('apt-get'): return 'apt'
    if has('dnf'):return 'dnf'
    if has('pacman'):return 'pacman'
    return None


def install_linux(packages):
    manager=linux_package_manager()
    if manager is None:
        raise RuntimeError('No supported package manager (apt, dnf, pacman) found; install dependencies manually.')
    elevate=elevate_prefix()
    if manager=='apt':
        run(elevate+['apt-get','update'],'Refresh apt repository indexes')
        run(elevate+['apt-get','install','-y']+packages['apt'],'Install Debian/Ubuntu packages')
    elif manager=='dnf':
        run(elevate+['dnf','install','-y']+packages['dnf'],'Install Fedora packages')
    elif manager=='pacman':
        run(elevate+['pacman','-Sy','--needed','--noconfirm']+packages['pacman'],'Install Arch packages')


def maybe_add_executable_dirs():
    candidates=[]
    if sys.platform=='darwin':
        candidates += ['/opt/homebrew/bin','/usr/local/bin','/Library/TeX/texbin','/Applications/Docker.app/Contents/Resources/bin']
    elif sys.platform=='win32':
        for prefix in [os.environ.get('ProgramFiles',r'C:\Program Files'), os.environ.get('LOCALAPPDATA','')]:
            if prefix:
                candidates.extend([str(Path(prefix)/'Docker'/'Docker'/'resources'/'bin'),str(Path(prefix)/'Programs'/'DockerDesktop'/'resources'/'bin'),str(Path(prefix)/'MiKTeX'/'miktex'/'bin'/'x64'),str(Path(prefix)/'Programs'/'MiKTeX'/'miktex'/'bin'/'x64')])
    else:
        candidates += ['/usr/local/bin','/usr/bin']
    old=os.environ.get('PATH','').split(os.pathsep)
    os.environ['PATH']=os.pathsep.join([path for path in candidates if Path(path).is_dir() and path not in old]+old)


def ensure_homebrew(auto_yes, no_install):
    maybe_add_executable_dirs()
    if has('brew'):return
    consent('Homebrew is required for the automatic macOS installation. It may request system permissions and Apple command-line tools.', auto_yes,no_install)
    # Official installer is served over HTTPS. Users are informed and authorize execution.
    import tempfile
    from urllib.request import urlopen
    url='https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh'
    say('Downloading the official Homebrew installer: '+url)
    with urlopen(url, timeout=40) as response:
        content=response.read(250000)
    if b'HOMEBREW' not in content.upper():
        raise RuntimeError('Downloaded Homebrew installer did not pass basic content validation.')
    with tempfile.TemporaryDirectory() as tmp:
        script=Path(tmp)/'install-homebrew.sh';script.write_bytes(content)
        run(['/bin/bash',str(script)],'Install Homebrew')
    maybe_add_executable_dirs()
    if not has('brew'):raise RuntimeError('Homebrew installed, but not yet on PATH. Reopen the terminal and try again.')


def install_docker(auto_yes,no_install):
    consent('Docker is not installed. Install Docker Desktop on macOS/Windows or Docker Engine on Linux? Docker Desktop has separate terms and may need a reboot or administrator approval.',auto_yes,no_install)
    if sys.platform=='win32':
        if not has('winget'):raise RuntimeError('Windows Package Manager (winget) is required. Update App Installer from Microsoft Store first.')
        run(['winget','install','--id','Docker.DockerDesktop','--exact','--silent','--accept-package-agreements','--accept-source-agreements'],'Install Docker Desktop')
    elif sys.platform=='darwin':
        ensure_homebrew(auto_yes,no_install)
        run(['brew','install','--cask','docker'],'Install Docker Desktop')
    elif sys.platform.startswith('linux'):
        install_linux({'apt':['docker.io'],'dnf':['moby-engine','docker-cli'],'pacman':['docker']})
        if has('systemctl'):
            try:run(elevate_prefix()+['systemctl','enable','--now','docker'],'Start Docker Engine')
            except RuntimeError as exc:say('Docker service startup was not automatic: '+str(exc))
    else:raise RuntimeError('This operating system is not supported for Docker installation.')
    maybe_add_executable_dirs()


def running_docker(prefix):
    try:
        return subprocess.run(prefix+['info','--format','{{.ServerVersion}}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=15).returncode==0
    except (OSError,subprocess.TimeoutExpired):return False


def launch_docker():
    if sys.platform=='darwin':
        run(['open','-a','Docker'],'Start Docker Desktop')
    elif sys.platform=='win32':
        names=[]
        for base in [os.environ.get('ProgramFiles',r'C:\Program Files'), os.environ.get('LOCALAPPDATA','')]:
            names += [str(Path(base)/'Docker'/'Docker'/'Docker Desktop.exe'),str(Path(base)/'Programs'/'DockerDesktop'/'Docker Desktop.exe')]
        found=next((p for p in names if Path(p).is_file()),None)
        if not found:raise RuntimeError('Docker Desktop app not found; start Docker Desktop from the Start menu.')
        subprocess.Popen([found],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        say('Docker Desktop launch requested.')
    elif sys.platform.startswith('linux') and has('systemctl'):
        run(elevate_prefix()+['systemctl','start','docker'],'Start Docker Engine')


def ensure_docker(no_install=False,auto_yes=False):
    maybe_add_executable_dirs()
    if not has('docker'):
        install_docker(auto_yes,no_install)
    if not has('docker'):
        raise RuntimeError('Docker CLI is not on PATH after installation. Reopen terminal or finish installation and retry.')
    if running_docker(['docker']):return ['docker']
    try:launch_docker()
    except RuntimeError as exc:say(str(exc))
    # When Linux restricts the Docker socket to the docker group, a one-time
    # interactive sudo authentication can make the current invocation work.
    # Group membership itself takes effect only after a new login.
    if sys.platform.startswith('linux') and has('sudo'):
        authentication = subprocess.run(['sudo','-v'],check=False)
        if authentication.returncode == 0 and running_docker(['sudo','-n','docker']):
            say('Using sudo -n docker; a new login may be required for unprivileged Docker.')
            return ['sudo','-n','docker']
    # Docker Desktop can take time to initialize its VM/WSL backend.
    for _ in range(60):
        if running_docker(['docker']):return ['docker']
        time.sleep(3)
    # On Linux, sudo may be usable without modifying docker group membership.
    if sys.platform.startswith('linux') and has('sudo') and running_docker(['sudo','-n','docker']):
        say('Docker requires sudo for this session. Using sudo -n docker.')
        return ['sudo','-n','docker']
    raise RuntimeError('Docker daemon is unavailable. Finish Docker Desktop first-run consent, enable WSL2/virtualization if requested, restart or re-login when necessary, and retry.')


def ensure_image(prefix,image,refresh=False):
    inspect=subprocess.run(prefix+['image','inspect',image],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=False)
    if inspect.returncode!=0 or refresh:
        run(prefix+['pull',image],'Download TeX Live image (first run may be several GB)')
    else:say('Using cached TeX image: '+image)


def install_native(auto_yes,no_install):
    consent('A complete LaTeX toolchain is not detected. Install TeX Live (macOS/Linux) or MiKTeX (Windows)? Downloads may require several gigabytes and administrator approval.',auto_yes,no_install)
    if sys.platform=='win32':
        if not has('winget'):raise RuntimeError('Install or update Microsoft App Installer to obtain winget, then retry.')
        run(['winget','install','--id','MiKTeX.MiKTeX','--exact','--silent','--accept-package-agreements','--accept-source-agreements'],'Install MiKTeX')
    elif sys.platform=='darwin':
        ensure_homebrew(auto_yes,no_install)
        run(['brew','install','--cask','mactex-no-gui'],'Install TeX Live via MacTeX (no GUI)')
    elif sys.platform.startswith('linux'):
        install_linux({'apt':['texlive-full','latexmk'],'dnf':['texlive-scheme-full','latexmk'],'pacman':['texlive-meta','texlive-binextra']})
    else:raise RuntimeError('Unsupported operating system for automatic LaTeX installation.')
    maybe_add_executable_dirs()


def ensure_native(no_install=False,auto_yes=False):
    maybe_add_executable_dirs()
    required=['pdflatex','makeindex']
    missing=[name for name in required if not has(name)]
    if not (has('bibtex8') or has('bibtex')):missing.append('bibtex8/bibtex')
    if missing:
        say('Missing: '+', '.join(missing))
        install_native(auto_yes,no_install)
        missing=[name for name in required if not has(name)]
        if not (has('bibtex8') or has('bibtex')):missing.append('bibtex8/bibtex')
        if missing:raise RuntimeError('LaTeX installed but commands not available on PATH: '+', '.join(missing)+'. Reopen your terminal or finish setup, then retry.')
    say('Native LaTeX tools found: '+shutil.which('pdflatex'))
