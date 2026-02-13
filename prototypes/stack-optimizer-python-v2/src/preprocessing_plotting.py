from matplotlib import cm, patches, pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def plot_individual_bay(ax, bay, max_stacks, max_tiers):
    unique_times = set(container[1] for stack in bay.values() for container in stack)
    num_unique_times = len(unique_times)
    colors = cm.rainbow(np.linspace(0, 1, num_unique_times))

    for i, (stack_name, stack) in enumerate(sorted(bay.items())):
        bottom = 0
        for j, (container_id, container_time) in enumerate(stack):
            color_index = list(unique_times).index(container_time)
            ax.bar(i, 1, bottom=bottom, color=colors[color_index], edgecolor='black', width=1)
            ax.text(i, bottom + 0.5, f"{container_id} ({container_time})", color='black', ha='center', va='center')
            bottom += 1

    ax.set_xticks(np.arange(max_stacks))
    ax.set_xticklabels([f'{i+1}' for i in range(max_stacks)])

    ax.set_yticks(np.arange(max_tiers) + 0.5)
    ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])

    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=True)

    ax.set_xlim(left=-0.5, right=max_stacks - 0.5)
    ax.set_ylim(top=max_tiers)

def plot_all_bays_side_by_side(input_bays, final_bays, block_config, pdf_filename='bays_comparison.pdf'):
    figures = []  # store the figures in a list first
    
    for block_id, bays in input_bays.items():
        max_stacks = block_config[block_id]['max_stacks']
        max_tiers = block_config[block_id]['max_tiers']
        
        for bay_id, input_bay in bays.items():
            final_bay = final_bays[block_id][bay_id]
            
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
            
            plot_individual_bay(axs[0], input_bay, max_stacks, max_tiers)
            axs[0].set_title('Before Preprocessing')
            
            plot_individual_bay(axs[1], final_bay, max_stacks, max_tiers)
            axs[1].set_title('After Preprocessing')
            
            plt.suptitle(f'Block {block_id}, Bay {bay_id}', fontsize=16)
            
            plt.show()  
            
            figures.append(fig)
            plt.close(fig)

    with PdfPages(pdf_filename) as pdf:
        for fig in figures:
            pdf.savefig(fig)




def plot_bays_with_plotly(input_bays, final_bays):
    unique_times = set()
    for bay in list(input_bays.values())[0].values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])

    unique_times = sorted(list(unique_times))
    colors = ['red', 'green', 'blue', 'yellow', 'purple'][:len(unique_times)]  # Assign a color to each unique time

    for block_id, bays in input_bays.items():
        for bay_id, before_bay in bays.items():
            after_bay = final_bays[block_id][bay_id]
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Before", "After"))

            for i, bay in enumerate([before_bay, after_bay]):
                for stack_num, stack_content in enumerate(bay.values()):
                    y = 0
                    for container_id, container_time in stack_content:
                        fig.add_shape(
                            type="rect",
                            x0=stack_num + i*5, x1=stack_num + 1 + i*5,
                            y0=y, y1=y + 1,
                            line=dict(color="RoyalBlue"),
                            fillcolor=colors[unique_times.index(container_time)],
                            row=1, col=i+1
                        )
                        fig.add_annotation(
                            text=f"{container_id} ({container_time})",
                            xref="x", yref="y",
                            x=stack_num + 0.5 + i*5, y=y + 0.5,
                            showarrow=False,
                            font_size=8,
                            row=1, col=i+1
                        )
                        y += 1

            fig.update_xaxes(range=[-1, 10])
            fig.update_yaxes(range=[0, 5])

            title = f"Block {block_id}, Bay {bay_id}"
            fig.update_layout(height=400, width=800, title_text=title)

            # Saving each bay configuration as a separate HTML file
            file_name = f"block_{block_id}_bay_{bay_id}.html"
            fig.write_html(file_name)

'''
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
        #draw_rtg_crane(ax, list(bay.keys()).index(target_stack), len(bay[target_stack]))

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


def plot_all_bays_with_moves_1(all_bays, all_moves, pdf_filename='all_bays_with_moves.pdf', max_stacks=5, max_tiers=4):
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
                #draw_rtg_crane(ax, list(bay.keys()).index(target_stack), len(bay[target_stack]))

                ax.set_xticks(np.arange(max_stacks))  # set xticks to max_stacks
                ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])  # set xticklabels accordingly

                ax.set_yticks(np.arange(max_tiers) + 0.5)  # set yticks to max_tiers
                ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])  # set yticklabels accordingly
                ax.set_xlim(left=-0.5,right=max_stacks-0.5)
                ax.set_ylim([0, max_tiers])

                plt.title(f'Bay: {bay_num} , Move: {move[0]} to {move[1]}')
                pdf.savefig(fig)  # save the current figure into the pdf file
                plt.close(fig)  # close the figure to free up memory



import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import cm
import matplotlib.patches as patches

def plot_all_bays_with_moves(all_bays, all_moves, pdf_filename='all_bays_with_moves.pdf', max_stacks=5, max_tiers=4):
    container_width=8
    container_height=8.5
    container_height = container_height/container_width  # Adjusted for the aspect ratio

    with PdfPages(pdf_filename) as pdf:
        for bay_num, moves in all_moves.items():
            bay = all_bays[bay_num]
            for idx, move in enumerate(moves):
                source_stack, target_stack = move
                if bay[source_stack]:
                    source_container = bay[source_stack].pop()
                    bay[target_stack].append(source_container)
                else:
                    print(f"Warning: Attempted to pop from an empty stack '{source_stack}' in bay!")
                    continue

                source_container = bay[source_stack].pop()
                bay[target_stack].append(source_container)

                fig, ax = plt.subplots()

                unique_times = set(container[1] for stack in bay.values() for container in stack)
                colors = cm.rainbow(np.linspace(0, 1, len(unique_times)))

                for i in range(max_stacks):
                    stack_name = f'stack{i+1}'
                    stack = bay.get(stack_name, [])
                    bottom = 0
                    for j, (container_id, container_time) in enumerate(stack):
                        color_index = list(unique_times).index(container_time)
                        color = colors[color_index]

                        hatch = '//' if stack_name == target_stack and (container_id, container_time) == source_container else None

                        ax.bar(i, container_height, bottom=bottom, color=color, edgecolor='black', width=1, hatch=hatch)
                        ax.text(i, bottom + 0.5 * container_height, f"{container_id} ({container_time})", color='black', ha='center', va='center')
                        bottom += container_height

                rect = patches.Rectangle((list(bay.keys()).index(source_stack) - 0.5, len(bay[source_stack]) * container_height), 1, container_height,
                                         edgecolor='magenta', facecolor='magenta', fill=True, alpha=0.5, hatch='//')
                ax.add_patch(rect)
                ax.text(list(bay.keys()).index(source_stack), (len(bay[source_stack]) + 0.5) * container_height,
                        f"{source_container[0]} ({source_container[1]})", color='black', ha='center', va='center')

                ax.set_xticks(np.arange(max_stacks))
                ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])

                ax.set_yticks(np.arange(max_tiers) * container_height + 0.5 * container_height)
                ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])
                ax.set_xlim(left=-0.5, right=max_stacks-0.5)
                ax.set_ylim([0, max_tiers * container_height])

                plt.title(f'Bay: {bay_num} , Move: {move[0]} to {move[1]}')
                pdf.savefig(fig)
                plt.close(fig)

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


def plot_bays_1(bays, max_stacks=5, max_tiers=4, pdf_filename='bays_plots.pdf'):
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
import matplotlib.cm as cm

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

    # Adjust the aspect ratio based on container size
    container_width = 8  # feet
    container_height = 8.5  # feet
    aspect_ratio = container_height / container_width

    with PdfPages(pdf_filename) as pdf:
        for bay_num, bay in bays.items():
            fig, ax = plt.subplots(figsize=(max_stacks * container_width / 10, max_tiers * container_height / 10))  # Dividing by 10 for aesthetics
            
            # Ensure that all stacks are displayed
            for i in range(max_stacks):
                stack_name = f'stack{i+1}'
                if stack_name not in bay:
                    bay[stack_name] = []  # initialize an empty list for the stack

            for i, (stack_name, stack) in enumerate(sorted(bay.items())):
                bottom = 0
                for j, (container_id, container_time) in enumerate(stack):
                    color_index = list(unique_times).index(container_time)
                    ax.bar(i, aspect_ratio, bottom=bottom, color=colors[color_index], edgecolor='black', width=1)
                    ax.text(i, bottom + 0.5*aspect_ratio, f"{container_id} ({container_time})", color='black', ha='center', va='center')
                    bottom += aspect_ratio

            ax.set_xticks(np.arange(max_stacks))  # there are 5 stacks
            ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])

            ax.set_yticks(np.arange(0, max_tiers * aspect_ratio, aspect_ratio) + 0.5 * aspect_ratio)
            ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])

            plt.tick_params(
                axis='x',
                which='both',
                bottom=False,
                top=False,
                labelbottom=True)

            ax.set_xlim(left=-0.5, right=max_stacks-0.5)  # adjust right limit
            ax.set_ylim(top=max_tiers*aspect_ratio)  # adjust top limit
            plt.title(f'Container Location in Bay {bay_num}')

            pdf.savefig(fig)  # save the current figure into the pdf file
            plt.close()  # close the figure to free up memory

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
    }}


all_bays=   {1: {'stack1': [('C13', 2), ('C11', 2), ('C1', 1)],
  'stack2': [('C10', 2), ('C5', 1)],
  'stack3': [('C8', 2), ('C3', 1), ('C2', 1)],
  'stack4': [('C9', 2), ('C7', 1)],
  'stack5': [('C12', 2), ('C6', 1), ('C4', 1)]},
 2: {'stack1': [('C14', 2),
   ('C15', 2),
   ('C17', 2),
   ('C16', 2),
   ('C22', 2),
   ('C23', 2),
   ('C20', 1)],
  'stack2': [('C21', 1)],
  'stack3': [('C25', 1), ('C24', 2), ('C19', 1), ('C18', 1)],
  'stack4': [('C26', 1), ('C27', 2), ('C28', 3), ('C29', 4)],
  'stack5': [('C32', 3), ('C31', 3), ('C30', 3), ('C33', 4)]},
 3: {'stack1': [('C38', 1)],
  'stack2': [('C35', 1)],
  'stack3': [('C34', 1)],
  'stack4': [('C37', 1)],
  'stack5': [('C36', 1)]},
 4: {'stack1': [('C49', 2), ('C40', 1)],
  'stack2': [('C47', 1), ('C48', 1), ('C41', 1), ('C42', 1)],
  'stack3': [('C39', 1)],
  'stack4': [('C50', 2), ('C46', 1), ('C44', 1), ('C43', 1)],
  'stack5': [('C45', 1)]}}

plot_bays(all_bays)


import matplotlib.pyplot as plt
import numpy as np

def plot_bays_3d(bays, output_filename='3D-plots-output-bay.png', max_stacks=5, max_tiers=4):
    # Determine the total number of unique time windows
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])
    num_unique_times = len(unique_times)

    # Use a more visually appealing color palette
    colors = plt.cm.viridis(np.linspace(0, 1, num_unique_times))

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    bay_gap=0.02
    stack_gap=0.02

    for bay_num, (bay_name, bay) in enumerate(bays.items()):
        for i, (stack_name, stack) in enumerate(sorted(bay.items())):
            z_position = 0
            for j, (container_id, container_time) in enumerate(stack):
                color_index = list(unique_times).index(container_time)
                ax.bar3d(bay_num+bay_gap*bay_num, i+stack_gap*i, z_position, 1, 1, 1, color=colors[color_index], shade=True, linewidth=0.5, edgecolor='black')
                ax.text(bay_num + 0.5 + bay_gap * bay_num, i + 0.5 + stack_gap * i, z_position + 0.5, f"{container_id}\n({container_time})", color='black', ha='center', va='center', fontsize=8)
                z_position += 1

    ax.set_xticks(np.arange(len(bays)) + 0.5)
    ax.set_xticklabels(list(bays.keys()), fontsize=10)
    
    ax.set_yticks(np.arange(max_stacks) + 0.5)
    ax.set_yticklabels([f'stack{i+1}' for i in range(max_stacks)], fontsize=10)
    
    ax.set_zticks(np.arange(max_tiers) + 0.5)
    ax.set_zticklabels([f'Tier {i+1}' for i in range(max_tiers)], fontsize=10)

    ax.set_xlabel('Bays', fontsize=12, labelpad=10)
    ax.set_ylabel('Stacks', fontsize=12, labelpad=10)
    ax.set_zlabel('Tiers', fontsize=12, labelpad=10)

    # Adjust perspective for better visibility
    ax.view_init(elev=20, azim=-35)

    # Remove the background grid
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(False)

    plt.tight_layout()
    plt.savefig(output_filename)  # Save the figure using the specified filename
    plt.show()

# Example usage:
# plot_bays_3d(your_bays_data, 'custom_output_filename.png')



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




def plot_all_bays_with_moves_for_blocks(all_results, max_stacks, max_tiers, base_pdf_filename='all_bays_with_moves'):
    for block_id, result in all_results.items():
        input_bays = result['bays']
        all_moves = result['moves']
        pdf_filename = f"{base_pdf_filename}_block{block_id}.pdf"
        plot_all_bays_with_moves(input_bays, all_moves, pdf_filename, max_stacks, max_tiers)


def plot_bays_for_blocks(results, data_blocks, base_pdf_filename='bays_plots'):
    for block_id, block_data in results.items():
        max_stacks = data_blocks[data_blocks['block_id'] == block_id]['stacks_per_bay'].values[0]
        max_tiers = data_blocks[data_blocks['block_id'] == block_id]['tiers_per_bay'].values[0]
        plot_bays(block_data['all_bays'], max_stacks, max_tiers, pdf_filename=f"{base_pdf_filename}_block_{block_id}.pdf")



def generate_plots(bays, max_stacks=5, max_tiers=4):
    plots = []
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])

    num_unique_times = len(unique_times)
    colors = cm.rainbow(np.linspace(0, 1, num_unique_times))
    container_width = 8
    container_height = 8.5
    aspect_ratio = container_height / container_width

    for bay_num, bay in bays.items():
        fig, ax = plt.subplots(figsize=(max_stacks * container_width / 10, max_tiers * container_height / 10))
        for i in range(max_stacks):
            stack_name = f'stack{i+1}'
            if stack_name not in bay:
                bay[stack_name] = []

        for i, (stack_name, stack) in enumerate(sorted(bay.items())):
            bottom = 0
            for j, (container_id, container_time) in enumerate(stack):
                color_index = list(unique_times).index(container_time)
                ax.bar(i, aspect_ratio, bottom=bottom, color=colors[color_index], edgecolor='black', width=1)
                ax.text(i, bottom + 0.5*aspect_ratio, f"{container_id} ({container_time})", color='black', ha='center', va='center')
                bottom += aspect_ratio

        ax.set_xticks(np.arange(max_stacks))
        ax.set_xticklabels([f'stack{i+1}' for i in range(max_stacks)])
        ax.set_yticks(np.arange(0, max_tiers * aspect_ratio, aspect_ratio) + 0.5 * aspect_ratio)
        ax.set_yticklabels([f'Tier {i+1}' for i in range(max_tiers)])
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
        ax.set_xlim(left=-0.5, right=max_stacks - 0.5)
        ax.set_ylim(top=max_tiers * aspect_ratio)
        plt.title(f'Container Location in Bay {bay_num}')

        plots.append(fig)
        plt.close(fig)
    return plots

# Save all plots to a PDF
def save_plots_to_pdf(plots, filename):
    with PdfPages(filename) as pdf:
        for plot in plots:
            pdf.savefig(plot)


import matplotlib.pyplot as plt
import numpy as np

def compare_bays_side_by_side(*bays, title='Bay Comparison', cmap='viridis', show=True):
    n = len(bays)  # Number of bays to compare

    if n == 0:  # If no bays are provided, just return
        print("No bays provided for comparison.")
        return

    # Determine the number of stacks and tiers from the first bay
    # Assume all bays have the same structure
    num_stacks = len(bays[0])
    num_tiers = max(len(stack) for stack in bays[0].values())

    fig, axes = plt.subplots(1, n, figsize=(5*n, 5), sharey=True)
    if n == 1:
        axes = [axes]  # Make sure axes is a list even if there’s only one subplot

    for i, bay in enumerate(bays):
        ax = axes[i]
        ax.set_title(f'Bay {i+1}')

        for j, (stack, containers) in enumerate(bay.items()):
            containers = sorted(containers, key=lambda x: x[1])  # Sort containers by the second element of the tuple
            container_ids, container_values = zip(*containers)

            y = np.arange(len(container_values))
            x = np.full_like(y, fill_value=j)  # X coordinate is based on the stack index

            scatter = ax.scatter(x, y, c=container_values, cmap=cmap, s=500)

        ax.set_xticks(range(num_stacks))
        ax.set_xticklabels(bay.keys())
        ax.set_xlabel('Stacks')
        ax.set_yticks(range(num_tiers))
        ax.set_yticklabels(range(1, num_tiers+1))
        ax.set_ylabel('Tiers')

    fig.suptitle(title)
    fig.colorbar(scatter, ax=axes, orientation='horizontal', fraction=0.02, pad=0.1)

    if show:
        plt.show()

# Example usage
# This is assuming bay1, bay2 are dictionaries containing your bay data
# compare_bays_side_by_side(bay1, bay2, title='Bay Comparison Example')
initial_bay: {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 2)],
        'stack2': [('d1', 3)],
        'stack3': [('e1', 2)],
        'stack4': [('f1', 1), ('f2', 3)],
        'stack5': [('g1', 4), ('g2', 1), ('g3', 2)]}

updated_bay: {
        'stack1': [('d1', 3), ('c2', 4), ('c3', 2)],
        'stack2': [('c1', 1)],
        'stack3': [('e1', 2)],
        'stack4': [('f1', 1), ('f2', 3)],
        'stack5': [('g1', 4), ('g2', 1), ('g3', 2)]}

'''
