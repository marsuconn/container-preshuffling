import random
import pandas as pd
from datetime import datetime, timedelta, time
import string

print("hello")

def generate_bays_data(num_bays=20, num_blocks=1, max_containers=14, min_containers=10, stacks=5, tiers=4, 
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
    total_hours = (appointment_end_time.hour - appointment_start_time.hour)

    # Initialize list to store the bay data
    data = []

    # Generate data for num_bays bays and num_blocks blocks
    for block in range(1, num_blocks + 1):
        for bay in range(1, num_bays + 1):
            # Determine the number of containers in the bay
            num_containers = random.randint(min_containers, max_containers)

            # Generate data for each container
            for container in range(1, num_containers + 1):
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



df_test=generate_bays_data(num_bays=20, num_blocks=1, max_containers=14, min_containers=10, stacks=5, tiers=4, 
                       appointment_start_date="2023-10-07", appointment_end_date="2023-10-10", 
                       appointment_start_time="08:00", appointment_end_time="17:00", scheduled_proportion=1)