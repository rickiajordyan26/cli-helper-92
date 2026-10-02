# cli-helper-92

`cli-helper-92` is a lightweight Python utility designed to streamline common CLI workflows by automating repetitive task execution. It provides a robust wrapper around standard system operations to ensure cross-platform consistency for shell scripting.

## Features

*   **Task Orchestration:** Execute complex multi-step terminal workflows using simple, chainable configuration files.
*   **Intelligent Logging:** Automatically captures and timestamps stdout/stderr streams to dedicated log files for easier debugging.
*   **Environment Validation:** Built-in checks to verify that required system dependencies are present before triggering execution.
*   **Cross-Platform Core:** Optimized for native performance on macOS, Linux, and Windows Subsystem for Linux (WSL).

## Installation

Install the package directly via pip:

```bash
pip install cli-helper-92
```

To install from source for development purposes:

```bash
git clone https://github.com/Developer/cli-helper-92.git
cd cli-helper-92
pip install -e .
```

## Usage

Define your command tasks in a `tasks.yaml` file and execute them with a single command.

**Example `tasks.yaml`:**
```yaml
build:
  command: "python setup.py sdist bdist_wheel"
  description: "Package the application"
```

**Running the tool:**
```bash
cli-helper run build --verbose
```

You can also list all available tasks defined in your configuration:

```bash
cli-helper list
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.