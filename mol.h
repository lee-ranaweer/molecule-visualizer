#ifndef myheader
#define myheader

//Import libraries
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define M_PI 3.14159265358979323846

//atom - describes an atom in 3-dimensional space
//element - element name 
//x, y, z -  represents the 3-dimensional space of the atom
typedef struct atom{
 char element[3];
 double x, y, z;
} atom;


//bond - describes a covalent bond between 2 atoms
//a1, a2 - indices of 2 atoms in atoms
//epairs - number of electron pairs in the bond
//x1, x2, y1, y2 - x and y coordinates of a1 and a2
//z - average z value of a1 and a2
//len - distance from a1 to a2
//dx, dy - differences between the x and y values of a2 and a1 divided by the length of the bond
typedef struct bond{
 unsigned short a1, a2;
 unsigned char epairs;
 atom *atoms;
 double x1, x2, y1, y2, z, len, dx, dy;
} bond;

//molecule - describes a molecule consisting of 0 or more atoms and 0 or more bonds
//atom_max - records dimensionality of array pointed to by atoms
//atom_no - number of atoms currently stored in atoms
//atoms - allocated space for atoms in the molecule
//atom_ptrs - pointers to atoms in the molecule
//bond_max - records the dimensionality of array pointed to be bonds
//bond_no - number of bonds currently stored in bonds
//bonds - allocated space for bonds in the molecule
//bond_ptrs - pointers to bonds in the molecule
typedef struct molecule{
 unsigned short atom_max, atom_no;
 atom *atoms, **atom_ptrs;
 unsigned short bond_max, bond_no;
 bond *bonds, **bond_ptrs;
} molecule;

//xform_matrix - represents a 3-d affine transformation matrix
typedef double xform_matrix[3][3];

//Creates a struct mx_wrapper which will be converted into a mx_wrapper class in the molecule.i file
typedef struct mx_wrapper{
  xform_matrix xform_matrix;
} mx_wrapper;

//Copies the values of element, x, y, and z into the atom
void atomset(atom *atom, char element[3], double *x, double *y, double *z);

//Copies the values in the atom to element, x, y, and z
void atomget(atom *atom, char element[3], double *x, double *y, double *z);

//Copies the values of a1, a2, atoms, and epairs into the the bond
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);

//Copies the values in the bond to a1, a2, atoms and epairs
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);

//Computes the z, x1, y1, x2, y2, len, dx, and dy values of the bond
void compute_coords(bond *bond);

//Returns the address of allocated memory for a molecule
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max);

//Returns the address of allocated memory for a molecule with copied values from src 
molecule *molcopy(molecule *src);

//Free the molecule in memory associated with ptr
void molfree(molecule *ptr);

//Appends an atom to atoms in the molecule
void molappend_atom(molecule *molecule, atom *atom);

//Appends a bond to bonds in the molecule
void molappend_bond(molecule *molecule, bond *bond);

//Compares two atoms
int atom_comp(const void *a, const void *b);

//Compares two bonds
int bond_comp(const void *a, const void *b);

//Sorts the molecule with ascending z values in the atoms and bonds
void molsort(molecule *molecule);

//Sets values in an affine transformation matrix corresponding to a rotation of deg degrees around the x axis
void xrotation(xform_matrix xform_matrix, unsigned short deg);

//Sets values in an affine transformation matrix corresponding to a rotation of deg degrees around the y axis
void yrotation(xform_matrix xform_matrix, unsigned short deg);

//Sets values in an affine transformation matrix corresponding to a rotation of deg degrees around the z axis
void zrotation(xform_matrix xform_matrix, unsigned short deg);

//Applies the transformation matrix to all the atoms in the molecule
void mol_xform(molecule *molecule, xform_matrix matrix);

#endif
