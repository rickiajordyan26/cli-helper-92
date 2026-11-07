# cli-helper-92

`cli-helper-92` is a lightweight Python utility designed to streamline common command-line interface interactions and task automation. It simplifies argument parsing, logging, and configuration management for developers building robust terminal applications.

## Features

*   **Simplified CLI Scaffolding:** Rapidly define complex subcommands and argument flags with an intuitive, chainable syntax.
*   **Automatic Configuration Persistence:** Seamlessly load and save user preferences to local JSON or YAML files with built-in validation.
*   **Structured Logging:** Integrated colorful console output and file logging with multi-level severity support.
*   **Zero-Dependency Core:** Built using only the Python standard library to ensure high performance and zero-conflicts in virtual environments.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install cli-helper-92
```

To install from the source repository:

```bash
git clone https://github.com/Developer/cli-helper-92.git
cd cli-helper-92
pip install .
```

## Usage

Define a simple command-line tool by initializing the helper and mapping functions to commands:

```python
from cli_helper_92 import CLI

app = CLI(name="my-tool", version="1.0.0")

@app.command(help="Greet the user")
def greet(name: str, formal: bool = False):
    prefix = "Greetings," if formal else "Hi"
    print(f"{prefix} {name}!")

if __name__ == "__main__":
    app.run()
```

Run your new tool from the terminal:

```bash
python my_app.py greet --name "Alice" --formal
# Output: Greetings, Alice!
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.