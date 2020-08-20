import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from data import DiffData

class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self):
        self.stream = self.data_stream()

        diff = DiffData('https://www.basketball-reference.com/boxscores/pbp/202008170TOR.html')
        self.full_data = diff.data
        self.current_data = np.empty([2,2], dtype=float)
        self.current_data[0] = np.array([0,0])
        self.current_data[1] = np.array([0,0])
        self.tick = 0
        self.ticks_per_second = 1


        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots(figsize=(18, 9), dpi=80)
        self.ax.axis([0, 4, -20, 30])
        self.ax.set_yticks(range(-20, 31, 10), minor=False)
        self.ax.set_yticks(range(-20, 31, 5), minor=True)
        self.ax.grid(which='major', axis='y', linestyle='-', linewidth='1', color='black', alpha=0.1)
        self.ax.grid(which='minor', axis='y', linestyle='-', linewidth='1', color='black', alpha=0.1)

        self.ax.set_xticks(range(0, 5, 1), minor=False)
        self.ax.grid(which='major', axis='x', linestyle='-', linewidth='1', color='black', alpha=0.3)

        self.ax.set_xlabel('Time (in quaters)')
        self.ax.set_ylabel('Point Differential\n-Nets        +Raptors')
        # self.ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('Quater %'))

        # self.fig.(num=None, )

        self.line, = self.ax.plot([], [], 'o-', lw=2, ms=1.5, alpha=0.8)
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=2880, interval=1, blit=True)
        # self.ani.save('basic_animation.mp4', fps=60, extra_args=['-vcodec', 'libx264'])


    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y = next(self.stream).T
        # self.scat = self.ax.plot(x, y, '-ok')
        # self.scat = self.ax.scatter(x, y, vmin=0, vmax=1,
        #                             cmap="jet", edgecolor="k")
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        # return self.scat,

    def data_stream(self):
        """Generate a random walk (brownian motion). Data is scaled to produce
        a soft "flickering" effect."""

        while True:
            self.tick += 1
            current_second = self.tick / self.ticks_per_second 

            if(current_second > self.full_data[0][0]):
                next_point = np.array([self.full_data[0]], dtype=float)
                next_point[0][0] /= (60.0*12.0)
                self.current_data = np.concatenate((self.current_data, next_point), axis=0)
                self.current_data = np.concatenate((self.current_data, next_point), axis=0)
                self.full_data = np.delete(self.full_data, 0,0)
            else:
                self.current_data[-1] = np.array([current_second/(12*60), self.current_data[-1][1]])

            yield self.current_data

    def update(self, i):
        """Update the scatter plot."""
        data = next(self.stream)
        # print(data[:,0])
        # Set x and y data...
        # self.scat.set_offsets(data)
        self.line.set_data(data[:,0], data[:,1])

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.line,


if __name__ == '__main__':
    a = AnimatedScatter()
    plt.show()