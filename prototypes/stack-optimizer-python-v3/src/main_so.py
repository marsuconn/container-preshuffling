
import sys
sys.path.append('')
from src.stackoptimizer.container_preprocessing_multiple_blocks import *


def main_so(containers_location_appointment_df,block_config_df,plot_filepath ):
    
    if not isinstance(containers_location_appointment_df, pd.DataFrame) or not isinstance(block_config_df, pd.DataFrame):
        raise TypeError("Both containers_location_appointment_df and block_config_df should be pandas DataFrames")
    
    if not isinstance(plot_filepath, str):
        raise TypeError("plot_filepath should be a string indicating the path to save the plot")
    
    # Ensure the DataFrame is not empty
    if containers_location_appointment_df.empty or block_config_df.empty:
        raise ValueError("Input DataFrames should not be empty")
    
    # Processing appointment data with error handling
    try:
        df_containers = process_appointment_data(containers_location_appointment_df)
    except Exception as e:
        raise RuntimeError(f"Error processing appointment data: {str(e)}")
    
    # Creating block configuration with error handling
    try:
        block_config = create_block_config(block_config_df)
    except Exception as e:
        raise RuntimeError(f"Error creating block configuration: {str(e)}")
    
    
    # Initialize final results dictionary
    final_results = {}

    # Process each block
    for container_location_block in df_containers['container_location_block'].unique():
        block_df = df_containers[df_containers['container_location_block'] == container_location_block]
        
        max_stacks = block_config[container_location_block]['max_stacks']
        max_tiers = block_config[container_location_block]['max_tiers']

        # Process data for specific block
        bays = process_data_for_block(block_df, max_stacks, max_tiers)
        
        # Parameters for local search heuristic

        α, λ1, λ2, H = 0.75, 1, 1, max_tiers
        
        # Solve the block
        block_results = solve_block(bays, α, λ1, λ2, H)

        # Store the results
        final_results[container_location_block] = block_results
    
    container_summary_data = get_container_summary_data(df_containers, final_results)
    moves_summary=get_moves_summary(final_results)

    final_bays=create_final_output_bays(final_results)
    work_orders=get_moves_and_erms_summary(final_results)

    general_run_summary = create_general_run_summary(final_results)
    work_orders_v2 = create_general_run_summary_v2(final_results)
    
    plots=plot_all_bays_side_by_side(input_bays, final_bays, block_config, plot_filepath)


    return container_summary_data,moves_summary, work_orders,work_orders_v2, general_run_summary,plots

