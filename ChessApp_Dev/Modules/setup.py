# setup.py
from cx_Freeze import setup, Executable

setup(name = "Magachess" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("__main__.pyc")])