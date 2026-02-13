import pandas as pd

df_containers = pd.read_csv("C:/Users/Ashrafur.Rahman/Downloads/1containers_location_appointment_df.csv",parse_dates=['appointment_start_time'])
df_containers['appointment_time'] = df_containers['appointment_start_time'].astype('category').cat.codes + 1
#df = pd.DataFrame(df, columns=["container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_time"])
#date_needed = '2023-05-09'
#df_containers = df_containers[df_containers['appointment_start_time'].dt.date == pd.Timestamp(date_needed).date()]
'''
stacks=5
bays = {}
for _, row in df_containers.iterrows():
    bay = row['container_location_bay']
    stack = f'stack{row["container_location_stack"]}'
    
    if bay not in bays:
        bays[bay] = {f'stack{i }': [] for i in range(stacks)}

    appointment_time = row['appointment_time']
    bays[bay][stack].append((row['container_id'], appointment_time))

for bay in bays.values():
    for stack_containers in bay.values():
        stack_containers.sort(key=lambda x: x[1])

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

df_containers = pd.read_csv("C:/Users/Ashrafur.Rahman/Downloads/1containers_location_appointment_df.csv",parse_dates=['appointment_start_time'])


df_containers['appointment_time'] = df_containers['appointment_start_time'].astype('category').cat.codes + 1
#df = pd.DataFrame(df, columns=["container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_time"])
date_needed = '2023-05-09'
df_containers = df_containers[df_containers['appointment_start_time'].dt.date == pd.Timestamp(date_needed).date()]

  # Process each block
for container_location_block in df_containers['container_location_block'].unique():
    block_df = df_containers[df_containers['container_location_block'] == container_location_block]
    
    max_stacks = 5
    max_tiers = 4

    # Process data for specific block
    bays = process_data_for_block(block_df, max_stacks, max_tiers)


