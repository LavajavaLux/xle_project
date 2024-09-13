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
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from Core import Configuration
from Models import xle_model
from threading import Timer
import time
import re
import os
import tkinter.dialog as dialog

from Views.settings import SettingsWindow

class xle_view_controller:
    warning_shown = False

    def __init__(self, root, xle):
        self.config = Configuration()
        self.xle = xle
        
    def save_tests(self, test_entry, test_edit_text):
        """
        saves the tests from the tests text widget to the testfile
        """
        test_file_path = test_entry.get()
        if test_file_path != "":
            try:
                with open(test_file_path, "w") as file:
                    file.write(test_edit_text.get("1.0", tk.END))
            except FileNotFoundError:
                print("Datei nicht gefunden")
            test_edit_text.yview_moveto(1.0)

    def load_grammar(self, grammar_entry, results_text):
        """
        checks if the grammar file exists and displays error messages in the results text widget
        """
        results_text.config(state=tk.NORMAL)
        try:
            with open(grammar_entry.get(), 'r') as grammar_file:
                self.xle.load_grammar(grammar_entry.get())
                results_text.insert(tk.END, "Grammar loaded successfully.\n\n")
        except FileNotFoundError:
            results_text.insert(tk.END, "Grammar file not found.\n\n")
        except PermissionError:
            results_text.insert(tk.END, "Permission denied to read grammar file.\n\n")
        except Exception as e:
            results_text.insert(tk.END, f"An error occurred: {e}\n\n")   
        results_text.config(state=tk.DISABLED)    

    def load_tests(self, test_entry, test_edit_text):
        """
        loads the tests from the testfile to the test text widget
        """
        test_file_path = test_entry.get()
        if test_file_path != "":
            self.xle.load_test(test_file_path)
            try:
                with open(test_file_path, "r") as test_file:
                    test_edit_text.delete("1.0", tk.END)
                    test_edit_text.insert(tk.END, test_file.read())
            except FileNotFoundError:
                test_edit_text.insert(tk.END, "Test file not found.\n\n")
            except Exception as e:
                test_edit_text.insert(tk.END, f"An error occurred: {e}\n\n")

    def open_test_file_dialog(self, test_entry, test_edit_text):
        """
        opens a file dialog to select the test file
        """
        file_path = filedialog.askopenfilename()
        if file_path == "":
            return
        test_entry.delete(0, tk.END)
        test_entry.insert(0, file_path)
        self.load_tests(test_entry, test_edit_text)

    def open_grammar_file_dialog(self, grammar_entry):
        """
        opens a file dialog to select the grammar file
        """
        file_path = filedialog.askopenfilename()
        if file_path == "":
            return
        grammar_entry.delete(0, tk.END)
        grammar_entry.insert(0, file_path)
        self.xle.load_grammar(file_path)

    def parse_sentence(self, sentence_entry, results_text):
        """
        parses the sentence in the sentence entry
        """
        results_text.config(state=tk.NORMAL)
        results_text.insert(tk.END, "Parsing sentence: {}\n\n".format(sentence_entry.get()))
        results_text.config(state=tk.DISABLED)
        self.xle.parse(sentence_entry.get())
        results_text.yview_moveto(1.0)

        if ("MORPHOLOGY" in self.xle.grammar_file or "morphology" in self.xle.grammar_file or "morphconfig" in self.xle.grammar_file) and f"{self.xle.xle_directory}/english-morph/english-std-morphconfig-with-paths." not in self.xle.grammar_file:
            results_text.config(state=tk.NORMAL)
            results_text.insert(tk.END, "Bearbeite deine Tests \nin dem Textfeld rechts. \n\nDu kannst direkt \nmit dem Textfeld interagieren \noder die Sätze \nüber den Button zu den \nTests hinzufügen. \n\nBenutze dafür das Textfeld \ndas du auch \nzum Parsen verwendest\n\n")
            results_text.insert(tk.END, "Append this to the configuration of your grammar: \n" + f"FILES {self.xle.xle_directory}/english-morph/english-std-morphconfig-with-paths.\nMORPHOLOGY (STANDARD ENGLISH).\n\n")
            results_text.config(state=tk.DISABLED)
            results_text.yview_moveto(1.0)
            if not self.warning_shown:
                tk.messagebox.showinfo("Only applies when using the morphological analyzer", f"You should put \n\nFILES {self.xle.xle_directory}/english-morph/english-std-morphconfig-with-paths.\nMORPHOLOGY (STANDARD ENGLISH).\n\nin your grammar file\n\n")
                self.warning_shown = True

    def run_tests(self, results_text):
        """
        runs the tests and displays the results in the results text widget
        """
        results_text.config(state=tk.NORMAL)
        results_text.insert(tk.END, "Running tests...\n\n")
        self.xle.run_tests()
        results_text.insert(tk.END, self.xle.test_results)
        results_text.insert(tk.END, "\n\n")
        results_text.config(state=tk.DISABLED)

        results_text.yview_moveto(1.0)

        try:
            with open(self.xle.test_file_path + ".errors", "r") as error_file:
                error_message = error_file.read()
                if re.search(r"[a-zA-Z]", error_message):
                    test_window = Test_window(self.xle)
        except FileNotFoundError:
            pass

    def add_sentence_to_tests(self, sentence_entry, test_entry, test_edit_text):
        """
        Adds the sentence in the sentence entry to the test file.
        """
        test_file_path = test_entry.get()
        if test_file_path != "":
            with open(test_file_path, "a") as test_file:
                sentence = sentence_entry.get()
                if sentence.startswith("*"):
                    formatted_sentence = "\n\n" + sentence.strip("*") + "(0! 0 0 0)"
                else:
                    formatted_sentence = "\n\n" + sentence + "(1! 1 0 0)"
                test_file.write(formatted_sentence)

            self.load_tests(test_entry, test_edit_text)
            test_edit_text.yview_moveto(1.0)       

    
class TextField(ttk.Entry):
    def __init__(self, parent, placeholder, *args, **kwargs):
        super().__init__(parent, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder
        #if self.get() == "":
        #    self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self.on_entry_focusin)
        self.bind("<FocusOut>", self.on_entry_focusout)

    def show_placeholder(self):
        self.configure(show="")
        if self.get() == "":
            self.insert("0", self.placeholder)

    def hide_placeholder(self):
        self.delete("0", tk.END)

    def on_entry_focusin(self, event):
        if self.get() == self.placeholder:
            self.delete("0", tk.END)

    def on_entry_focusout(self, event):
        if not self.get():
            self.show_placeholder()



class xle_view:
    def __init__(self, root):
        self.config = Configuration()
        self.xle = xle_model.xle_model()
        self.controller = xle_view_controller(root, self.xle)
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        TW_width = 30
        EW_width_s = 40
        EW_width_l = 50
        win_width = root.winfo_width()

        grammarfile_placeholder = "Path to grammar file"
        testfile_placeholder = "Path to test file"

        # the frame for grammar and test file path entries
        directoriesFrame = tk.Frame(root)

        grammar_entry_label = tk.Label(directoriesFrame, text="Grammar file:")
        grammar_entry_label.pack(anchor=tk.W)
        grammar_entry_frame = tk.Frame(directoriesFrame)
        grammar_entry = TextField(grammar_entry_frame, grammarfile_placeholder, width=EW_width_s)
        grammar_entry.insert(0, self.config.getConfigurations("grammarfile"))
        grammar_entry.show_placeholder()
        grammar_entry.bind("<FocusOut>", lambda _: self.controller.load_grammar(grammar_entry, results_text))
        grammar_entry.pack(side=tk.LEFT, padx=5, pady=5)

        grammar_file_dialog = ttk.Button(grammar_entry_frame, text="open", command=lambda: self.controller.open_grammar_file_dialog(grammar_entry))
        grammar_file_dialog.pack(padx=5, pady=5)
        grammar_entry_frame.pack()

        test_entry_label = tk.Label(directoriesFrame, text="Test file:")
        test_entry_label.pack(anchor=tk.W)
        test_entry_frame = tk.Frame(directoriesFrame)
        test_entry = TextField(test_entry_frame, testfile_placeholder, width=EW_width_s)
        test_entry.insert(0, self.config.getConfigurations("testfile"))
        test_entry.show_placeholder()
        test_entry.bind("<FocusOut>", lambda _: self.controller.load_tests(test_entry, test_edit_text))
        test_entry.pack(side=tk.LEFT, padx=5, pady=5)

        test_file_dialog = ttk.Button(test_entry_frame, text="open", command=lambda: self.controller.open_test_file_dialog(test_entry, test_edit_text))
        test_file_dialog.pack(padx=5, pady=5)
        test_entry_frame.pack()

        directoriesFrame.pack()
        
        # frame for entry of sentence to parse
        sentence_frame = tk.Frame(root)

        enter_sentence_label = tk.Label(sentence_frame, text="Fütter mich:")
        enter_sentence_label.pack(anchor=tk.W)
        sentence_entry = TextField(sentence_frame, "Enter sentence here", width=EW_width_l)
        sentence_entry.bind("<Return>", lambda e: self.controller.parse_sentence(sentence_entry, results_text))
        sentence_entry.focus_set()
        sentence_entry.pack()

        sentence_frame.pack()
        
        # the frame for the buttons
        buttons_frame = tk.Frame(root)

        parse_button = ttk.Button(buttons_frame, text="Parse", command=lambda: self.controller.parse_sentence(sentence_entry, results_text))
        parse_button.pack(side=tk.LEFT, padx=5, pady=5)

        run_tests_button = ttk.Button(buttons_frame, text="Run tests", command=lambda: self.controller.run_tests(results_text))
        run_tests_button.pack(side=tk.LEFT, padx=5, pady=5)

        add_to_tests_button = ttk.Button(buttons_frame, text="Satz zu Testdatei hinzufügen", command=lambda: self.controller.add_sentence_to_tests(sentence_entry, test_entry, test_edit_text))
        add_to_tests_button.pack(side=tk.LEFT, padx=5, pady=5)

        buttons_frame.pack()

        # the frame for the results
        output_frame = tk.Frame(root)

        results_frame = tk.Frame(output_frame)
        results_label = tk.Label(results_frame, text="Results:")
        results_label.pack(anchor=tk.W)

        results_text = tk.Text(results_frame, width=TW_width)
        #results_text.bind("<FocusIn>", lambda _: sentence_entry.focus_set())
        xle_dir = self.config.getConfigurations("xle_path") if self.config.getConfigurations("xle_path") else "YOUR_XLE_PATH"
        results_text.insert(tk.END, "Bearbeite deine Tests \nin dem Textfeld rechts. \n\nDu kannst direkt \nmit dem Textfeld interagieren \noder die Sätze \nüber den Button zu den \nTests hinzufügen. \n\nBenutze dafür das Textfeld \ndas du auch \nzum Parsen verwendest\n\n")
        results_text.insert(tk.END, "Append this to the configuration of your grammar: \n" + f"FILES {xle_dir}/english-morph/english-std-morphconfig-with-paths.\nMORPHOLOGY (STANDARD ENGLISH).\n\n")
        results_text.config(state=tk.DISABLED)
        results_text.pack(side=tk.LEFT, padx=5, pady=5)
        results_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        test_frame = tk.Frame(output_frame)
        test_label = tk.Label(test_frame, text="Tests:")
        test_label.pack(anchor=tk.W)

        test_edit_text = tk.Text(test_frame, width=TW_width)
        test_edit_text.pack(padx=5, pady=5)
        test_edit_text.bind("<KeyRelease>", lambda _: self.controller.save_tests(test_entry, test_edit_text))
        test_frame.pack(padx=5, pady=5)

        output_frame.pack()

        self.controller.load_grammar(grammar_entry, results_text)
        self.controller.load_tests(test_entry, test_edit_text)

        # canvas with color of buttons
        #canvas = tk.Canvas(root, height=20, background="#696969")
        #canvas.pack(fill=tk.X, expand=True)

        ttk.Button(root, text="Pfad zu XLE", command=lambda: SettingsWindow(root)).pack(side=tk.RIGHT, padx=5, pady=5)
        xle_path_label = tk.Label(root, text="Define the path to the XLE folder here:")
        xle_path_label.pack(side=tk.RIGHT, padx=5, pady=5)

        





class Table(tk.Frame):
    """
    creates a table from a list of rows and a list of column names

    parameters:
    ------------
    parent: the parent widget
    rows: a list of lists, each containing the data for one row
    columns: a list of strings containing the column names
    """
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        # Create headers
        for i, column in enumerate(columns):
            label = tk.Label(self, text=column, relief=tk.SOLID, width=15, background=f"#{90:02x}{90:02x}{90:02x}", foreground="white")
            label.grid(row=0, column=i, sticky=tk.NSEW)

        # Create data cells
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                label = tk.Label(self, text=cell, relief=tk.FLAT, width=15)
                label.grid(row=i+1, column=j, sticky=tk.NSEW)

        # Ensure cells expand to fill any extra space
        for i in range(len(columns)):
            self.grid_columnconfigure(i, weight=1)
    

class Test_window:
        """
        displays additional information about the test results in a separate window
        
        parameters:
        ------------
        testfile: the file with the tests to display the results for
        """
        def __init__(self, xle: xle_model.xle_model):

            self.xle = xle

            testWindow = tk.Tk()
            testWindow.geometry("400x300")
            # title is 'test' + current time
            title = "Test-Ergebnisse " + time.strftime("%H:%M:%S")
            testWindow.title(title)

            # tries to open the test file if that failes it shows a warning 
            stats_file_path = self.xle.test_file_path + ".stats"

            try:
                with open(stats_file_path, "r") as stats_file:
                    open_file = stats_file.readlines()

                    # Check if required strings ("range", "parsed", "failed") are present in the file
                    if any("range" in line and "parsed" in line and "failed" in line for line in open_file):
                        table = []
                        table_start_index = 0
                        for i in range(len(open_file) - 1, max(len(open_file) - 21, 0), -1):
                            if "range" in open_file[i] and "parsed" in open_file[i] and "failed" in open_file[i]:
                                table_start_index = i
                                break
                        
                        # Extract table data
                        if table_start_index > 0:
                            for line in open_file[table_start_index:table_start_index + 2]:
                                table.append(re.split(r"\s+", line.strip()))

                            # Example data
                            columns = table[0]
                            data = table[1:]

                            # Create the table (assuming Table is a custom widget or class)
                            table_widget = Table(testWindow, data, columns)
                            table_widget.pack(expand=True, fill=tk.BOTH)
                        else:
                            print("Table start index not found in the file.")
                    else:
                        print("Required strings ('range', 'parsed', 'failed') not found in the file.")
            except FileNotFoundError:
                print(f"Stats file not found: {stats_file_path}")

            error_file = self.xle.test_file_path + ".errors"
            open_errors = open(error_file, "r").read()

            background = "systemWindowBackgroundColor" if self.xle.get_os_type() != "Windows" else "white"
            error_label = tk.Text(testWindow, width=30, background=background)
            error_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

            error_label.insert(tk.END, "Error: \n" + open_errors)
            error_label.config(state=tk.DISABLED)

            testWindow.mainloop()
