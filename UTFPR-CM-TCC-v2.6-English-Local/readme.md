# UTFPR-CM v2.6 — English-language variant

This is a **separate English-ready adaptation** of the UTFPR-CM v2.6 LaTeX template included in the supplied backup. The original Portuguese reference template has not been modified.

## Overleaf configuration
- **Compiler:** `pdfLaTeX`
- **TeX Live version:** `TeXLive-Latest`
- **Main document:** `main.tex`

The file `main.tex` selects `english` as the primary Babel language, while keeping `brazil` available for optional Portuguese sections. The UTFPR class's English definitions and targeted corrections ensure captions use **Table** and **Figure**; the front matter uses **List of Tables**, **List of Figures**, **List of Abbreviations and Acronyms**, and **Contents**. References, source notices, the approval date and the sample text are also English.

## Getting started
1. Import the complete project ZIP into UTFPR Overleaf (New Project → Upload Project) or another Overleaf installation.
2. Set the options listed above and compile `main.tex`.
3. Edit `variaveis.tex` to provide **your own** academic data. The provided details are sample placeholders, not real students or faculty.
4. Replace the English sample chapters in `capitulos/` and the English abstract in `PreTexto/abstract.tex`.
5. Keep `utfpr.cls`, `configuracoes.tex`, `main.bib`, images and the other class support assets unless you understand the consequences.
6. Decide whether to include acknowledgments, dedication, Portuguese resumo, appendices or annexes by uncommenting the relevant commands in `main.tex`.

## Language details
- The *primary language* is set at the `\documentclass` options in `main.tex`: **`brazil, english`**, with `english` last. The file also passes `main=english` to Babel.
- The UTFPR-specific macros in `utfpr.cls` retain their names (e.g., `\incluirlistadetabelas`), but their **rendered output** uses English labels.
- The demonstration includes a real table with `\caption`, a figure, bibliography citation, and glossary acronyms.
- English abstract is provided as the main abstract. A Portuguese resumo can be enabled separately; check the language of its heading and its keywords to meet your program's specific requirements.
- Official Portuguese institutional names, source references, and authors' proper names may remain Portuguese intentionally.

## Compatibility corrections
- The UTFPR class's English-language label definitions were completed and typographical strings translated where appropriate.
- Replaced `\glossarystyle{long}` by `\setglossarystyle{long}` in the customized glossary style.
- Removed the unsafe `\xmakefirstuc` applied to complete numbered table-of-contents entries, which can fail in newer TeX Live.
- Replaced the **malformed v2.6 project-local `abntex2-alf.bst`** with the valid `abntex2-alf.bst` from the provided v2.5a reference folder, retaining ABNT-style BibTeX processing. The original v2.6 bibliography style has known syntax/stack errors when tested against real bibliographies.
- Translated built-in title-page/approval-page/source/license explanatory text for this English adaptation.
- Retained original sample source text (where applicable) in `reference-portuguese/`, which is **not included** in the build.

## Caveats
- This is an **unofficial adaptation**, not a UTFPR- or ABNT-approved replacement. Confirm with your advisor and library whether an English manuscript, abstract, and cover-page formatting are accepted.
- `pdfx` requests PDF/A-3b, which does **not** establish PDF/A compliance on its own; validate separately if required.
- The text in `variaveis.tex` and example chapters is illustrative and must be replaced.
- Simply importing this standalone template does not change the language of any existing thesis project. To update an existing project, adapt its main class options and the English-specific class fixes, while preserving its substantive source.
