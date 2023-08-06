import webbrowser
import pyautogui
import wget
import sys
import os


def Browser_Downloads(url, namefile) -> None:
	wget.download(url, namefile)

def Web_Page_Opening(url) -> None:
	webbrowser.open(url)

def Screenshot(namefile) -> None:
	pyautogui.screenshot(namefile)

def WidgetView() -> None:
	print("Widgets not found!")