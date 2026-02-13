
import copy
import random


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
    Gets the position (stack # and tier #) of a container in the bay.

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

def min_h_s(bay):
    return min(max(time_window for _, time_window in stack) if stack else 0 for stack in bay.values())

def max_l_s(bay):
    return max(min(time_window for _, time_window in stack) if stack else 0 for stack in bay.values())



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
        ##print('selecting from  stacks with reloc moves < alpha ')
    else:
        # If no valid stacks, select one with the smallest minimum time frame
        available_stacks = [stack_name for stack_name, stack in bay.items() if len(stack) < H and stack_name not in exclude_stacks]
        # Sort the stacks by the smallest minimum time frame
        sorted_stacks = sorted(available_stacks, key=lambda k: get_smallest_time_frame(bay[k]))
        # Select λ2 stacks with the smallest minimum time frame
        selected_stacks = sorted_stacks[:λ2]
        ##print('selecting from stacks with len(stack) < H and stack_name not in exclude_stack')
    # Select a stack randomly
    if selected_stacks:  # Check if the list is not empty
        s_double_prime = random.choice(selected_stacks)
    else:
        s_double_prime = None
    ##print('available stack for relocation : ', available_stacks)
    
    ##print('lambda_2 selected stack for relocation : ',selected_stacks)
    #print('s_double_prime: ', s_double_prime)
    return s_double_prime # s_double_prime is a subset of s_prime(available_stacks)

def select_stack_for_c(bay, s_c, H):
    # Find the available stacks for moving container c
    available_stacks = [s for s in bay.keys() if s != s_c and len(bay[s]) < H]
    
    # If no stacks are available, return None
    if not available_stacks:
        return None

    # Find the stack with the highest number of containers
    highest_stack = max(available_stacks, key=lambda s: len(bay[s]))
    #print('available stack for c : ', available_stacks)
    #print('highest stack for c : ',highest_stack)
    return highest_stack


def preprocessing_moves_algo3(bay, container_c, stack_s, α, λ1, λ2, H):
    P = []
    bay_copy = copy.deepcopy(bay)

    s_c, p_c = get_container_position(bay, container_c)  
    t_c = get_container_time(bay, container_c)

    O_c = {c[0]: index for index, c in enumerate(bay[s_c]) if index > p_c}
    M_c = {c[0]: index for index, c in enumerate(bay[stack_s]) 
           if (calculate_u_c(bay, c[0]) < t_c) or (get_container_time(bay,c[0]) < t_c)}
    #print("O_c: ",O_c)
    #print("M_c :",M_c)
    while O_c or M_c:
        o = max(O_c, key=O_c.get) if O_c else None
        m = max(M_c, key=M_c.get) if M_c else None
        
        if m is not None and (o is None or get_container_time(bay, m) >= get_container_time(bay, o)):
            c_prime = m
            M_c.pop(c_prime)
            p_1 = stack_s
        else:
            c_prime = o
            O_c.pop(c_prime)
            p_1 = s_c

        t_c_prime = get_container_time(bay, c_prime)
        s_double_prime = select_stack_for_relocation(bay_copy, [s_c, stack_s], c_prime, t_c_prime, α, λ1, λ2, H)
        #print('s_double_prime :',s_double_prime)
        if s_double_prime is None:  
            return [], bay
        
        if len(bay_copy[s_double_prime]) < H:#looks redundant condition
            bay_copy[s_double_prime].append((c_prime, t_c_prime))
        else:
            #  for debugging if needed:
            # #print(f"Stack {s_double_prime} is full. Cannot add container {c_prime}")
            continue
        
        bay_copy[p_1] = [c for c in bay_copy[p_1] if c[0] != c_prime]
        P.append((p_1, s_double_prime, c_prime))
        #print("while not null", P)
    

    if len(bay_copy[stack_s]) < H:
        bay_copy[stack_s].append((container_c, t_c))
        bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != container_c]
        P.append((s_c, stack_s, container_c))
        #print(P)

    return P, bay_copy




def preprocessing_moves_algo4(bay, container_c, α, λ1, λ2, H):
    P = []
    bay_copy = copy.deepcopy(bay)
    s_c, p_c = get_container_position(bay, container_c)
    t_c = get_container_time(bay, container_c)

    S1 = {c[0]: index for index, c in enumerate(bay[s_c]) if index > p_c}
    S2 = {c[0]: index for index, c in enumerate(bay[s_c]) 
          if index < p_c and calculate_u_c(bay, container_c) < t_c and get_container_time(bay,c[0])<t_c}

    while S1:
        c_prime = max(S1, key=S1.get)
        t_c_prime = get_container_time(bay, c_prime)

        s_double_prime = select_stack_for_relocation(bay_copy, s_c, c_prime, t_c_prime, α, λ1, λ2, H)

        if s_double_prime is None:
            return [], bay
        
        if len(bay_copy[s_double_prime]) < H: #might be a redundant condition
            bay_copy[s_double_prime].append((c_prime, t_c_prime))
        else:
            # Uncomment the #print statement for debugging if needed
            # #print(f"Stack {s_double_prime} is full. Cannot add container {c_prime}")
            continue

        bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != c_prime]
        P.append((s_c, s_double_prime, c_prime))

        S1.pop(c_prime)

    stack_triple_prime = select_stack_for_c(bay_copy, s_c, H)
    
    if stack_triple_prime is None:
        return [], bay
    
    bay_copy[stack_triple_prime].append((container_c, t_c))
    bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != container_c]
    P.append((s_c, stack_triple_prime, container_c))

    while S2:
        c_prime = max(S2, key=S2.get)
        t_c_prime = get_container_time(bay, c_prime)
        s_double_prime = select_stack_for_relocation(bay_copy, [s_c, stack_triple_prime], c_prime, t_c_prime, α, λ1, λ2, H)
        
        if s_double_prime is None:
            return [], bay
        
        if len(bay_copy[s_double_prime]) < H:
            bay_copy[s_double_prime].append((c_prime, t_c_prime))
        else:
            # Uncomment the #print statement for debugging if needed
            # #print(f"Stack {s_double_prime} is full. Cannot add container {c_prime}")
            continue

        bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != c_prime]
        P.append((s_c, s_double_prime, c_prime))

        S2.pop(c_prime)

    bay_copy[s_c].append((container_c, t_c))
    bay_copy[stack_triple_prime] = [c for c in bay_copy[stack_triple_prime] if c[0] != container_c]
    P.append((stack_triple_prime, s_c, container_c))

    return P, bay_copy


def local_search_heuristic_v2(bay, α, λ1, λ2, H):
    preprocessing_moves = []  # Store all preprocessing moves cumulatively
    move_sequences = {}  # Store individual move sequences
    erms = {0: calculate_expected_relocation_moves(bay)}
    best_bay_configs = {}  # Store best bay configurations
    move_sequence_counter = 0  # Counter for naming move sequences
    
    Z = max(time for stack in bay.values() for _, time in stack)
    
    for p in range(Z, 0, -1):
        A_p = {c for stack in bay.values() for c, t in stack if t == p}

        while A_p:
            incorrectly_placed_containers = [container for container in A_p if not is_correctly_placed(bay, container)]

            if incorrectly_placed_containers:
                c = random.choice(incorrectly_placed_containers)
                A_p.remove(c)
            else:
                break

            current_moves = calculate_expected_relocation_moves(bay)
            best_improvement = 0
            best_bay = copy.deepcopy(bay)
            best_moves = []

            for s in bay:
                bay_copy = copy.deepcopy(bay)

                if s != get_container_position(bay, c)[0]:
                    pre_moves, updated_bay = preprocessing_moves_algo3(bay_copy, c, s, α, λ1, λ2, H)
                else:
                    pre_moves, updated_bay = preprocessing_moves_algo4(bay_copy, c, α, λ1, λ2, H)

                if not pre_moves:
                    continue

                expected_relocation_moves = calculate_expected_relocation_moves(updated_bay)
                improvement = current_moves - expected_relocation_moves

                if improvement > best_improvement:
                    best_improvement = improvement
                    best_bay = updated_bay
                    best_moves = pre_moves

            if best_improvement > 0:
                bay = best_bay
                preprocessing_moves += best_moves  # Add moves to the cumulative list
                erms[move_sequence_counter + 1] = calculate_expected_relocation_moves(bay)
                
                # Naming and storing the move sequences and corresponding bay configurations
                move_sequence_name = f"move_sequence_{move_sequence_counter + 1}"
                move_sequences[move_sequence_name] = best_moves
                best_bay_configs[move_sequence_name] = best_bay

                move_sequence_counter += 1

    results = {
        "preprocessing_moves": preprocessing_moves,
        "move_sequences": move_sequences,
        "erms": erms,
        "intermidiate_bays_configs": best_bay_configs
    }

    return results, bay

def local_search_heuristic(bay, α, λ1, λ2, H):
    """
    Performs local search to find an optimal sequence of container moves in a bay.

    Parameters:
    bay (dict): A dictionary representing the container bay. Keys are stack names, 
                values are lists of tuples representing containers in the stack.
    α (float): A weight parameter for the heuristic function.
    λ1 (int): A weight parameter for the heuristic function.
    λ2 (float): A weight parameter for the heuristic function.
    H (int): The maximum allowed stack height.

    Returns:
    list: A list of moves that lead to an improved bay configuration. Each move is 
          represented as a tuple containing the source stack and the destination stack.
    dict: The updated bay after all the moves have been processed.
    """
    # Initialize pre-processing moves
    P = [] # preprocessing moves
    R=[calculate_expected_relocation_moves(bay)] #Relocation moves
    erms={}
    erms[0]=calculate_expected_relocation_moves(bay)
    best_relocation_moves = 0  # Initialize to default value

    #best_bay=copy.deepcopy(bay)
    # Determine the maximum time frame Z
    Z = max(time for stack in bay.values() for _, time in stack)
    #print('Time Windows or Time Frames :', Z)
    # Start with the largest time frame
    for p in range(Z, 0, -1):
        # Get he containers with time frame p
        A_p = {c for stack in bay.values() for c, t in stack if t == p}
        #print('Containers in ', p, 'time window :', A_p )
        while A_p:
            # Select randomly a container c with time frame p that is not correctly placed
            incorrectly_placed_containers = [container for container in A_p if not is_correctly_placed(bay, container)]
            #print("####################")
            #print('incorrectly_placed_containers  ', p, 'time window :', incorrectly_placed_containers)

            if incorrectly_placed_containers:  # Check if the list is not empty
                c = random.choice(incorrectly_placed_containers)
                
                A_p.remove(c)
            else:
                break  # Exit the while loop if no incorrectly placed containers are found

            # Calculate the expected number of moves in the current bay configuration
            #print("Target Container in",p," time window :", c)
            current_moves = calculate_expected_relocation_moves(bay)
            #print('Excpected relocation with the current config: ', current_moves)
            best_improvement = 0
            best_stack = None
            #best_bay = None
            best_bay=copy.deepcopy(bay)
            best_moves = []

            # Consider each stack as a potential destination for the container c
            for s in bay:
                # Skip if the current stack is the same as the destination stack
                #print("___________________________________")
                #print('checkin stack :',s)
                # Create a copy of the current bay configuration
                #bay_copy = bay.copy()
                bay_copy = copy.deepcopy(bay)

                #print('bay copy: ',bay_copy)
                #print('bay: ',bay)

                # Attempt to move container c to stack s
                if s != get_container_position(bay, c)[0]:  # If destination stack is not the same as the original
                    pre_moves, updated_bay = preprocessing_moves_algo3(bay_copy, c, s, α, λ1, λ2, H)
                else:
                    pre_moves, updated_bay = preprocessing_moves_algo4(bay_copy, c, α, λ1, λ2, H)

                #if pre_moves is None or bay_copy is None:  # If the move was not feasible, skip to the next iteration
                if not pre_moves:  # If the move was not feasible, skip to the next iteration
                    continue
                    
                #print('pre-moves for ',s,' stack :', pre_moves)
                #print('new Bay orientation for ',s,' stack :', updated_bay)
                #print('original Bay orientation for ',s,' stack :', bay)
                # Calculate the improvement
                expected_relocation_moves = calculate_expected_relocation_moves(updated_bay)
                m_s = len(pre_moves)
                #improvement = current_moves - (α * m_s + new_moves)
                
                #print('Expected relocation moves: ', expected_relocation_moves)
                improvement = current_moves -  expected_relocation_moves
                #print('improvement = current_moves -  new_moves: ', improvement)

                # Update the best improvement and the best destination stack
                if improvement > best_improvement:
                    best_improvement = improvement
                    best_relocation_moves=expected_relocation_moves
                    best_stack = s
                    best_bay = updated_bay
                    best_moves = pre_moves

                    #print("*** improvement achieved***")
                    #print("best moves: ", best_moves)
                    #print("best bay :", updated_bay)
                    #print("best expected relocation moves :", best_relocation_moves)
            # If the best improvement is positive, update the bay configuration and the pre-processing moves
            if best_improvement >= 0:
                bay = best_bay
                P += best_moves
                R.append(best_relocation_moves)   
                erms[tuple(best_moves)]=best_relocation_moves             
                #print('move to stack ',best_stack)
                #print('pre-moves: ', best_moves)
                #print('new bay: ',bay)

    return P,R,erms,bay











