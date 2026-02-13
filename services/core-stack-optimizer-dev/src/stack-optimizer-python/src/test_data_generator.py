import random
import pandas as pd
from collections import OrderedDict

def generate_bays_data(num_bays=20, max_containers=14, min_containers=10, stacks=5, tiers=4, time_windows=8, file_name="bays_data.xlsx"):
    # Initialize list to store the bay data
    data = []

    # Generate data for num_bays bays
    for bay in range(1, num_bays+1):
        # Determine the number of containers in the bay
        num_containers = random.randint(min_containers, max_containers)
        
        # Create a dictionary to store used tiers for each stack
        used_tiers = {f'stack{i+1}': [] for i in range(stacks)}
        
        # Generate data for each container
        for container in range(1, num_containers + 1):
            container_id = f"c{container}"
            container_location_bay = bay
            
            # Randomly select a stack ensuring that the selected stack is not full
            while True:
                container_location_stack = f"stack{random.randint(1, stacks)}"
                if len(used_tiers[container_location_stack]) < tiers:
                    break
            
            # Add the tier to the used tiers in the selected stack
            container_location_tier = len(used_tiers[container_location_stack])
            used_tiers[container_location_stack].append(container_location_tier)
            
            # Randomly assign an appointment time for the container, with 90% chance of getting an appointment within the defined time window
            appointment_time = random.randint(1, time_windows + 1) if random.random() < 0.9 else 9

            # Add the container data to the list
            data.append([
                container_id,
                container_location_bay,
                container_location_stack,
                container_location_tier,
                appointment_time
            ])

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["container_id", "container_location_bay", "container_location_stack", "container_location_tier", "appointment_time"])

    # Write the DataFrame to an Excel file
    df.to_excel(file_name, index=False, engine='openpyxl')

    # Convert the DataFrame to a bays dictionary
    bays = {}
    for idx, row in df.iterrows():
        bay = row['container_location_bay']
        stack = row['container_location_stack']
        if bay not in bays:
            bays[bay] = {f'stack{i+1}': [] for i in range(stacks)}  # initialize all stacks
        bays[bay][stack].append((row['container_id'], row['appointment_time'], row['container_location_tier']))
    
    # Sort containers in each stack based on tier
    for bay in bays.values():
        for stack_containers in bay.values():
            stack_containers.sort(key=lambda x: x[2])  # sort by tier
            for i in range(len(stack_containers)):  # remove tier from container data
                stack_containers[i] = stack_containers[i][:2]  # keep only container_id and appointment_time

    # Return the bays dictionary
    return bays
test_bays=generate_bays_data(num_bays=20, max_containers=14, min_containers=10, stacks=5, tiers=4, time_windows=8, file_name="bays_data_test.xlsx")
