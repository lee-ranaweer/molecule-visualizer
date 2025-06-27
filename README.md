# Molecule Visualizer

### Overview

A fullstack app that converts SDF files of molecular structures into interactive 3D models using a custom-built library. You can upload files to visualize molecules directly in the web browser. Uploaded molecules are saved in a local database for easy management.

### How to run

1. Clone the repository
```
git clone https://gitlab.socs.uoguelph.ca/w25-4030-section-01/group_09/holo.git
```
2. Navigate to the project directory
```
cd molecule-visualizer
```
3. Run the following commands
```
make
export LD_LIBRARY_PATH=.
python3 server.py 8000
```
4. Access the following addresses on your browser: localhost:8000/home.html
5. Terminate the program using
```
crtl+c
```

### Technologies used
- C
- Python
- SQLite
- HTML
- CSS
- Javascript
