# cli-helper-92

`cli-helper-92` is a lightweight Python utility designed to streamline common terminal tasks and automate repetitive command-line workflows. It provides a robust interface for managing system processes and configuration files without the overhead of heavy framework dependencies.

## Features

*   **Process Orchestrator:** Effortlessly spawn, monitor, and terminate background sub-processes with real-time logging.
*   **Dynamic Config Parser:** Automatic detection and synchronization of local `.yaml` and `.json` configuration files into Python objects.
*   **Interactive Prompts:** Built-in boilerplate for CLI menus, spinners, and progress bars to enhance user experience.
*   **Cross-Platform Path Handling:** Native abstraction layer for filesystem operations ensuring compatibility across Linux, macOS, and Windows.

## Installation

Ensure you have Python 3.8 or higher installed. Install the package via pip:

```bash
pip install cli-helper-92
```

To install from source for development:

```bash
git clone https://github.com/Developer/cli-helper-92.git
cd cli-helper-92
pip install -e .
```

## Basic Usage

Import the `TaskRunner` to handle execution chains or use the `ConfigLoader` to manage your app settings:

```python
from cli_helper_92 import TaskRunner, ConfigLoader

# Load your configuration
config = ConfigLoader.load("settings.yaml")

# Execute a system command with progress tracking
runner = TaskRunner()
runner.run("echo 'Hello, World!'")

# Access config values directly
print(f"Loaded environment: {config.get('env')}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.