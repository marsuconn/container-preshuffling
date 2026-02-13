import pandas as pd
from test_instance import generate_bays_data
from utils import*
from preprocessing import *
from plotting import plot_bays, plot_bay,plot_bay_with_moves,plot_all_bays_with_moves
#from plotting import plot_bays

input_bays = generate_bays_data(file_name="bays_data.xlsx")
plot_bays(input_bays,5,4, pdf_filename='initial_bays_plots.pdf')


α = 0.75
λ1 = 1
λ2 = 1
H = 4

def solve_all_bays(input_bays, α, λ1, λ2, H):
    
    all_moves = {}
    all_bays = {}

    # Loop over each bay in the dictionary
    for bay_num, bay in input_bays.items():
        print(f"SOLVE BAY {bay_num} ***")
        moves, new_bay = local_search_heuristic(bay, α, λ1, λ2, H)
        
        # Store the moves and the new bay configuration in the dictionaries
        all_moves[bay_num] = moves
        all_bays[bay_num] = new_bay

    return all_moves, all_bays

def export_moves_to_excel(all_moves, file_name='moves.xlsx'):
    data = []
    for bay_id, moves in all_moves.items():
        for move in moves:
            source_stack, destination_stack = move
            data.append([bay_id, source_stack, destination_stack])
    df = pd.DataFrame(data, columns=['Bay', 'Source Stack', 'Destination Stack'])
    df.to_excel(file_name, index=False)
    print(f'Excel file saved as {file_name}')

def export_bays_to_excel(all_bays, file_name='bays.xlsx'):
    data = []
    for bay_id, bay in all_bays.items():
        for stack_id, stack in bay.items():
            for tier, container_info in enumerate(stack, 1):  # Assuming tier starts from 1
                container_id, time_window = container_info
                data.append([bay_id, stack_id, tier, container_id, time_window])
    df = pd.DataFrame(data, columns=['Bay', 'Stack', 'Tier', 'Container', 'Time Window'])
    df.to_excel(file_name, index=False)
    print(f'Excel file saved as {file_name}')

# α, λ1, λ2, and H are parameters of your heuristic, replace them with their actual values

all_moves, all_bays = solve_all_bays(input_bays, α, λ1, λ2, H)

plot_bays(all_bays, pdf_filename='preprocessed_bays_plots.pdf')
plot_all_bays_with_moves(input_bays,all_moves,pdf_filename='preprocessed_bays_with_moves_plots.pdf')
export_moves_to_excel(all_moves, 'pre_processing_moves.xlsx')
export_bays_to_excel(all_bays, 'preprocessed_bays.xlsx') 



def main():
    pass

if __name__ == "__main__":
    main()


