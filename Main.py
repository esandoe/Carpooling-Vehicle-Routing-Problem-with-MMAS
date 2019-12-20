from data import datasets
from Window import *
from MultiSimulation import Simulation
import sys


def simulate(datakey, N, gui: bool = True, iterations=1000):
    sim = Simulation(datasets[datakey], N=N)
    if gui:
        app = QApplication(sys.argv)
        window = Window(sim, datakey)

        timer = QTimer()
        timer.timeout.connect(window.update)
        timer.start(0)

        window.show()
        sys.exit(app.exec_())
    else:
        best_log = []
        for i in range(iterations):
            sim.update()
            best_log.append(sim.best_score)
        return best_log


if __name__ == '__main__':
    simulate(datakey='1', N=1, gui=True)
