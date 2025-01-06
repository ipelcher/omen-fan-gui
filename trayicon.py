from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QLineEdit, QInputDialog, QMessageBox

import os
import sys
import subprocess

def critical(message):
    QMessageBox.critical(None, 'Error Message', message)
    sys.exit(1)

def checkFanStatus():
    process = subprocess.run(['python3', omen_fan_utlity_path, 'i'], stdout=subprocess.PIPE)
    result = process.stdout.decode('utf-8')
    for line in result.split('\n'):
        if 'Fan Boost' in line:
            if 'Enabled' in line:
                fanStatus = 'Enabled'
                on.setDisabled(True)
                off.setDisabled(False)
            else:
                fanStatus = 'Disabled'
                on.setDisabled(False)
                off.setDisabled(True)
    return fanStatus

def boostOn():
    process = subprocess.run(['pkexec', 'python3', omen_fan_utlity_path, 'x', '1'], stdout=subprocess.PIPE)
    on.setDisabled(True)
    off.setDisabled(False)

def boostOff():
    process = subprocess.run(['pkexec', 'python3', omen_fan_utlity_path, 'x', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(process.stdout.decode('utf-8'))
    print(process.stderr.decode('utf-8'))
    on.setDisabled(False)
    off.setDisabled(True)

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Check if the path to omen-fan utility was provided
if os.path.isfile('omen-fan-utility-path.txt'):
    with open('omen-fan-utility-path.txt', 'r') as f:
        omen_fan_utlity_path = f.read()
        process = subprocess.run(['python3', omen_fan_utlity_path, 'i'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            critical('The path you provided is not correct! \n\n' + process.stderr.decode('utf-8'))
else:
    # Ask for the path to omen-fan utility
    widget = QWidget()
    text, okPressed = QInputDialog.getText(widget, 'Path Dialog', 'Please provide the path to omen-fan utility:', QLineEdit.Normal, '')
    if okPressed and text != '':
        process = subprocess.run(['python3', text, 'i'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            critical('The path you provided is not correct! \n\n' + process.stderr.decode('utf-8'))
        else:
            isCorrect = QMessageBox.question(None, 'Success Message', 'The path you provided is correct! Does the information below look correct? \n\n' + process.stdout.decode('utf-8'), QMessageBox.Yes, QMessageBox.No)
            if isCorrect == QMessageBox.No:
                critical('Your omen-fan installation is corrupt or the path you provided is not correct!')
            else:
                omen_fan_utlity_path = text
                with open('omen-fan-utility-path.txt', 'w') as f:
                    f.write(omen_fan_utlity_path)
    else:
        critical('The path to omen-fan utility was not provided!')
        

# Load icon
trayicon = QIcon('computer-fan-1024x1024.png')

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(trayicon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
menu.aboutToShow.connect(checkFanStatus)

# Add title to the menu
title = QAction('Omen Fan Control Utility GUI')
title.setDisabled(True)
menu.addAction(title)

# Add omen-fan utility path to the menu
path = QAction('omen-fan utility path: \n' + omen_fan_utlity_path)
path.setDisabled(True)
menu.addAction(path)

# Add first separator to the menu
separator1 = QAction('')
separator1.setDisabled(True)
menu.addAction(separator1)

# Add boost on option to the menu
on = QAction('Boost on')
on.triggered.connect(boostOn)
menu.addAction(on)

# Add boost off option to the menu
off = QAction('Boost off')
off.triggered.connect(boostOff)
menu.addAction(off)

# Add second separator to the menu
separator2 = QAction('')
separator2.setDisabled(True)
menu.addAction(separator2)

# Add this project link to the menu
thislink = QAction('omen-fan-gui project by ipelcher')
thislink.triggered.connect(lambda: subprocess.Popen(['xdg-open', 'https://github.com/ipelcher/omen-fan-gui']))
menu.addAction(thislink)

# Add original project link to the menu
origlink = QAction('omen-fan utility by alou-S')
origlink.triggered.connect(lambda: subprocess.Popen(['xdg-open', 'https://github.com/alou-S/omen-fan']))
menu.addAction(origlink)

# Add a Quit option to the menu
quit = QAction('Quit')
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec()
