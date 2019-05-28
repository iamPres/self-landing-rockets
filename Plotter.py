import matplotlib.pyplot as plt


class Plotter:

    def show(self, arr):
        plt.close()
        style = 'ro-'

        plt.plot(range(len(arr)),arr, style, markersize=2, linewidth=2)

        plt.show(block=False)
