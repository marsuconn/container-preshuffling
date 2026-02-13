from matplotlib import cm, patches, pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


def plot_bay_with_moves(bay, moves, max_stacks=5, max_tiers=4):
    """
    plot all moves in a bay
    """
    for idx, move in enumerate(moves):
        # Perform the move
        source_stack, target_stack = move
        source_container = bay[source_stack].pop()
        bay[target_stack].append(source_container)
        
        # Create a plot
        fig, ax = plt.subplots()

        # Color map setup
        unique_times = set(container[1] for stack in bay.values() for container in stack)
        colors = cm.rainbow(np.linspace(0, 1, len(unique_times)))

        for i in range(max_stacks):  # loop over max_stacks, not bay.items()
            stack_name = f'stack{i+1}'  # generate the stack_name 
            stack = bay.get(stack_name, [])  # use get() method to avoid KeyError
            bottom = 0
            for j, (container_id, container_time) in enumerate(stack):
                # Get color
                color_index = list(unique_times).index(container_time)
                color = colors[color_index]
                
                # Add hatch to the moved container
                hatch = 'x' if stack_name == target_stack and (container_id, container_time) == source_container else None

                ax.bar(i, 1, bottom=bottom, color=color, edgecolor='black', width=1, hatch=hatch)
                ax.text(i, bottom + 0.5, f"{container_id} ({container_time})", color='black', ha='center', va='center')
                bottom += 1

        # Marking source container (empty rectangle)
        rect = patches.Rectangle((list(bay.keys()).index(source_stack) - 0.5, len(bay[source_stack])), 1, 1,
                                 edgecolor='red', facecolor='red', fill=True, alpha=0.5, hatch='x')
        ax.add_patch(rect)
        ax.text(list(bay.keys()).index(source_stack), len(bay[source_stack]) + 0.5,
                f"{source_container[0]} ({source_container[1]})", color='black', ha='center', va='center')

        ax.set_xticks(np.arange(max_stacks))  # set xticks to max_stacks
        ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])  # set xticklabels accordingly

        ax.set_yticks(np.arange(max_tiers) + 0.5)  # set yticks to max_tiers
        ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])  # set yticklabels accordingly
        ax.set_xlim(left=-0.5,right=max_stacks-0.5)
        ax.set_ylim([0, max_tiers])

        plt.title(f'Move: {move[0]} to {move[1]}')
        plt.show()



def plot_all_bays_with_moves(all_bays, all_moves, pdf_filename='all_bays_with_moves.pdf', max_stacks=5, max_tiers=4):
    with PdfPages(pdf_filename) as pdf:
        for bay_num, moves in all_moves.items():
            bay = all_bays[bay_num]  # get the current state of the bay
            for idx, move in enumerate(moves):
                # Perform the move
                source_stack, target_stack = move
                source_container = bay[source_stack].pop()
                bay[target_stack].append(source_container)
                
                # Create a plot
                fig, ax = plt.subplots()

                # Color map setup
                unique_times = set(container[1] for stack in bay.values() for container in stack)
                colors = cm.rainbow(np.linspace(0, 1, len(unique_times)))

                for i in range(max_stacks):  # loop over max_stacks, not bay.items()
                    stack_name = f'stack{i+1}'  # generate the stack_name
                    stack = bay.get(stack_name, [])  # use get() method to avoid KeyError
                    bottom = 0
                    for j, (container_id, container_time) in enumerate(stack):
                        # Get color
                        color_index = list(unique_times).index(container_time)
                        color = colors[color_index]
                        
                        # Add hatch to the moved container
                        hatch = '//' if stack_name == target_stack and (container_id, container_time) == source_container else None

                        ax.bar(i, 1, bottom=bottom, color=color, edgecolor='black', width=1, hatch=hatch)
                        ax.text(i, bottom + 0.5, f"{container_id} ({container_time})", color='black', ha='center', va='center')
                        bottom += 1

                # Marking source container (empty rectangle)
                rect = patches.Rectangle((list(bay.keys()).index(source_stack) - 0.5, len(bay[source_stack])), 1, 1,
                                         edgecolor='magenta', facecolor='magenta', fill=True, alpha=0.5, hatch='//')
                ax.add_patch(rect)
                ax.text(list(bay.keys()).index(source_stack), len(bay[source_stack]) + 0.5,
                        f"{source_container[0]} ({source_container[1]})", color='black', ha='center', va='center')

                ax.set_xticks(np.arange(max_stacks))  # set xticks to max_stacks
                ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])  # set xticklabels accordingly

                ax.set_yticks(np.arange(max_tiers) + 0.5)  # set yticks to max_tiers
                ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])  # set yticklabels accordingly
                ax.set_xlim(left=-0.5,right=max_stacks-0.5)
                ax.set_ylim([0, max_tiers])

                plt.title(f'Bay: {bay_num} , Move: {move[0]} to {move[1]}')
                pdf.savefig(fig)  # save the current figure into the pdf file
                plt.close(fig)  # close the figure to free up memory

def plot_bay(bay, max_stacks=5, max_tiers=4):
    """
    plot a single bay
    """
    fig, ax = plt.subplots()

    
    # Determine the total number of unique time windows
    unique_times = set()
    for stack in bay.values():
        for container in stack:
            unique_times.add(container[1])
    num_unique_times = len(unique_times)

    # Generate a color for each unique time window
    colors = cm.rainbow(np.linspace(0, 1, num_unique_times))

    for i in range(max_stacks):  # loop over max_stacks, not bay.items()
        stack_name = f'stack{i+1}'  # generate the stack_name without the apostrophe
        stack = bay.get(stack_name, [])  # use get() method to avoid KeyError
        bottom = 0
        for j, (container_id, container_time) in enumerate(stack):
            color_index = list(unique_times).index(container_time)
            ax.bar(i, 1, bottom=bottom, color=colors[color_index], edgecolor='black', width=1)
            ax.text(i, bottom + 0.5, f"{container_id} ({container_time})", color='black', ha='center', va='center')
            bottom += 1

    ax.set_xticks(np.arange(max_stacks))  # set xticks to max_stacks
    ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])  # set xticklabels accordingly

    ax.set_yticks(np.arange(max_tiers) + 0.5)  # set yticks to max_tiers
    ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])  # set yticklabels accordingly

    plt.tick_params(
        axis='x',          
        which='both',      
        bottom=False,      
        top=False,        
        labelbottom=True)

    ax.set_xlim(left=-0.5, right=max_stacks-0.5)  # adjust right limit
    ax.set_ylim(top=max_tiers)  # adjust top limit

    plt.show()

def plot_bays(bays, max_stacks=5, max_tiers=4, pdf_filename='bays_plots.pdf'):
    # Determine the total number of unique time windows
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])
    num_unique_times = len(unique_times)

    # Generate a color for each unique time window
    colors = cm.rainbow(np.linspace(0, 1, num_unique_times))

    with PdfPages(pdf_filename) as pdf:
        for bay_num, bay in bays.items():
            fig, ax = plt.subplots()

            # Ensure that all stacks are displayed
            for i in range(max_stacks):
                stack_name = f'stack{i+1}'
                if stack_name not in bay:
                    bay[stack_name] = []  # initialize an empty list for the stack

            for i, (stack_name, stack) in enumerate(sorted(bay.items())):
                bottom = 0
                for j, (container_id, container_time) in enumerate(stack):
                    color_index = list(unique_times).index(container_time)
                    ax.bar(i, 1, bottom=bottom, color=colors[color_index], edgecolor='black', width=1)
                    ax.text(i, bottom + 0.5, f"{container_id} ({container_time})", color='black', ha='center', va='center')
                    bottom += 1

            ax.set_xticks(np.arange(max_stacks))  # there are 5 stacks
            ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])

            ax.set_yticks(np.arange(max_tiers) + 0.5)
            ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])

            plt.tick_params(
                axis='x',
                which='both',
                bottom=False,
                top=False,
                labelbottom=True)

            ax.set_xlim(left=-0.5, right=max_stacks-0.5)  # adjust right limit
            ax.set_ylim(top=max_tiers)  # adjust top limit
            plt.title(f'Container Location in Bay {bay_num}')

            pdf.savefig(fig)  # save the current figure into the pdf file
            plt.close()  # close the figure to free up memory
