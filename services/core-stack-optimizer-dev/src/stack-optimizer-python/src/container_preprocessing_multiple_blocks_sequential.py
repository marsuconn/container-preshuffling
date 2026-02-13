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


if __name__ == "__main__":
    data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
    columns_needed = ["block_id", "container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_start_time", "appointment_end_time"]
    df_containers = data_containers[columns_needed]
    df_containers = process_appointment_data(df_containers)

    data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')

    results = main(df_containers, data_blocks)