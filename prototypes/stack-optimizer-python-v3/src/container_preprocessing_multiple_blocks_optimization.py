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
    data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks_v2.xlsx', sheet_name='containers')
    data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks_v2.xlsx', sheet_name='blocks')  
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


import random
import pandas as pd
from datetime import datetime, timedelta, time
import string

print("hello")

def generate_bays_data(num_bays=20, num_blocks=1, max_containers=14, min_containers=10, stacks=5, tiers=4, 
                       appointment_start_date="2023-10-07", appointment_end_date="2023-10-10", 
                       appointment_start_time="08:00", appointment_end_time="17:00", scheduled_proportion=1):
    # Validate the scheduled_proportion input
    if scheduled_proportion < 0 or scheduled_proportion > 1:
        raise ValueError("scheduled_proportion must be between 0 and 1 inclusive.")
    
    # Parse the dates and times
    appointment_start_date = datetime.strptime(appointment_start_date, "%Y-%m-%d")
    appointment_end_date = datetime.strptime(appointment_end_date, "%Y-%m-%d")
    appointment_start_time = datetime.strptime(appointment_start_time, "%H:%M").time()
    appointment_end_time = datetime.strptime(appointment_end_time, "%H:%M").time()

    total_days = (appointment_end_date - appointment_start_date).days + 1
    total_hours = (appointment_end_time.hour - appointment_start_time.hour)

    # Initialize list to store the bay data
    data = []

    # Generate data for num_bays bays and num_blocks blocks
    for block in range(1, num_blocks + 1):
        for bay in range(1, num_bays + 1):
            # Determine the number of containers in the bay
            num_containers = random.randint(min_containers, max_containers)

            # Generate data for each container
            for container in range(1, num_containers + 1):
                # Create alphanumeric container ID
                container_id = ''.join(random.choices(string.ascii_uppercase, k=4)) + ''.join(random.choices(string.digits, k=6))
                container_location_block = block  # New column for block
                container_location_bay = bay

                # Randomly select a stack ensuring that the selected stack is not full
                container_location_stack = random.randint(1, stacks)
                container_location_tier = random.randint(0, tiers - 1)

                # Assign an appointment time for the container based on the scheduled_proportion
                if random.random() < scheduled_proportion:
                    random_date = appointment_start_date + timedelta(days=random.randint(0, total_days - 1))
                    random_hour = random.randint(appointment_start_time.hour, appointment_end_time.hour - 1)
                    appointment_start_time_final = datetime.combine(random_date, time(random_hour, 0))
                    appointment_end_time_final = appointment_start_time_final + timedelta(hours=1)
                else:
                    appointment_start_time_final = "not scheduled"
                    appointment_end_time_final = "not scheduled"

                # Add the container data to the list
                data.append([
                    container_id,
                    container_location_block,
                    container_location_bay,
                    container_location_stack,
                    container_location_tier,
                    appointment_start_time_final,
                    appointment_end_time_final
                ])

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["container_id", "container_location_block", "container_location_bay",
                                     "container_location_stack", "container_location_tier", 
                                     "appointment_start_time", "appointment_end_time"])

    # Convert datetime objects to string for not scheduled containers
    df[['appointment_start_time', 'appointment_end_time']] = df[['appointment_start_time', 'appointment_end_time']].astype(str)

    # Return the DataFrame for further processing if needed
    return df
