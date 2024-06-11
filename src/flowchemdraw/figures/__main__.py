

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from flowchemdraw.figures import *
    fig, ax = plt.subplots(figsize=(5, 5))
    obj = chromatography(ax=ax)
    for p in obj.connection_points:
        ax.plot(p[0], p[1], 'x', color='r')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    #ax.grid(True)
    plt.show()