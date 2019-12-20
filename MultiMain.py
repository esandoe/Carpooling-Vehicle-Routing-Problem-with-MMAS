from multiprocessing.pool import Pool

from Main import *


def simulate_many(datakey, N, simulations = 100, iterations = 1000, threads = 16):
    pg.setConfigOptions(antialias=True)

    with Pool(threads) as pool:
        args = [(datakey, N, False, iterations) for _ in range(simulations)]
        results = pool.starmap(simulate, args)

    t = list(map(list, zip(*results)))

    worst = []
    percentile10 = []
    percentile20 = []
    percentile50 = []
    percentile80 = []
    percentile90 = []
    best = []
    average = []

    for iterationresults in t:
        iterationresults.sort(reverse=False)
        best.append(iterationresults[-1])
        percentile90.append(iterationresults[9*len(iterationresults)//10])
        percentile80.append(iterationresults[4*len(iterationresults)//5])
        percentile50.append(iterationresults[len(iterationresults)//2])
        percentile20.append(iterationresults[len(iterationresults)//5])
        percentile10.append(iterationresults[len(iterationresults)//10])
        worst.append(iterationresults[0])
        average.append(sum(iterationresults)/len(iterationresults))

    app = QApplication(sys.argv)
    title = str.format(
        "dataset {0}, simulations = {1}, iterations = {2}, N = {3}, β = {4}, R = {5}",
        datakey, simulations, iterations, N, Ant.b, Ant.R)
    w = pg.PlotWidget(labels={'left': 'score', 'bottom': 'iteration'}, title=title)
    w.getPlotItem().addLegend(offset=(-20,-20))
    w.getPlotItem().plot(best, name="best score", pen=pg.mkPen(color='#a0f0f0', width=3))
    w.getPlotItem().plot(percentile90, name="90th percentile", pen=pg.mkPen(color='#a0a0a0', width=3))
    w.getPlotItem().plot(percentile80, name="80th percentile", pen=pg.mkPen(color='#606060', width=3))
    w.getPlotItem().plot(percentile50, name="50th percentile", pen=pg.mkPen(color='#000000', width=3))
    w.getPlotItem().plot(percentile20, name="20th percentile", pen=pg.mkPen(color='#606060', width=3))
    w.getPlotItem().plot(percentile10, name="10th percentile", pen=pg.mkPen(color='#a0a0a0', width=3))
    w.getPlotItem().plot(worst, name="worst score", pen=pg.mkPen(color='#f0a0f0', width=3))
    # w.getPlotItem().plot(average, name="average score", pen=pg.mkPen(color='#ff0000', width=3))
    w.setBackground(pg.mkColor('w'))
    w.show()
    app.exec()

if __name__ == '__main__':
    simulate_many('1', 1, simulations=5000, iterations=25, threads=16)

