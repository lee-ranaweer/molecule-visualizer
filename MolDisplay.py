import molecule;

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">\n"""

footer = """</svg>"""

offsetx = 500
offsety = 500

#Represents an atom in a molecule
class Atom:
    def __init__(self, c_atom):
        self.atom = c_atom
        self.z = c_atom.z
    
    def __str__(self):
        return '%s %f %f %f' % (self.atom.element, self.atom.x, self.atom.y, self.atom.z)
    
    #Retrun svg string for atom
    def svg(self):
        x = self.atom.x * 100.00 + offsetx
        y = self.atom.y * 100.0 + offsety

        #Set radius
        if self.atom.element in radius:
            r = radius[self.atom.element]
        
        #If colour is not found in radius array then set to default 
        else:
            r = radius['X']

        #Set colour
        if self.atom.element in element_name:
            colour = element_name[self.atom.element]
        
        #If colour is not found in element_name array then set to default 
        else:
            colour = element_name['X']

        return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (x, y, r, colour)
    
#Represents a bond in a molecule
class Bond:
    def __init__(self, c_bond):
        self.bond = c_bond
        self.z = c_bond.z
    
    def __str__(self):
        return '%f %f %f %f %f %f %f %f %f %f %f' % (self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2,self. bond.y2, self.bond.len, self.bond.dx, self.bond.dy, self.bond.z)

    #Retrun svg string for bond
    def svg(self):
        x1 = (self.bond.x1 * 100.0 + offsetx) - self.bond.dy * 10
        y1 = (self.bond.y1 * 100.0 + offsety) + self.bond.dx * 10
        x2 = (self.bond.x1 * 100.0 + offsetx) + self.bond.dy * 10
        y2 = (self.bond.y1 * 100.0 + offsety) - self.bond.dx * 10
        x3 = (self.bond.x2 * 100.0 + offsetx) + self.bond.dy * 10
        y3 = (self.bond.y2 * 100.0 + offsety) - self.bond.dx * 10
        x4 = (self.bond.x2 * 100.0 + offsetx) - self.bond.dy * 10
        y4 = (self.bond.y2 * 100.0 + offsety) + self.bond.dx * 10

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x1, y1, x2, y2, x3, y3, x4, y4)

#Represents a molecule
class Molecule(molecule.molecule):
    def __str__(self):
        str = ''
        for i in range(self.atom_no):
            atom = Atom(self.get_atom(i))
            str += atom.__str__()
            str += '\n'
        
        for i in range(self.bond_no):
            bond = Bond(self.get_bond(i))
            str += bond.__str__()
            str += '\n'
        
        return str

    #Retrun svg string for molecule using atom and bond svg methods
    def svg(self):
        str = ''

        str += header

        atom_no = 0
        bond_no = 0

        while((atom_no < self.atom_no) and (bond_no < self.bond_no)):
            atom = Atom(self.get_atom(atom_no))
            bond = Bond(self.get_bond(bond_no))
            if(atom.z < bond.z):
                str += atom.svg()
                atom_no += 1
                
            else:
                bond = Bond(self.get_bond(bond_no))
                str += bond.svg()
                bond_no += 1
                
        while(atom_no < self.atom_no):
            atom = Atom(self.get_atom(atom_no))
            str += atom.svg()
            atom_no += 1
        
        while(bond_no < self.bond_no):
            bond = Bond(self.get_bond(bond_no))
            str += bond.svg()
            bond_no += 1
    
        str += footer

        return str
    
    #Parse an sdf file into the molecule object
    def parse(self, file):

        for i in range(3):
            f = file.readline()
        
        line = file.readline().split()
        atom_no = int(line[0])
        bond_no = int(line[1])

        for i in range(atom_no):
            line = file.readline().split()
            element = line[3]
            x = float(line[0])
            y = float(line[1])
            z = float(line[2])

            self.append_atom(element, x, y, z)
        
        for i in range(bond_no):
            line = file.readline().split()
            a1 = int(line[0]) - 1
            a2 = int(line[1]) - 1
            epairs = int(line[2])

            self.append_bond(a1, a2, epairs)
