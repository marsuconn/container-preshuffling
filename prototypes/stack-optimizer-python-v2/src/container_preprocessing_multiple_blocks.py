
import pandas as pd
from preprocessing_algorithms import local_search_heuristic_v2  # Import the local search heuristic function
from preprocessing_plotting import plot_all_bays_side_by_side, plot_bays_with_plotly
from preprocessing_utils import *


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
  
    data_containers = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='containers')
    data_blocks = pd.read_excel('./preprocessing/input/input_samples_datetime_mutliple_blocks.xlsx', sheet_name='blocks')  
    block_config = create_block_config(data_blocks)

    df_containers = process_appointment_data(data_containers)
    
    input_bays=create_input_data(df_containers, data_blocks)

    # Initialize final results dictionary
    final_results = {}

    # Process each block
    for block_id in df_containers['block_id'].unique():
        block_df = df_containers[df_containers['block_id'] == block_id]
        
        max_stacks = block_config[block_id]['max_stacks']
        max_tiers = block_config[block_id]['max_tiers']

        # Process data for specific block
        bays = process_data_for_block(block_df, max_stacks, max_tiers)

        # Parameters for local search heuristic
        α, λ1, λ2, H = 0.75, 1, 1, max_tiers
        
        #solve for individual block
        block_results = solve_block(bays, α, λ1, λ2, H)

        # Store the results
        final_results[block_id] = block_results
    
    final_bays=create_final_output_bays(final_results)


    container_summary_data = get_container_summary_data(df_containers, final_results)
    work_orders=get_moves_and_erms_summary(final_results)

    general_run_summary = create_general_run_summary(final_results)
    work_orders_v2 = create_general_run_summary_v2(final_results)



    plot_all_bays_side_by_side(input_bays, final_bays, block_config, 'bays_comparison.pdf')
    #plot_bays_with_plotly(input_bays, final_bays)