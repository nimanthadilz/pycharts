import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from chart.chart import BaseChart
import sys


class Icicle(BaseChart):

    def __init__(self, data, left_color="#8B008B", right_color="#FF00FF", element_width=1.5,
                 chart_height=20):
        super().__init__(data)
        self._maxHeight = chart_height  # overall height of the chart
        self._width = element_width  # width of a single rectangle
        self._color_l = left_color  # user input
        self._color_r = right_color  # user input

        self.draw_chart()

    def get_figure(self):
        return self.figure

    def __convert_data(self):
        keys = list(self.data.keys())
        self._max = -1000000000000000000
        self._min = sys.maxsize

        for i in range(1, len(keys)):
            current_parent = self.data[keys[i]][1]
            current_node = self.data[keys[i]]

            while current_parent != None:
                if current_node[0] != None:
                    self._max = current_node[0] if self._max < current_node[0] else self._max
                    self._min = current_node[0] if self._min > current_node[0] else self._min

                    updated_value = self.data[keys[keys.index(current_parent)]][0] + current_node[0] if \
                        self.data[keys[keys.index(current_parent)]][0] != None else current_node[0]
                    self.data[keys[keys.index(current_parent)]] = (
                        updated_value, self.data[keys[keys.index(current_parent)]][1])

                current_parent = self.data[current_parent][1]

        self._max = self.data[keys[0]][0] if self._max < self.data[keys[0]][0] else self._max
        self._min = self.data[keys[0]][0] if self._min > self.data[keys[0]][0] else self._min

    def __calculate_color(self, value):
        # converting the colors into int
        color_l = int(self._color_l[1:], 16)
        color_r = int(self._color_r[1:], 16)

        # calculate the color responding to the given value
        return "#" + str(
            hex(int((color_r * (value - self._min) + color_l * (self._max - value)) / (self._max - self._min)))[2:])

    def __configure_plot(self):
        self.figure, self.ax = plt.subplots()  # define Matplotlib figure and axis
        self.ax.get_xaxis().set_visible(False)  # hide x-axis
        self.ax.get_yaxis().set_visible(False)  # hide y-axis
        self.ax.set_axis_off()
        self.ax.plot()

    def draw_chart(self):
        self.__convert_data()
        self.__configure_plot()
        keys = list(self.data.keys())

        # add rectangle to plot for the first root parent
        color = self.__calculate_color(self.data[keys[0]][0])
        self.ax.add_patch(Rectangle((0, 0), self._width, self._maxHeight, fill=True, facecolor=color))
        self.ax.text(self._width / 3, self._maxHeight / 2, keys[0], color='white', fontsize=8)

        # update the list with width and height of the element
        self.data[keys[0]] = [self.data[keys[0]][0], self.data[keys[0]][1], 0, 0, 2, 20]

        index = 1

        for e in self.data:
            if e != keys[0]:
                item = self.data[e]
                height = 20
                start_x = -1
                start_y = -1

                # iterating through the list to find the parent
                for i in range(index - 1, -1, -1):
                    # parent has other children
                    if self.data[keys[i]][1] == item[1]:
                        height = self.data[self.data[keys[i]][1]][5] * (
                                item[0] / self.data[self.data[keys[i]][1]][0])
                        start_x = self.data[keys[i]][2]
                        start_y = self.data[keys[i]][3] - height
                        break

                # current elem is the first or sole elem
                if start_x == start_y == -1:
                    height = self.data[item[1]][5] * (item[0] / self.data[item[1]][0])
                    start_x = self.data[item[1]][2] + self._width
                    start_y = self.data[item[1]][3] + self.data[item[1]][5] - height

                # finding the color depending on the value
                color = self.__calculate_color(item[0])

                # add the rectangle
                self.ax.add_patch(
                    Rectangle((start_x, start_y), self._width, height,
                              fill=True, edgecolor="white", linewidth=1, facecolor=color))

                # update the main array with coordinates
                self.data[keys[index]] = [item[0], item[1], start_x, start_y, self._width, height]
                # add text into the rectangle
                self.ax.text(start_x + self._width / 3, start_y + height / 2, keys[index], color='white', fontsize=8)

                index += 1

        # display plot
        plt.show()