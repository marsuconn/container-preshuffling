
import numpy as np
import pandas as pd
import pandas as pd
from datetime import datetime

'''
def process_appointment_data(df):
    #df = df.sort_values(by=['container_location_block', 'appointment_start_time'])
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
    
    if not all(column in block_data.columns for column in ['container_location_block', 'stacks_per_bay', 'tiers_per_bay']):
        raise ValueError("The DataFrame must contain 'container_location_block', 'stacks_per_bay', and 'tiers_per_bay' columns.")
    
    block_config = {}
    for _, row in block_data.iterrows():
        container_location_block = row['container_location_block'] # need to comply with database
        max_stacks = row['stacks_per_bay']
        max_tiers = row['tiers_per_bay']
        block_config[container_location_block] = {'max_stacks': max_stacks, 'max_tiers': max_tiers}

    return block_config

'''

def process_appointment_data(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The input should be a pandas DataFrame")
    
    if 'appointment_start_time' not in df.columns:
        raise ValueError("The DataFrame must contain the 'appointment_start_time' column")
    
    if df['appointment_start_time'].isnull().any():
        raise ValueError("There are NaN values in the 'appointment_start_time' column")
    
    

    df['appointment_time'] = df['appointment_start_time'].astype('category').cat.codes + 1
    
    if df['appointment_time'].isnull().any():
        raise ValueError("Conversion error: There are NaN values in the 'appointment_time' column after conversion")

    return df




def process_data_for_block(block_df, stacks, tiers):
    if not isinstance(block_df, pd.DataFrame):
        raise TypeError("block_df should be a pandas DataFrame")
    
    required_columns = ['container_location_bay', 'container_location_stack', 'appointment_time', 'container_id']
    if not all(col in block_df.columns for col in required_columns):
        raise ValueError(f"The DataFrame is missing one or more of the required columns: {required_columns}")
    
    #if not isinstance(stacks, int) or not isinstance(tiers, int):
    #    raise TypeError("Stacks and tiers should be integers")
    
    #if stacks <= 0 or tiers <= 0:
    #    raise ValueError("Stacks and tiers should be positive integers")
    
    bays = {}
    for _, row in block_df.iterrows():
        bay = row['container_location_bay']
        stack_number = row['container_location_stack']
        
        #if not isinstance(bay, int) or not isinstance(stack_number, int):
        #    raise TypeError("Bay and stack number should be integers")
        
        #if stack_number < 0 or stack_number >= stacks:
        #    raise ValueError(f"Stack number should be between 0 and {stacks - 1}")
        
        stack = f'stack{stack_number + 1}'
        
        if bay not in bays:
            bays[bay] = {f'stack{i + 1}': [] for i in range(stacks)}

        appointment_time = row['appointment_time']
        if not isinstance(appointment_time, int) or appointment_time <= 0:
            raise ValueError("Appointment time should be a positive integer")
        
        bays[bay][stack].append((row['container_id'], appointment_time))

    for bay in bays.values():
        for stack_containers in bay.values():
            stack_containers.sort(key=lambda x: x[1])
    
    return bays

def create_block_config(block_data: pd.DataFrame) -> dict:
    if not isinstance(block_data, pd.DataFrame):
        raise TypeError("Input block_data should be a pandas DataFrame")
    
    required_columns = ['container_location_block', 'stacks_per_bay', 'tiers_per_bay']
    if not all(column in block_data.columns for column in required_columns):
        raise ValueError(f"The DataFrame must contain {', '.join(required_columns)} columns.")
    
    if block_data[required_columns].isnull().values.any():
        raise ValueError("The DataFrame contains NaN values in one or more of the required columns.")
    
    if block_data.duplicated(['container_location_block']).any():
        raise ValueError("There are duplicated container_location_block values.")
    
    if not (block_data['stacks_per_bay'].dtype == np.int64 and block_data['tiers_per_bay'].dtype == np.int64):
        raise TypeError("'stacks_per_bay' and 'tiers_per_bay' should be of int type.")
    
    if not block_data['stacks_per_bay'].apply(lambda x: x > 0).all() or not block_data['tiers_per_bay'].apply(lambda x: x > 0).all():
        raise ValueError("'stacks_per_bay' and 'tiers_per_bay' should be greater than 0.")
    
    block_config = {}
    for _, row in block_data.iterrows():
        container_location_block = row['container_location_block']
        max_stacks = row['stacks_per_bay']
        max_tiers = row['tiers_per_bay']
        block_config[container_location_block] = {'max_stacks': max_stacks, 'max_tiers': max_tiers}

    return block_config




def get_container_summary_data(df_containers, results):
    initial_positions = df_containers[[
        'container_id', 
        'container_location_block', # need to comply with Suraj's data column
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
    
    for container_location_block, block_data in results.items():
        for bay_id, bay in block_data['all_final_bays'].items():
            for stack_id, stack in bay.items():
                numeric_stack_id = int(stack_id.lstrip('stack'))  # Convert stack id to numeric
                for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                    container_id, _ = container_info  
                    final_positions_data.append([container_id, container_location_block, bay_id, numeric_stack_id, tier])
        
        #intermediate_positions_data[container_location_block] = block_data['all_intermidate_bays_configs']

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


def create_input_data(df_containers, data_blocks):
    input_data = {}
    
    for container_location_block in df_containers['container_location_block'].unique():
        block_df = df_containers[df_containers['container_location_block'] == container_location_block]
        
        stacks = int(data_blocks.loc[data_blocks['container_location_block'] == container_location_block, 'stacks_per_bay'].values[0])
        tiers = int(data_blocks.loc[data_blocks['container_location_block'] == container_location_block, 'tiers_per_bay'].values[0])

        bays = process_data_for_block(block_df, stacks, tiers)
        input_data[container_location_block] = bays

    return input_data


def create_final_output_bays(final_results):
    final_output_bays = {}
    
    for container_location_block, block_results in final_results.items():
        final_output_bays[container_location_block] = block_results['all_final_bays']
        
    return final_output_bays



def get_moves_and_erms_summary(final_results):
    summary_data = []
    
    for container_location_block, block_data in final_results.items():
        all_move_sequences = block_data['all_move_sequences']
        all_erms = block_data['all_erms']
        
        for bay_id, move_sequences in all_move_sequences.items():
            erms = all_erms[bay_id]
            
            for move_sequence_id, move_sequence in enumerate(move_sequences.values(), start=1):
                work_order = move_sequence_id
                erm = erms[move_sequence_id]
                
                summary_data.append([work_order, container_location_block, bay_id, move_sequence, erm])
    
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





def get_moves_summary(final_results):
    summary_data = []
    
    for container_location_block, block_data in final_results.items():
        all_move_sequences = block_data['all_move_sequences']
        
        for bay_id, move_sequences in all_move_sequences.items():
            for move_sequence_name, moves in move_sequences.items():
                for move_sequence_no, (from_stack, to_stack, container_id) in enumerate(moves, start=1):
                    work_order = move_sequence_no  # Adjust as needed to make work_order unique per bay
                    
                    summary_data.append([
                        work_order, 
                        container_location_block, 
                        bay_id, 
                        move_sequence_no, 
                        from_stack, 
                        to_stack, 
                        container_id
                    ])
    
    summary_df = pd.DataFrame(summary_data, columns=[
        'work_orders', 
        'block', 
        'bay', 
        'move_sequence_no',
        'current_stack', 
        'new_stack', 
        'container_id'
    ])

    return summary_df



