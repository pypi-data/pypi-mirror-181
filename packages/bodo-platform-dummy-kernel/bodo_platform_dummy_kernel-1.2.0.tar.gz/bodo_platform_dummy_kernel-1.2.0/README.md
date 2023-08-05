# bodo-platform-dummy-kernel

[![PyPI version](https://badge.fury.io/py/bodo-platform-dummy-kernel.svg)](https://badge.fury.io/py/bodo-platform-dummy-kernel)

`bodo-platform-dummy-kernel` is a simple IPython Kernel that displays a warning before executing commands.
Intended for use on the Bodo Platform as the default kernel installed on notebook instances.

Inspired by [echo_kernel](https://github.com/jupyter/echo_kernel).

## Installation

To install `bodo-platform-dummy-kernel` from PyPI::

    pip install bodo-platform-dummy-kernel
    python -m bodo_platform_dummy_kernel.install

When installing inside a conda environment or virtualenv (recommended), do::

    pip install bodo-platform-dummy-kernel
    python -m bodo_platform_dummy_kernel.install --sys-prefix
