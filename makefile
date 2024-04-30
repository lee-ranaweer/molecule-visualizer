CC = clang 
CFLAGS = -Wall -std=c99 -pedantic

all: _molecule.so
	
mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

molecule_wrap.c molecule.py: molecule.i
	swig -python molecule.i

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -I/usr/include/python3.11 -c molecule_wrap.c -fPIC -o molecule_wrap.o

_molecule.so: molecule_wrap.o libmol.so
	$(CC) molecule_wrap.o -shared -L/usr/lib/python3.11/config3.11m-x86_64-linux-gnu -lpython3.11 -L. -lmol -dynamiclib -o _molecule.so

clean:
	rm -f *.o *.so