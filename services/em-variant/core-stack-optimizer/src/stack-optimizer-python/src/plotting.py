from matplotlib import cm, patches, pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
#import seaborn as sns


def draw_rtg_crane(ax, stack_index, tier_position):
    """Draw an RTG crane and its trolley on the given axes."""
    crane_height = 1  # height of the crane from the top of the highest tier
    crane_width = 1.5  # width of the RTG crane (horizontal part)
    trolley_width = 0.4  # width of the trolley
    max_tiers = 4

    ax.plot(stack_index, tier_position + 1.5, 'ko', markersize=10)  # crane's trolley
    ax.plot([stack_index, stack_index], [tier_position + 1, tier_position + 2], 'k-', linewidth=2)  # trolley's cable

    # Drawing the main body (horizontal part) of the crane
    ax.plot([stack_index - crane_width / 2, stack_index + crane_width / 2],
            [max_tiers + crane_height] * 2, color='k', linewidth=3)

    # Drawing the trolley
    ax.plot([stack_index - trolley_width / 2, stack_index + trolley_width / 2],
            [tier_position, tier_position], color='r', linewidth=2)

    # Drawing the lines that hang the trolley from the crane
    ax.plot([stack_index, stack_index],
            [tier_position, max_tiers + crane_height], color='k', linestyle='--')




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
        # Drawing the RTG crane
        draw_rtg_crane(ax, list(bay.keys()).index(target_stack), len(bay[target_stack]))

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
        #ax.set_ylim([0, max_tiers])
        ax.set_ylim([0, max_tiers + 1])  

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
                # Drawing the RTG crane
                draw_rtg_crane(ax, list(bay.keys()).index(target_stack), len(bay[target_stack]))

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


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot_bays_3d(bays, max_stacks=5, max_tiers=4, pdf_filename='bays_plots_3d.pdf'):
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
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Ensure that all stacks are displayed
            for i in range(max_stacks):
                stack_name = f'stack{i+1}'
                if stack_name not in bay:
                    bay[stack_name] = []  # initialize an empty list for the stack

            for i, (stack_name, stack) in enumerate(sorted(bay.items())):
                bottom = 0
                for j, (container_id, container_time) in enumerate(stack):
                    color_index = list(unique_times).index(container_time)
                    ax.bar3d(i, bottom, 0, 0.8, 1, 0.8, color=colors[color_index], shade=True)
                    ax.text(i, bottom + 0.5, 0, f"{container_id}\n({container_time})", color='black', ha='center', va='center')
                    bottom += 1

            ax.set_xticks(np.arange(max_stacks))
            ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])

            ax.set_yticks(np.arange(max_tiers) + 0.5)
            ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])

            ax.set_zticks([])

            ax.set_xlabel('Stacks')
            ax.set_ylabel('Tiers')
            ax.set_title(f'Container Location in Bay {bay_num}')

            pdf.savefig(fig)  # save the current figure into the pdf file
            plt.close()  # close the figure to free up memory


bays = {
    'Bay 1': {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 2)],
        'stack2': [('c4', 3)],
        'stack3': [('c5', 3), ('c6', 2)],
        'stack4': [('c7', 1)],
        'stack5': []
    },
    'Bay 2': {
        'stack1': [('c8', 1), ('c9', 3)],
        'stack2': [('c10', 2)],
        'stack3': [('c11', 1), ('c12', 4)],
        'stack4': [('c13', 1), ('c14', 3)],
        'stack5': [('c15', 2)]
    }
}
plot_bays_3d(bays)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot_bays_3d(bays, max_stacks=5, max_tiers=4, pdf_filename='bays_plots_3d.pdf'):
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
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Ensure that all stacks are displayed
            for i in range(max_stacks):
                stack_name = f'stack{i+1}'
                if stack_name not in bay:
                    bay[stack_name] = []  # initialize an empty list for the stack

            for i, (stack_name, stack) in enumerate(sorted(bay.items())):
                bottom = 0
                for j, (container_id, container_time) in enumerate(stack):
                    color_index = list(unique_times).index(container_time)
                    ax.bar3d(i, bottom, 0, 0.8, 1, 0.8, color=colors[color_index], shade=True)
                    ax.text(i, bottom + 0.5, 0, f"{container_id}\n({container_time})", color='black', ha='center', va='center')
                    bottom += 1

            ax.set_xticks(np.arange(max_stacks))
            ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])

            ax.set_yticks(np.arange(max_tiers) + 0.5)
            ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])

            ax.set_zticks([])

            ax.set_xlabel('Stacks')
            ax.set_ylabel('Tiers')
            ax.set_title(f'Container Location in Bay {bay_num}')

            pdf.savefig(fig)  # save the current figure into the pdf file
            plt.close()  # close the figure to free up memory

# Test the function
bays = {
    'Bay 1': {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 2)],
        'stack2': [('d1', 3)],
        'stack3': [('e1', 2)],
        'stack4': [('f1', 1), ('f2', 3)],
        'stack5': [('g1', 4), ('g2', 1), ('g3', 2)]
    }
}
plot_bays_3d(bays)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot_bays_3d(bays, max_stacks=5, max_tiers=4):
    # Determine the total number of unique time windows
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])
    num_unique_times = len(unique_times)

    # Generate a color for each unique time window
    colors = cm.rainbow(np.linspace(0, 1, num_unique_times))
    
    for bay_num, bay in bays.items():
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Ensure that all stacks are displayed
        for i in range(max_stacks):
            stack_name = f'stack{i+1}'
            if stack_name not in bay:
                bay[stack_name] = []  # initialize an empty list for the stack

        for i, (stack_name, stack) in enumerate(sorted(bay.items())):
            z_position = 0
            for j, (container_id, container_time) in enumerate(stack):
                color_index = list(unique_times).index(container_time)
                ax.bar3d(i, 0, z_position, 0.8, 0.8, 1, color=colors[color_index], shade=True)
                ax.text(i, 0, z_position + 0.5, f"{container_id}\n({container_time})", color='black', ha='center', va='center')
                z_position += 1

        ax.set_xticks(np.arange(max_stacks))
        ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])
        
        ax.set_yticks([])
        
        ax.set_zticks(np.arange(max_tiers) + 0.5)
        ax.set_zticklabels([f'Tier {i+1}' for i in range(max_tiers)])

        ax.set_xlabel('Stacks')
        ax.set_zlabel('Tiers')
        ax.set_title(f'Container Location in Bay {bay_num}')

        plt.show()  # Show the plot interactively

# Test the function
bays = {
    'Bay 1': {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 2)],
        'stack2': [('c4', 3)],
        'stack3': [('c5', 3), ('c6', 2)],
        'stack4': [('c7', 1)],
        'stack5': []
    },
    'Bay 2': {
        'stack1': [('c8', 1), ('c9', 3)],
        'stack2': [('c10', 2)],
        'stack3': [('c11', 1), ('c12', 4)],
        'stack4': [('c13', 1), ('c14', 3)],
        'stack5': [('c15', 2)]
    }
}
plot_bays_3d(bays)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')

def plot_bays_3d(bays, max_stacks=5, max_tiers=4):
    # Determine the total number of unique time windows
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])
    num_unique_times = len(unique_times)

    # Generate a color for each unique time window
    colors = cm.rainbow(np.linspace(0, 1, num_unique_times))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    width = 0.75
    depth = 0.75

    for bay_num, (bay_name, bay) in enumerate(bays.items()):

        # Ensure that all stacks are displayed
        for i in range(max_stacks):
            stack_name = f'stack{i+1}'
            if stack_name not in bay:
                bay[stack_name] = []  # initialize an empty list for the stack

        for i, (stack_name, stack) in enumerate(sorted(bay.items())):
            z_position = 0
            for j, (container_id, container_time) in enumerate(stack):
                color_index = list(unique_times).index(container_time)
                ax.bar3d(bay_num + (1-width)/10, i + (1-depth)/, z_position, width, depth, 1, color=colors[color_index], shade=True, linewidth=0.25, edgecolor='black')  # Adjust width, depth, and edgecolor here
                ax.text(bay_num + 0.5, i + 0.5, z_position + 0.5, f"{container_id}\n({container_time})", color='black', ha='center', va='center')
                z_position += 1

    ax.set_xticks(np.arange(len(bays)) + 0.5)
    ax.set_xticklabels(list(bays.keys()))
    
    ax.set_yticks(np.arange(max_stacks) + 0.5)
    ax.set_yticklabels([f'stack{i+1}' for i in range(max_stacks)])
    
    ax.set_zticks(np.arange(max_tiers) + 0.5)
    ax.set_zticklabels([f'Tier {i+1}' for i in range(max_tiers)])

    ax.set_xlabel('Bays')
    ax.set_ylabel('Stacks')
    ax.set_zlabel('Tiers')

    plt.show()  # Show the plot interactively

# Test the function
bays = {
    'Bay 1': {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 2)],
        'stack2': [('d1', 3)],
        'stack3': [('e1', 2)],
        'stack4': [('f1', 1), ('f2', 3)],
        'stack5': [('g1', 4), ('g2', 1), ('g3', 2)]
    },
    'Bay 2': {
        'stack1': [('h1', 1)],
        'stack2': [('i1', 2), ('i2', 3)],
        'stack3': [('j1', 4)],
        'stack4': [('k1', 1)],
        'stack5': [('l1', 4)]
    }
}

plot_bays_3d(bays)



import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot_bays_3d(bays, max_stacks=5, max_tiers=4):
    # Determine the total number of unique time windows
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])
    num_unique_times = len(unique_times)

    # Generate a color for each unique time window
    colors = cm.rainbow(np.linspace(0, 1, num_unique_times))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    bay_gap = 0.02
    stack_gap=0.03
    for bay_num, (bay_name, bay) in enumerate(bays.items()):

        # Ensure that all stacks are displayed
        for i in range(max_stacks):
            stack_name = f'stack{i+1}'
            if stack_name not in bay:
                bay[stack_name] = []  # initialize an empty list for the stack

        for i, (stack_name, stack) in enumerate(sorted(bay.items())):
            z_position = 0
            for j, (container_id, container_time) in enumerate(stack):
                color_index = list(unique_times).index(container_time)
                ax.bar3d(bay_num+bay_gap*bay_num, i+stack_gap*i, z_position, 1, 1, 1, color=colors[color_index], shade=True,linewidth=0.5, edgecolor='black')  # Adjust the width and depth here
                ax.text(bay_num + 0.5, i + 0.5, z_position + 0.5, f"{container_id}\n({container_time})", color='black', ha='center', va='center')
                z_position += 1

    ax.set_xticks(np.arange(len(bays)) + 0.5)
    ax.set_xticklabels(list(bays.keys()))
    
    ax.set_yticks(np.arange(max_stacks) + 0.5)
    ax.set_yticklabels([f'stack{i+1}' for i in range(max_stacks)])
    
    ax.set_zticks(np.arange(max_tiers) + 0.5)
    ax.set_zticklabels([f'Tier {i+1}' for i in range(max_tiers)])

    ax.set_xlabel('Bays')
    ax.set_ylabel('Stacks')
    ax.set_zlabel('Tiers')

    plt.show()  # Show the plot interactively

# Test the function
bays = {
    'Bay 1': {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 2)],
        'stack2': [('d1', 3)],
        'stack3': [('e1', 2)],
        'stack4': [('f1', 1), ('f2', 3)],
        'stack5': [('g1', 4), ('g2', 1), ('g3', 2)]
    },
    'Bay 2': {
        'stack1': [('h1', 1)],
        'stack2': [('i1', 2), ('i2', 3)],
        'stack3': [('j1', 4)],
        'stack4': [('k1', 1)],
        'stack5': [('l1', 4)]
    }
}

plot_bays_3d(bays)
