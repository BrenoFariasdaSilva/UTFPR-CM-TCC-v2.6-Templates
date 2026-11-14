<div align="center">
  
# [UTFPR-CM-TCC-v2.6-Templates.](https://github.com/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates) <img src="https://github.com/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates/blob/d4173c3b2249a77b6b1a223b86e801ea2042eddc/.assets/Icons/GitHub%20Colored%20Icon.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Four automated LaTeX TCC v2.6 templates for UTFPR Campo Mourão, available in Portuguese and English with Docker or local compilation on Windows, macOS, and Linux. Includes dependency setup, bibliography processing, acronym lists, PDF generation, and full build logs.
  
---

</div>

<div align="center">

![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![GitHub Commits](https://img.shields.io/github/commit-activity/t/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates/main)
![GitHub Last Commit](https://img.shields.io/github/last-commit/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![GitHub Forks](https://img.shields.io/github/forks/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![GitHub Language Count](https://img.shields.io/github/languages/count/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![GitHub License](https://img.shields.io/github/license/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![GitHub Stars](https://img.shields.io/github/stars/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![GitHub Contributors](https://img.shields.io/github/contributors/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![GitHub Created At](https://img.shields.io/github/created-at/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates)
![wakatime](https://wakatime.com/badge/github/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates.svg)

</div>

<div align="center">
  
![RepoBeats Statistics](https://repobeats.axiom.co/api/embed/e1194b1207a4250b450f4c82aa87ff003f24b902.svg "Repobeats analytics image")

</div>

## Table of Contents
- [UTFPR-CM-TCC-v2.6-Templates. ](#utfpr-cm-tcc-v26-templates-)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Setup](#setup)
    - [Clone the repository](#clone-the-repository)
  - [Installation:](#installation)
  - [Run Programing Language Code:](#run-programing-language-code)
    - [Dependencies](#dependencies)
    - [Dataset - Optional](#dataset---optional)
  - [Usage](#usage)
  - [Results - Optional](#results---optional)
  - [How to Cite?](#how-to-cite)
  - [Contributing](#contributing)
  - [Collaborators](#collaborators)
  - [License](#license)
    - [Apache License 2.0](#apache-license-20)

## Introduction

This repository provides four versions of the **UTFPR Campo Mourão TCC v2.6 LaTeX template**, combining two document languages (Portuguese and English) with two compilation methods (Docker and native LaTeX). Each version is a self-contained project with automated compilation, bibliography and acronym processing, and PDF/log generation.

| Language | Compilation method | Project directory |
|---|---|---|
| Portuguese | Docker | `UTFPR-CM-TCC-v2.6-Docker/` |
| English | Docker | `UTFPR-CM-TCC-v2.6-English-Docker/` |
| English | Local (without Docker) | `UTFPR-CM-TCC-v2.6-English-Local/` |
| Portuguese | Local (without Docker) | `UTFPR-CM-TCC-v2.6-Local/` |

The templates support Windows, macOS, and Linux. This is an independent community project, not an official UTFPR distribution. University formatting requirements and final PDF/A conformance must still be verified independently.

## Requirements

- **For one-click use:** a Windows, macOS, or Linux computer and permission to run the appropriate starter script. GNU Make is not required for these launchers.
- **For terminal commands:** GNU Make and Python 3.9 or newer. On Windows, GNU Make is not installed by default; use the Windows launcher if Make is unavailable.
- **Docker variants:** Docker Desktop or Docker Engine. The scripts detect Docker and offer installation/startup where supported.
- **Local variants:** a working LaTeX distribution (MiKTeX on Windows, MacTeX on macOS, or TeX Live on Linux), or permission to install it through the provided setup workflow.
- **For first-time setup:** an internet connection, sufficient disk space (possibly several gigabytes), and any administrator permissions, license confirmations, virtualization support, or restart required by the operating system.

## Setup

### Clone the repository

1. Clone the repository with the following command:

   ```bash
   git clone https://github.com/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates.git
   cd UTFPR-CM-TCC-v2.6-Templates
   ```

## Installation:

* Programing Language:

  * Manually:
      ```bash
      # Programing Language:
      sudo apt install program-language -y
      ```

  * Using Makefile:
      ```bash
      make install
      ```

  * Using ShellScript:
      ```bash
      chmod +x install.sh
      sudo ./install.sh
      ```  

## Run Programing Language Code:

```bash
# Command here 
```

### Dependencies

1. Install the project dependencies with the following command:

   ```bash
   make dependencies
   ```

### Dataset - Optional

1. Download the dataset from [WEBSITE-HERE]() and place it in this project directory `(/UTFPR-CM-TCC-v2.6-Templates)` and run the following command:

   ```bash
   make dataset
   ```

## Usage

In order to run the project, run the following command:

```bash
make run
```

## Results - Optional

Discuss the results obtained in the project.

## How to Cite?

If you use the UTFPR-CM-TCC-v2.6-Templates in your research, please cite it using the following BibTeX entry:

```
@misc{softwareUTFPR-CM-TCC-v2.6-Templates:2026,
  title        = {{UTFPR-CM-TCC-v2.6-Templates}: Automated Cross-Platform LaTeX Compilation Templates for UTFPR Campo Mourão},
  author       = {Breno Farias da Silva},
  year         = {2026},
  howpublished = {\url{https://github.com/BrenoFariasdaSilva/UTFPR-CM-TCC-v2.6-Templates}},
  note         = {A collection of four UTFPR-CM TCC v2.6 LaTeX templates in Portuguese and English, supporting automated compilation with Docker or native tools on Windows, macOS, and Linux. Accessed on November 14, 2026}
}
```

Additionally, a `main.bib` file is available in the root directory of this repository, in which contains the BibTeX entry for this project.

If you find this repository valuable, please don't forget to give it a ⭐ to show your support! Contributions are highly encouraged, whether by creating issues for feedback or submitting pull requests (PRs) to improve the project. For details on how to contribute, please refer to the [Contributing](#contributing) section below.

Thank you for your support and for recognizing the contribution of this tool to your work!

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. If you have suggestions for improving the code, your insights will be highly welcome.
In order to contribute to this project, please follow the guidelines below or read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details on how to contribute to this project, as it contains information about the commit standards and the entire pull request process.
Please follow these guidelines to make your contributions smooth and effective:

1. **Set Up Your Environment**: Ensure you've followed the setup instructions in the [Setup](#setup) section to prepare your development environment.

2. **Make Your Changes**:
   - **Create a Branch**: `git checkout -b feature/YourFeatureName`
   - **Implement Your Changes**: Make sure to test your changes thoroughly.
   - **Commit Your Changes**: Use clear commit messages, for example:
     - For new features: `git commit -m "FEAT: Add some AmazingFeature"`
     - For bug fixes: `git commit -m "FIX: Resolve Issue #123"`
     - For documentation: `git commit -m "DOCS: Update README with new instructions"`
     - For refactorings: `git commit -m "REFACTOR: Enhance component for better aspect"`
     - For snapshots: `git commit -m "SNAPSHOT: Temporary commit to save the current state for later reference"`
   - See more about crafting commit messages in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

3. **Submit Your Contribution**:
   - **Push Your Changes**: `git push origin feature/YourFeatureName`
   - **Open a Pull Request (PR)**: Navigate to the repository on GitHub and open a PR with a detailed description of your changes.

4. **Stay Engaged**: Respond to any feedback from the project maintainers and make necessary adjustments to your PR.

5. **Celebrate**: Once your PR is merged, celebrate your contribution to the project!

## Collaborators

We thank the following people who contributed to this project:

<table>
  <tr>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://github.com/BrenoFariasdaSilva.png" width="100px;" alt="My Profile Picture"/><br>
        <sub>
          <b>Breno Farias da Silva</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## License

### Apache License 2.0

This project is licensed under the [Apache License 2.0](LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](LICENSE) file in this repository.
