import sys
sys.path.append("C:/Users/Ashrafur.Rahman/OneDrive - Blume Global/Data and Codes/Yard Crane Scheduling/core-stack-optimizer/")

import pandas as pd
import src.stackoptimizer.test_data_generator import generate_bays_data
from src.stackoptimizer.preprocessing_algorithms import local_search_heuristic_v2  # Import the local search heuristic function
from src.stackoptimizer.preprocessing_plotting import plot_all_bays_side_by_side
from src.stackoptimizer.preprocessing_utils import *


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


if __name__ == "__main__":
  
    #data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
    #data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')  
    data_containers=generate_bays_data(num_bays=20, max_containers=14, min_containers=10, stacks=5, tiers=4, 
                       appointment_start_date="2023-10-07", appointment_end_date="2023-10-10", 
                       appointment_start_time="08:00", appointment_end_time="17:00", scheduled_proportion=1,
                       )


    block_config = {'R': {'max_stacks': 5, 'max_tiers': 4}}

    df_containers = process_appointment_data(data_containers)
    
    input_bays=create_input_data(df_containers, data_blocks)

    final_results = {}


    # Process each block
    for container_location_block in df_containers['container_location_block'].unique():
        block_df = df_containers[df_containers['container_location_block'] == container_location_block]
        
        stacks = data_blocks.loc[data_blocks['container_location_block'] == container_location_block, 'stacks_per_bay'].values[0]
        tiers = data_blocks.loc[data_blocks['container_location_block'] == container_location_block, 'tiers_per_bay'].values[0]

        # Process data for specific block
        bays = process_data_for_block(block_df, stacks, tiers)

        # Parameters for local search heuristic, you can customize these values
        α, λ1, λ2, H = 0.75, 1, 1, tiers
        
        # Solve the block
        block_results = solve_block(bays, α, λ1, λ2, H)

        # Store the results
        final_results[container_location_block] = block_results
    
    container_summary_data = get_container_summary_data(df_containers, final_results)
    move_summary=get_moves_summary(final_results)

    final_bays=create_final_output_bays(final_results)
    work_orders=get_moves_and_erms_summary(final_results)

    general_run_summary = create_general_run_summary(final_results)
    work_orders_v2 = create_general_run_summary_v2(final_results)



    plot_all_bays_side_by_side(input_bays, final_bays, block_config, 'bays_comparison.pdf')
    #plot_bays_with_plotly(input_bays, final_bays)