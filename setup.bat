@echo off


:start
cls

set python_ver=36

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install mysql.connector
pip install customtkinter
pip install tkinter
pip install hashlib
pip install tkintermapview
pip install geopy
pip install osmnx
pip install networkx

pause
exit
