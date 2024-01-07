
# sharkservers-api [![skeleton](https://img.shields.io/badge/57cf553-skeleton?label=%F0%9F%92%80%20bswck/skeleton&labelColor=black&color=grey&link=https%3A//github.com/bswck/skeleton)](https://github.com/bswck/skeleton/tree/57cf553)


[![Documentation Status](https://readthedocs.org/projects/sharkservers-api/badge/?version=latest)](https://sharkservers-api.readthedocs.io/en/latest/?badge=latest)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/Qwizi/sharkservers-api.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/Qwizi/sharkservers-api)
[![License](https://img.shields.io/github/license/Qwizi/sharkservers-api.svg?label=License)](https://github.com/Qwizi/sharkservers-api/blob/HEAD/LICENSE)

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

sharkservers-api

# Installation for contributors


<!--
This section was generated from bswck/skeleton@57cf553.
Instead of changing this particular file, you might want to alter the template:
https://github.com/bswck/skeleton/tree/57cf553/project/%23%25%20if%20docs%20%25%23docs%23%25%20endif%20%25%23/index.md.jinja
-->

!!! Note
    If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).



1.  Fork the [sharkservers-api repository](https://github.com/Qwizi/sharkservers-api) on GitHub.

1.  [Install Poetry](https://python-poetry.org/docs/#installation).<br/>
    Poetry is an amazing tool for managing dependencies & virtual environments, building packages and publishing them.
    You might use [pipx](https://github.com/pypa/pipx#readme) to install it globally (recommended):

    ```shell
    pipx install poetry
    ```

    <sub>If you encounter any problems, refer to [the official documentation](https://python-poetry.org/docs/#installation) for the most up-to-date installation instructions.</sub>

    Be sure to have Python 3.11 installed—if you use [pyenv](https://github.com/pyenv/pyenv#readme), simply run:

    ```shell
    pyenv install 3.11
    ```

1.  Clone your fork locally and install dependencies.

    ```shell
    git clone https://github.com/your-username/sharkservers-api path/to/sharkservers-api
    cd path/to/sharkservers-api
    poetry env use $(cat .python-version)
    poetry install
    ```

    Next up, simply activate the virtual environment and install pre-commit hooks:

    ```shell
    poetry shell
    pre-commit install --hook-type pre-commit --hook-type pre-push
    ```

For more information on how to contribute, check out [CONTRIBUTING.md](https://github.com/Qwizi/sharkservers-api/blob/HEAD/CONTRIBUTING.md).<br/>
Always happy to accept contributions! ❤️


# Legal info
© Copyright by Adrian Ciołek ([@Qwizi](https://github.com/Qwizi)).
<br />This software is licensed under the terms of [GPL-3.0 License](https://github.com/Qwizi/sharkservers-api/blob/HEAD/LICENSE).
