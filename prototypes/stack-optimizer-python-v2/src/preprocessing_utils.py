
import numpy as np
import pandas as pd
import pandas as pd
from datetime import datetime


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


def create_block_config(block_data: pd.DataFrame) -> dict:
    
    if not all(column in block_data.columns for column in ['block_id', 'stacks_per_bay', 'tiers_per_bay']):
        raise ValueError("The DataFrame must contain 'block_id', 'stacks_per_bay', and 'tiers_per_bay' columns.")
    
    block_config = {}
    for _, row in block_data.iterrows():
        block_id = row['block_id']
        max_stacks = row['stacks_per_bay']
        max_tiers = row['tiers_per_bay']
        block_config[block_id] = {'max_stacks': max_stacks, 'max_tiers': max_tiers}

    return block_config

def get_container_summary_data(df_containers, results):
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

    final_positions_data = []
    #intermediate_positions_data = {}  # Store intermediate bay configurations
    
    for block_id, block_data in results.items():
        for bay_id, bay in block_data['all_final_bays'].items():
            for stack_id, stack in bay.items():
                numeric_stack_id = int(stack_id.lstrip('stack'))  # Convert stack id to numeric
                for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                    container_id, _ = container_info  
                    final_positions_data.append([container_id, block_id, bay_id, numeric_stack_id, tier])
        
        #intermediate_positions_data[block_id] = block_data['all_intermidate_bays_configs']

    final_positions = pd.DataFrame(final_positions_data, columns=[
        'container_id', 
        'new_block', 
        'new_bay', 
        'new_stack', 
        'new_tier'
    ])

    container_summary_data = pd.merge(initial_positions, final_positions, on='container_id', how='left')

    # Filling NaN values for containers that didn't move
    container_summary_data['new_block'].fillna(container_summary_data['current_block'], inplace=True)
    container_summary_data['new_bay'].fillna(container_summary_data['current_bay'], inplace=True)
    container_summary_data['new_stack'].fillna(container_summary_data['current_stack'], inplace=True)
    container_summary_data['new_tier'].fillna(container_summary_data['current_tier'], inplace=True)

    return container_summary_data#, intermediate_positions_data


def create_input_data(df_containers, block_config):
    input_data = {}
    
    for block_id in df_containers['block_id'].unique():
        block_df = df_containers[df_containers['block_id'] == block_id]
        
        max_stacks = block_config[block_id]['max_stacks']
        max_tiers = block_config[block_id]['max_tiers']
        bays = process_data_for_block(block_df, max_stacks, max_tiers)
        input_data[block_id] = bays

    return input_data


def create_final_output_bays(final_results):
    final_output_bays = {}
    
    for block_id, block_results in final_results.items():
        final_output_bays[block_id] = block_results['all_final_bays']
        
    return final_output_bays



def get_moves_and_erms_summary(final_results):
    summary_data = []
    
    for block_id, block_data in final_results.items():
        all_move_sequences = block_data['all_move_sequences']
        all_erms = block_data['all_erms']
        
        for bay_id, move_sequences in all_move_sequences.items():
            erms = all_erms[bay_id]
            
            for move_sequence_id, move_sequence in enumerate(move_sequences.values(), start=1):
                work_order = move_sequence_id
                erm = erms[move_sequence_id]
                
                summary_data.append([work_order, block_id, bay_id, move_sequence, erm])
    
    summary_df = pd.DataFrame(summary_data, columns=[
        'work_orders', 
        'block', 
        'bay', 
        'move_sequence', 
        'calculated_erms'
    ])

    return summary_df

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

def create_general_run_summary_v2(final_results):
    summary_data = []
    for block, block_data in final_results.items():
        for bay, bay_data in block_data['all_preprocessing_moves'].items():
            total_preprocessing_moves = len(bay_data)
            erms_before = block_data['all_erms'][bay][0]
            erms_after = block_data['all_erms'][bay][len(block_data['all_erms'][bay]) - 1]
            
            # Concatenate all preprocessing moves into a string
            all_moves = ', '.join([str(move) for move in bay_data]) 

            # Add two new columns at the beginning
            summary_data.append([
                f"Work Order for Block {block}, Bay {bay}",  # New column
                all_moves,  # New column
                block, 
                bay, 
                total_preprocessing_moves, 
                erms_before, 
                erms_after
            ])

    df = pd.DataFrame(summary_data, columns=[
        'work_orders',  # New column header
        'all_preprocessing_moves',  # New column header
        'block', 
        'bay', 
        'number_of_preprocessing_moves', 
        'calculated_erms_before_preprocessing', 
        'calculated_erms_after_preprocessing'
    ])

    return df

'''

def export_to_excel(all_bays, file_name='bays.xlsx'):
    data = []
    for bay_id, bay in all_bays.items():
        for stack_id, stack in bay.items():
            for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                container_id, time_window = container_info
                data.append([bay_id, stack_id, tier, container_id, time_window])
    df = pd.DataFrame(data, columns=['Bay', 'Stack', 'Tier', 'Container', 'Time Window'])
    df.to_excel(file_name, index=False)
    print(f'Excel file saved as {file_name}')


def export_moves_to_excel(all_moves, file_name='moves.xlsx'):
    data = []
    for bay_id, moves in all_moves.items():
        for move in moves:
            source_stack, destination_stack = move
            data.append([bay_id, source_stack, destination_stack])
    df = pd.DataFrame(data, columns=['Bay', 'Source Stack', 'Destination Stack'])
    df.to_excel(file_name, index=False)
    print(f'Excel file saved as {file_name}')

'''


