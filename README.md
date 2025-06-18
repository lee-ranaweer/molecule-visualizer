### Molecule Visualizer: 
This project runs a webserver that allows users to add unique elements, upload
SDF files containing molecules, and view the molecules on the server. The
interface is made up of 4 pages, 'Home', 'Add/remove element',
'Upload SDF file', and 'View molecules'. The element data will be used to
provide the visual representation of each atom. Once a molecule has been
uploaded it can be displayed on the View molecules page. A 'testfiles' folder
with instructions has been included in the project directory.

### How to run: 
Run the following commands
```
make
export LD_LIBRARY_PATH=.
python3 server.py 8000
```

Access the following addresses on your browser: localhost:8000/home.html

Terminate the program using
```
crtl+c
```

### Technologies used:
- C
- Python
- SQLite
- HTML
- Javascript
- CSS
