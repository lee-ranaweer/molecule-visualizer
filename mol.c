#include "mol.h"

//Copies the values of element, x, y, and z into the atom stored at atom
void atomset(atom *atom, char element[3], double *x, double *y, double *z){
    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

//Copies the values in the atom to element, x, y, and z
void atomget(atom *atom, char element[3], double *x, double *y, double *z){
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

//Copies the values of a1, a2, atoms, and epairs into the the bond stored at bond
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);
}

//Copies the values in the bond to a1, a2, atoms and epairs
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}

//Computes the z, x1, y1, x2, y2, len, dx, and dy values of the bond
void compute_coords(bond *bond){
    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2.0;
    bond->len = sqrt((bond->x2 - bond->x1) * (bond->x2 - bond->x1)  + (bond->y2 - bond->y1) * (bond->y2 - bond->y1));
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;
}

//Returns the address of allocated memory for a molecule
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max){
    //Allocate memory for a molecule
    molecule *newMolecule = malloc(sizeof(struct molecule));

    if(newMolecule == NULL){
        return NULL;
    }

    newMolecule->atom_max = atom_max; 
    newMolecule->atom_no = 0;
    newMolecule->atoms = malloc(sizeof(struct atom) * atom_max);
    newMolecule->atom_ptrs = malloc(sizeof(struct atom*) * atom_max);

    newMolecule->bond_max = bond_max;
    newMolecule->bond_no = 0;
    newMolecule->bonds = malloc(sizeof(struct bond) * bond_max);
    newMolecule->bond_ptrs = malloc(sizeof(struct bond*) * bond_max);

    //Return pointer to allocated molecule
    return newMolecule;
}

//Returns the address of allocated memory for a molecule with copied atoms and bonds from src 
molecule *molcopy(molecule *src){
    //Allocate memory for a molecule 
    molecule *newMolecule = molmalloc(src->atom_max, src->bond_max);

    if(newMolecule == NULL){
        return NULL;
    }

    //Copy the atoms from src to the molecule
    for(int i = 0; i < src->atom_no; i++){
        molappend_atom(newMolecule, src->atom_ptrs[i]);
    }

    //Copy the bonds from src to the molecule
    for(int i = 0; i < src->bond_no; i++){
        molappend_bond(newMolecule, src->bond_ptrs[i]);
    }

    for(int i = 0; i < newMolecule->bond_no; i++){
        newMolecule->bond_ptrs[i]->atoms = newMolecule->atoms;
    }
    
    //Return pointer to allocated molecule
    return newMolecule;
}

//Free the molecule in memory associated with ptr
void molfree(molecule *ptr){
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

//Appends an atom to atoms in the molecule
void molappend_atom(molecule *molecule, atom *atom){
    //If atom_max is equal to atom_no then increment atom_max
    if(molecule->atom_no == molecule->atom_max){
        //If atom_max was equal to 0 incremented it to 1 
        if(molecule->atom_max == 0){
            molecule->atom_max = 1;
        }
        
        //Otherwise it should be doubled
        else{
            molecule->atom_max *= 2;
        }
        
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);

        for(int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &(molecule->atoms[i]);
        }
    }

    //Append the new atom to the first available space in atoms
    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &(molecule->atoms[molecule->atom_no]);
    molecule->atom_no++;
}

//Appends a bond to bonds in the molecule
void molappend_bond(molecule *molecule, bond *bond){
    if(molecule->bond_no == molecule->bond_max){
        //If bond_max was equal to 0 incremented it to 1 
        if(molecule->bond_max == 0){
            molecule->bond_max = 1;
        }
        
        //Otherwise it should be doubled
        else{
            molecule->bond_max *= 2;
        }
        
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);

        //Update atoms in every bond to the new molecule atoms
        for(int i = 0; i < molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &(molecule->bonds[i]);
        }
    }

    //Append the new bond to the first available space in bonds
    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &(molecule->bonds[molecule->bond_no]);
    molecule->bond_no++;
}

//Compares two atoms
int atom_comp(const void *a, const void *b){
    atom **atom_a, **atom_b;
    atom_a = (struct atom**)(a); 
    atom_b = (struct atom**)(b);

    //Compare the z values of each atomn
    if((*atom_a)->z > (*atom_b)->z){
        return 1;
    }

    if((*atom_a)->z == (*atom_b)->z){
        return 0;
    }

    else{
        return -1;
    }
}

//Compares two bonds
int bond_comp(const void *a, const void *b){
    bond **bond_a, **bond_b;
    bond_a = (struct bond**)(a);
    bond_b = (struct bond**)(b);

    if((*bond_a)->z > (*bond_b)->z){
        return 1;
    }

    if((*bond_a)->z == (*bond_b)->z){
        return 0;
    }

    else{
        return -1;
    }
}

//Sorts the molecule with ascending z values in the atoms and bonds
void molsort(molecule *molecule){
    //Sort the atoms in atom_ptrs
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom*), atom_comp);
    
    //Sort the bonds in bond_ptrs
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond*), bond_comp);
}

//Sets values in an affine transformation matrix corresponding to a rotation of deg degrees around the x axis
void xrotation(xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0); 
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

//Sets values in an affine transformation matrix corresponding to a rotation of deg degrees around the y axis
void yrotation(xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0); 
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

//Sets values in an affine transformation matrix corresponding to a rotation of deg degrees around the z axis
void zrotation(xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0); 
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

//Applies the transformation matrix to all the atoms in the molecule
void mol_xform(molecule *molecule, xform_matrix matrix){
    double x;
    double y;
    double z;
    for(int i = 0; i < molecule->atom_no; i++){
        x = matrix[0][0] * molecule->atom_ptrs[i]->x + matrix[0][1] * molecule->atom_ptrs[i]->y + matrix[0][2] * molecule->atom_ptrs[i]->z;
        y = matrix[1][0] * molecule->atom_ptrs[i]->x + matrix[1][1] * molecule->atom_ptrs[i]->y + matrix[1][2] * molecule->atom_ptrs[i]->z;
        z = matrix[2][0] * molecule->atom_ptrs[i]->x + matrix[2][1] * molecule->atom_ptrs[i]->y + matrix[2][2] * molecule->atom_ptrs[i]->z;

        molecule->atom_ptrs[i]->x = x;
        molecule->atom_ptrs[i]->y = y;
        molecule->atom_ptrs[i]->z = z;
    }

    for(int i = 0; i < molecule->bond_no; i++){
        compute_coords(molecule->bond_ptrs[i]);
    }
}
