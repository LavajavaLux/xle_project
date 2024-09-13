import tkinter as tk
from tkinter import filedialog

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Editor")

        self.text_widget = tk.Text(self.root, wrap="word")
        self.text_widget.pack(expand=True, fill="both")

        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open grammar file", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.root.config(menu=self.menu_bar)

        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete("1.0", tk.END)  # Clear previous content
                self.text_widget.insert(tk.END, content)

    def save_file(self):
        if self.current_file:
            content = self.text_widget.get("1.0", tk.END)
            with open(self.current_file, "w") as file:
                file.write(content)
                tk.messagebox.showinfo("Saved", "File saved successfully.")
        else:
            tk.messagebox.showwarning("Warning", "No file is currently open.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
