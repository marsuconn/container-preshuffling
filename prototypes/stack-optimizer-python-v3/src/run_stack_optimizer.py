import sys
from preprocessing_utils import*
from preprocessing_algorithms import *
from preprocessing_plotting import *
import pandas as pd
import os
import copy


def run_stack_optimizer(data,config):
    columns_needed=["container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_start_time", "appointment_end_time"]
    df = data[columns_needed]
    df=process_appointment_data(df)

    stacks = config['stacks']
    tiers = config['tiers']

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
        all_relocation_moves={}
        all_erms={}

        # Loop over each bay in the dictionary
        for bay_num, bay in input_bays.items():
            # print(f"SOLVE {bay_num} ***")
            moves, relocation_moves,erms, new_bay = local_search_heuristic(bay, α, λ1, λ2, H)
            #expected_moves = calculate_expected_relocation_moves(new_bay)

            # Store the moves and the new bay configuration in the dictionaries
            all_moves[bay_num] = moves
            all_relocation_moves[bay_num]=relocation_moves
            all_bays[bay_num] = new_bay
            all_erms[bay_num]=erms
            

        return all_moves, all_relocation_moves,all_erms,all_bays

    all_moves, all_relocation_moves,all_erms, all_bays = solve_all_bays(input_bays, α, λ1, λ2, H)

    optimized_bays = get_output_bays(all_bays)
    optimized_moves = get_output_moves(all_moves)

    # plot_bays(input_bays,stacks,tiers, pdf_filename='./preprocessing/output/input_bays_plot.pdf')
    # plot_bays(all_bays,stacks,tiers, pdf_filename='./preprocessing/output/output_bays_plot.pdf')

    # plot_all_bays_with_moves(input_bays,all_moves,pdf_filename='./preprocessing/output/pre_processing_moves_plot.pdf',max_stacks=stacks, max_tiers=tiers)
    # plot_bays_3d(all_bays, max_stacks=stacks, max_tiers=tiers)

    return {"optimized_bays":optimized_bays, "optimized_moves":optimized_moves}


if __name__ == "__main__":
    #path = "C:/Users/sheetalanns.philip/OneDrive - Blume Global/Work/Projects/Appointment Scheduling/GitHub/core-stack-optimizer/src/stackoptimizer/"

    data = pd.read_excel('./preprocessing/input/input_samples_datetime.xlsx')
    config={'stacks':5,'tiers':1}
    output = run_stack_optimizer(data,config)
    print(output['optimized_bays'].head())
    print(output['optimized_moves'].head())