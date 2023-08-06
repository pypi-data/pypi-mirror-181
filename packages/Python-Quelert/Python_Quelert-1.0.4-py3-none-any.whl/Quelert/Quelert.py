from tkinter import messagebox

import webbrowser
import pyautogui
import wget
import sys
import os


def init(packages):
	if packages == "qw":
		from qw import Widgets
	else:
		messagebox.showerror("Error 219", "Error: 219 | Package not found!")

def Browser_Downloads(url, namefile):
	wget.download(url, namefile)

def Web_Page_Opening(url):
	webbrowser.open(url)

def Screenshot(namefile):
	pyautogui.screenshot(namefile)

def WidgetView():
	print("Quelert-Widgets - [QW-qw]")