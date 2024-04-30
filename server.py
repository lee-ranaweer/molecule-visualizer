#Import libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys   
import urllib  
import molsql
import MolDisplay
import tempfile
import os
import re

if __name__ == '__main__':
    db = molsql.Database(reset=True)
    db.create_tables()
    db['Elements'] = (0, 'X', 'default', 828282, 828282, 828282, 25)

#Acessible files
public_files = ['/home.html', '/add_remove_elements.html', '/upload_sdf_file.html', '/style.css', '/script.js']

#Pages for rendering molecule SVG files
molecule_files = []

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #If the requested URL is one of the public_files
        if self.path in public_files:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')

            #Retreive the corresponding HTML from local directory
            fp = open(self.path[1:])
            page = fp.read()
            fp.close()

            #Display the HTML content on the server
            self.send_header('Content-length', len(page))
            self.end_headers()
            self.wfile.write(bytes(page, 'utf-8'))
        
        #If the user selects the 'View molecules page'
        elif self.path == '/view_molecules.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            molecule = db.get_molecule_info()

            page = '<html<head><title>Nelith Ranaweera A4</title><link rel="stylesheet" type="text/css" href="style.css" /></head><body><h1>Molecules</h1>'

            page += """<body>
                        <!-- Navigation bar -->
                        <div class="navbar">
                            <a href="home.html">Home</a>
                            <a href="add_remove_elements.html">Add/remove elements</a>
                            <a href="upload_sdf_file.html">Upload SDF file</a>
                            <a class="active" href="#">View molecules</a>
                        </div>

                        <!-- View molecules page -->
                        <div class="content">
                            <h1>View Molecules</h1>
                        </div>
                    </body>"""
            
            #Add each molecule to the page
            if len(molecule) == 0:
                page += '<p>No molecules found</p>'
            else:
                page += '<table class = "view_molecules"><tr><th>Name</th><th>ID</th><th>Atoms</th><th>Bonds</th></tr>'
                for info in molecule:
                    molecule_files.append("/" + info[0])
                    page += f'<tr><td><a href="/{info[0]}">{info[0]}</a></td><td>{info[1]}</td><td>{info[2]}</td><td>{info[3]}</td></tr>'
                page += '</table>'

            page += '</body></html>'

            #Display the HTML content on the server
            self.send_header('Content-length', len(page))
            self.end_headers()
            self.wfile.write(bytes(page, 'utf-8'))

        #If the user chooses to view a molecule
        elif self.path in molecule_files:
            self.send_response(200)
            molecule = self.path[1:]
            MolDisplay.radius = db.radius();
            MolDisplay.element_name = db.element_name();
            MolDisplay.header += db.radial_gradients();

            mol = db.load_mol( molecule );
            mol.sort();
            output = mol.svg()

            page = '<html<head><title>Nelith Ranaweera A4</title><link rel="stylesheet" type="text/css" href="style.css" /><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script><script src="script.js" /></script></head><body><h1>Molecules</h1>'

            page += """<body>
                        <!-- Navigation bar -->
                        <div class="navbar">
                            <a href="home.html">Home</a>
                            <a href="add_remove_elements.html">Add/remove elements</a>
                            <a href="upload_sdf_file.html">Upload SDF file</a>
                            <a class="active" href="#">View molecules</a>
                        </div>

                        <!-- View molecules page -->
                        <div class="content">
                            <h1>View Molecules</h1>
                        </div>
                    </body>"""

            # View molecules page
            page += '<div class="content">'

            #Create the SVG
            page += '<div>' + output + '</div>'

            page += '</div></body></html>'
            
            #Display the SVG on the server
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(page))
            self.end_headers()

            self.wfile.write(bytes(page, 'utf-8'))


        #If the requested URL is not one of the public_files
        else: 
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('404: not found', 'utf-8'))
    
    def do_POST(self):
        #Post request for adding an element to the database
        if self.path == '/add_element_values.html':
            content_length = int(self.headers['Content-Length'])

            body = self.rfile.read(content_length)

            #Convert POST content into a dictionary
            elementValues = urllib.parse.parse_qs(body.decode('utf-8'))

            for key, value in elementValues.items():
                elementValues[key] = value[0].strip()

            #Send message to server indicating successful post
            message = 'Element ' + elementValues['elementname'] + ' was successfully added'

            #Add element to elements table
            db['Elements'] = (elementValues['elementnumber'], elementValues['elementcode'], elementValues['elementname'], elementValues['colour1'], elementValues['colour2'], elementValues['colour3'], 25)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-length', len(message))
            self.end_headers()
            self.wfile.write(bytes(message, 'utf-8'))
        
        #Post request for deleting an element from the database
        elif self.path == '/delete_element_values.html':
            content_length = int(self.headers['Content-Length'])

            body = self.rfile.read(content_length)

            #Convert POST content into a dictionary
            elementValues = urllib.parse.parse_qs(body.decode('utf-8'))

            for key, value in elementValues.items():
                elementValues[key] = value[0].strip()

            db.remove_element(elementValues['elementToDelete'])
            
            #Send message to server indicating successful post
            message = 'Element ' + elementValues['elementToDelete'] + ' was successfully deleted'

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-length', len(message))
            self.end_headers()
            self.wfile.write(bytes(message, 'utf-8'))
        
        #Post request for uploading an SDF file
        elif self.path == '/upload_sdf_file.html':
            content_length = int(self.headers['Content-Length'])

            skipped = 0

            #Skip 4 lines on the SDF file
            for i in range(0,4):
                string = next(self.rfile)

                skipped += len(string)
            
            #Create a temporary file to store the file content
            file_data = self.rfile.read(content_length - skipped)

            with tempfile.NamedTemporaryFile(delete=False) as sdf_file:
                sdf_file.write(file_data)

            with open(sdf_file.name, 'r') as f:
                content = f.read()

            moleculeName = re.search(r'name="moleculeName"\s+(.*)', content).group(1)
            
            #Add the molecule described in the file
            db.add_molecule(moleculeName, open(sdf_file.name))

            os.remove(sdf_file.name)

            #Create a message to return to the server
            message = "Molecule " + moleculeName + " was successfully added"

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-length', len(message))
            self.end_headers()
            self.wfile.write(bytes(message, 'utf-8'))
        
        #If the requested POST is not specified above
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('404: not found', 'utf-8'))

#Run the server indefinitely 
httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
httpd.serve_forever()