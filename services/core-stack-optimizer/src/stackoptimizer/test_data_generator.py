import random
import pandas as pd
from datetime import datetime, timedelta, time
import string

def generate_bays_data(num_blocks=1, num_bays=20, max_containers=14, min_containers=10, stacks=5, tiers=4, 
                       appointment_start_date="2023-10-07", appointment_end_date="2023-10-10", 
                       appointment_start_time="08:00", appointment_end_time="17:00", scheduled_proportion=1):
    # Validate the scheduled_proportion input
    if scheduled_proportion < 0 or scheduled_proportion > 1:
        raise ValueError("scheduled_proportion must be between 0 and 1 inclusive.")
    
    # Parse the dates and times
    appointment_start_date = datetime.strptime(appointment_start_date, "%Y-%m-%d")
    appointment_end_date = datetime.strptime(appointment_end_date, "%Y-%m-%d")
    appointment_start_time = datetime.strptime(appointment_start_time, "%H:%M").time()
    appointment_end_time = datetime.strptime(appointment_end_time, "%H:%M").time()

    total_days = (appointment_end_date - appointment_start_date).days + 1

    # Initialize list to store the bay data
    data = []

    # Generate data for num_bays bays and num_blocks blocks
    for block in range(1, num_blocks + 1):
        for bay in range(1, num_bays + 1):
            # Determine the number of containers in the bay
            num_containers = random.randint(min_containers, max_containers)

            # Generate data for each container
            for _ in range(1, num_containers + 1):  # Removed the unused 'container' variable
                # Create alphanumeric container ID
                container_id = ''.join(random.choices(string.ascii_uppercase, k=4)) + ''.join(random.choices(string.digits, k=6))
                container_location_block = block  # New column for block
                container_location_bay = bay

                # Randomly select a stack ensuring that the selected stack is not full
                container_location_stack = random.randint(1, stacks)
                container_location_tier = random.randint(0, tiers - 1)

                # Assign an appointment time for the container based on the scheduled_proportion
                if random.random() < scheduled_proportion:
                    random_date = appointment_start_date + timedelta(days=random.randint(0, total_days - 1))
                    random_hour = random.randint(appointment_start_time.hour, appointment_end_time.hour - 1)
                    appointment_start_time_final = datetime.combine(random_date, time(random_hour, 0))
                    appointment_end_time_final = appointment_start_time_final + timedelta(hours=1)
                else:
                    appointment_start_time_final = "not scheduled"
                    appointment_end_time_final = "not scheduled"

                # Add the container data to the list
                data.append([
                    container_id,
                    container_location_block,
                    container_location_bay,
                    container_location_stack,
                    container_location_tier,
                    appointment_start_time_final,
                    appointment_end_time_final
                ])

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["container_id", "container_location_block", "container_location_bay",
                                     "container_location_stack", "container_location_tier", 
                                     "appointment_start_time", "appointment_end_time"])

    # Convert datetime objects to string for not scheduled containers
    df[['appointment_start_time', 'appointment_end_time']] = df[['appointment_start_time', 'appointment_end_time']].astype(str)

    # Return the DataFrame for further processing if needed
    return df

def generate_block_info(num_blocks=1, num_bays=20, stacks=5, tiers=4):
    block_info = []
    crane_locations = []
    time_available_minutes = []

    for block_id in range(1, num_blocks + 1):
        # Generate stacks_per_bay and tiers_per_bay
        stacks_per_bay = stacks
        tiers_per_bay = tiers

        # Generate random crane location within the number of bays (1 to num_bays)
        crane_location = random.randint(1, num_bays)

        # Generate random time_available_minutes between 60 and 240 minutes (1 to 4 hours)
        time_available_minutes.append(random.randint(60, 240))

        # Append the block information to the list
        block_info.append([block_id, stacks_per_bay, tiers_per_bay])
        crane_locations.append([block_id, crane_location])

    # Create DataFrames for block info, crane locations, and time available
    block_df = pd.DataFrame(block_info, columns=["block_id", "stacks_per_bay", "tiers_per_bay"])
    crane_df = pd.DataFrame(crane_locations, columns=["block_id", "crane_location"])
    time_available_df = pd.DataFrame(time_available_minutes, columns=["block_id"])

    return block_df, crane_df, time_available_df

# Example usage
num_blocks = 2
stacks = 5
tiers = 4
num_bays = 20

block_info_df, crane_locations_df, time_available_df = generate_block_info(num_blocks=num_blocks, num_bays=num_bays, stacks=stacks, tiers=tiers)
bays_data = generate_bays_data(num_blocks=num_blocks, num_bays=num_bays, stacks=stacks, tiers=tiers)

print("Container Data:")
print(bays_data)

print("\nBlock Info:")
print(block_info_df)

print("\nCrane Locations:")
print(crane_locations_df)

print("\nTime Available (minutes):")
print(time_available_df)
