# GitHub Security Tool

This project is designed to scan and remediate GitHub accounts.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Scanner](#running-the-scanner)
  - [Running the Remediation](#running-the-remediation)
  - [Running the Orchestrator](#running-the-orchestrator)
- [Extending the Project](#extending-the-project)

## Overview

The Scanner and Remediation project provides tools to:

1. Scan GitHub accounts for misconfigurations.
2. Remediate identified misconfigurations.

## Getting Started

### Prerequisites

- Python 3.7+
- GitHub account with a personal access token

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/github-security-tool.git
   cd github-security-tool
    ```
2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
### Configuration

Create a .env file in the project root directory and add your GitHub token:
    ```
    GITHUB_TOKEN=your_github_token
    ```

## Usage
### Running the Scanner
To run the GitHub scanner independently, execute the following command:

```bash
python -m src.scanner.scanner.py --repo-name name-of-your-repository
```
This will scan your GitHub account and save the scan results to a JSON file in the results directory.

The --repo-name flag is optional and specify the branch to scan.

### Running the Remediation
To run the GitHub remediation independently, execute the following command:

```bash
python -m src.remediation.remediation.py --scanner-results-path path/to/your/scanner_results.json --remediation-user-interface True
```

the --scanner-results-path flag is optional and specifies the scanner results file path. 

the --remediation-user-interface flag is optional and specify weather to enable the remediation user interface. 

### Running the Orchestrator
The orchestrator handles running both the scanner and the remediation sequentially. To run the orchestrator, execute:

```bash
python -m src.orchestrator
```
This will run the scanner and immediately follow up with the remediation based on the scan results.
