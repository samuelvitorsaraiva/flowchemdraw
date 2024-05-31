

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from undefined import undefined
    fig, ax = plt.subplots(figsize=(5, 5))
    undefined(ax=ax)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    #ax.grid(True)
    plt.show()