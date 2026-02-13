from preprocessing_utils import*
from preprocessing_algorithms import *
from preprocessing_plotting import *
import pandas as pd
import json
import os
import multiprocessing

# Using os
num_cores = os.cpu_count()
print(f"Number of cores using os: {num_cores}")

# Using multiprocessing
num_cores_multiprocessing = multiprocessing.cpu_count()
print(f"Number of cores using multiprocessing: {num_cores_multiprocessing}")

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


def process_and_solve_block(args):
    block_id, specific_block_data, stacks, tiers = args
    bays = process_data_for_block(specific_block_data, stacks, tiers)

    α, λ1, λ2, H = 0.75, 1, 1, 4
    all_moves, all_relocation_moves, all_erms, all_bays = solve_block(bays, α, λ1, λ2, H)

    return block_id, {
        'all_moves': all_moves,
        'all_relocation_moves': all_relocation_moves,
        'all_erms': all_erms,
        'all_bays': all_bays
    }

def main(df_containers, data_blocks):
    args_list = []
    for block_id in df_containers['block_id'].unique():
        specific_block_data = df_containers[df_containers['block_id'] == block_id]
        stacks = data_blocks[data_blocks['block_id'] == block_id]['stacks_per_bay'].values[0]
        tiers = data_blocks[data_blocks['block_id'] == block_id]['tiers_per_bay'].values[0]
        
        args_list.append((block_id, specific_block_data, stacks, tiers))
    
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    results_list = pool.map(process_and_solve_block, args_list)
    
    # Convert the list of results into a dictionary
    results = {block_id: data for block_id, data in results_list}

    return results

if __name__ == "__main__":
    data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
    columns_needed = ["block_id", "container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_start_time", "appointment_end_time"]
    df_containers = data_containers[columns_needed]
    df_containers = process_appointment_data(df_containers)

    data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')

    results = main(df_containers, data_blocks)

