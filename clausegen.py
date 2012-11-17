def enc(i,j,v):
    return i*100 + j*10 + v

import sys

g = open(sys.argv[1])

count = 1
for sudoku in g:
    count += 1
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

    total = 11664 + 81 + len(unitarias)

    f.write("p cnf 999 "+str(total)+"\n")

    # Reglas unitarias: casillas con valor fijo 
    for c in unitarias:
        f.write(str(c)+" 0\n")

    # Cada casilla debe tener un valor 81 clausulas
    for i in range(1,10):
        for j in range(1,10):
            s = str(enc(i,j,1))
            for v in range(2,10):
                s += " "+str(enc(i,j,v))
            s += " 0\n"
            f.write(s)

    # Solo Un valor por casilla 2916 clausulas 
    for i in range(1,10):
        for j in range(1,10):
            for v in range(1,10):
                for v2 in range(v+1,10):
                    f.write(str(-enc(i,j,v))+" "+str(-enc(i,j,v2))+" 0\n")

    #No repetir valores en fila 2916 clausulas 
    for i in range(1,10):
        for j in range(1,10):
            for j2 in range(j+1,10):
                for v in range(1,10):
                    f.write(str(-enc(i,j,v))+" "+str(-enc(i,j2,v))+" 0\n")

    #No repetir valores en columna 2916 clausulas
    for i in range(1,10):
        for i2 in range(i+1,10):
            for j in range(1,10):
                for v in range(1,10):
                    f.write(str(-enc(i,j,v))+" "+str(-enc(i2,j,v))+" 0\n")


    # No se repiten valores en los cuadrados 1458
    limites = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
    cuadrados = []

    for (fi,c) in limites:
        set = []
        for i in range(fi,fi+3):
            for j in range(c,c+3):
                set.append((i,j))
        cuadrados.append(set)

    for c in cuadrados:
        for ind in range(9):
            for ind2 in range(ind+1,9):
                for v in range(1,10):
                    (i,j) = c[ind]
                    (i2,j2) = c[ind2]
                    if (i==i2 or j==j2): continue
                    f.write(str(-enc(i,j,v))+" "+str(-enc(i2,j2,v))+" 0\n")

    f.close()

    import subprocess

    null = open("/dev/null")

    subprocess.call(["./minisat_static","clauses.cnf","result"], stdout=null)

    res = open("result")

    l1 = res.readline()
    if l1 == "SAT\n":
        l2 = res.readline()
        res = ""
        for i in l2.split(" "):
            n = int(i)
            if n > 0:
                res += str( (n % 10) )
        print res
    else:
        print "UNSAT"
