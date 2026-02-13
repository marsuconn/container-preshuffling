import random
from matplotlib.backends.backend_pdf import PdfPages

from matplotlib import cm, pyplot as plt
import numpy as np
import pandas as pd


def process_appointment_data(df):
    df['appointment_start_time'] = pd.to_datetime(df['appointment_start_time'])
    df = df.sort_values(by='appointment_start_time')
    df['appointment_time'] = df['appointment_start_time'].astype('category').cat.codes + 1
    df = df.drop(columns=['appointment_start_time', 'appointment_end_time'])

    return df

#database connection
from sqlalchemy import create_engine

def get_user_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid integer.")

            
def get_data_from_database():
    # Set up the connection string
    # for SQLite.
    #DATABASE_URL = "sqlite:///mydatabase.db"
    
    # For PostgreSQL :
    # DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"
    
    # For MySQL :
    DATABASE_URL = "mysql://username:password@localhost/mydatabase"
    engine = create_engine(DATABASE_URL)

    query = 'SELECT * FROM your_table_name'
    df = pd.read_sql(query, engine)
    
    return df


def calculate_u_c(bay, container):
    """
    Calculates u(c), the smallest time frame of all containers located underneath container 'c'.
    
    Parameters:
    bay (dict): A dictionary representing the container bay.
    container (str): The ID of the container.

    Returns:
    int or float: The smallest time frame of all containers located underneath container 'c'.
                  Returns 'inf' if the container is not in the stack or it's at the bottom.
    """
    # Get the stack and the index of the container
    stack, index = get_container_position(bay, container)
    if index is None or index == 0:  # If the container is not in the stack or it's at the bottom
        return float('inf')
    else:
        return min(c[1] for c in bay[stack][:index])  # Return the smallest time frame of the containers below

def get_container_time(bay, container):
    """
    Gets the time frame of a container.

    Parameters:
    bay (dict): A dictionary representing the container bay.
    container (str): The ID of the container.

    Returns:
    int or None: The time frame of the container if found, else None.
    """
    for stack in bay.values():
        for c, t in stack:
            if c == container:
                return t
    return None

    # Function to get container position
def get_container_position(bay, container_id):
    """
    Gets the position of a container in the bay.

    Parameters:
    bay (dict): A dictionary representing the container bay.
    container_id (str): The ID of the container.

    Returns:
    tuple or (None, None): A tuple of stack name and position if found, else (None, None).
    """
    for stack_name, stack in bay.items():
        for position, (id, _) in enumerate(stack):
            if id == container_id:
                return stack_name, position
    return None, None

def calculate_q_values(bay):
    """
    Calculates the q values for each container in the bay.

    Parameters:
    bay (dict): A dictionary representing the container bay.

    Returns:
    dict: A dictionary with the same keys as 'bay', and values being lists of q values for each container in the stack.
    """
    # Initialize q_values dictionary
    q_values = {stack_name: [] for stack_name in bay.keys()}

    # Calculate q(c) for each container in the bay
    for stack_name, stack in bay.items():
        for i, container in enumerate(stack):
            if i == 0:  # no container underneath
                u_c = float('inf')  # assign it to infinity
            else:
                u_c = min(time_window for _, time_window in stack[:i])  # Smallest time frame of containers underneath c

            t_c = container[1]  # t(c) is the time window of the container
            if u_c > t_c:
                q_c = 1
            elif u_c == t_c:
                q_c = 2
            elif u_c > min_h_s(bay) or t_c < max_l_s(bay):
                q_c = 3
            else:
                q_c = 4

            # Add to q_values
            q_values[stack_name].append(q_c)
    return q_values

def calculate_expected_relocation_moves(bay):
    """
    Calculates the total expected relocation moves for the entire bay.

    Parameters:
    bay (dict): A dictionary representing the container bay.

    Returns:
    float: The total expected relocation moves for the entire bay.
    """
    # Calculate q_values
    q_values = calculate_q_values(bay)

    # Calculate and return the total expected relocation moves for the entire bay
    return sum(1.4 if q_c == 4 else 1 if q_c == 3 else 0.5 if q_c == 2 else 0 
               for stack_name in bay.keys() 
               for q_c in q_values[stack_name])

def calculate_expected_moves(bay, stack):
    """
    Calculates the expected moves for a stack.

    Parameters:
    bay (dict): A dictionary representing the container bay.
    stack (str): The name of the stack.

    Returns:
    float: The expected moves for the stack.
    """
    # Calculate q_values
    q_values = calculate_q_values(bay)

    # Calculate and return the expected moves for a stack
    return sum(1.4 if q_c == 4 else 1 if q_c == 3 else 0.5 if q_c == 2 else 0 for q_c in q_values[stack])

# Functions to compute the minimum of the largest time frames and the maximum of the smallest time frames
#def min_h_s(bay):
#    return min(max(time_window for _, time_window in stack) for stack in bay.values())

#def max_l_s(bay):
#    return max(min(time_window for _, time_window in stack) for stack in bay.values())

def min_h_s(bay):
    return min(max(time_window for _, time_window in stack) if stack else 0 for stack in bay.values())

def max_l_s(bay):
    return max(min(time_window for _, time_window in stack) if stack else 0 for stack in bay.values())

    
def get_smallest_time_frame(stack):
    if not stack:  # The stack is empty
        return float('inf')
    else:
        return min([c[1] for c in stack])


def get_containers_below(bay, container):
    # Get the stack of the container
    stack = next((stack for stack, containers in bay.items() if any(c[0] == container for c in containers)), None)
    # Get the position of the container in the stack
    container_position = next((index for index, c in enumerate(bay[stack]) if c[0] == container), None)
    # Get all the containers below the specified container in the stack
    containers_below = [c[0] for index, c in enumerate(bay[stack]) if index < container_position]
    return containers_below

def is_correctly_placed(bay, container_c):
    # Identify the current stack of the container c (s_c) and its position (p_c)
    s_c, p_c = get_container_position(bay, container_c)
    t_c = get_container_time(bay, container_c)  # get the time window of the container c

    # Get all the containers below c in stack s_c
    containers_below_c = get_containers_below(bay, container_c)

    # Check if all containers below c have a larger time frame
    for container in containers_below_c:
        if get_container_time(bay, container) <= t_c:
            return False  # c is incorrectly placed

    return True  # If all conditions are met, c is correctly placed

def select_stack_for_relocation(bay, exclude_stacks, c_prime, t_c_prime, α, λ1, λ2, H):
    # If there exists a stack s' in S \ exclude_stacks for which n(s') < H and l(s') > t(c') and f(B, s') <= α
    
    available_stacks = [stack_name for stack_name, stack in bay.items() if len(stack) < H and stack_name not in exclude_stacks and get_smallest_time_frame(stack) > t_c_prime and calculate_expected_moves(bay, stack_name) <= α]
    
    if available_stacks:
        # Sort the stacks by the smallest minimum time frame
        sorted_stacks = sorted(available_stacks, key=lambda k: get_smallest_time_frame(bay[k]))
        # Select λ1 stacks with the smallest minimum time frame
        selected_stacks = sorted_stacks[:λ1]
        print('selecting from  stacks with reloc moves < alpha ')
    else:
        # If no valid stacks, select one with the smallest minimum time frame
        available_stacks = [stack_name for stack_name, stack in bay.items() if len(stack) < H and stack_name not in exclude_stacks]
        # Sort the stacks by the smallest minimum time frame
        sorted_stacks = sorted(available_stacks, key=lambda k: get_smallest_time_frame(bay[k]))
        # Select λ2 stacks with the smallest minimum time frame
        selected_stacks = sorted_stacks[:λ2]
        print('selecting from stacks with len(stack) < H and stack_name not in exclude_stack')
    # Select a stack randomly
    if selected_stacks:  # Check if the list is not empty
        s_double_prime = random.choice(selected_stacks)
    else:
        s_double_prime = None
    print('available stack for relocation : ', available_stacks)
    
    print('lambda_2 selected stack for relocation : ',selected_stacks)
    print('s_double_prime: ', s_double_prime)
    return s_double_prime

def select_stack_for_c(bay, s_c, H):
    # Find the available stacks for moving container c
    available_stacks = [s for s in bay.keys() if s != s_c and len(bay[s]) < H]
    
    # If no stacks are available, return None
    if not available_stacks:
        return None

    # Find the stack with the highest number of containers
    highest_stack = max(available_stacks, key=lambda s: len(bay[s]))
    print('available stack for c : ', available_stacks)
    print('highest stack for c : ',highest_stack)
    return highest_stack




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


def export_to_excel_multiple_blocks(results, file_name='bays.xlsx'):
    data = []
    for block_id, block_data in results.items():
        for bay_id, bay in block_data['all_bays'].items():
            for stack_id, stack in bay.items():
                for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                    container_id, time_window = container_info
                    data.append([block_id, bay_id, stack_id, tier, container_id, time_window])
    
    df = pd.DataFrame(data, columns=['Block', 'Bay', 'Stack', 'Tier', 'Container', 'Time Window'])
    df.to_excel(file_name, index=False)
    

def export_moves_to_excel_multiple_blocks(results, file_name='moves.xlsx'):
    data = []
    for block_id, block_data in results.items():
        for bay_id, moves in block_data['all_moves'].items():
            for move in moves:
                source_stack, destination_stack = move
                data.append([block_id, bay_id, source_stack, destination_stack])
    
    df = pd.DataFrame(data, columns=['Block', 'Bay', 'Source Stack', 'Destination Stack'])
    df.to_excel(file_name, index=False)
    

