import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from Views.settings import SettingsWindow
import platform

class Menubar(tk.Menu):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_menu()

    def create_menu(self):
        if platform.system() == 'Darwin':
            # MacOS specific menu
            self.create_macos_menu()
        else:
            # Other platforms
            self.create_default_menu()

    def create_macos_menu(self):
        app_menu = tk.Menu(self, name='apple')
        self.add_cascade(menu=app_menu)
        app_menu.add_command(label='About MyApp')
        app_menu.add_separator()
        app_menu.add_command(label='Settings', command=self.open_settings)

    def create_default_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.add_cascade(label="File", menu=file_menu)

    def open_settings(self):
        settings = SettingsWindow(self.master)
        settings.focus_set()
        settings.grab_set()
        settings.transient(self.master)
        settings.wait_window(settings)
