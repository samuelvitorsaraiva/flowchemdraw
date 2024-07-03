

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from flowchemdraw.figures import *
    fig, ax = plt.subplots(figsize=(5, 5))
    obj = pump(ax=ax)
    obj.command = 'with'
    obj.operation_theta = 270
    obj.operation = True
    obj.operation_set()
    for p in obj.connection_points:
        ax.plot(p[0], p[1], 'x', color='r')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    for i in range(500):
        obj.operation_set()
    #ax.grid(True)
    plt.show()