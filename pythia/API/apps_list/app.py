# Import necessary modules
from flask import Flask  # Flask web framework
import xml.etree.ElementTree as ET  # ElementTree module for parsing XML
import json  # JSON library for encoding data
import os  # os module for interacting with the operating system

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the root URL "/"
@app.route("/")
def get_scenario_data():
    
    # Parse the XML file "scenario.xml" using ElementTree
    tree = ET.parse('scenario.xml')
    
    # Get the root element of the XML document
    root = tree.getroot()

    # Create an empty list to hold extracted data
    lista = []

    # Find all "mec_app" elements in the XML document
    for desc in tree.findall("mec_app"):
        # Extract the attributes of each "mec_app" element and add them to the list
        lista = lista + [desc.attrib]

    # Encode the extracted data as a JSON-encoded string and return it as the response
    return json.dumps(lista)

# Run the Flask application if the script is being executed directly
if __name__ == '__main__':
    app.run()
