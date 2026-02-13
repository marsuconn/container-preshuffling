import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

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
    plt.savefig(output_filename)  
    plt.show()


bays = {
    'Bay1': {
        'stack1': [('c1', 1), ('c2', 4), ('c3', 4)],
        'stack2': [('d1', 3),('c3', 2),('c3', 4)],
        'stack3': [('e1', 2),('c3', 2)],
        'stack4': [('f1', 1), ('f2', 3)],
        'stack5': [('g1', 4), ('g2', 1), ('g3', 4)]
    },
    'Bay2': {
        'stack1': [('h1', 1),('i2', 3)],
        'stack2': [('i1', 2),('i2', 3) ],
        'stack3': [('j1', 4),('i2', 3)],
        'stack4': [('k1', 1),('i2', 3)],
        'stack5': [('l1', 4),('i2', 3)]
    },
    'Bay3': {
        'stack1': [('h1', 1)],
        'stack2': [('i1', 2), ('i2', 4)],
        'stack3': [('j1', 4),('i2', 1)],
        'stack4': [('k1', 1),('i2', 1)],
        'stack5': [('l1', 4)]
    },
    'Bay4': {
        'stack1': [('h1', 1)],
        'stack2': [('i1', 2), ('i2', 3)],
        'stack3': [('j1', 4)],
        'stack4': [('k1', 1)],
        'stack5': [('l1', 4)]
    },
    'Bay5': {
        'stack1': [('h1', 1)],
        'stack2': [('i1', 2), ('i2', 3)],
        'stack3': [('j1', 4),('i2', 3)],
        'stack4': [('k1', 1),('i2', 3)],
        'stack5': [('l1', 4),('i2', 3)]
    },
    'Bay6': {
        'stack1': [('h1', 1),('g2', 1), ('g3', 4)],
        'stack2': [('i1', 2), ('i2', 1),('i2', 1)],
        'stack3': [('j1', 4),('g2', 2), ('g3', 4)],
        'stack4': [('k1', 1),('g2', 4), ('g3', 1)],
        'stack5': [('l1', 4),('g2', 1), ('g3', 1)]
    },
    'Bay7': {
        'stack1': [('h1', 1),('g2', 1), ('g3', 2)],
        'stack2': [('i1', 2), ('i2', 1),('i2', 3)],
        'stack3': [('j1', 4),('g2', 1), ('g3', 3)],
        'stack4': [('k1', 1),('g2', 5), ('g3', 4)],
        'stack5': [('l1', 4),('g2', 1), ('g3', 3)]
    },
    'Bay8': {
        'stack1': [('h1', 1),('g2', 1), ('g3', 2)],
        'stack2': [('i1', 2), ('i2', 1),('i2', 1)],
        'stack3': [('j1', 4),('g2', 2), ('g3', 1)],
        'stack4': [('k1', 1),('g2', 4), ('g3', 1)],
        'stack5': [('l1', 4),('g2', 1), ('g3', 3)]
    }
     
}

plot_bays_3d(bays)



