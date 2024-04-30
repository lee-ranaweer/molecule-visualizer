import os;
import sqlite3;
import MolDisplay

class Database:
    #Constructor to create a database connection to "molecules.db"
    def __init__(self, reset=False):
        #If reset is set to true delete the file "molecules.db"
        if reset and os.path.exists('molecules.db'):
            os.remove('molecules.db')

        #Create a database connection to "molecules.db"
        self.conn = sqlite3.connect('molecules.db')

    def create_tables(self):
        #If the Elements table does not exist create it
        if not self.table_exists('Elements'):
            self.conn.execute('''CREATE TABLE Elements
                                (ELEMENT_NO   INTEGER      NOT NULL,
                                 ELEMENT_CODE VARCHAR(3)   NOT NULL,
                                 ELEMENT_NAME VARCHAR(32)  NOT NULL,
                                 COLOUR1      CHAR(6)      NOT NULL,
                                 COLOUR2      CHAR(6)      NOT NULL,
                                 COLOUR3      CHAR(6)      NOT NULL,
                                 RADIUS       DECIMAL(3)   NOT NULL,
                                 PRIMARY KEY(ELEMENT_CODE))''')
        
        #If the Atoms table does not exist create it
        if not self.table_exists('Atoms'):
            self.conn.execute('''CREATE TABLE Atoms
                                (ATOM_ID      INTEGER      NOT NULL     PRIMARY KEY  AUTOINCREMENT,
                                 ELEMENT_CODE VARCHAR(3)   NOT NULL,
                                 X            DECIMAL(7,4) NOT NULL,
                                 Y            DECIMAL(7,4) NOT NULL,
                                 Z            DECIMAL(7,4) NOT NULL,
                                 FOREIGN KEY(ELEMENT_CODE) REFERENCES Elements)''')

        #If the Bonds table does not exist create it
        if not self.table_exists('Bonds'):
            self.conn.execute('''CREATE TABLE Bonds
                                (BOND_ID      INTEGER      NOT NULL     PRIMARY KEY  AUTOINCREMENT,
                                 A1           INTEGER      NOT NULL,
                                 A2           INTEGER      NOT NULL,
                                 EPAIRS       INTEGER      NOT NULL)''')

        #If the Molecules table does not exist create it
        if not self.table_exists('Molecules'):
            self.conn.execute('''CREATE TABLE Molecules
                                (MOLECULE_ID  INTEGER      NOT NULL     PRIMARY KEY  AUTOINCREMENT,
                                 NAME         TEXT         NOT NULL     UNIQUE)''')

        #If the MoleculeAtom table does not exist create it
        if not self.table_exists('MoleculeAtom'):
            self.conn.execute('''CREATE TABLE MoleculeAtom
                                (MOLECULE_ID  INTEGER      NOT NULL,
                                 ATOM_ID      INTEGER      NOT NULL,
                                 PRIMARY KEY(MOLECULE_ID, ATOM_ID),
                                 FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules,
                                 FOREIGN KEY(ATOM_ID) REFERENCES Atoms)''')

        #If the MoleculeBond table does not exist create it
        if not self.table_exists('MoleculeBond'):
            self.conn.execute('''CREATE TABLE MoleculeBond
                                (MOLECULE_ID  INTEGER      NOT NULL,
                                 BOND_ID      INTEGER      NOT NULL,
                                 PRIMARY KEY(MOLECULE_ID, BOND_ID),
                                 FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules,
                                 FOREIGN KEY(BOND_ID) REFERENCES Bonds)''')

    #Sets the values in the table named table based on the values in the tuple values
    def __setitem__(self, table, values):
        placeholders = ','.join(['?'] * len(values))
        query = 'INSERT INTO {} VALUES ({})'.format(table, placeholders)
        self.conn.execute(query, values)

    #Adds the attributes of the atom object to the Atoms table
    def add_atom(self, molname, atom):
        values = str(atom).split()

        #Add the atom as an entry in the Atoms table
        self.conn.execute('INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z) VALUES (?, ?, ?, ?)', (values[0], values[1], values[2], values[3]))
        #Retrieve the atom ID from the previous insert
        atom_id = self.conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        #Link molecule to the atom in the MoleculeAtom table
        self.conn.execute('INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES ((SELECT MOLECULE_ID FROM Molecules WHERE NAME=?), ?)', (molname, atom_id))

    #Adds the attributes of the bond object to the Bonds table
    def add_bond(self, molname, bond):
        values = str(bond).split()

        #Add the bond as an entry in the Bonds table
        self.conn.execute('INSERT INTO Bonds (A1, A2, EPAIRS) VALUES (?, ?, ?)', (values[0], values[1], values[2]))
        #Retrieve the bond ID from the previous insert
        bond_id = self.conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        #Link molecule to the bond in the MoleculeBond table
        self.conn.execute('INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES ((SELECT MOLECULE_ID FROM Molecules WHERE NAME=?), ?)', (molname, bond_id))

    #Adds a molecule as an entry in the Molecules table
    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        
        mol.parse(fp)

        self.conn.execute('INSERT INTO Molecules (NAME) VALUES (?)', (name,))

        #Add the atoms in the molecule as entries in the Atoms table
        for i in range(mol.atom_no):
            self.add_atom(name, MolDisplay.Atom(mol.get_atom(i)))
        
        #Add the bonds in the molecule as entries in the Bonds table
        for i in range(mol.bond_no):
            self.add_bond(name, MolDisplay.Bond(mol.get_bond(i)))
            
    #Returns a Molecule object initialized based on the molecule named name
    def load_mol(self, name):
        mol = MolDisplay.Molecule()

        #Retrieve all atoms and append them to the Molecule object in order of increasing ATOM_ID
        atoms = self.conn.execute('''SELECT Atoms.*
                                     FROM Atoms
                                     JOIN MoleculeAtom
                                     ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
                                     JOIN Molecules
                                     ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
                                     WHERE Molecules.NAME = ?''', (name,)).fetchall()

        for atom in atoms:
            mol.append_atom(atom[1], atom[2], atom[3], atom[4])

        #Retrieve all bonds and append them to the Molecule object in order of increasing BOND_ID
        bonds = self.conn.execute('''SELECT Bonds.*
                                     FROM Bonds
                                     JOIN MoleculeBond
                                     ON Bonds.BOND_ID = MoleculeBond.BOND_ID
                                     JOIN Molecules
                                     ON MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
                                     WHERE Molecules.NAME = ?
                                     ORDER BY Bonds.BOND_ID''', (name,)).fetchall()

        for bond in bonds:
            mol.append_bond(bond[1], bond[2], bond[3])

        return mol

    #Returns a dictionary mapping ELEMENT_CODE values to RADIUS values based on the Elements table
    def radius(self):
        radiusvalues = self.conn.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements").fetchall()
        
        #Create a dictionary mapping ELEMENT_CODE to RADIUS
        dictionary = {radius[0]: radius[1] for radius in radiusvalues}
        
        return dictionary
    
    #Returns a dictionary mapping ELEMENT_CODE values to ELEMENT_NAME values based on the Elements table
    def element_name(self):
        elementvalues = self.conn.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements").fetchall()

        #Create a dictionary mapping ELEMENT_CODE to ELEMENT_NAME
        dictionary = {element[0]: element[1] for element in elementvalues}

        return dictionary
    
    #Returns SVG string for radial gradients
    def radial_gradients( self ):
        query = "SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements"
        rows = self.conn.execute(query).fetchall()

        gradients = ""
        for row in rows:
            ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 = row
            radialGradientSVG = """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/>
                <stop offset="50%%" stop-color="#%s"/>
                <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3)
            gradients += radialGradientSVG

        return gradients

    #Determines if a table exists in the database
    def table_exists(self, table_name):
        result = self.conn.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table_name,))
        return result.fetchone() is not None

    #Removes element from Elements table
    def remove_element(self, element_code):
        #Remove element with matching element_code
        self.conn.execute('DELETE FROM Elements WHERE ELEMENT_CODE=?', (element_code,))
    
    #Retreives info on all molecules
    def get_molecule_info(self):
        cursor = self.conn.cursor()

        molecules = self.conn.execute('SELECT NAME, MOLECULE_ID FROM Molecules').fetchall()

        molecule_info = []
        
        for row in molecules:
            molecule_id = row[1]
            cursor.execute('SELECT COUNT(*) FROM MoleculeAtom WHERE MOLECULE_ID=?', (molecule_id,))
            num_atoms = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM MoleculeBond WHERE MOLECULE_ID=?', (molecule_id,))
            num_bonds = cursor.fetchone()[0]
            molecule_info.append((row[0], molecule_id, num_atoms, num_bonds))

        return molecule_info
        