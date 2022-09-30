import collections
import matplotlib.pyplot as plt
import numpy as np

from itertools import groupby
from typing import DefaultDict, Dict, List, Optional, Tuple
from matplotlib.patches import Wedge
from matplotlib.figure import Figure

from chart.chart import BaseChart
from chart.sunburst_path import Path
from utils.utils import get_root_node_key

STRING_DELIM = "/"
Angles = collections.namedtuple("Angles", ["theta1", "theta2"])

class Sunburst(BaseChart):
    """
    The class to represent the sunburst chart type.
    
    Attributes
    ----------
    data: dictionary of type "Node" : (Value, "Parent")
    axes:
    origin: coordinates of the center of the chart of type (float, float)
    cmap: controls the coloring based on the angle
    base_ring_width: default width of a wedge as float
    base_edge_color: default edge color of a wedge as tuple 
    base_line_width: default line width of a wedge as float
    plot_center: plot a circle in the center as boolean
    plot_minimal_angle: plot only wedges if the angle is bigger than plot_minimal_angle as float
    label_minimal_angle: label only wedges if the angle is bigger than plot_minimal_angle as float
    order: to change the order of the converted pathvalue dictionary as a string
        syntax = "keep" | "value" | "key" and "reversed"
        keep    : keep the order of the dictionary
        value   : sort values in the ascending order
        key     : sort paths alphabetically
        reversed: take any syntax from above options and reverse it
    base_textbox_props: properties of the testbos that annonating the wedge corresponding to the path
    """
    def __init__(self,
                data,
                axes: Optional[plt.axes] = None,
                origin = (0.0, 0.0),
                cmap = plt.get_cmap("autumn"),
                base_ring_width = 0.4, 
                base_edge_color = (0, 0, 0, 1),
                base_line_width = 0.75,
                plot_center = False,
                plot_minimal_angle = 0, 
                label_minimal_angle = 0,
                order = "value reverse",
                base_textbox_props = None,
        ):
        super().__init__(data)
        
        if axes is None:
            axes = plt.gca()
        
        self.figure, self.axes = plt.subplots()
        
        self.data = self.__dict_to_pv(self.__convert_data(data))
        self.cmap = cmap
        self.origin = origin
        self.base_wedge_width = base_ring_width
        self.base_edge_color = base_edge_color
        self.base_line_width = base_line_width
        self.plot_center = plot_center
        self.plot_minimal_angle = plot_minimal_angle
        self.label_minimal_angle = label_minimal_angle
        self.order = order
        self.base_textbox_props = base_textbox_props
        
        if not base_textbox_props:
            self.base_textbox_props = dict(
                boxstyle="round, pad=0.2",
                fc=(1, 1, 1, 0.8),
                ec=(0.4, 0.4, 0.4, 1),
                lw=0.0,
            )
            
        # Variables
        self._completed_pv = {}  # type: Dict[Path, float]
        self._completed_paths = []  # type: List[Path]
        self._max_level = 0  # type: int
        self._structured_paths = []  # type: List[List[List[Path]]]
        self._angles = {}  # type: Dict[Path, Angles]

        # Output
        self.wedges = {}  # type: Dict[Path, Wedge]
        
        # Plot the chart 
        self.__plot(setup_axes=True)
    
    def get_figure(self):
        return self.figure
        
    # ===============================================================================================
    def __get_parent_key(self, data:dict,  node: str):
        """
        Returns the directory of a node from the root as a string
        
        e.g.
        data = {
            "Root" : (None, None),
            "Grand Parent1" : (None, "Root"),
            "Parent1" : (None, "Grand Parent1"),
            "Child1" : (10, "Parent1"),
            "Parent2" : (None, "Grand Parent1"),
            "Child2" : (15, "Parent2"),
            "Grand Parent2" : (None, "Root"),
            "Parent3" : (None, "Grand Parent2"),
            "Child3" : (22, "Parent3"),
        }
        
        node = "Child1"
        
        function returns "Root/Grand Parent1/Parent1"
        
        Parameters
        -----------
        data: dictionary of type "node": (Value, "Parent")
        node: the node that has to find the directory
            
        Returns
        -------
        String
        """
        root_node = get_root_node_key(data)
        for key, value in data.items():
            if key == node:
                if value[1] != root_node:
                    return self.__get_parent_key(data, value[1]) + '/' + str(value[1])
                else:
                    return str(value[1])
    
    def __convert_data(self, data:dict):
        """
        Returns a dictionary of type [String, Float]
        
        e.g.
        data = {
            "Root" : (None, None),
            "Grand Parent1" : (None, "Root"),
            "Parent1" : (None, "Grand Parent1"),
            "Child1" : (10, "Parent1"),
            "Parent2" : (None, "Grand Parent1"),
            "Child2" : (15, "Parent2"),
            "Grand Parent2" : (None, "Root"),
            "Parent3" : (None, "Grand Parent2"),
            "Child3" : (22, "Parent3"),
        }
        
        function returns
        {
            'Root/Grand Parent1/Parent1/Child1': 10, 
            'Root/Grand Parent1/Parent2/Child2': 15, 
            'Root/Grand Parent2/Parent3/Child3': 22
        }
        
        Parameters
        ----------
        data: dictionary of type "node": (Value, "Parent")

        Returns
        -------
        dictionary[Str, Float]
        """
        modified_data = {}
        for key, value in data.items():
            if value[0] != None:
                pair = {self.__get_parent_key(data, key) + '/' + key : value[0]}
                modified_data.update(pair)
        return modified_data
    # ===============================================================================================

    def __dict_to_pv(self, data: dict, delim=STRING_DELIM):
        """
        Returns a dictionary of type [Path, float]
        
        e.g.
        data = {
            "Root/Grand Parent1/Parent1/Child1": 10,
            "Root/Grand Parent1/Parent2/Child2": 15,
            "Root/Grand Parent2/Parent3/Child3": 22,
        }
        
        function returns
        {
            Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )): 10, 
            Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )): 15, 
            Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )): 22
        }
        
        Parameters
        data: dictionary of type Path: Value
        delim: split the items i
        """
        assert all(isinstance(item, str) for item in data.keys())
        return {Path(item.split(delim)): value for item, value in data.items()}
    # ===============================================================================================
    
    def __complete_pv(self, pathvalues: Dict[Path, float]) -> Dict[Path, float]:
        if Path(()) in pathvalues:
            raise ValueError(
                "This function does not allow the empty path as item"
                "in the data list."
            )
        completed: DefaultDict[Path, float] = collections.defaultdict(float)
        
        for path, value in pathvalues.items():
            for level in range(0, len(path) + 1):
                completed[path[:level]] += value
        return dict(completed)
    
    def __complete_paths(self, paths: List[Path]) -> List[Path]:
        ret = [Path(())]
        for path in paths:
            for i in range(1, len(path)):
                ancestor = path[:i]
                if ancestor not in paths and ancestor not in ret:
                    ret.append(ancestor)
            ret.append(path)
        return ret
    
    def __structure_paths(self, paths: List[Path]) -> List[List[List[Path]]]:
        structured = []

        def level(path):
            return len(path)

        def parent(path):
            return path.parent()

        # sort by level
        paths.sort(key=level)
        paths_by_level = (list(group) for _, group in groupby(paths, key=level))

        # sort by parent
        for paths_of_level in paths_by_level:
            paths_of_level.sort(key=parent)
            paths_by_parent = [
                list(group) for _, group in groupby(paths_of_level, key=parent)
            ]
            structured.append(paths_by_parent)

        return structured
        
    def __calculate_angles(self, structured_paths: List[List[List[Path]]], path_values: Dict[Path, float],) -> Dict[Path, Angles]:
        angles: Dict[Path, Angles] = {}
        # the total sum of all elements (on one level)
        value_sum = path_values[Path(())]
        for level_no, groups in enumerate(structured_paths):
            for group in groups:
                theta2 = None 
                for path_no, path in enumerate(group):
                    if level_no == 0:
                        theta1 = 0
                    elif path_no == 0:
                        theta1 = angles[path.parent()].theta1
                    else:
                        theta1 = theta2  # type: ignore
                    theta2 = theta1 + 360 * path_values[path] / value_sum
                    angles[path] = Angles(theta1, theta2)
        return angles
    # ===============================================================================================
    
    def __prepare_data(self):
        self._completed_pv = self.__complete_pv(self.data)
        ordered_paths: List[Path] = []
        
        if self.order:
            order_options = set(self.order.split(" "))
        else:
            order_options = set()
            
        lonely_order_options = {"value", "key", "keep"}
        allowed_order_options = lonely_order_options | {"reverse"}
        if not order_options <= allowed_order_options:
            raise ValueError(
                "'order' option must consist of a subset of "
                "strings from {}, joined by "
                "spaces.".format(allowed_order_options)
            )
        if not len(order_options & lonely_order_options) <= 1:
            raise ValueError(
                "Only one of the options {} "
                "allowed.".format(lonely_order_options)
            )
            
        if not order_options:
            ordered_paths = list(self.data.keys())
        elif "keep" in self.order:
            ordered_paths = list(self.data.keys())
            if type(self.data) is dict:
                print(
                    "Warning: Looks like you want to keep the order of your"
                    "input pathvalues, but pathvalues are of type dict "
                    "which does keep record of the order of its items."
                )
        elif "value" in self.order:
            ordered_paths = sorted(
                self._completed_pv.keys(),
                key=lambda key: self._completed_pv[key],
            )
        elif "key" in self.order:
            ordered_paths = sorted(self._completed_pv.keys())
        
        if "reverse" in self.order:
            ordered_paths = list(reversed(ordered_paths))
            
        self._completed_paths = self.__complete_paths(ordered_paths)
        self._max_level = max((len(path) for path in self._completed_paths))
        self._structured_paths = self.__structure_paths(self._completed_paths)
        self._angles = self.__calculate_angles(
            self._structured_paths, self._completed_pv
        )

        for path in self._completed_paths:
            if self.plot_center or len(path) >= 1:
                angle = self._angles[path].theta2 - self._angles[path].theta1
                if len(path) == 0 or angle > self.plot_minimal_angle:
                    self.wedges[path] = self.__wedge(path)

    def __is_outmost(self, path: Path) -> bool:
        level = len(path)
        if level == self._max_level:
            return True
        for group in self._structured_paths[level + 1]:
            for p in group:
                if p.startswith(path):
                    return False
                continue
        return True
    
    def __wedge_width(self, path: Path)-> float:
        return self.base_wedge_width
    
    def __wedge_spacing(self, path: Path) -> Tuple[float, float]:
        return 0, 0

    def _wedge_outer_radius(self, path: Path) -> float:
        return self._wedge_inner_radius(path) + self.__wedge_width(path)
    
    def _wedge_inner_radius(self, path: Path) -> float:
        start = 0 if self.plot_center else 1
        ancestors = [path[:i] for i in range(start, len(path))]
        return (
            sum(
                self.__wedge_width(ancestor) + sum(self.__wedge_spacing(ancestor))
                for ancestor in ancestors
            )
            + self.__wedge_spacing(path)[0]
        )
        
    def __wedge_mid_radius(self, path: Path) -> float:
        return (
            self._wedge_outer_radius(path) + self._wedge_inner_radius(path)
        ) / 2
        
    def __edge_color(self, path: Path) -> Tuple[float, float, float, float]:
        return self.base_edge_color
    
    def __line_width(self, path: Path) -> float:
        return self.base_line_width;
    
    def __face_color(self, path: Path) -> Tuple[float, float, float, float]:
        if len(path) == 0:
            color: List[float] = [1, 1, 1, 1]
        else:
            angle = (self._angles[path].theta1 + self._angles[path].theta2) / 2
            color = list(self.cmap(angle / 360))
            for i in range(3):
                color[i] += (
                    (1 - color[i]) * 0.7 * (len(path) / (self._max_level + 1))
                )
        return tuple(color)
    
    def __alpha(self, path: Path) -> float:
        return 1
    
    def __textbox_props(self, path: Path, text_type: str) -> Dict:
        return self.base_textbox_props
    
    def __format_path_text(self, path) -> str:
        return path[-1] if path else ""
    
    def __format_value_text(self, value: float) -> str:
        return "{0:.2f}".format(value)
    
    def __format_text(self, path: Path) -> str:
        path_text = self.__format_path_text(path)
        value_text = self.__format_value_text(self._completed_pv[path])
        if path_text and value_text:
            return "{} ({})".format(path_text, value_text)
        return path_text
    
    def __radial_text(self, path: Path) -> None:
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        radius = self.__wedge_mid_radius(path)
        if self.__is_outmost(path):
            radius = self._wedge_inner_radius(path)

        mid_x = self.origin[0] + radius * np.cos(np.deg2rad(angle))
        mid_y = self.origin[1] + radius * np.sin(np.deg2rad(angle))

        if 0 <= angle < 90:
            rotation = angle
        elif 90 <= angle < 270:
            rotation = angle - 180
        elif 270 < angle <= 360:
            rotation = angle - 360
        else:
            raise ValueError

        if self.__is_outmost(path):
            if 0 <= angle < 90:
                va = "bottom"
                ha = "left"
            elif 90 <= angle <= 180:
                va = "bottom"
                ha = "right"
            elif 180 <= angle <= 270:
                va = "top"
                ha = "right"
            elif 270 <= angle <= 360:
                va = "top"
                ha = "left"
            else:
                raise ValueError
        else:
            ha = "center"
            va = "center"

        text = self.__format_text(path)
        self.axes.text(
            mid_x,
            mid_y,
            text,
            ha=ha,
            va=va,
            rotation=rotation,
            bbox=self.__textbox_props(path, "radial"),
        )
    
    def __tangential_text(self, path: Path) -> None:
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        radius = self.__wedge_mid_radius(path)
        mid_x = self.origin[0] + radius * np.cos(np.deg2rad(angle))
        mid_y = self.origin[1] + radius * np.sin(np.deg2rad(angle))

        if 0 <= angle < 90:
            rotation = angle - 90
        elif 90 <= angle < 180:
            rotation = angle - 90
        elif angle == 180:
            rotation = angle - 180
        elif 180 < angle < 270:
            rotation = angle - 270
        elif 270 <= angle < 360:
            rotation = angle - 270
        else:
            raise ValueError

        text = self.__format_text(path)
        self.axes.text(
            mid_x,
            mid_y,
            text,
            ha="center",
            va="center",
            rotation=rotation,
            bbox=self.__textbox_props(path, "tangential"),
        )
    
    def __add_annotation(self, path):
        angle = self._angles[path].theta2 - self._angles[path].theta1

        if not angle > self.label_minimal_angle:
            return

        if len(path) * angle > 90:
            self.__tangential_text(path)
        else:
            self.__radial_text(path)
            
    def __plot(self, setup_axes=False, interactive=False)-> None:    
        self.axes.set_title("Title")
        
        if not self.wedges:
            self.__prepare_data()
        
        for path, wedge in self.wedges.items():
            self.axes.add_patch(wedge)
            if not interactive:
                self.__add_annotation(path)
        
        if setup_axes:
            self.axes.autoscale()
            self.axes.set_aspect("equal")
            self.axes.autoscale_view(True, True, True)
            self.axes.axis("off")
            self.axes.margins(x=0.1, y=0.1)
            
        if interactive:
            def hover(event):
                if event.inaxes == self.axes:
                    found = False
                    for path in self.wedges:
                        if not found:
                            cont, ind = self.wedges[path].contains(event)
                        else:
                            cont = False
                        if cont:
                            self.wedges[path].set_alpha(0.5)
                            self.axes.set_title(self.__format_text(path))
                        else:
                            self.wedges[path].set_alpha(1.0)
                    self.axes.figure.canvas.draw_idle()
            self.axes.figure.canvas.mpl_connect("motion_notify_event", hover)
    
    def __wedge(self, path: Path) -> Wedge:
        return Wedge(
            (self.origin[0], self.origin[1]),
            self._wedge_outer_radius(path),
            self._angles[path].theta1,
            self._angles[path].theta2,
            width=self.__wedge_width(path),
            label=self.__format_text(path),
            facecolor=self.__face_color(path),
            edgecolor=self.__edge_color(path),
            linewidth=self.__line_width(path),
            fill=True,
            alpha=self.__alpha(path),
        )