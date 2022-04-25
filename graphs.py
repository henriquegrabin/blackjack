import matplotlib.pyplot as plt
import numpy as np

def plot_count(count: np.array):
    # Count
    fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(nrows= 2, ncols= 2, figsize = (9,9))

    def formatter(number: int) -> str:
        if number > 1_000_000:
            return str(round(number / 1_000_000, 1)) + 'm'
        elif number > 1_000:
            return str(round(number / 1_000, 1)) + 'k'
        else:
            return str(number)
    def plot_heatmap(ax: plt.Axes, count: np.array, usable_ace: bool, stay_hit: bool):
        ace_string = 'Usable ace' if usable_ace else 'No usable ace'
        stay_hit_string = 'Hit' if stay_hit else 'Stay'
        usable_ace = int(usable_ace)
        stay_hit = int(stay_hit)
        ax.imshow(count[:,usable_ace,:, stay_hit])
        ax.set_xlabel('Dealer')
        ax.set_ylabel('Player')
        ax.set_xticks(np.arange(len(count[:,usable_ace,0, stay_hit])), labels=list(range(2,12)))
        ax.set_yticks(np.arange(len(count[0,usable_ace,:, stay_hit])), labels=list(range(12,22)))
        for i in range(len(range(12,22))):
            for j in range(len(range(2,12))):
                text = ax.text(j, i, formatter(count[i, usable_ace, j, stay_hit]),
                            ha="center", va="center", color="w")
        ax.set_title(ace_string + ', ' + stay_hit_string)    

    plot_heatmap(ax11, count, False, False)
    plot_heatmap(ax12, count, False, True)
    plot_heatmap(ax21, count, True, False)
    plot_heatmap(ax22, count, True, True)
    fig.suptitle("Occurences count")
    plt.tight_layout()

    plt.show()

def plot_q(q: np.array):
    # Q
    fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(nrows= 2, ncols= 2, figsize= (9,9))

    def plot_q_heatmap(ax: plt.Axes, q: np.array, usable_ace: bool, stay_hit: bool):
        ace_string = 'Usable ace' if usable_ace else 'No usable ace'
        stay_hit_string = 'Hit' if stay_hit else 'Stay'
        usable_ace = int(usable_ace)
        stay_hit = int(stay_hit)     
        ax.imshow(q[:,usable_ace,:, stay_hit])
        ax.set_xlabel('Dealer')
        ax.set_ylabel('Player')
        ax.set_xticks(np.arange(len(q[:,usable_ace,0, stay_hit])), labels=list(range(2,12)))
        ax.set_yticks(np.arange(len(q[0,usable_ace,:, stay_hit])), labels=list(range(12,22)))
        for i in range(len(range(12,22))):
            for j in range(len(range(2,12))):
                text = ax.text(j, i, round(q[i, usable_ace, j, stay_hit],2),
                            ha="center", va="center", color="w")
        ax.set_title(ace_string + ', ' + stay_hit_string)

    plot_q_heatmap(ax11, q, False, False)
    plot_q_heatmap(ax12, q, False, True)
    plot_q_heatmap(ax21, q, True, False)
    plot_q_heatmap(ax22, q, True, True)
    fig.suptitle('Q plot')
    fig.tight_layout()
    plt.show()

def plot_policy(policy: np.array):
    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))
    ax1.imshow(policy[:,0,:])
    ax1.set_xlabel('Dealer')
    ax1.set_ylabel('Player')
    ax1.set_xticks(np.arange(len(policy[:,0,0])), labels=list(range(2,12)))
    ax1.set_yticks(np.arange(len(policy[0,0,:])), labels=list(range(12,22)))
    for i in range(len(range(12,22))):
        for j in range(len(range(2,12))):
            text = ax1.text(j, i, round(policy[i, 0, j], 2),
                        ha="center", va="center", color="w")
    ax1.set_title('No usable ace')

    ax2.imshow(policy[:,1,:])
    ax2.set_xlabel('Dealer')
    ax2.set_ylabel('Player')
    ax2.set_xticks(np.arange(len(policy[:,0,0])), labels=list(range(2,12)))
    ax2.set_yticks(np.arange(len(policy[0,0,:])), labels=list(range(12,22)))
    ax2.set_title('Usable ace')
    for i in range(len(range(12,22))):
        for j in range(len(range(2,12))):
            text = ax2.text(j, i, round(policy[i, 1, j], 2),
                        ha="center", va="center", color="w")
    fig.suptitle('Policy plot')
    fig.tight_layout()
    
    plt.show()