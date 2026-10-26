[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# cli-helper-92

`cli-helper-92` is a lightweight Python command-line utility designed to automate repetitive terminal workflows and standardize output formatting across developer environments. It seamlessly manages command execution presets, transforms standard stdout into structured formats, and tracks terminal session analytics without requiring heavy shell reconfigurations.

## Features

* **Context-Aware Execution:** Automatically injects pre-configured environment variables and flags based on your current working directory.
* **Structured Output Pipeline:** Pipes and converts raw terminal outputs directly into clean JSON, YAML, or formatted ASCII tables.
* **Interactive Command Presets:** Save, tag, and parameterize multi-step shell scripts into single executable commands with built-in argument validation.
* **Execution Audit Logs:** Tracks runtime metrics, exit codes, and output histories in a local SQLite database for quick debugging.

## Installation

Install directly via `pip`:

```bash
pip install cli-helper-92
```

Alternatively, install from source:

```bash
git clone https://github.com/Developer/cli-helper-92.git
cd cli-helper-92
pip install -e .
```

## Quick Start

Save a multi-flag command as a reusable preset:

```bash
cli-helper preset add build-image --cmd "docker build -t service:v1 . && docker scan service:v1"
```

Execute a preset and convert the output directly to JSON format:

```bash
cli-helper run build-image --format json
```

View execution logs for recent runs:

```bash
cli-helper history --limit 5
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.