# What's New In V1.1
- Added support for **C#** format and coloring.
- Files with extensions other than **.cs** and **.py** no longer have any format or coloring applied to them.
- when opening a file after clicking on the **Open** button, the **extension** of that file is checked first before applying any formatting or coloring.
- Changed the **Save** button to **Save as .py**
- Added a **Save as .cs** inside **File** in order to save as **.cs** file
- Saved file is now named **SavedFile.py** and **SavedFile.cs**, respectively, instead of **main.py**.


# Anubis IDE
It's an **open source** IDE code Created by **Graduation Project** Team at Faculty of **Engineering** **Ain-Shams** Univeristy .  

(![Anubis](https://www13.0zz0.com/2020/07/22/02/845694578.png))

# Objective
- This is a simple IDE which will allow you to perform some basic functionalities, created by Anubis Graduation project team in faculty of engineering Ainshams university, supervisor (Professor: **Ayman Bahaa**) 
- The goal of the Anubis IDE was to provide a simple environment to write, edit, compile, and run micropython codes. but It's now an open-source editor which you can freely access and develop.
- We developed Anubis IDE using PYQT5 .
- PyQt5 is a library that lets you use the Qt GUI framework from Python. Qt itself is written in C++. By using it from Python, you can build applications much more quickly while not sacrificing much of the speed of C++.

## Requirements 
- Python3
- Pyserial (**Important for detecting ports section**)
- PYQT5

## Install Requirements 
(It's recommended to create virtual env before installing the requirements)
- pip3 install -r requirements.txt
### **NOTE**
If python3 is the default use this: 
- pip install -r requirements.txt 

## Run
- Clone the repo .
- Be sure you exist in the repo folder after cloning .

### Windows
- py Anubis.py

### Linux
- python3 Anubis.py

