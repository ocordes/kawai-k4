#!/bin/bash

pyside6-uic form.ui -o ui_form.py
python mainwindow.py $*
