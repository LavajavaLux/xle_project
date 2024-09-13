# ································································
# :                                                              :
# :                                                              :
# :              ^=!                     @      AUX~-_   ADJ     :
# :     ^=!;  /  ^=!  ~(^NUM)           ADJ     AUX   \  ADJ     :
# :      NP:./   ^=! !OBJ  xle ____    /UNCT    AUX    | NUM     :
# :      (AUX)   ^=! P-V(___P)        /  PASS   AUX   /  NUM     :
# :       /@(P)  ^=! SUBJ    ,       /___XCOMP  AUX\-`   NUM     :
# :      /  V:^= |||/ "."___/       /      SUBJ AUX      NUM     :
# :                                                              :
# :     Author: Lukikew                                          :
# ································································
# 
import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import tkinter as tk
from tkinter import Menu
import platform

from Core.config import Configuration
from Models.xle_model import xle_model
#from Core.validation import Validation
from Views.menubar import Menubar

from Views.xle_view import xle_view
from Views.settings import SettingsWindow

config = Configuration()
config.createConfigFile()
xle = xle_model()

root = tk.Tk()
root.title("XLE API")
root.geometry("500x650")
#root.configure(background="systemWindowBackgroundColor")
#print(root.config()["background"])

menubar = Menubar(root)
root.config(menu=menubar)


xle_view = xle_view(root)

root.mainloop()


# # # # # # # # # # # # # # # # # # #
# ································· #
# :                               : #
# :                               : #
# :              ^=!              : #
# :     ^=!;  /  ^=!  ~(^NUM)     : #
# :      NP:./   ^=! !OBJ  xle    : #
# :      (AUX)   ^=! P-V(___P)    : #
# :       /@(P)  ^=! SUBJ    ,    : #
# :      /  V:^= |||/ "."___/     : #
# :                               : #
# :                               : #
# :                               : #
# ································· #
# # # # # # # # # # # # # # # # # # #
