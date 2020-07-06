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

1.  Install ChromeDriver.
    - Using pip (**recommended**)  
        Use the major version number which version of Chrome you are using.  
        In addition, the version of ChromeDriver for the current stable release of Chrome can be found at [here](https://chromedriver.storage.googleapis.com/LATEST_RELEASE).  
        e.g.
        ```
        python -m pip install chromedriver-binary==83.0.*
        ```
    - Download from Google
        1.  Download from [here](https://sites.google.com/a/chromium.org/chromedriver/).
        1.  Place ChromeDriver included in downloaded zip file in the same folder as main.py.

1.  Install kivy and its dependencies.
    - Using Conda
        ```
            conda install kivy -c conda-forge
        ```
    - Install in a native Python installation  
        Please also refer to [the installation instructions](https://kivy.org/doc/stable/gettingstarted/installation.html).  
        Ensure you have the latest pip, wheel.
        ```
            python -m pip install --upgrade pip wheel
        ```
        - On Windows
            1.  Follow [this instructions](https://kivy.org/doc/stable/installation/installation-windows.html#installing-the-kivy-stable-release) to install Kivy dependencies.
                ```
                python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
                ```
            1.  Install kivy
                - Using Wheels that has already been compiled (**recommended**)  
                    Replace [whl] with Wheel path that can be downloaded [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#kivy) (unofficial) or link can be found [here](https://kivy.org/downloads/appveyor/kivy/) (snapshot).
                    ```
                    python -m pip install [whl]
                    ```
                    e.g. `python -m pip install Kivy-1.11.1-cp37-cp37m-win_amd64.whl` or `python -m pip install https://kivy.org/downloads/appveyor/kivy/Kivy-2.0.0rc3-cp37-cp37m-win_amd64.whl`
                - Using the source code
                    ```
                    python -m pip install kivy
                    ```
        - On macOS
            - Using the source code (**recommended**)
                ```
                python -m pip install kivy
                ```
            - Using Wheels that has already been compiled  
                Replace [whl] with Wheel link can be found [here](https://kivy.org/downloads/ci/osx/kivy/) (snapshot).
                ```
                python -m pip install [whl]
                ```
                e.g. `python -m pip install https://kivy.org/downloads/ci/osx/kivy/Kivy-2.0.0rc3-cp38-cp38-macosx_10_14_x86_64.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl`
            - Using The Kivy.app  
                Follow [this instructions](https://kivy.org/doc/stable/installation/installation-osx.html#using-the-kivy-app)
        - On Linux
            - Using Precompiled Wheels (**recommended**)
                ```
                python -m pip install --upgrade --user setuptools
                python -m pip install kivy
                ```
                - Nightly wheel installation  
                    Replace [whl] with Wheel link can be found [here](https://kivy.org/downloads/ci/linux/kivy/) (snapshot).
                    ```
                    python -m pip install [whl]
                    ```
                    e.g. `python -m pip install https://kivy.org/downloads/ci/linux/kivy/Kivy-2.0.0.dev0-cp37-cp37m-manylinux2010_x86_64.whl`
            - Using software packages  
                Follow [this instructions](https://kivy.org/doc/stable/installation/installation-linux.html#using-software-packages-ppa-etc)

1.  Install dependencies.
    ```
    python -m pip install -r requirements.txt
    garden install matplotlib
    ```

If you are running on Windows, add `-X utf8` command line option or set the `PYTHONUTF8=1` environment variable.

## Author

[@y9k8i](https://github.com/y9k8i)
