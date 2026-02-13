import copy
import random
from utils import *

def preprocessing_moves_algo3(bay, container_c, stack_s,α, λ1, λ2, H):
    """
    Preprocesses moves for moving container from original stack to destination staack.

    Parameters:
    bay (dict): A dictionary representing the container bay. Keys are stack names, 
                values are lists of tuples representing containers in the stack.
    container_c (str): The ID of the container to be relocated.
    stack_s (str): The name of the stack where the container will be moved.
    α (float): A weight parameter for the heuristic function.
    λ1 (int): A weight parameter for the heuristic function.
    λ2 (int): A weight parameter for the heuristic function.
    H (int): The maximum allowed stack height.

    Returns:
    list: The processed list of moves, where each move is represented as a tuple
          containing the source stack and the destination stack.
    dict: The updated bay after all the moves have been processed.
    """
    
    print("====================")
    print('algorithm 3 is used')
    print("====================")
    P = []
    bay_copy=copy.deepcopy(bay)
    
    s_c, p_c = get_container_position(bay, container_c)  # Get original stack of c
    t_c = get_container_time(bay, container_c)

    O_c = {c[0]: index for index, c in enumerate(bay[s_c]) if index > p_c}
    #M_c = {c[0]: index for index, c in enumerate(bay[stack_s]) if calculate_u_c(bay, c[0]) < t_c}
    M_c = {c[0]: index for index, c in enumerate(bay[stack_s]) if (calculate_u_c(bay, c[0]) < t_c) or (get_container_time(bay,c[0]) < t_c)}

    print ('Set O_c:' ,O_c)
    print('Set M_c:', M_c)
    while O_c or M_c:
        o = max(O_c, key=O_c.get) if O_c else None
        m = max(M_c, key=M_c.get) if M_c else None
        
        if m is not None and (o is None or get_container_time(bay, m) >= get_container_time(bay, o)):
            print('get_container_time(bay, m) >= get_container_time(bay, o)')
            c_prime = m
            print('c_prime :',c_prime )
            M_c.pop(c_prime)
            p_1 = stack_s
            print('p_1: ',p_1)
        else:
            print('get_container_time(bay, m) < get_container_time(bay, o)')
            c_prime = o
            print('c_prime :',c_prime )
            O_c.pop(c_prime)
            p_1 = s_c
            print('p_1: ',p_1)

        t_c_prime = get_container_time(bay, c_prime)
        s_double_prime = select_stack_for_relocation(bay_copy, [s_c, stack_s], c_prime, t_c_prime, α, λ1, λ2, H)

        if s_double_prime is None:  # If there is no stack available for relocation
            #return P, None  # Return current pre-processing moves and None to indicate that the operation was not feasible
            return [], bay
        
        if s_double_prime is not None:
            print('Move non target container, ', c_prime, ',from stack, ' ,p_1, ' to ',s_double_prime )
            bay_copy[s_double_prime].append((c_prime, t_c_prime))
            bay_copy[p_1] = [c for c in bay_copy[p_1] if c[0] != c_prime]
            P.append((p_1, s_double_prime))
            print('pre-processing moves: ',P)

    # Move container c to the destination stack and update the bay
    print('move target container ',container_c, ' to destiantion stack ', stack_s)
    bay_copy[stack_s].append((container_c,t_c))
    bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != container_c]
    P.append((s_c, stack_s))
    print('pre-processing moves after mvoing container c ;', P)

    return P, bay_copy


def preprocessing_moves_algo4(bay, container_c, α, λ1, λ2, H):
    """
    Preprocesses moves for moving container within the original stack.

    Parameters:
    bay (dict): A dictionary representing the container bay. Keys are stack names, 
                values are lists of tuples representing containers in the stack.
    container_c (str): The ID of the container to be relocated.
    stack_s (str): The name of the stack where the container will be moved.
    α (float): A weight parameter for the heuristic function.
    λ1 (int): A weight parameter for the heuristic function.
    λ2 (int): A weight parameter for the heuristic function.
    H (int): The maximum allowed stack height.

    Returns:
    list: The processed list of moves, where each move is represented as a tuple
          containing the source stack and the destination stack.
    dict: The updated bay after all the moves have been processed.
    """
    print("====================")
    print('algorithm 4 is used')
    print("====================")
    P = []
    bay_copy=copy.deepcopy(bay)
    s_c, p_c = get_container_position(bay, container_c)  # Get original stack of c
    t_c = get_container_time(bay, container_c)

    S1 = {c[0]: index for index, c in enumerate(bay[s_c]) if index > p_c}
    #S2 = {c[0]: index for index, c in enumerate(bay[s_c]) if index < p_c and calculate_u_c(bay, container_c) < t_c}
    print('S1:', S1)
    #S2 = {c[0]: index for index, c in enumerate(bay[s_c]) if index < p_c and calculate_u_c(bay, container_c) < t_c}
    #S2 = {c[0]: index for index, c in enumerate(bay[s_c]) if index < p_c and calculate_u_c(bay, container_c) < t_c and not is_correctly_placed(bay, c[0])}
    S2 = {c[0]: index for index, c in enumerate(bay[s_c]) if index < p_c and calculate_u_c(bay, container_c) < t_c and get_container_time(bay,c[0])<t_c}

    print('S2:' ,S2)
    
    
    while S1:
        print('==for S1== ')
        c_prime = max(S1, key=S1.get) #top container
        print('c_prime: ',c_prime)
        t_c_prime = get_container_time(bay, c_prime) #get time of the container

        # Select s'' for relocation
        excluded_stacks=s_c
        s_double_prime = select_stack_for_relocation(bay_copy, excluded_stacks, c_prime, t_c_prime, α, λ1, λ2, H)
        
        if s_double_prime is None:  # If there is no stack available for relocation
            #return P, None  # Return current pre-processing moves and None to indicate that the operation was not feasible
            return [],bay
        
        # Relocate container c' to stack s''
        bay_copy[s_double_prime].append((c_prime, t_c_prime))
        bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != c_prime]
        #bay_copy[s_c].pop()

        # Update pre-processing moves and S1
        P.append((s_c, s_double_prime))
        print('preprocessing moves: ',P)
        S1.pop(c_prime)
    
    print("==for c==")
    # Move container c to the highest stack s''' with n (s''') < H
    stack_triple_prime = select_stack_for_c(bay_copy, s_c, H)
    print('available stack for temporary relocation of,' ,container_c, ': ', stack_triple_prime)
    if stack_triple_prime is None:  # If there is no stack available for relocation
            #return P, None  # Return current pre-processing moves and None to indicate that the operation was not feasible
        return [],bay
    bay_copy[stack_triple_prime].append((container_c, t_c))
    bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != container_c]  # remove container c from the stack
    #bay_copy[s-c].pop()
    P.append((s_c, stack_triple_prime))
    print('premoves after moving ,',container_c, ' : ',P)
    
    while S2:
        print('==for S2== ')
        c_prime = max(S2, key=S2.get)
        print('c_prime : ', c_prime)
        t_c_prime = get_container_time(bay, c_prime)
        # Select s'' for relocation
        excluded_stacks=[s_c,stack_triple_prime]
        s_double_prime = select_stack_for_relocation(bay_copy, excluded_stacks, c_prime, t_c_prime, α, λ1, λ2, H)
        
        if s_double_prime is None:  # If there is no stack available for relocation
            #return P, None  # Return current pre-processing moves and None to indicate that the operation was not feasible
            return [],bay
        
        # Relocate container c' to stack s''
        bay_copy[s_double_prime].append((c_prime, t_c_prime))
        bay_copy[s_c] = [c for c in bay_copy[s_c] if c[0] != c_prime]

        # Update pre-processing moves and S2
        P.append((s_c, s_double_prime))
        print('pre processing moves after moving ',c_prime, ' : ',P )
        S2.pop(c_prime)

    # Move container c to stack s
    bay_copy[s_c].append((container_c, t_c))
    bay_copy[stack_triple_prime] = [c for c in bay_copy[stack_triple_prime] if c[0] != container_c]
    P.append((stack_triple_prime, s_c))
    print("all preprocessing move : ", P)

    return P, bay_copy



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
    R=[] #Relocation moves
    
    #best_bay=copy.deepcopy(bay)
    # Determine the maximum time frame Z
    Z = max(time for stack in bay.values() for _, time in stack)
    print('Time Windows or Time Frames :', Z)
    # Start with the largest time frame
    for p in range(Z, 0, -1):
        # Get he containers with time frame p
        A_p = {c for stack in bay.values() for c, t in stack if t == p}
        print('Containers in ', p, 'time window :', A_p )
        while A_p:
            # Select randomly a container c with time frame p that is not correctly placed
            incorrectly_placed_containers = [container for container in A_p if not is_correctly_placed(bay, container)]
            print("####################")
            print('incorrectly_placed_containers  ', p, 'time window :', incorrectly_placed_containers)

            if incorrectly_placed_containers:  # Check if the list is not empty
                c = random.choice(incorrectly_placed_containers)
                
                A_p.remove(c)
            else:
                break  # Exit the while loop if no incorrectly placed containers are found

            # Calculate the expected number of moves in the current bay configuration
            print("Target Container in",p," time window :", c)
            current_moves = calculate_expected_relocation_moves(bay)
            print('Excpected relocation with the current config: ', current_moves)
            best_improvement = 0
            best_stack = None
            #best_bay = None
            best_bay=copy.deepcopy(bay)
            best_moves = []

            # Consider each stack as a potential destination for the container c
            for s in bay:
                # Skip if the current stack is the same as the destination stack
                print("___________________________________")
                print('checkin stack :',s)
                # Create a copy of the current bay configuration
                #bay_copy = bay.copy()
                bay_copy = copy.deepcopy(bay)

                print('bay copy: ',bay_copy)
                print('bay: ',bay)

                # Attempt to move container c to stack s
                if s != get_container_position(bay, c)[0]:  # If destination stack is not the same as the original
                    pre_moves, updated_bay = preprocessing_moves_algo3(bay_copy, c, s, α, λ1, λ2, H)
                else:
                    pre_moves, updated_bay = preprocessing_moves_algo4(bay_copy, c, α, λ1, λ2, H)

                #if pre_moves is None or bay_copy is None:  # If the move was not feasible, skip to the next iteration
                if not pre_moves:  # If the move was not feasible, skip to the next iteration
                    continue
                    
                print('pre-moves for ',s,' stack :', pre_moves)
                print('new Bay orientation for ',s,' stack :', updated_bay)
                print('original Bay orientation for ',s,' stack :', bay)
                # Calculate the improvement
                new_moves = calculate_expected_relocation_moves(updated_bay)
                m_s = len(pre_moves)
                #improvement = current_moves - (α * m_s + new_moves)
                
                print('Expected relocation moves: ', new_moves)
                improvement = current_moves -  new_moves
                print('improvement = current_moves -  new_moves: ', improvement)

                # Update the best improvement and the best destination stack
                if improvement > best_improvement:
                    best_improvement = improvement
                    best_relocation_moves=new_moves
                    best_stack = s
                    best_bay = updated_bay
                    best_moves = pre_moves
                    print("*** improvement achieved***")
                    print("best moves: ", best_moves)
                    print("best bay :", updated_bay)
                    print("best expected relocation moves :", best_relocation_moves)
            # If the best improvement is positive, update the bay configuration and the pre-processing moves
            if best_improvement > 0:
                bay = best_bay
                P += best_moves
                R.extend(best_relocation_moves)                
                print('move to stack, ',best_stack,)
                print('pre-moves: ', best_moves)
                print('new bay: ',bay)

    return P,R,bay


