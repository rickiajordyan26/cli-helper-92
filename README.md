# cli-helper-92

`cli-helper-92` is a lightweight Python utility designed to streamline command-line interactions and automate repetitive terminal workflows. It provides a robust wrapper for handling common CLI tasks, ensuring your scripts remain clean, readable, and maintainable.

### Features
* **Interactive Prompt Engine**: Simplifies the creation of complex user input flows with built-in validation and auto-completion.
* **Config Persistence**: Automatically manages local JSON/YAML configuration files to maintain user state across sessions.
* **Streamlined Logging**: Implements pre-configured color-coded logging levels to track process execution without cluttering standard output.
* **Sub-command Routing**: Offers a declarative decorator pattern to handle complex argument parsing and multi-level command nesting.

### Installation

Requires Python 3.8+ and `pip`. Install the package directly from PyPI:

```bash
pip install cli-helper-92
```

Alternatively, install from source:

```bash
git clone https://github.com/Developer/cli-helper-92.git
cd cli-helper-92
pip install .
```

### Usage

Integrate `cli-helper-92` into your project to handle argument parsing and interactive setup in seconds:

```python
from cli_helper_92 import CLIApp

app = CLIApp(name="MyTool", version="1.0.0")

@app.command(help="Greet the user")
def greet(name: str = "User"):
    app.logger.info(f"Hello, {name}!")

if __name__ == "__main__":
    app.run()
```

Run your tool from the terminal:

```bash
python main.py greet --name "Developer"
```

### License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the terms of the MIT License.