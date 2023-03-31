# --------------------------------------------
# Author: Lucieri
# This code creates a Flask web application with two routes. The first route returns a greeting message.
# The second route reads an XML file, extracts data, and returns it as a JSON string.
# The script also checks if it's being executed directly before running the application.
# --------------------------------------------
# Import necessary modules
from flask import Flask  # Flask web framework
from flask import request  # Flask web framework
import xml.etree.ElementTree as ET  # ElementTree module for parsing XML
import json  # JSON library for encoding data
import os  # os module for interacting with the operating system

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the root URL "/"
@app.route("/dev_app/v1/app_list")
def get_scenario_data():
    
    # Parse the XML file "scenario.xml" using ElementTree
    tree = ET.parse('scenario.xml')
    
    # Get the root element of the XML document
    root = tree.getroot()

    # Create an empty list to hold extracted data
    data = []

    # Find all "mec_app" elements in the XML document
    for element in tree.findall("mec_app"):
        # Extract the attributes of each "mec_app" element and add them to the list
        data = data + [element.attrib]

    #Parameter requests
    #appName = request.args.get('name')
    #appProvider = request.args.get('image')
    #appSoftVersion = request.args.get('')
    #vendorId = request.args.get('1')
    #appSoftVersion = request.args.get('')

    # Get the value of the query parameters from the request object
    name = request.args.get('name')
    image = request.args.get('image')
    ip = request.args.get('ip')
    command = request.args.get('command')

    filtered_list = data

    if name:
        filtered_list = [item for item in filtered_list if item['name'] == name]

    if image:
        filtered_list = [item for item in filtered_list if item['image'] == image]

    if ip:
        filtered_list = [item for item in filtered_list if item['ip'] == ip]

    if command:
        filtered_list = [item for item in filtered_list if item['command'] == command]



    # Encode the extracted data as a JSON-encoded string and return it as the response
    return json.dumps(filtered_list)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Run the Flask application if the script is being executed directly
if __name__ == '__main__':
    app.run()
