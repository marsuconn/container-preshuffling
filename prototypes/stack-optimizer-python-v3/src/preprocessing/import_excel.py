import pandas as pd

# Load the Excel file
stacks = 5
tiers = 4
data = pd.read_excel('../input/input_samples.xlsx')

df = pd.DataFrame(data, columns=["container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_time"])

# Process the dataframe to create the bays dictionary
# Convert the DataFrame to a bays dictionary
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

    # Append tuple (container_id, tier)
    bays[bay][stack].append((row['container_id'], row['container_location_tier']))

# Sort containers in each stack based on tier
for bay in bays.values():
    for stack_containers in bay.values():
        stack_containers.sort(key=lambda x: x[1])  # sort by tier

print(bays)
