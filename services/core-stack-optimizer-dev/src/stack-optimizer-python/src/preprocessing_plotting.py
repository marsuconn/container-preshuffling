from matplotlib import cm, patches, pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
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
'''
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

plot_bays(bays)
'''



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


'''
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

'''



import plotly.graph_objects as go
import numpy as np
import plotly.express as px


def plotly_bays(bays, max_stacks=5, max_tiers=4):
    # Determine the total number of unique time windows
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])
    num_unique_times = len(unique_times)

    # Generate a color for each unique time window
    colors = px.colors.sequential.Rainbow * num_unique_times
    
    fig = go.Figure()
    
    for bay_num, bay in bays.items():
        # Ensure that all stacks are displayed
        for i in range(max_stacks):
            stack_name = f'stack{i+1}'
            if stack_name not in bay:
                bay[stack_name] = []  # initialize an empty list for the stack

        for i, (stack_name, stack) in enumerate(sorted(bay.items())):
            bottom = 0
            for j, (container_id, container_time) in enumerate(stack):
                color_index = list(unique_times).index(container_time)
                fig.add_shape(type="rect",
                              x0=i, y0=bottom, x1=i+1, y1=bottom+1,
                              fillcolor=colors[color_index],
                              line=dict(color="black", width=1)
                             )
                fig.add_annotation(
                    x=i + 0.5, y=bottom + 0.5,
                    text=f"{container_id} ({container_time})",
                    showarrow=False,
                    font=dict(color="black")
                )
                bottom += 1

    fig.update_xaxes(
        tickvals=list(range(max_stacks)),
        ticktext=[f'stack{i+1}' for i in range(max_stacks)],
        tickangle=-45
    )

    fig.update_yaxes(
        tickvals=list(range(max_tiers)),
        ticktext=[f'Tier {i+1}' for i in range(max_tiers)]
    )

    fig.update_layout(
        title_text="Container Location in Bays",
        xaxis=dict(title='Stacks', range=[-0.5, max_stacks-0.5]),
        yaxis=dict(title='Tiers', range=[0, max_tiers]),
        autosize=False,
        width=800,
        height=500,
        showlegend=False
    )

    fig.show()





import plotly.graph_objects as go

def plot_bays_3d_with_plotly(bays, max_stacks=5, max_tiers=4):
    # Determine the total number of unique time windows
    unique_times = set()
    for bay in bays.values():
        for stack in bay.values():
            for container in stack:
                unique_times.add(container[1])

    unique_times = sorted(list(unique_times))
    colors = ['blue', 'red', 'green']  # Add more colors if needed

    # Initialize figure
    fig = go.Figure()

    bay_gap = 0.02
    stack_gap = 0.02

    for bay_num, (bay_name, bay) in enumerate(bays.items()):
        for stack_index, (stack_name, stack) in enumerate(sorted(bay.items())):
            z_position = 0
            for j, (container_id, container_time) in enumerate(stack):
                color_index = unique_times.index(container_time)
                color = colors[color_index]

                # Define the 8 vertices of the rectangular box
                x = [bay_num, bay_num, bay_num+1, bay_num+1, bay_num, bay_num, bay_num+1, bay_num+1]
                y = [stack_index, stack_index+1, stack_index+1, stack_index, stack_index, stack_index+1, stack_index+1, stack_index]
                z = [z_position, z_position, z_position, z_position, z_position+1, z_position+1, z_position+1, z_position+1]

                # Define the 12 triangles composing the plot
                i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
                j = [3, 4, 1, 7, 5, 6, 5, 2, 0, 1, 6, 3]
                k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 2, 7]

                fig.add_trace(go.Mesh3d(x=x, y=y, z=z, color=color, opacity=1.0, i=i, j=j, k=k))
                z_position += 1

    fig.update_layout(scene=dict(
                        xaxis=dict(nticks=len(bays), tickvals=list(range(len(bays))),
                                   ticktext=list(bays.keys())),
                        yaxis=dict(nticks=max_stacks, tickvals=list(range(max_stacks)),
                                   ticktext=[f'stack{i+1}' for i in range(max_stacks)]),
                        zaxis=dict(nticks=max_tiers, tickvals=list(range(max_tiers)),
                                   ticktext=[f'Tier {i+1}' for i in range(max_tiers)])
                       ))
    fig.show()

# Sample data
#bays = {
##    'Bay1': {'Stack1': [('A', '1'), ('B', '2')], 'Stack2': [('C', '2')]},
#    'Bay2': {'Stack1': [('D', '1')], 'Stack2': [('E', '3'), ('F', '3')]}
#}

# Call function
#plot_bays_3d_with_plotly(bays)






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