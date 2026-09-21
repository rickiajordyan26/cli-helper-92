[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# cli-helper-92

`cli-helper-92` is a lightweight Python toolkit designed to simplify building robust, interactive command-line interfaces with minimal boilerplate. It combines seamless argument parsing, styled terminal output, and automated configuration management into a single developer-friendly package.

## Features

* **Decorator-Based Command Routing:** Register commands, options, and type-checked arguments effortlessly using clean Python decorators.
* **Rich Terminal Outputs:** Built-in support for ANSI colors, status spinners, formatted tables, and progress bars without extra dependencies.
* **Auto-Persisted Configs:** Automatically generate, load, and save user settings in JSON or YAML formats across runtime sessions.
* **Interactive User Input:** Prompt users for text, confirmation toggles, and masked passwords with native validation rules.

## Installation

Install the package directly from PyPI using `pip`:

```bash
pip install cli-helper-92
```

Or install the development version locally:

```bash
git clone https://github.com/Developer/cli-helper-92.git
cd cli-helper-92
pip install -e .
```

## Quick Start

Create a file named `app.py`:

```python
from cli_helper_92 import CLI, style

app = CLI(name="demo", description="Quick start example using cli-helper-92")

@app.command()
def deploy(environment: str, verbose: bool = False):
    """Deploy the project to a specified environment."""
    if verbose:
        app.log("Preparing build context...", level="debug")
    
    app.spinner_start("Deploying build artifacts...")
    # Perform deployment tasks here
    app.spinner_stop()
    
    print(style.success(f"Successfully deployed to {environment}!"))

if __name__ == "__main__":
    app.run()
```

Run your command directly from the terminal:

```bash
python app.py deploy production --verbose
```

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.