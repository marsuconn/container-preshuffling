'''
from preprocessing_utils import*
from preprocessing_algorithms import *
from preprocessing_plotting import *
import pandas as pd
import json
import copy

import os
import multiprocessing

# Using os
num_cores = os.cpu_count()
print(f"Number of cores using os: {num_cores}")

# Using multiprocessing
num_cores_multiprocessing = multiprocessing.cpu_count()
print(f"Number of cores using multiprocessing: {num_cores_multiprocessing}")


#data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
#columns_needed = ["block_id", "container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_start_time", "appointment_end_time"]
#df_containers = data_containers[columns_needed]
#df_containers = process_appointment_data(df_containers)

#data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')

def process_data_for_block(block_df, stacks, tiers):
    bays = {}
    for idx, row in block_df.iterrows():
        bay = row['container_location_bay']
        if isinstance(row['container_location_stack'], str):
            stack = row['container_location_stack'].lower()
        else:
            continue
        
        if bay not in bays:
            bays[bay] = {f'stack{i+1}': [] for i in range(stacks)}

        bays[bay][stack].append((row['container_id'], int(row['appointment_time'])))

    for bay in bays.values():
        for stack_containers in bay.values():
            stack_containers.sort(key=lambda x: x[1])
    
    return bays

def solve_block(bays, α, λ1, λ2, H):
    all_moves, all_relocation_moves, all_erms, all_bays = {}, {}, {}, {}
    for bay_num, bay in bays.items():
        moves, relocation_moves, erms, new_bay = local_search_heuristic(bay, α, λ1, λ2, H)
        all_moves[bay_num] = moves
        all_relocation_moves[bay_num] = relocation_moves
        all_bays[bay_num] = new_bay
        all_erms[bay_num] = erms

    return all_moves, all_relocation_moves, all_erms, all_bays

def main(df_containers, data_blocks):
    results = {}
    for block_id in df_containers['block_id'].unique():
        specific_block_data = df_containers[df_containers['block_id'] == block_id]
        stacks = data_blocks[data_blocks['block_id'] == block_id]['stacks_per_bay'].values[0]
        tiers = data_blocks[data_blocks['block_id'] == block_id]['tiers_per_bay'].values[0]
        
        bays = process_data_for_block(specific_block_data, stacks, tiers)

        α, λ1, λ2, H = 0.75, 1, 1, 4
        all_moves, all_relocation_moves, all_erms, all_bays = solve_block(bays, α, λ1, λ2, H)
        
        results[block_id] = {
            'all_moves': all_moves,
            'all_relocation_moves': all_relocation_moves,
            'all_erms': all_erms,
            'all_bays': all_bays
        }

    return results

    #plot_bays_for_blocks(all_results, stacks, tiers, base_pdf_filename='./preprocessing/output/input_bays_plot')
    #plot_all_bays_with_moves_for_blocks(all_results, stacks, tiers, base_pdf_filename='./preprocessing/output/pre_processing_moves_plot')
    #export_to_excel_for_blocks(all_results, base_file_name='./preprocessing/output/pre_processed_bays')
    #export_moves_to_excel_for_blocks(all_results, base_file_name='./preprocessing/output/pre_processing_moves')


def get_final_positions(results):
    data = []
    for block_id, block_data in results.items():
        for bay_id, bay in block_data['all_bays'].items():
            for stack_id, stack in bay.items():
                for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                    container_id, _ = container_info  
                    data.append([container_id, block_id, bay_id, stack_id, tier])

    df = pd.DataFrame(data, columns=['container_id', 'new_block', 'new_bay', 'new_stack', 'new_tier'])
    return df



if __name__ == "__main__":
    data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
    columns_needed = ["block_id", "container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_start_time", "appointment_end_time"]
    df_containers = data_containers[columns_needed]
    df_containers = process_appointment_data(df_containers)
    df_containers['container_id'] = df_containers['container_id'].astype(str)  # Ensure the container_id column has the same data type in both DataFrames

    data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')

    results = main(df_containers, data_blocks)

    final_positions = get_final_positions(results)
    summary = pd.merge(df_containers, final_positions, on='container_id')
    summary = summary[['container_id', 'block_id', 'container_location_bay', 'new_block', 'new_bay',
                       'container_location_stack', 'container_location_tier', 'new_stack', 'new_tier']]
    summary.columns = ['container_id', 'current_block', 'current_bay', 'new_block', 'new_bay',
                       'current_stack', 'current_tier', 'new_stack', 'new_tier']
    
    summary.to_excel('./preprocessing/output/summary.xlsx', index=False)

'''


'''

from preprocessing_utils import *
from preprocessing_algorithms import *
from preprocessing_plotting import generate_plots,save_plots_to_pdf
import pandas as pd
import os

# Determine the number of cores
#num_cores = os.cpu_count()
#print(f"Number of cores: {num_cores}")



def solve_block(bays, α, λ1, λ2, H):
    all_moves, all_relocation_moves, all_erms, all_bays = {}, {}, {}, {}
    for bay_num, bay in bays.items():
        moves, relocation_moves, erms, new_bay = local_search_heuristic(bay, α, λ1, λ2, H)
        all_moves[bay_num] = moves
        all_relocation_moves[bay_num] = relocation_moves
        all_bays[bay_num] = new_bay
        all_erms[bay_num] = erms

    return all_moves, all_relocation_moves, all_erms, all_bays

# Main function to process and solve all blocks
def main(df_containers, data_blocks):
    results = {}
    for block_id in df_containers['block_id'].unique():
        specific_block_data = df_containers[df_containers['block_id'] == block_id]
        
        # Safely getting stacks and tiers values, providing default values in case of NaNs
        stacks = int(data_blocks.loc[data_blocks['block_id'] == block_id, 'stacks_per_bay'].fillna(5))
        tiers = int(data_blocks.loc[data_blocks['block_id'] == block_id, 'tiers_per_bay'].fillna(4))

        bays = process_data_for_block(specific_block_data, stacks, tiers)
        α, λ1, λ2, H = 0.75, 1, 1, 4  # These can be parameterized for flexibility
        all_moves, all_relocation_moves, all_erms, all_bays = solve_block(bays, α, λ1, λ2, H)

        results[block_id] = {
            'all_moves': all_moves,
            'all_relocation_moves': all_relocation_moves,
            'all_erms': all_erms,
            'all_bays': all_bays
        }

    return results

# Function to get final positions of containers
def get_final_positions(results):
    data = []
    for block_id, block_data in results.items():
        for bay_id, bay in block_data['all_bays'].items():
            for stack_id, stack in bay.items():
                for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                    container_id, _ = container_info  
                    data.append([container_id, block_id, bay_id, stack_id, tier])

    df = pd.DataFrame(data, columns=['container_id', 'new_block', 'new_bay', 'new_stack', 'new_tier'])
    return df

# Main execution
if __name__ == "__main__":
    data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
    columns_needed = [
        "block_id", 
        "container_id", 
        "container_location_bay", 
        "container_location_stack", 
        "container_location_tier", 
        "appointment_start_time", 
        "appointment_end_time"
    ]
    df_containers = data_containers[columns_needed].dropna()  # Drop rows with NaN values to avoid errors
    df_containers = process_appointment_data(df_containers)
  

    data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')
    data_blocks.set_index('block_id', inplace=True) #block_id in data_block should be unique

    blocks = df_containers['block_id'].unique()
    results = {}
    for block in blocks:
        block_df = df_containers[df_containers['block_id'] == block]
        stacks = data_blocks.loc[block, 'stacks_per_bay']
        tiers = data_blocks.loc[block, 'tiers_per_bay']

        #stacks = block_df['container_location_stack'].nunique()
        #tiers = block_df['container_location_tier'].nunique()
        results[block] = process_data_for_block(block_df, stacks, tiers)
    
    
    results = main(df_containers, data_blocks)
    final_positions = get_final_positions(results)

    # Ensure data types are compatible for merging
    df_containers['container_id'] = df_containers['container_id'].astype(str)
    final_positions['container_id'] = final_positions['container_id'].astype(str)

    summary = pd.merge(df_containers, final_positions, on='container_id')
    summary = summary[[
        'container_id', 
        'block_id', 
        'container_location_bay', 
        'new_block', 
        'new_bay',
        'container_location_stack', 
        'container_location_tier', 
        'new_stack', 
        'new_tier'
    ]]
    summary.columns = [
        'container_id', 
        'current_block', 
        'current_bay', 
        'new_block', 
        'new_bay',
        'current_stack', 
        'current_tier', 
        'new_stack', 
        'new_tier'
    ]
# create a function for summary 
    summary.to_excel('./preprocessing/output/summary.xlsx', index=False)
    all_plots = []
    for block_data in results.values():
        all_bays = block_data['all_bays']
        plots = generate_plots(all_bays)  
        all_plots.extend(plots) 

    #save_plots_to_pdf(all_plots, './preprocessing/output/all_bays_plots.pdf')
    #export_to_excel_multiple_blocks(results, file_name='./preprocessing/output/preprocessed_bays_multiple_blocks.xlsx')
    #export_moves_to_excel_multiple_blocks(results, file_name='./preprocessing/output/moves_multiple_blocks.xlsx')

'''


import pandas as pd
from preprocessing_algorithms import local_search_heuristic_v2  # Import the local search heuristic function


def process_appointment_data(df):
    #df = df.sort_values(by=['block_id', 'appointment_start_time'])
    df['appointment_time'] = df['appointment_start_time'].astype('category').cat.codes + 1
    return df


def process_data_for_block(block_df, stacks, tiers):
    bays = {}
    for _, row in block_df.iterrows():
        bay = row['container_location_bay']
        stack = f'stack{row["container_location_stack"]}'
        
        if bay not in bays:
            bays[bay] = {f'stack{i + 1}': [] for i in range(stacks)}

        appointment_time = row['appointment_time']
        bays[bay][stack].append((row['container_id'], appointment_time))

    for bay in bays.values():
        for stack_containers in bay.values():
            stack_containers.sort(key=lambda x: x[1])
    
    return bays


def solve_block(bays, α, λ1, λ2, H):
    all_preprocessing_moves = {} 
    all_move_sequences = {} 
    all_erms = {} 
    all_intermidate_bays_configs={}
    all_final_bays = {}  
    
    for bay_num, bay in bays.items():
        results, new_bay = local_search_heuristic_v2(bay, α, λ1, λ2, H)
        
        all_preprocessing_moves[bay_num] = results["preprocessing_moves"]
        all_move_sequences[bay_num] = results["move_sequences"]
        all_erms[bay_num] = results["erms"]
        all_intermidate_bays_configs[bay_num]=results['intermidiate_bays_configs']
        all_final_bays[bay_num] = new_bay

    return {
        'all_preprocessing_moves': all_preprocessing_moves,
        'all_move_sequences': all_move_sequences,
        'all_erms': all_erms,
        'all_intermidate_bays_configs':all_intermidate_bays_configs,
        'all_final_bays': all_final_bays  }




def get_container_summary_data(df_containers, results):
    # Getting initial positions of containers
    initial_positions = df_containers[[
        'container_id', 
        'block_id', 
        'container_location_bay', 
        'container_location_stack', 
        'container_location_tier'
    ]].copy()
    
    initial_positions.columns = [
        'container_id',
        'current_block',
        'current_bay',
        'current_stack',
        'current_tier'
    ]

    # Getting final positions of containers
    final_positions_data = []
    #intermediate_positions_data = {}  # Store intermediate bay configurations
    
    for block_id, block_data in results.items():
        for bay_id, bay in block_data['all_final_bays'].items():
            for stack_id, stack in bay.items():
                numeric_stack_id = int(stack_id.lstrip('stack'))  # Convert stack id to numeric
                for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                    container_id, _ = container_info  
                    final_positions_data.append([container_id, block_id, bay_id, numeric_stack_id, tier])
        
        # Storing intermediate bay configurations
        #intermediate_positions_data[block_id] = block_data['all_intermidate_bays_configs']

    final_positions = pd.DataFrame(final_positions_data, columns=[
        'container_id', 
        'new_block', 
        'new_bay', 
        'new_stack', 
        'new_tier'
    ])

    # Merging initial and final positions
    container_summary_data = pd.merge(initial_positions, final_positions, on='container_id', how='left')

    # Filling NaN values for containers that didn't move
    container_summary_data['new_block'].fillna(container_summary_data['current_block'], inplace=True)
    container_summary_data['new_bay'].fillna(container_summary_data['current_bay'], inplace=True)
    container_summary_data['new_stack'].fillna(container_summary_data['current_stack'], inplace=True)
    container_summary_data['new_tier'].fillna(container_summary_data['current_tier'], inplace=True)

    return container_summary_data#, intermediate_positions_data


def create_input_data(df_containers, data_blocks):
    input_data = {}
    
    for block_id in df_containers['block_id'].unique():
        block_df = df_containers[df_containers['block_id'] == block_id]
        
        stacks = int(data_blocks.loc[data_blocks['block_id'] == block_id, 'stacks_per_bay'].values[0])
        tiers = int(data_blocks.loc[data_blocks['block_id'] == block_id, 'tiers_per_bay'].values[0])

        bays = process_data_for_block(block_df, stacks, tiers)
        input_data[block_id] = bays

    return input_data


def create_final_output_bays(final_results):
    final_output_bays = {}
    
    for block_id, block_results in final_results.items():
        final_output_bays[block_id] = block_results['all_final_bays']
        
    return final_output_bays

import pandas as pd

def get_moves_and_erms_summary(final_results):
    # Create a list to hold all rows of the summary table
    summary_data = []
    
    for block_id, block_data in final_results.items():
        all_move_sequences = block_data['all_move_sequences']
        all_erms = block_data['all_erms']
        
        for bay_id, move_sequences in all_move_sequences.items():
            erms = all_erms[bay_id]
            
            for move_sequence_id, move_sequence in enumerate(move_sequences.values(), start=1):
                work_order = move_sequence_id
                erm = erms[move_sequence_id]
                
                # Append a new row to the summary_data list
                summary_data.append([work_order, block_id, bay_id, move_sequence, erm])
    
    # Create a DataFrame from the summary_data list
    summary_df = pd.DataFrame(summary_data, columns=[
        'work_orders', 
        'block', 
        'bay', 
        'move_sequence', 
        'calculated_erms'
    ])

    return summary_df

import pandas as pd

def create_general_run_summary(final_results):
    summary_data = []
    for block, block_data in final_results.items():
        for bay, bay_data in block_data['all_preprocessing_moves'].items():
            total_preprocessing_moves = len(bay_data)
            erms_before = block_data['all_erms'][bay][0]
            erms_after = block_data['all_erms'][bay][len(block_data['all_erms'][bay]) - 1]
            summary_data.append([block, bay, total_preprocessing_moves, erms_before, erms_after])

    df = pd.DataFrame(summary_data, columns=[
        'block', 
        'bay', 
        'number_of_preprocessing_moves', 
        'calculated_erms_before_preprocessing', 
        'calculated_erms_after_preprocessing'
    ])

    return df




if __name__ == "__main__":
    # Load your data
    data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
    data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')  
    
    # Process appointment data
    df_containers = process_appointment_data(data_containers)
    
    input_bays=create_input_data(df_containers, data_blocks)

    # Initialize final results dictionary
    final_results = {}

    # Process each block
    for block_id in df_containers['block_id'].unique():
        block_df = df_containers[df_containers['block_id'] == block_id]
        
        stacks = data_blocks.loc[data_blocks['block_id'] == block_id, 'stacks_per_bay'].values[0]
        tiers = data_blocks.loc[data_blocks['block_id'] == block_id, 'tiers_per_bay'].values[0]

        # Process data for specific block
        bays = process_data_for_block(block_df, stacks, tiers)

        # Parameters for local search heuristic, you can customize these values
        α, λ1, λ2, H = 0.75, 1, 1, 4
        
        # Solve the block
        block_results = solve_block(bays, α, λ1, λ2, H)

        # Store the results
        final_results[block_id] = block_results
    
    container_summary_data = get_container_summary_data(df_containers, final_results)
    final_bays=create_final_output_bays(final_results)
    work_orders=get_moves_and_erms_summary(final_results)
    general_run_summary = create_general_run_summary(final_results)



## Optimizaion of crane route movement and move_sequences selection

def create_all_S(final_results):
    all_S = {}  

    for block_id, results_data in final_results.items():
        erms = results_data['all_erms']
        all_S[block_id] = {}
        
        for bay_id, bay_erms in erms.items():
            S = {(bay_id, lambda_k): erms_value for lambda_k, erms_value in bay_erms.items()}
            all_S[block_id][bay_id] = S
            
    return all_S


initial_bay_df = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='crane_location')
time_available_df = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='optimization_parameters')

# Convert dataframes to dictionaries for easier access
initial_bay_dict = initial_bay_df.set_index('block_id')['crane_location'].to_dict()
time_available_dict = time_available_df.set_index('block_id')['time_available_minutes'].to_dict()

from ortools.linear_solver import pywraplp

all_S = create_all_S(final_results)

# Now iterate over each block and solve the MIP problem using the parameters from Excel
for block_id in initial_bay_dict.keys():
    initial_bay = initial_bay_dict[block_id]
    T = time_available_dict[block_id] * 60  # Convert to seconds if needed
    S = all_S[block_id]  # Get the S data for the current block

    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Correcting the extraction of bays and lambda_k values
    bays = list(S.keys())
    lambdas = {bay: list(range(len(S[bay]))) for bay in bays} 

    # Then proceed with the rest of your existing MIP setup and solving code
    Y = {(k, lambda_k): solver.BoolVar(f'Y_{k}_{lambda_k}') for k in bays for lambda_k in lambdas[k]}
    X = {(i, j): solver.BoolVar(f'X_{i}_{j}') for i in bays for j in bays if i != j}
    
    # Corrected Objective Function
    objective = solver.Objective()
    for bay in S.keys():
        for lambda_k, erms_value in S[bay].items():  # Corrected this line
            objective.SetCoefficient(Y[(bay, lambda_k)], erms_value)
    objective.SetMinimization()

   
    tau = 30  # Fixed preprocessing time in seconds for each move
    tau_dict = {}
    for bay in bays:
        cumulative_tau = 0 
        for lambda_k in lambdas[bay]:
            num_moves = len(move_sequences[bay][f'move_sequence_{lambda_k}']) if lambda_k > 0 else 0
            cumulative_tau += tau * num_moves
            tau_dict[(bay, lambda_k)] = cumulative_tau

   

    # Time Constraint
    lhs = sum(t[(k, l)] * X[(k, l)] for k in bays for l in bays if k != l)
    lhs += sum(tau_dict[(k, lambda_k)] * Y[(k, lambda_k)] for k in bays for lambda_k in lambdas[k])
    solver.Add(lhs <= T)

    # Solving the MIP
    status = solver.Solve()

    # Outputting the results
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Optimal solution found for block {block_id} with objective value {solver.Objective().Value()}")
        for k, lambda_k in Y:
            if Y[(k, lambda_k)].solution_value() > 0.5:
                print(f'Perform {lambda_k} pre-processing moves in Bay {k}')
        for i, j in X:
            if X[(i, j)].solution_value() > 0.5:
                print(f'Move crane from Bay {i} to Bay {j}')
    else:
        print(f"No optimal solution found for block {block_id}")

    print("\n" + "="*50 + "\n")
