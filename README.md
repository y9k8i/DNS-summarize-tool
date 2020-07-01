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
        1.  Place ChromeDriver (`chromedriver.exe` or `chromedriver`) in downloaded zip file in this directory.

1.  Install kivy.
    - Using Wheels that has already been compiled (**recommended**)  
        Replace [whl] with Wheel (with a .whl extension) path that can be downloaded [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#kivy) (unofficial) or link can be found [here](https://kivy.org/downloads/appveyor/kivy/) (snapshot).  
        e.g. `python -m pip install Kivy-1.11.1-cp37-cp37m-win_amd64.whl` or `python -m pip install https://kivy.org/downloads/appveyor/kivy/Kivy-2.0.0rc3-cp37-cp37m-win_amd64.whl`
        ```
        python -m pip install --upgrade wheel
        python -m pip install [whl]
        ```
    - Using the source code
        Follow [this instructions](https://kivy.org/doc/stable/installation/installation-windows.html#installing-the-kivy-stable-release) to install Kivy dependencies.
        ```
        python -m pip install kivy
        ```

1.  Install dependencies.
    ```
    python -m pip install -r requirements.txt
    garden install matplotlib
    ```

If you are running on Windows, add `-X utf8` command line option or set the `PYTHONUTF8=1` environment variable.

## Author

[@y9k8i](https://github.com/y9k8i)
