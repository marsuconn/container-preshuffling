from test_instance import generate_bays_data
from utils import*
from preprocessing import *
from plotting import plot_bays, plot_all_bays_with_moves
import os
import copy

script_dir = os.path.dirname(os.path.realpath(__file__))
#input_bays = generate_bays_data(file_name='../input/input_bays.xlsx')
import pandas as pd

# Load the Excel file
stacks = 5
tiers = 4
data = pd.read_excel('../input/input_samples.xlsx')

df = pd.DataFrame(data, columns=["container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_time"])

# Process the dataframe to create the bays dictionary
# Convert the DataFrame to a bays dictionary
bays = {}
for idx, row in df.iterrows():
    bay = row['container_location_bay']
    
    # Check if the stack value is a string before converting to lowercase
    if isinstance(row['container_location_stack'], str):
        stack = row['container_location_stack'].lower()
    else:
        continue  # Skip this row if 'container_location_stack' is not a string
    
    if bay not in bays:
        bays[bay] = {f'stack{i+1}': [] for i in range(stacks)}  # initialize all stacks

    # Append tuple (container_id, tier), and convert appointment_time to integer
    bays[bay][stack].append((row['container_id'], int(row['appointment_time'])))

# Sort containers in each stack based on tier
for bay in bays.values():
    for stack_containers in bay.values():
        stack_containers.sort(key=lambda x: x[1])  # sort by tier



input_bays=copy.deepcopy(bays)

α = 0.75
λ1 = 1
λ2 = 1
H = 4

def solve_all_bays(input_bays, α, λ1, λ2, H):
    all_moves = {}
    all_bays = {}

    # Loop over each bay in the dictionary
    for bay_num, bay in input_bays.items():
        print(f"SOLVE {bay_num} ***")
        moves, new_bay = local_search_heuristic(bay, α, λ1, λ2, H)
        
        # Store the moves and the new bay configuration in the dictionaries
        all_moves[bay_num] = moves
        all_bays[bay_num] = new_bay

    return all_moves, all_bays

# α, λ1, λ2, and H are parameters of your heuristic, replace them with their actual values

all_moves, all_bays = solve_all_bays(input_bays, α, λ1, λ2, H)

plot_bays(input_bays,5,4, pdf_filename='../output/input_bays_plot_lmabda.pdf')
plot_bays(all_bays,5,4, pdf_filename='../output/output_bays_plot_lambda.pdf')

export_to_excel(all_bays,file_name='../output/pre_processed_bays_lambda.xlsx')
export_moves_to_excel(all_moves,file_name='../output/pre_processing_moves_lambda.xlsx')

plot_all_bays_with_moves(input_bays,all_moves,pdf_filename='../output/pre_processing_moves_plot_lambda.pdf')
#plot_bays(all_bays,5,4, pdf_filename='output/pre_processed_bays_plot.pdf')



def main():
    
    pass

if __name__ == "__main__":
    main()
