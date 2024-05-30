

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from valve import valve
    fig, ax = plt.subplots(figsize=(5, 5))
    valve(ax=ax)
    ax.grid(True)
    plt.show()