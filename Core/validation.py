import re

class Validation:
    def __init__(self):
        pass

    
    @staticmethod
    def validate_path(path):
        """
        sanitizes the given string for usage in a shell command

        parameters:
        ------------
        string: the string to sanitize
        """
        pattern1 = r"^(.+)\/([^\/]+)\s*$"
        pattern2 = r"^[a-zA-Z]:\\(((?![<>:\"/\\|?*]).)+((?<![ .])\\)?)*\s*$"
        if (not re.match(pattern1, path) and not re.match(pattern2, path)) or re.search(r"[^_\-/\\0-9A-Za-züäö.#+%&ß:\s]",path): #or re.search(r"(?:\;|\(|\)|\,|\"|\`|\'|\s)+",string)
            print("Ein Pfad enthält keine Sonderzeichen wie zum Beispiel ;()\" oder Leerzeichen. Statt leerzeichen verwende \"_\" oder \"-\".")
            raise ValueError("Invalid path")


    @staticmethod
    def validate_sentence(sentence):
        """
        sanitizes the given string for usage in a shell command

        parameters:
        ------------
        string: the string to sanitize
        """
        if "{" in sentence or "}" in sentence or "\\" in sentence:
            print("Satz enthält unerlaubte Zeichen: { oder } oder \\")
            raise ValueError("Invalid sentence")
        return sentence
    
    @staticmethod
    def validate_testfile(test_file_path):
        """
        validates the given testfile

        parameters:
        ------------
        test_file_path: the path to the testfile
        """
        with open(test_file_path, "r") as test_file:
            for line in test_file:
                if "{" in line or "}" in line or "\\" in line:
                    print("Testfile enthält unerlaubte Zeichen: { oder } oder \\")
                    raise ValueError("Invalid testfile")
                

