import os
import sys
#current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#sys.path.append(current_dir)


import tkinter as tk
from tkinter import ttk
from Core import Configuration
import tkinter.filedialog as filedialog
import platform
from tkinter import Menu


class SettingsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.config = Configuration()
        self.xle_path = tk.StringVar(value=self.config.getConfigurations("xle_path"))
        self.title("Settings")
        self.geometry("512x200")
        self.resizable(False, False)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Pfad zu Xle", font=("Arial", 20)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        #ttk.Entry(self, textvariable=self.xle_path, state="readonly").bind("<FocusIn>", lambda e: self.browse_xle()).grid(row=1, column=0, padx=10, pady=10)#.bind("<FocusIn>", lambda e: self.browse_xle())
        xle_entry = ttk.Entry(self, textvariable=self.xle_path, state="readonly", width=40)
        xle_entry.bind("<FocusIn>", lambda e: self.browse_xle())
        xle_entry.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(self, text="Browse", command=self.browse_xle).grid(row=1, column=1, padx=10, pady=10)

        #ttk.Button(self, text="Save", command=self.save_settings).grid(row=2, column=0, columnspan=2, pady=20)

    def browse_xle(self):
        #xle_path to the folder of xle 
        xle_path = filedialog.askdirectory(title="Select Xle Path", initialdir=self.config.getConfigurations("xle_path"))
        if xle_path:
            self.xle_path.set(xle_path)
            self.config.updateConfiguration("xle_path", xle_path)

        self.focus_set()
        




#
#if __name__ == "__main__":
#    root = tk.Tk()
#    SettingsWindow(root)
#    root.mainloop()