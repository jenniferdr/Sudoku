def enc(i,j,v):
    return i*100 + j*10 + v


f = open("clauses.cnf", "w")

sudoku = "...8.91....15..63..8.6.45..3.....7...7...2.949......56..5........7...92.1........"

sudoku2 = "....6...4..6.3....1..4..5.77.....8.5...8.....6.8....9...2.9....4....32....97..1.."

unitarias = []

i = 1
j = 0

for l in sudoku:
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

# Cada casilla debe tener un valor
for i in range(1,10):
    for j in range(1,10):
        s = str(enc(i,j,1))
        for v in range(2,10):
            s += " "+str(enc(i,j,v))
        s += " 0\n"
        f.write(s)

# Un valor por casilla
for i in range(1,10):
    for j in range(1,10):
        for v in range(1,10):
            for v2 in range(v+1,10):
                f.write(str(-enc(i,j,v))+" "+str(-enc(i,j,v2))+" 0\n")

#No repetir valores en fila
for i in range(1,10):
    for j in range(1,10):
        for j2 in range(j+1,10):
            for v in range(1,10):
                f.write(str(-enc(i,j,v))+" "+str(-enc(i,j2,v))+" 0\n")

#No repetir valores en columna
for i in range(1,10):
    for i2 in range(i+1,10):
        for j in range(1,10):
            for v in range(1,10):
                f.write(str(-enc(i,j,v))+" "+str(-enc(i2,j,v))+" 0\n")

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
                f.write(str(-enc(i,j,v))+" "+str(-enc(i2,j2,v))+" 0\n")

f.close()

import subprocess

null = open("/dev/null")

subprocess.call(["./minisat_static","clauses.cnf","result"], stdout=null)

res = open("result")

l1 = res.readline()
if l1 == "SAT\n":
    l2 = res.readline()
    count = 0
    res = ""
    for n in l2.split(" "):
        if int(n) < 0: continue
        count +=1
        if (count > 9):
            res += "\n"
            count = 0
        res += str(int(n) % 100)
    print res
else:
    print "UNSAT"
