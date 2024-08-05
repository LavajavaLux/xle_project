import xml.etree.ElementTree as ET
import os

class Configuration:
    """
    Configuration class to handle the configuration file
    """
    def __init__(self, conf_file = None):
        self.current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.conf_file = conf_file if conf_file is not None else "{}/xle_config.xml".format(self.current_dir)

    def getConfigurations(self, attribute):
        """
        returns the value of the given attribute from the configuration file

        parameters:
        ------------
        attribute: the attribute to get the value for

        returns:
        ------------
        the value of the given attribute or None if the attribute does not exist
        """
        tree = ET.parse(self.conf_file)
        root = tree.getroot()
        element = root.find(attribute)
        if element is not None:
            return element.text
        else:
            print("Attribute {} not found in configuration file".format(attribute))
            return ""

    def createConfigFile(self):
        """
        creates the configuration file if it doesn't exist
        """
        try:
            configFile = open(self.conf_file, "r")
            configFile.close()
        except FileNotFoundError:
            root = ET.Element("configurations")

            tree = ET.ElementTree(root)

            tree.write(self.conf_file)

    def updateConfiguration(self, attribute, value):
        """
        updates the value of the given attribute in the configuration file or adds a new attribute if it doesn't exist

        parameters:
        ------------
        attribute: the attribute to update the value for
        value: the new value for the attribute
        """
        self.createConfigFile()# create the configuration file if it doesn't exist
        tree = ET.parse(self.conf_file)
        root = tree.getroot()

        # Check if the attribute already exists
        existing_element = root.find(attribute)

        if existing_element is not None:
            # If it exists, update the value
            existing_element.text = value
        else:
            # If it doesn't exist, add a new element
            new_element = ET.SubElement(root, attribute)
            new_element.text = value

        tree.write(self.conf_file)

    #def dock_icon():
    #    """
    #    sets an icon for the python script running in the dock
    #
    #    the user needs to have the PIL library installed for this to work
    #    """
    #    try:
    #        from PIL import Image, ImageTk
    #        current_directory = os.path.dirname(os.path.abspath(__file__))
    #        ico = Image.open(current_directory + '/xlepic.png')
    #        photo = ImageTk.PhotoImage(ico)
    #        root.wm_iconphoto(False, photo)
    #    except:
    #        pass    


