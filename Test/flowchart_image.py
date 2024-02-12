import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_flowchart():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    # Draw boxes and arrows
    ax.add_patch(patches.Rectangle((2, 5), 2, 1, fill=None, edgecolor='black'))
    ax.add_patch(patches.Arrow(4, 5.5, 0, -1, width=0.1, edgecolor='black'))
    ax.add_patch(patches.Rectangle((2, 3), 2, 1, fill=None, edgecolor='black'))
    ax.add_patch(patches.Arrow(4, 3.5, 0, -1, width=0.1, edgecolor='black'))

    # Add text
    ax.text(3, 5.5, "(Condition)", ha='center', va='center')
    ax.text(3, 4, "YES", ha='center', va='center')
    ax.text(3, 3.5, "NO", ha='center', va='center')

    ax.text(3, 3, "(Exploration)", ha='center', va='center')
    ax.text(3, 2.5, "(Exploitation)", ha='center', va='center')

    ax.text(3, 2, "Randomly choose an action", ha='center', va='center')
    ax.text(3, 1.5, "Choose the action with the highest estimated value", ha='center', va='center')

    ax.axis('off')
    plt.savefig('flowchart.png')
    plt.show()

draw_flowchart()
