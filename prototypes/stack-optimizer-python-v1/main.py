from test_instance import generate_bays_data
from utils import*
from preprocessing import *
from plotting import plot_bays, plot_all_bays_with_moves
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_bays = generate_bays_data(file_name='../input/input_bays.xlsx')


α = 0.75
λ1 = 1
λ2 = 1
H = 4

def solve_all_bays(input_bays, α, λ1, λ2, H):
    all_moves = {}
    all_bays = {}

    # Loop over each bay in the dictionary
    for bay_num, bay in input_bays.items():
        print(f"SOLVE {bay_num} ***")
        moves, new_bay = local_search_heuristic(bay, α, λ1, λ2, H)
        
        # Store the moves and the new bay configuration in the dictionaries
        all_moves[bay_num] = moves
        all_bays[bay_num] = new_bay

    return all_moves, all_bays

# α, λ1, λ2, and H are parameters of your heuristic, replace them with their actual values

all_moves, all_bays = solve_all_bays(input_bays, α, λ1, λ2, H)

#plot_bays(input_bays,5,4, pdf_filename='../output/input_bays_plot.pdf')
#plot_bays(all_bays,5,4, pdf_filename='../output/output_bays_plot.pdf')

#export_to_excel(all_bays,file_name='../output/pre_processed_bays.xlsx')
#export_moves_to_excel(all_moves,file_name='../output/pre_processing_moves.xlsx')

#plot_all_bays_with_moves(input_bays,all_moves,pdf_filename='../output/pre_processing_moves_plot.pdf')
#plot_bays(all_bays,5,4, pdf_filename='output/pre_processed_bays_plot.pdf')



def main():
    
    pass

if __name__ == "__main__":
    main()
