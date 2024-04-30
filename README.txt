Developed by Nelith Ranaweera - April 2023

Description: 
This project runs a webserver that allows users to add unique elements, upload
SDF files containing molecules, and view the molecules on the server. The
interface is made up of 4 pages, 'Home', 'Add/remove element',
'Upload SDF file', and 'View molecules'. The element data will be used to
provide the visual representation of each atom. Once a molecule has been
uploaded it can be displayed on the View molecules page. A 'testfiles' folder
with instructions has been included in the project directory.

Instructions: 
- Run "make" command in linux terminal 
- "export LD_LIBRARY_PATH=." may be necessary 
- Run "python3 server.py 8000" in terminal 
- Load "localhost:8000/home.html" into browser
- Navigate the tabs to access different functions
