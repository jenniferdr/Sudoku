# Javier Muniz  08-11277
# Jennifer Dos Reis 08-10323
# Jose Goncalves 08-10455

# El sudoku se representa como un conjunto de variables (una por cada combinacion
# de fila, columna y valor) que deben satisfacer las restricciones normales
# de un sudoku.
# Este script genera las clausulas minimas que debe cumplir todo sudoku, en
# formato DIMACS. Luego para cada sudoku de la entrada se agrega un clausula
# unitaria por cada valor fijo y se utiliza MiniSAT para resolverlo.

import subprocess
import sys

# Representa una casilla y su valor en un entero, para usarlo de nombre de
# variable en la formula CNF
def enc(i,j,v):
    return i*100 + j*10 + v

limites = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
cuadrados = [] # Guarda las listas con las casillas que conforman cada cuadrado

for (fi,c) in limites:
    set = []
    for i in range(fi,fi+3):
        for j in range(c,c+3):
            set.append((i,j))
    cuadrados.append(set)

# Generar las clausulas basicas
clauses = ""

# Cada casilla debe tener un valor: 81 clausulas
for i in range(1,10):
    for j in range(1,10):
        s = str(enc(i,j,1))
        for v in range(2,10):
            s += " "+str(enc(i,j,v))
        s += " 0\n"
        clauses += s

# Solo Un valor por casilla: 2916 clausulas 
for i in range(1,10):
    for j in range(1,10):
        for v in range(1,10):
            for v2 in range(v+1,10):
                clauses += str(-enc(i,j,v))+" "+str(-enc(i,j,v2))+" 0\n"

#No repetir valores en fila: 2916 clausulas 
for i in range(1,10):
    for j in range(1,10):
        for j2 in range(j+1,10):
            for v in range(1,10):
                clauses += str(-enc(i,j,v))+" "+str(-enc(i,j2,v))+" 0\n"

#No repetir valores en columna: 2916 clausulas
for i in range(1,10):
    for i2 in range(i+1,10):
        for j in range(1,10):
            for v in range(1,10):
                clauses += str(-enc(i,j,v))+" "+str(-enc(i2,j,v))+" 0\n"


# No se repiten valores en los cuadrados: 1458
for c in cuadrados:
    for ind in range(9):
        for ind2 in range(ind+1,9):
            for v in range(1,10):
                (i,j) = c[ind]
                (i2,j2) = c[ind2]
                if (i==i2 or j==j2): continue
                clauses += str(-enc(i,j,v))+" "+str(-enc(i2,j2,v))+" 0\n"

g = open(sys.argv[1]) # Archivo con los sudokus a resolver

for sudoku in g:

    f = open("clauses.cnf", "w")

    unitarias = []

    i = 1
    j = 0

    for l in sudoku[0:len(sudoku)-2]:
        j += 1
        if j > 9:
            j = 1
            i += 1
        if l == ".": continue
        v = int(l)
        unitarias.append(enc(i,j,v))

    total = 10206 + 81 + len(unitarias)

    f.write("p cnf 999 "+str(total)+"\n")

    # Reglas unitarias: casillas con valor fijo 
    for c in unitarias:
        f.write(str(c)+" 0\n")

    f.write(clauses)
    f.close()

    null = open("/dev/null")

    subprocess.call(["./minisat_static","clauses.cnf","result"], stdout=null)

    res = open("result")

    sud = {}

    l1 = res.readline()
    if l1 == "SAT\n":
        l2 = res.readline()
        res = ""
        for i in l2.split(" "):
            n = int(i)
            if n > 0:
                res += str( (n % 10) )
                sud[(n / 100, (n / 10) % 10)] = n % 10
        print res
    else:
        print "UNSAT"
