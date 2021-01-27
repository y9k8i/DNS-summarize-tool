# DNS Summarize Tool

A simple GUI tool for collecting reverse DNS (PTR) records.

**Currently, this tool only supports Japanese language.**

## System Requirements

- Microsoft Windows
- Apple macOS (Mac OS X)
- GNU/Linux

Other OSes and mobile phones are not currently supported.

## Getting Started

### Using a binary

You do not need to install any additional software.
1.  Download the latest build from [here](https://github.com/y9k8i/DNS-summarize-tool/releases/latest) and unzip the downloaded archive.
1.  You simply run the executable file!

### Downloading the source

If [Python](https://www.python.org/) is not installed, it must be installed first.  
Note: Kivy 1.11.1 is the last release that supports Python 2.

1.  Clone a repository.
    ```
    git clone https://github.com/y9k8i/DNS-summarize-tool.git
    cd DNS-summarize-tool
    ```

1.  If you want to install the dependencies in a virtual environment (**recommended**), create and activate that environment.

1.  Ensure you have the latest pip, wheel.
    ```
    python -m pip install --upgrade pip wheel
    ```

1.  Install dependencies.
    ```
    python -m pip install -r requirements.txt
    garden install matplotlib --kivy
    ```

- You're done! You only need to type `python main.py` to execute a program.

If something is not working while installing Kivy, please follow the steps below to install kivy without using Pre-compiled Wheels.
- Using Conda
    ```
    conda install kivy -c conda-forge
    ```
- Install in a native Python installation  
Please also refer to [the installation instructions](https://kivy.org/doc/stable/gettingstarted/installation.html). 
    - On Windows
        - Using Wheels that has already been compiled
            Replace [whl] with Wheel path that can be downloaded [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#kivy) (unofficial) or link can be found [here](https://kivy.org/downloads/appveyor/kivy/) (snapshot).
            ```
            python -m pip install [whl]
            ```
            e.g. `python -m pip install Kivy‑2.0.0‑cp37‑cp37m‑win_amd64.whl` or `python -m pip install https://kivy.org/downloads/appveyor/kivy/Kivy-2.1.0.dev0-cp37-cp37m-win_amd64.whl`
        - Using the source code
            If a wheel is not available or is not working, Kivy can be installed from source:
            ```
            python -m pip install kivy[base] --no-binary kivy
            ```

        To install the last pre-release version of Kivy, please follow [this instructions](https://kivy.org/doc/stable/gettingstarted/installation.html#install-kivy).

    - On macOS
        - Using Wheels that has already been compiled  
            Replace [whl] with Wheel link can be found [here](https://kivy.org/downloads/ci/osx/kivy/) (snapshot).
            ```
            python -m pip install [whl]
            ```
            e.g. `python -m pip install https://kivy.org/downloads/ci/osx/kivy/Kivy-2.1.0.dev0-cp38-cp38-macosx_10_14_x86_64.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl`
        - Using The Kivy.app  
            Please follow [this instructions](https://kivy.org/doc/stable/installation/installation-osx.html#using-the-kivy-app).
    - On Linux
        - Using Precompiled nightly Wheels
            Replace [whl] with Wheel link can be found [here](https://kivy.org/downloads/ci/linux/kivy/) (snapshot).
            ```
            python -m pip install [whl]
            ```
            e.g. `python -m pip install https://kivy.org/downloads/ci/linux/kivy/Kivy-2.1.0.dev0-cp37-cp37m-manylinux2010_x86_64.whl`
        - Using software packages  
            Please follow [this instructions](https://kivy.org/doc/stable/installation/installation-linux.html#using-software-packages-ppa-etc).

## Author

[@y9k8i](https://github.com/y9k8i)
