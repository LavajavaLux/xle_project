import shlex
import subprocess
import time
import os
import platform
import tkinter as tk
from tkinter import messagebox

from Core.config import Configuration
from Core.validation import Validation

class xle_model:
    def __init__(self):
        self.config = Configuration()
        self.grammar_file_path = None
        self.test_file_path = None
        self.grammar_file = None
        self.test_file = None
        self.test_results = None
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.xle_path = "{}/xle.sh".format(os.path.dirname(self.current_dir)) # path to the xle.sh script
        self.xle_directory = self.config.getConfigurations("xle_path")

    def load_grammar(self, grammar_file_path):
        self.config.updateConfiguration("grammarfile", grammar_file_path)

        self.grammar_file_path = grammar_file_path
        try:
            with open(grammar_file_path, 'r') as grammar_file:
                self.grammar_file = grammar_file.read()
        except FileNotFoundError:
            print(f"Error: File '{grammar_file_path}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to read file '{grammar_file_path}'.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {str(e)}")

    def load_test(self, test_file_path):
        self.config.updateConfiguration("testfile", test_file_path)

        self.test_file_path = test_file_path
        try:
            with open(test_file_path, 'r') as test_file:
                self.test_file = test_file.read()
        except FileNotFoundError:
            print(f"Error: File '{test_file_path}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to read file '{test_file_path}'.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {str(e)}")

    def run_tests(self):
        """
        Runs the tests in the given testfile with the given grammar using XLE (Xerox Linguistic Environment).

        Warning: Be careful with your input, because it will be executed directly in the terminal.
        The input is thoroughly sanitized for that reason but some malformed input may still cause problems.

        Parameters:
        ------------
        testfile: The file with the tests to run.
        grammar: The grammar to use for parsing.
        """
        self.load_test(self.test_file_path)

        Validation.validate_path(self.test_file_path)
        Validation.validate_path(self.grammar_file_path)
        Validation.validate_testfile(self.test_file_path)

        self.xle_directory = self.config.getConfigurations("xle_path")

        testfile = shlex.quote(self.test_file_path)
        grammar = shlex.quote(self.grammar_file_path)

        command = [self.xle_path, self.xle_directory, "create-parser " + "\"{}\"".format(grammar) + "; parse-testfile " + "\"{}\"; exit;".format(testfile)]
        #command = "{}/xle.sh create-parser {}; parse-testfile {}".format(self.current_dir, grammar, testfile)

        env = os.environ.copy()
        env['XLEPATH'] = self.xle_directory
        env['PATH'] = f"{self.xle_directory}/bin:{env.get('PATH', '')}"
        env['LD_LIBRARY_PATH'] = f"{self.xle_directory}/lib:{env.get('LD_LIBRARY_PATH', '')}"
        env['DYLD_LIBRARY_PATH'] = f"{self.xle_directory}/lib:{env.get('DYLD_LIBRARY_PATH', '')}"

        command = [
            'xle', '-e',
            "create-parser " + "\"{}\"".format(grammar) + "; parse-testfile " + "\"{}\"; exit;".format(testfile)
        ]

        try:
            subprocess.run(command, env=env, timeout=5)

            stats_file_path = "{}.stats".format(self.test_file_path)
            with open(stats_file_path, "r") as stats_file:
                self.test_results = stats_file.read()

        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running the subprocess: {e}")
            self.test_results = ""
        except FileNotFoundError:
            print(f"Stats file not found: {stats_file_path}")
            self.test_results = ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.test_results = ""

    def parse(self, sentence):
        """
        parses the given sentence with the given grammar with xle (Xerox Linguistic Environment)

        warning: be careful with your input, because it will be executed directly in the terminal.
        the input is thouroughly sanitized for that reason but some malformed may still cause problems

        parameters:
        ------------
        sentence: the sentence to parse
        grammar: the grammar to use for parsing
        """

        Validation.validate_path(self.grammar_file_path)
        Validation.validate_sentence(sentence)
        self.xle_directory = self.config.getConfigurations("xle_path")

        self.kill()

        grammar = shlex.quote(self.grammar_file_path)
        print("Geparster Satz: " + sentence)


        env = os.environ.copy()  
        env['XLEPATH'] = self.xle_directory
        env['PATH'] = f"{self.xle_directory}/bin:{env.get('PATH', '')}"
        env['LD_LIBRARY_PATH'] = f"{self.xle_directory}/lib:{env.get('LD_LIBRARY_PATH', '')}"
        env['DYLD_LIBRARY_PATH'] = f"{self.xle_directory}/lib:{env.get('DYLD_LIBRARY_PATH', '')}"

        command = [
            'xle', '-e',
            f"create-parser \"{grammar}\"; parse {{{sentence}}};",
        ]

        #result = subprocess.run(command, env=env)
        process = subprocess.Popen(
            command, env=env,
        )

        if ("MORPHOLOGY" in self.grammar_file or "morphology" in self.grammar_file or "morphconfig" in self.grammar_file) and " " in self.xle_directory:
            tk.messagebox.showinfo("Only applies when using the morphological analyzer", "The path to xle should not contain any spaces\n when using a morphological analyzer or other kind of extensions with xle.")


        #command = [self.xle_path, "create-parser " + "\"{}\"".format(grammar) + "; parse {" + sentence + "}"]
        #subprocess.Popen(command)


    def get_os_type(self):
        """
        returns the type of operating system
        """
        system = platform.system()
        if system == "Windows":
            return "Windows"
        elif system == "Linux" or system == "Darwin":
            return "Unix"
        else:
            return "Unknown"

    def kill(self):
        """
        kills all xle processes
        """
        if self.get_os_type() == "Windows":
            # command for windows
            subprocess.Popen(["taskkill", "/F", "/IM", "xle.exe"])
        else:
            # command for unix
            subprocess.Popen(["killall", "xle"])

