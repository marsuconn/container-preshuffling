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
    
    for container_location_block, bays in input_bays.items():
        max_stacks = block_config[container_location_block]['max_stacks']
        max_tiers = block_config[container_location_block]['max_tiers']
        
        for bay_id, input_bay in bays.items():
            final_bay = final_bays[container_location_block][bay_id]
            
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
            
            plot_individual_bay(axs[0], input_bay, max_stacks, max_tiers)
            axs[0].set_title('Before Preprocessing')
            
            plot_individual_bay(axs[1], final_bay, max_stacks, max_tiers)
            axs[1].set_title('After Preprocessing')
            
            plt.suptitle(f'Block {container_location_block}, Bay {bay_id}', fontsize=16)
            
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

    for container_location_block, bays in input_bays.items():
        for bay_id, before_bay in bays.items():
            after_bay = final_bays[container_location_block][bay_id]
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

            title = f"Block {container_location_block}, Bay {bay_id}"
            fig.update_layout(height=400, width=800, title_text=title)

            # Saving each bay configuration as a separate HTML file
            file_name = f"block_{container_location_block}_bay_{bay_id}.html"
            fig.write_html(file_name)


