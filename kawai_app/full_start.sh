#!/bin/bash

pyside6-uic form.ui -o ui_form.py
pyside6-uic sect_dialog.ui -o ui_sect_dialog.py
python mainwindow.py $*
