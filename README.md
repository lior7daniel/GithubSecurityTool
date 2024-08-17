# GitHub Security Tool

This project is designed to scan and remediate various environments and cloud accounts. Currently, it supports scanning and remediating GitHub accounts. The project is built to be easily expanded to support additional services in the future.

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
2. Automatically remediate identified misconfigurations.

The project architecture is designed to be modular and extensible, enabling support for additional services beyond GitHub.


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
python -m src.services.github.github_scanner --service-type github
```
This will scan your GitHub account and save the scan results to a JSON file in the results/github directory.

The --service-type flag is mandatory and specifies the type of service to remediate. Currently, only "github" is supported.

### Running the Remediation
To run the GitHub remediation independently, execute the following command:

```bash
python -m src.services.github.github_remediation --service-type github --scanner-results-path path/to/your/scanner_results.json
```

Also here, the --service-type flag is mandatory and specifies the type of service to remediate. Currently, only "github" is supported.

If you do not specify --scanner-results-path, the script will automatically use the latest scan results file from the results/github directory.


### Running the Orchestrator
The orchestrator handles running both the scanner and the remediation sequentially. To run the orchestrator, execute:

```bash
python -m src.orchestrator
```
This will run the scanner and immediately follow up with the remediation based on the scan results.

## Extending the Project
To add support for additional services:

1. Create a new directory for your service under src/services.
2. Implement the client, scanner, and remediation classes similar to the GitHub implementation.
3. Update the orchestrator to include the new service.
