import pulp

n = 3    # высота/ширина квадрата
M = n*(n*n+1)/2    # постоянная магического квадрата

print("M =", int(M))

prob = pulp.LpProblem("Magic Square", pulp.LpMinimize)
vals = range(1, n*n+1)
rows = cols = diags = range(1, n+1)
choices = pulp.LpVariable.dicts("Choice", (vals, rows, cols, diags), cat="Binary")
square = [ [(i+1,j+1) for i in range(n)] for j in range(n) ]

# A constraint ensuring that only one value can be in square is created
for r in rows:
    for c in cols:
        for d in diags:
            prob += pulp.lpSum([choices[v][r][c][d] for v in vals]) == 1
'''
# сумма элементов в каждой строке равна M
for i in range(n):    
    prob += (pulp.lpSum([square[i][j] for j in range(n)]) == M)
    
# сумма элементов в каждом столбце равна M
for i in range(n):    
    prob += (pulp.lpSum([square[j][i] for j in range(n)]) == M)
    
# сумма элементов в диагоналях равна M
prob += (pulp.lpSum([square[i][i] for i in range(n)]) == M)
prob += (pulp.lpSum([square[i][n-i-1] for i in range(n)]) == M)
'''
while True:
    prob.solve()
    # The status of the solution is printed to the screen
    print("Status:", pulp.LpStatus[prob.status])
    # The solution is printed if it was deemed "optimal" i.e met the constraints
    if pulp.LpStatus[prob.status] == "Optimal":
        for r in rows:
            for c in cols:
                for d in diags:
                    for v in vals:
                        if pulp.value(choices[v][r][c][d]) == 1:
                            print(str(v).rjust(2), end=' ')
                print()
            print()
        print()
        prob += (
            pulp.lpSum(
                [
                    choices[v][r][c][d]
                    for v in vals
                    for r in rows
                    for c in cols
                    for d in diags
                    if pulp.value(choices[v][r][c][d]) == 1
                ]
            )
            <= 80
        )
        break
    else:
        break
