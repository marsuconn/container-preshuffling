def get_heights_from_bay(bay):
    return [len(bay[stack]) for stack in sorted(bay.keys())]

def get_mins_from_bay(bay):
    return [min([container[1] for container in bay[stack]], default=float('inf')) for stack in sorted(bay.keys())]


def expected_minmax(c_time, s_key, bay, S):
    heights = get_heights_from_bay(bay)
    mins = get_mins_from_bay(bay)
    # Convert stack key to index for processing
    s = int(s_key[-1]) - 1

    # Define large placeholder value for empty stacks
    C_plus_1 = max(mins) + 2

    # Rule 1
    min_greater_than_c = [min_val if min_val > c_time else C_plus_1 for min_val in mins]
    M = min(min_greater_than_c)
    if M != C_plus_1:
        eligible_stacks = [i for i, val in enumerate(min_greater_than_c) if val == M and i != s]
        # Break ties by choosing from the highest ones
        eligible_stacks.sort(key=lambda x: heights[x], reverse=True)
        return f"stack{eligible_stacks[0]+1}"

    # Rule 2
    M = max([min_val for i, min_val in enumerate(mins) if i != s])
    eligible_stacks = [i for i, val in enumerate(mins) if val == M and i != s]
    # Select those with the minimum number of containers labeled M
    eligible_stacks.sort(key=lambda x: heights[x])
    # Break ties by choosing from the highest ones
    eligible_stacks.sort(key=lambda x: heights[x], reverse=True)
    return f"stack{eligible_stacks[0]+1}"

# Example
bay = {
    'stack1': [('c1', 1), ('c2', 4),('c3', 7), ('c4', 4), ('c5', 2)],
    'stack2': [('c6', 7), ('c7', 4)],
    'stack3': [],
    'stack4': [('c8', 7), ('c9', 3)],

}
c_time = 2
s_key = 'stack1'
S = 4
print(expected_minmax(c_time, s_key, bay, S))  # This should output the key of the selected stack



def expected_minmax(c_time, s_key, bay, S, max_height=5):
    # Rule 1
    min_values = {}
    for key in bay.keys():
        if key != s_key and len(bay[key]) < max_height:
            if not bay[key]:  # Empty stack
                min_val = float('inf')
            else:
                min_val = bay[key][0][1]  # First container's time

            min_values[key] = min_val

    # Get stacks where min is greater than c_time
    viable_stacks = {k: v for k, v in min_values.items() if v > c_time}

    # If there exists such stack, return the one with the smallest min value
    if viable_stacks:
        chosen_stack = min(viable_stacks, key=viable_stacks.get)
        return chosen_stack

    # Rule 2
    # Here, we are just getting the stack with the maximum min value
    chosen_stack = max(min_values, key=min_values.get)
    return chosen_stack

def retrieve_container(bay, s_key):
    return bay[s_key].pop()

def place_container(bay, s_key, container):
    bay[s_key].append(container)

def retrieve_and_relocate(bay, target_container):
    s_key = None
    for key, stack in bay.items():
        if target_container in stack:
            s_key = key
            break

    if not s_key:
        return bay  # Container not found

    S = len(bay)

    # Start relocating all blocking containers
    while bay[s_key][-1] != target_container:
        d_key = expected_minmax(bay[s_key][-1][1], s_key, bay, S)
        relocated_container = retrieve_container(bay, s_key)
        place_container(bay, d_key, relocated_container)

    # At this point, the target container is on top and can be retrieved
    retrieve_container(bay, s_key)

    return bay

# Example bay structure
bay = {
    'stack1': [('c1', 1), ('c2', 4), ('c3', 7), ('c4', 4), ('c5', 2)],
    'stack2': [('c6', 7), ('c7', 4)],
    'stack3': [],
    'stack4': [('c8', 7), ('c9', 3)]
}

# Retrieve container with time 1
target_container = ('c1', 1)
new_bay_config = retrieve_and_relocate(bay, target_container)
print(new_bay_config)




def get_min(s):
    return min(s, key=lambda x: x[1])[1] if s else float('inf')

def relocate_container(container, bay):
    S = len(bay)
    T = max(len(stack) for stack in bay.values())
    
    current_stack = None
    for stack, containers in bay.items():
        if container in containers:
            current_stack = stack
            break

    if not current_stack:
        return

    # Rule 1
    M_values = [get_min(bay[stack]) for stack in bay if stack != current_stack and get_min(bay[stack]) > container[1]]
    if M_values:
        M = min(M_values)
        candidate_stacks = [stack for stack in bay if get_min(bay[stack]) == M]
        selected_stack = max(candidate_stacks, key=lambda x: len(bay[x])) # select the highest ones
        bay[selected_stack].append(container)
        bay[current_stack].remove(container)
        return

    # Rule 2
    M = max(get_min(bay[stack]) for stack in bay if stack != current_stack)
    candidate_stacks = [stack for stack in bay if get_min(bay[stack]) == M]
    
    # select those with the minimum number of containers labeled M
    min_containers_with_M = min(len(bay[stack]) for stack in candidate_stacks if get_min(bay[stack]) == M)
    candidate_stacks = [stack for stack in candidate_stacks if len(bay[stack]) == min_containers_with_M]
    
    selected_stack = max(candidate_stacks, key=lambda x: len(bay[x])) # select the highest ones
    bay[selected_stack].append(container)
    bay[current_stack].remove(container)

def retrieve_container(target_container, bay):
    while target_container not in bay['stack1']:
        for container in reversed(bay['stack1'][:-1]):  # Don't consider the target container itself
            relocate_container(container, bay)
    bay['stack1'].remove(target_container)

bay = {
    'stack1': [('c1', 1), ('c2', 4),('c3', 7), ('c4', 4), ('c5', 2)],
    'stack2': [('c6', 7), ('c7', 4)],
    'stack3': [ ],
    'stack4': [('c8', 7), ('c9', 3)],
}

retrieve_container(('c1', 1), bay)
print(bay)



def get_min(s):
    return min(s, key=lambda x: x[1])[1] if s else float('inf')

def relocate_container(container, bay):
    S = len(bay)
    T = max(len(stack) for stack in bay.values())
    
    current_stack = None
    for stack, containers in bay.items():
        if container in containers:
            current_stack = stack
            break

    if not current_stack:
        return

    # Rule 1
    M_values = [get_min(bay[stack]) for stack in bay if stack != current_stack and get_min(bay[stack]) > container[1]]
    if M_values:
        M = min(M_values)
        candidate_stacks = [stack for stack in bay if get_min(bay[stack]) == M]
        selected_stack = max(candidate_stacks, key=lambda x: len(bay[x])) # select the highest ones
        bay[selected_stack].append(container)
        bay[current_stack].remove(container)
        return

    # Rule 2
    M = max(get_min(bay[stack]) for stack in bay if stack != current_stack)
    candidate_stacks = [stack for stack in bay if get_min(bay[stack]) == M]
    
    # select those with the minimum number of containers labeled M
    min_containers_with_M = min(len(bay[stack]) for stack in candidate_stacks if get_min(bay[stack]) == M)
    candidate_stacks = [stack for stack in candidate_stacks if len(bay[stack]) == min_containers_with_M]
    
    selected_stack = max(candidate_stacks, key=lambda x: len(bay[x])) # select the highest ones
    bay[selected_stack].append(container)
    bay[current_stack].remove(container)

def retrieve_container(target_container, bay):
    for stack, containers in bay.items():
        if target_container in containers:
            while containers[-1] != target_container:
                relocate_container(containers[-1], bay)
            containers.pop()  # Remove the target container
            return

bay = {
    'stack1': [('c1', 1), ('c2', 4),('c3', 7), ('c4', 4), ('c5', 2)],
    'stack2': [('c6', 7), ('c7', 4)],
    'stack3': [ ],
    'stack4': [('c8', 7), ('c9', 3)],
}

retrieve_container(('c1', 1), bay)
print(bay)
