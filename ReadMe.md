<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/shadezee/ShadeCopy">
    <img src="./assets/icons/app_icon.ico" alt="Logo" width="250" height="250">
  </a>

  <h3 align="center">Shade Util</h3>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project
A lightweight PyQt6-based desktop multi-utility application to streamline common Windows maintenance tasks.  
Includes features like driver reset, Bing wallpaper compilation, and temp file cleanup.

<br>

## Why it was built
Built out of pure frustration:
- My HID and Wi-Fi drivers kept acting up, usually at the worst times and manually resetting them was a tedious task.
- My Temp folder would *silently* fill up, adding to my list of things that *silently piss me off*. 
- Bing wallpaper service has 🔥**fire**🔥 content!!!

<br>

### Built With
[![Python][Python.com]][Python-url] [![Qt][Qt.com]][Qt-url]

<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

- Python 3.7+
- pip installer
- Qt Designer *(optional, but recommended if you want to edit the UI)*

### Installation
  #### 1. Clone the repository
  ```
    git clone https://github.com/shadezee/ShadeUtil.git
  ```

  #### 2. Create a virtual environment
  ```
    python -m venv .venv
  ```

  #### 3. Activate the virtual environment
  ```
    # Windows
    .venv\Scripts\activate

    # macOS/Linux
    source .venv/bin/activate
  ```

  #### 4. Install dependencies
  ```
    pip install -r requirements.txt
  ```

## Usage
  #### 1. Launch
  ```
    python main.py
  ```

  #### 2. Features
  #### ⚙️ Driver Tools
  - **Reset HID drivers**  
  - **Restart Wi-Fi adapter**  

  #### 🧹 Storage Tools
  - **Clear Temp Folder** (with optional Recycle Bin support)  
  - **Auto-detect Recycle Bin and Temp sizes**  

  #### 🖼️ Bing Wallpaper Compilation
  - Fetches and converts Windows Spotlight images (Bing wallpapers)  

  #### ⚙️ Settings
  - Easily manage the `devcon.exe` path and HID device ID  
  - Settings stored persistently in JSON

  #### 3. Development tools
  - To convert modified .ui files into Python:
  ```
    python -m PyQt6.uic.pyuic ./assets/ui_file.ui -o ./assets/ui_file.py
  ```

  - devcon.exe
  ```
    Usually located in:
    C:\Program Files (x86)\Windows Kits\10\Tools\10.0.26100.0\x64\devcon.exe
  ```
  or can be downloaded from this from [this link](https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/devcon).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better you can also simply open an issue with the tag `enhancement/relevant-name`.
Don't forget to give the project a star! Thanks again!

<!-- LICENSE -->
## License
This project is licensed under the MIT License — see the [LICENSE file](LICENSE)  for details.

<br>


## NOTE:
Shade Util has one known bug, currently two operations cannot be run at once.
Thanks 😉.

<br>
<p align="right"><a href="#readme-top">back to top</a></p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python.com]: https://img.shields.io/badge/Python-ffffff?style=for-the-badge&logo=python
[Python-url]: https://www.python.org
[Qt.com]: https://img.shields.io/badge/PyQt-ffffff?style=for-the-badge&logo=qt
[Qt-url]: https://riverbankcomputing.com/software/pyqt/intro
[devcon-link]: https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/devcon