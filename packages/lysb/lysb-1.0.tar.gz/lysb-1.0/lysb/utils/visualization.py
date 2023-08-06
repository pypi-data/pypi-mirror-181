import matplotlib.pyplot as plt

def visual_comparator(args):
    """Visualizes the performance of the input algorithms in comparison with each other.

    Parameters
    ----------
    args : Iterable
        List of trained Bandit algorithms.

    Returns
    -------
    None
    """
    assert hasattr(args,'__iter__')
    # add class check
    fig = plt.figure(figsize = (10, 5))
    for it in args:

        plt.plot([i for i in range(len(it.reward_collector))], it.reward_collector,label=f"{it.__class__.__name__}") # plot cumsum per bandit.

    plt.legend()
    plt.xlabel("Timestep")
    plt.ylabel("Log Cummulative Reward")
    plt.title("Log Commulative Reward of LinUCB Over Time")
    plt.yscale("log")
    plt.show() 