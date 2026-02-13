from test_instance import generate_bays_data
from utils import*
from preprocessing import *
#from plotting import plot_bays, plot_all_bays_with_moves
import os
import copy

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')  
import sys

#script_dir = os.path.dirname(os.path.realpath(__file__))
input_bays = generate_bays_data(file_name='../input/input_bays.xlsx')

α = 0.75
λ1 = 1
λ2 = 1
H = 4

def solve_all_bays(input_bays, α, λ1, λ2, H):
    all_moves = {}
    all_bays = {}
    all_relocation_moves={}
    all_erms={}

    # Loop over each bay in the dictionary
    for bay_num, bay in input_bays.items():
        print(f"SOLVE {bay_num} ***")
        moves, relocation_moves,erms, new_bay = local_search_heuristic(bay, α, λ1, λ2, H)
        #expected_moves = calculate_expected_relocation_moves(new_bay)

        # Store the moves and the new bay configuration in the dictionaries
        all_moves[bay_num] = moves
        all_relocation_moves[bay_num]=relocation_moves
        all_bays[bay_num] = new_bay
        all_erms[bay_num]=erms
        

    return all_moves, all_relocation_moves,all_erms,all_bays
# α, λ1, λ2, and H are parameters of your heuristic, replace them with their actual values

all_moves, all_relocation_moves,all_erms, all_bays = solve_all_bays(input_bays, α, λ1, λ2, H)

#plot_bays(input_bays,5,4, pdf_filename='../output/input_bays_plot.pdf')
#plot_bays(all_bays,5,4, pdf_filename='../output/output_bays_plot.pdf')

#export_to_excel(all_bays,file_name='../output/pre_processed_bays.xlsx')
#export_moves_to_excel(all_moves,file_name='../output/pre_processing_moves.xlsx')

#plot_all_bays_with_moves(input_bays,all_moves,pdf_filename='../output/pre_processing_moves_plot.pdf')
#plot_bays(all_bays,5,4, pdf_filename='output/pre_processed_bays_plot.pdf')



# Build S and lambdas variables based on the new_S_dict
bays=copy.deepcopy(input_bays)
S = {}
lambdas = {}
for bay, movement_dict in all_erms.items():
    for movement_group, s_value in movement_dict.items():
        S[(bay, movement_group)] = s_value
        if bay not in lambdas:
            lambdas[bay] = []
        lambdas[bay].append(movement_group)

#lambdas = {k: [lambda_k for (bay, lambda_k) in S.keys() if bay == k] for k in bays}

b = len(bays)
initial_bay = 2

def sort_bays(initial_bay, b):
    if initial_bay == 1:
        return [initial_bay] + [bay for bay in range(2, b+1)]
    elif initial_bay == b:
        return [initial_bay] + [bay for bay in range(b-1, 0, -1)]
    else:
        left = [bay for bay in range(initial_bay-1, 0, -1)]
        right = [bay for bay in range(initial_bay+1, b+1)]
        
        if initial_bay <= b/2:
            return [initial_bay] + left + right
        else:
            return [initial_bay] + right + left

sorted_bays = sort_bays(initial_bay, b)
print(sorted_bays)



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
T = 1000  # Some random number, adjust as needed

"""
# Create a tau dictionary to store the cumulative tau values for each lambda_k
tau_dict = {}
for bay in bays:
    cumulative_tau = tau
    for index, lambda_k in enumerate(lambdas[bay]):
        tau_dict[(bay, lambda_k)] = cumulative_tau
        cumulative_tau += tau

"""

def calculate_tau_for_group(movement_group):
    return 0 if movement_group is 0 else tau*len(movement_group) 

# Create a tau dictionary to store the cumulative tau values for each lambda_k
tau_dict = {}
for bay in bays:
    cumulative_tau = 0
    for movement_group in lambdas[bay]:
        tau_value = calculate_tau_for_group(movement_group)
        tau_dict[(bay, movement_group)] = cumulative_tau + tau_value
        cumulative_tau += tau_value


bays = list(range(1, b + 1))
bays=sort_bays(initial_bay, b)

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

# In the objective function
for k in bays:
    for movement_group in lambdas[k]:
        coefficient = S[(k, movement_group)]
        objective_terms.append(f"{coefficient}*Y[{k},{movement_group}]")


"""
for k in bays:
    # For each bay, iterate over all the lambda_k values
    for lambda_k in lambdas[k]:
        coefficient = S[(k, lambda_k)]
        objective_terms.append(f"{coefficient}*Y[{k},{lambda_k}]")
"""


objective_expression = " + ".join(objective_terms)
print(f"Objective Function: Minimize {objective_expression}")

for k, lambda_k in S.keys():
    objective.SetCoefficient(Y[(k, lambda_k)], S[(k, lambda_k)])

objective.SetMinimization()


bays = sorted_bays

# Constraints
for k in bays:
    solver.Add(sum(Y[(k, lambda_k)] for lambda_k in lambdas[k]) == 1)

for k in bays:
    if k != sorted_bays[0]:
        solver.Add(sum(Y[(k, lambda_k)] for lambda_k in lambdas[k] if lambda_k != 0) <= sum(X[(l, k)] for l in bays if l != k))

for l in bays:
    if l != sorted_bays[0]:
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
lhs += sum(tau_dict[(k, lambda_k)] * Y[(k, lambda_k)] for k in bays for lambda_k in lambdas[k])
rhs = T
solver.Add(lhs <= rhs)

#solver.Add(sum(X[i, j] for i in bays for j in bays if i != j) <= b-1)

M = len(bays)  # a large enough M value, based on the number of bays

for i in bays:
    for j in bays:
        if sorted_bays.index(j) > sorted_bays.index(i):
            for k in bays:
                if sorted_bays.index(k) > sorted_bays.index(j):
                    solver.Add(X[(i, k)] + X[(i, j)] <= 1)  


for i in bays:
    for j in bays:
        if sorted_bays.index(j) < sorted_bays.index(i):
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





#########
#Revised
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_crane_movements(X, Y, bays, initial_bay):
    fig, ax = plt.subplots(figsize=(12, 7))

    # Sort bays and define a position for each
    sorted_bays = sorted(bays)
    bay_position = {bay: i+1 for i, bay in enumerate(sorted_bays)}

    # Draw Bays
    for bay, position in bay_position.items():
        ax.add_patch(patches.Rectangle((position-0.5, 1), 1, 10, edgecolor='black', facecolor='lightgray'))

    # Define y-positions for arrows
    left_to_right_y = 8.5
    right_to_left_y = 7.5

    movements = [move for move, value in X.items() if value.solution_value() > 0.5]
    if movements:
        start_bay = movements[0][0]
        end_bay = movements[-1][1]

    # Drawing crane movements based on X values
    for (i, j), value in X.items():
        if value.solution_value() > 0.5:
            start = bay_position[i]
            end = bay_position[j]

            if start < end:
                y_position = left_to_right_y
            else:
                y_position = right_to_left_y

            ax.annotate("", xy=(end, y_position), xytext=(start, y_position),
                        arrowprops=dict(arrowstyle="->", lw=1.5))
            
            if i == start_bay:
                ax.text(start, y_position + 0.3, 'start bay', horizontalalignment='center', color='blue')
            if j == end_bay:
                ax.text(end, y_position - 0.7, 'end bay', horizontalalignment='center', color='blue')

        # Drawing the preprocessing moves (lambda_k) and bay names
    for bay, position in bay_position.items():
        for (k, lambda_k), value in Y.items():
            if k == bay and value.solution_value() > 0.5:
                ax.text(position, 3, f"{lambda_k} moves", color='red', horizontalalignment='center')
        ax.text(position, 2, f"Bay {bay}", horizontalalignment='center')

    # Initial crane position (RMGC)
    initial_position = bay_position[initial_bay]
    ax.add_patch(patches.Rectangle((initial_position-0.3, 11), 0.6, 1, edgecolor='black', facecolor='yellow'))
    ax.add_patch(patches.Rectangle((initial_position-0.3, 0), 0.6, 1, edgecolor='black', facecolor='yellow'))
    ax.text(initial_position, 11.5, 'RMGC', horizontalalignment='center', verticalalignment='center')
    ax.text(initial_position, 0.5, 'RMGC', horizontalalignment='center', verticalalignment='center')

    # RMGC final position
    final_position = bay_position[end_bay]
    ax.add_patch(patches.Rectangle((final_position-0.3, 11), 0.6, 1, edgecolor='black',linestyle='--', facecolor='yellow', hatch="//"))
    ax.add_patch(patches.Rectangle((final_position-0.3, 0), 0.6, 1, edgecolor='black',linestyle='--', facecolor='yellow', hatch="//"))
    ax.text(final_position, 11.5, 'RMGC', horizontalalignment='center', verticalalignment='center', backgroundcolor='yellow')
    ax.text(final_position, 0.5, 'RMGC', horizontalalignment='center', verticalalignment='center', backgroundcolor='yellow')

    # Setting the limits and the title
    ax.set_ylim(0, 13)
    ax.set_xlim(0, len(bays) + 2)
    ax.set_title("Crane Movements")
    ax.axis('off')
    plt.show()

# Call the visualization function
# Example call (Make sure X and Y dictionaries are defined before calling)
# initial_bay = 3  # Set this to the initial bay position
visualize_crane_movements(X, Y, bays, initial_bay)







def main():
    
    pass

if __name__ == "__main__":
    main()
