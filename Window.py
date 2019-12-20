from PyQt5.Qt import *
import pyqtgraph as pg

from Ant import *
from MultiSimulation import Simulation


class Window(QMainWindow):
    def __init__(self, simulation, datakey, *args):
        QMainWindow.__init__(self, *args)
        self.setWindowTitle("Dispatchimizer 4000")
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        self.simulation: Simulation = simulation
        self.update_ticks = 1

        # create main widgets
        title = str.format("dataset {0}, N = {1}, β = {2}, R = {3}", datakey, simulation.N, Ant.b, Ant.R)
        mapWidget = pg.PlotWidget(title=title)
        legend = mapWidget.addLegend(size=(80, 80), offset=(-20,-20))
        mapWidget.setXRange(min(node.x for node in simulation.nodes) - 15, max(node.x for node in simulation.nodes) + 15)
        mapWidget.setYRange(min(node.y for node in simulation.nodes) - 15, max(node.y for node in simulation.nodes) + 15)
        mapWidget.setBackground('#fff')
        groupBox = QGroupBox("DATA")
        groupBox.setFixedWidth(200)

        layout = QGridLayout()
        layout.addWidget(mapWidget, 0, 0)
        layout.addWidget(groupBox, 0, 1)

        self.costLabel = QLabel("Best solution cost: ")
        self.bestscoreLabel = QLabel("Best score: ")
        self.antLabel = QLabel("Ant number: ")
        self.maxpheroLabel = QLabel("Maximum pheromones: 0")
        self.minpheroLabel= QLabel("Minimum pheromones: 0")

        vbox = QVBoxLayout()

        vbox.addWidget(self.maxpheroLabel)
        vbox.addWidget(self.minpheroLabel)
        vbox.addWidget(self.costLabel)
        vbox.addWidget(self.bestscoreLabel)
        vbox.addWidget(self.antLabel)
        vbox.addWidget(HyperQSlider(self.simulation))

        bgSlider = CustomSlider(lambda x: mapWidget.setBackground((int(x*2.55), int(x*2.55), int(x*2.55))), 'Background', 100)
        vbox.addWidget(bgSlider)

        def update_ticks(t):
            self.update_ticks = int(t * 5) + 1
        speedSlider = CustomSlider(lambda t: update_ticks(t), 'Update interval', 3)
        vbox.addWidget(speedSlider)

        self.show_ants = True
        def show_hide_ants():
            self.show_ants = not self.show_ants
        show_hide_antsButton = QPushButton('Show/hide ants')
        show_hide_antsButton.clicked.connect(show_hide_ants)
        vbox.addWidget(show_hide_antsButton)

        self.paused = False
        def show_hide_ants():
            self.paused = not self.paused
        pauseButton = QPushButton('Pause/start simulation')
        pauseButton.clicked.connect(show_hide_ants)
        vbox.addWidget(pauseButton)

        groupBox.setLayout(vbox)

        self.bestCurves = [mapWidget.plot(pen=pg.mkPen(color=pg.hsvColor(i/self.simulation.N, sat=0.9, val=0.9), width=4)) for i in range(self.simulation.N)]
        self.lastCurves = [mapWidget.plot(pen=pg.mkPen(color=pg.hsvColor(i/self.simulation.N, alpha=0.4), width=2)) for i in range(self.simulation.N)]

        pickup_nodes: List(Tuple(int, int)) = []
        dropoff_nodes: List(Tuple(int, int)) = []

        for node in self.simulation.nodes:
            if node.dropoff == None:
                dropoff_nodes.append((node.x, node.y))
            else:
                pickup_nodes.append((node.x, node.y))

        self.outline = pg.mkPen(color=pg.mkColor('#fff'), width=4)
        mapWidget.plot([x for (x, y) in pickup_nodes], [y for (x, y) in pickup_nodes], name="pickup", pen=None, symbolPen=self.outline, symbol='o', symbolBrush=pg.mkBrush(color=pg.mkColor('#4d4')))
        mapWidget.plot([x for (x, y) in dropoff_nodes], [y for (x, y) in dropoff_nodes], name="delivery", pen=None, symbolPen=self.outline, symbol='o', symbolBrush=pg.mkBrush(color=pg.mkColor('#4ae')))

        sx, sy = (self.simulation.start_node.x, self.simulation.start_node.y)
        mapWidget.plot([sx], [sy], name="start", pen=None, symbolPen=None, symbol='o', symbolBrush=pg.mkBrush(color=pg.mkColor('#444')))

        # create parent widget
        cw = QWidget()
        cw.setLayout(layout)
        self.setCentralWidget(cw)

    def update(self):
        if self.paused:
            return

        solution = self.simulation.update()

        self.antLabel.setText("Ant number: " + str(self.simulation.iteration))
        if self.simulation.iteration % self.update_ticks > 0:
            return

        if not self.show_ants:
            for i in range(len(solution)):
                self.lastCurves[i].setData([],[])
        else:
            for i in range(len(solution)):
                route = solution[i]
                if len(route) == 0:
                    continue
                x = [edge.from_node.x for edge in route] + [route[-1].to_node.x]
                y = [edge.from_node.y for edge in route] + [route[-1].to_node.y]
                self.lastCurves[i].setData(x,y)

        for i in range(len(self.simulation.best_solution)):
            route = self.simulation.best_solution[i]
            if len(route) == 0:
                self.bestCurves[i].setData([], [])
            else:
                x = [edge.from_node.x for edge in route] + [route[-1].to_node.x]
                y = [edge.from_node.y for edge in route] + [route[-1].to_node.y]
                self.bestCurves[i].setData(x, y)

        pheromones = [edge.pheromones for edge in self.simulation.edges]
        max_pheromones = str(round(max(pheromones), 1))
        self.maxpheroLabel.setText("Maximum pheromones: " + max_pheromones)
        min_pheromones = str(round(min(pheromones), 1))
        self.minpheroLabel.setText("Minimum pheromones: " + min_pheromones)
        best_score = str(self.simulation.best_score)
        self.bestscoreLabel.setText("Best score: " + best_score)
        best_solution_cost = str(self.simulation.best_solution_cost)
        self.costLabel.setText("Best solution cost: " + best_solution_cost)


class CustomSlider(QWidget):
    def __init__(self, update_func, name: str, value: int = 0):
        QWidget.__init__(self)
        self.update_func = update_func
        self.name = name

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(value)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(10)
        self.sl.valueChanged.connect(self.update)

        self.label = QLabel(self.name + ": " + str(self.sl.value()))

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.sl)
        self.setLayout(vbox)

    def update(self):
        self.label.setText(self.name + ": " + str(self.sl.value()))
        self.update_func(self.sl.value())


class HyperQSlider(QWidget):
    def __init__(self, sim: Simulation):
        QWidget.__init__(self)

        self.sim = sim
        self.q = Ant.q

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(int(self.q * 100))
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(10)
        self.sl.valueChanged.connect(self.valuechange)

        self.label = QLabel("Q: " + str(self.q))

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.sl)
        self.setLayout(vbox)

    def valuechange(self):
        self.q = self.sl.value() / 100
        self.label.setText("Q: " + str(self.q))
        Ant.q = self.q
        #self.sim.reset_pheromones()