from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')  
import sys
# S values for bay 1
b=4
S = {
    (1, 0): 10,
    (1, 1): 8,
    (1, 2): 7,
    (1, 3): 5,
    (1, 4): 2,
    (1, 5): 1,
    (1,6):0
}
for bay in [2, 3,4]:
    current_S = 10  
    decrement = 1  
    for lambda_k in range(9):  
        S[(bay, lambda_k)] = current_S
        current_S = max(0, current_S - decrement)  

bays=[1,2,3,4]
lambdas = {k: [lambda_k for (bay, lambda_k) in S.keys() if bay == k] for k in bays}

# Fixed preprocessing time
#tau_value = 30
#tau = {(bay, lambda_k): tau_value for (bay, lambda_k) in S.keys() }

# Travel times between bays
def calculate_travel_time(from_bay, to_bay):
    if from_bay == to_bay:
        return 0  # No time to move within the same bay
    base_time = 40  # For adjacent bays
    separation = abs(from_bay - to_bay)   # Number of bays in between
    return base_time + (separation * 3.5)

t = {(i, j): calculate_travel_time(i, j) for i in range(1, b+1) for j in range(1, b+1) if i != j}

tau = 30  # Given
T = 6000  # Some random number, adjust as needed


Y = {}
X = {}
bays = list(range(1, b + 1))

Y = {}
for k, lambda_k in S.keys():
    Y[(k, lambda_k)] = solver.BoolVar(f'Y_{k}_{lambda_k}')


X = {}
for i in bays:
    for j in bays:
        if i != j:
            X[(i, j)] = solver.BoolVar(f'X_{i}_{j}')

objective_terms = []

# Objective Function
objective = solver.Objective()

for k in bays:
    # For each bay, iterate over all the lambda_k values
    for lambda_k in lambdas[k]:
        coefficient = S[(k, lambda_k)]
        objective_terms.append(f"{coefficient}*Y[{k},{lambda_k}]")

objective_expression = " + ".join(objective_terms)
print(f"Objective Function: Minimize {objective_expression}")

for k, lambda_k in S.keys():
    objective.SetCoefficient(Y[(k, lambda_k)], S[(k, lambda_k)])

objective.SetMinimization()



# Constraints
for k in bays:
    solver.Add(sum(Y[(k, lambda_k)] for lambda_k in lambdas[k]) == 1)

for k in bays:
    if k != 1:
        solver.Add(sum(Y[(k, lambda_k)] for lambda_k in lambdas[k] if lambda_k > 0) <= sum(X[(l, k)] for l in bays if l != k))

for l in bays:
    if l != 1:
           solver.Add(sum(X[(l, o)] for o in bays if o != l) <= sum(X[(k, l)] for k in bays if k != l))
#for l in bays:
#   solver.Add(sum(X[(k, l)] for k in bays if k != l) == sum(X[(l, o)] for o in bays if o != l))

# For Bay 1, only one exit
#solver.Add(sum(X[(1, o)] for o in bays if o != 1) == 1)

# For other bays, number of entries = number of exits
#for l in bays:
#    if l != 1:
#       solver.Add(sum(X[(l, o)] for o in bays if o != l) == sum(X[(k, l)] for k in bays if k != l))


lhs = sum(t[(k, l)] * X[(k, l)] for k in bays for l in bays if k != l)
lhs += sum(tau * lambda_k * Y[(k, lambda_k)] for k in bays for lambda_k in lambdas[k])
rhs = T
solver.Add(lhs <= rhs)

#solver.Add(sum(X[i, j] for i in bays for j in bays if i != j) <= b-1)

M = len(bays)  # a large enough M value, based on the number of bays

for i in bays:
    for j in bays:
        if j > i:
            for k in range(j+1, max(bays)+1):
                solver.Add(X[(i, k)] + X[(i, j)] <= 1)  # Either X[(i, j)] is 1 or X[(i, k)] is 1 but not both


for i in bays:
    for j in range(1, i):
        solver.Add(X[(i, j)] == 0)


#solver.Add(Y[(3, 8)] == 1)
#solver.Add(Y[(1, 5)] == 1)
#solver.Add(Y[(2, 8)] == 1)



# Solve the model
status = solver.Solve()

# Output the results
if status == pywraplp.Solver.OPTIMAL:
    print(f'Solution Found! Objective value = {solver.Objective().Value()}')
    for k, lambda_k in Y:
        if Y[(k, lambda_k)].solution_value() > 0.5:
            print(f'Perform {lambda_k} pre-processing moves in Bay {k}')
    for i, j in X:
        if X[(i, j)].solution_value() > 0.5:
            print(f'Move crane from Bay {i} to Bay {j}')
else:
    print('No optimal solution found!')



for k in bays:
    for lambda_k in lambdas[k]:
        print(f"Y[{k}, {lambda_k}] = {Y[(k, lambda_k)].solution_value()}")


for i in bays:
    for j in bays:
        if i != j:
            print(f"X[{i}, {j}] = {X[(i, j)].solution_value()}")





#print(solver.ExportModelAsLpFormat(False).replace('\\', '').replace(',_', ','), file=sys.stdout)

with open("output_filename.lp", "w") as file:
    file.write(solver.ExportModelAsLpFormat(False).replace('\\', '').replace(',_', ','))

