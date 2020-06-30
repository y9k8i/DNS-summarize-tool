# DNS Summarize Tool

## Getting Started
1.  Clone a repository.
    ```
    git clone https://github.com/y9k8i/DNS-summarize-tool.git
    cd DNS-summarize-tool
    ```
1.  If you want to install the dependencies in a virtual environment, create and activate that environment.
1.  Install kivy.
    - Using Wheels that has already been compiled  
        Replace [whl] with Wheel (with a .whl extension) path that can be downloaded [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#kivy) (unofficial) or link can be found [here](https://kivy.org/downloads/appveyor/kivy/) (snapshot).  
        e.g. `python -m pip install Kivy-1.11.1-cp37-cp37m-win_amd64.whl` or `python -m pip install https://kivy.org/downloads/appveyor/kivy/Kivy-2.0.0rc3-cp37-cp37m-win_amd64.whl`
        ```
        python -m pip install wheel
        python -m pip install [whl]
        ```
    - Using the Kivy source code with pip
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
