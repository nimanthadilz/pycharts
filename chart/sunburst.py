import collections
import matplotlib.pyplot as plt
import matplotlib as mpl
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
    chart_properties: dictionary type of title and chart font sizes and families
    origin: coordinates of the center of the chart of type (float, float)
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
                chart_properties: dict = {},
                axes: Optional[plt.Axes] = None,
        ):
        super().__init__(data)
        
        if axes is None:
            axes = plt.gca()
        
        self.figure, self.axes = plt.subplots()
        
        self.data = self.__dict_to_pv(self.__convert_data(data))
        self.origin = (0.0, 0.0)
        self.base_wedge_width = 0.4
        self.base_edge_color = (0, 0, 0, 1)
        self.base_line_width = 0.75
        self.plot_center = False
        self.plot_minimal_angle = 0
        self.label_minimal_angle = 0
        self.order = "value reverse"
        
        if chart_properties:
            self.chart_properties = chart_properties
        else:
            self.chart_properties = {
                "title" : "",
                "chart_font_family": "Arial",
                "chart_font_size": 8
            }
        
            
        # Variables
        self._completed_pv = {}  # type: Dict[Path, float]
        self._completed_paths = []  # type: List[Path]
        self._max_level = 0  # type: int
        self._structured_paths = []  # type: List[List[List[Path]]]
        self._angles = {}  # type: Dict[Path, Angles]

        # Output
        self.wedges = {}  # type: Dict[Path, Wedge]
        
        # Plot the chart 
        self.__plot()
        self.__customize_chart()
    
    def get_figure(self):
        return self.figure
        
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
        dict[Str, Float]
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
        ----------
        data: dictionary of type {Path: Value}
        delim: split the items using "/"
        
        Returns
        -------
        dict[Path, float]
        """
        assert all(isinstance(item, str) for item in data.keys())
        return {Path(item.split(delim)): value for item, value in data.items()}
    
    def __complete_pv(self, path_values: Dict[Path, float]):
        """
        e.g.
        data = {
            Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )): 10, 
            Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )): 15, 
            Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )): 22
        }
        
        function returns
        {
            Path((, )): 47.0, 
            Path(('Root', )): 47.0, 
            Path(('Root', 'Grand Parent1', )): 25.0, 
            Path(('Root', 'Grand Parent1', 'Parent1', )): 10.0, 
            Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )): 10.0, 
            Path(('Root', 'Grand Parent1', 'Parent2', )): 15.0, 
            Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )): 15.0, 
            Path(('Root', 'Grand Parent2', )): 22.0, 
            Path(('Root', 'Grand Parent2', 'Parent3', )): 22.0, 
            Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )): 22.0
        }
        
        Parameters
        ----------
        path_values: dictionary of type {Path: Value}
        
        Returns
        -------
        Dict[Path, float]
        """
        if Path(()) in path_values:
            raise ValueError(
                "This function does not allow the empty path as item"
                "in the data list."
            )
        completed: DefaultDict[Path, float] = collections.defaultdict(float)
        
        for path, value in path_values.items():
            for level in range(0, len(path) + 1):
                completed[path[:level]] += value
        return dict(completed)
    
    def __complete_paths(self, paths: List[Path]):
        """
        Preserve the order of path
        
        e.g.
        paths = [
            Path(('Root', )), Path((, )), Path(('Root', 'Grand Parent1', )), Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )), Path(('Root', 'Grand Parent2', 'Parent3', )), Path(('Root', 'Grand Parent2', )), Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )), Path(('Root', 'Grand Parent1', 'Parent2', )), Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )), Path(('Root', 'Grand Parent1', 'Parent1', ))
        ]
        
        function returns
        [
            Path((, )), Path(('Root', )), Path((, )), Path(('Root', 'Grand Parent1', )), Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )), Path(('Root', 'Grand Parent2', 'Parent3', )), Path(('Root', 'Grand Parent2', )), Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )), Path(('Root', 'Grand Parent1', 'Parent2', )), Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )), Path(('Root', 'Grand Parent1', 'Parent1', ))
        ]
        
        Parameters
        ----------
        path: list of type Path
        
        Returns
        -------
        List[Path]
        """
        ret = [Path(())]
        for path in paths:
            for i in range(1, len(path)):
                ancestor = path[:i]
                if ancestor not in paths and ancestor not in ret:
                    ret.append(ancestor)
            ret.append(path)
        return ret
    
    def __structure_paths(self, paths: List[Path]):
        """
        Takes a list of paths and groups the paths first by length (empty path length 0) and then by the parent (path[:len(path) - 1]).
        e.g.
        paths = [
            Path(('Root', )), Path((, )), Path(('Root', 'Grand Parent1', )), Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )), Path(('Root', 'Grand Parent2', 'Parent3', )), Path(('Root', 'Grand Parent2', )), Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )), Path(('Root', 'Grand Parent1', 'Parent2', )), Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )), Path(('Root', 'Grand Parent1', 'Parent1', ))
        ]
        
        function returns
        [
            [
                [Path((, )), Path((, ))]
            ], 
            [
                [Path(('Root', ))]
            ], 
            [
                [Path(('Root', 'Grand Parent1', )), Path(('Root', 'Grand Parent2', ))]
            ], 
            [
                [Path(('Root', 'Grand Parent1', 'Parent2', )), Path(('Root', 'Grand Parent1', 'Parent1', ))], 
                [Path(('Root', 'Grand Parent2', 'Parent3', ))]
            ], 
            [
                [Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', ))], 
                [Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', ))], 
                [Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', ))]
            ]    
        ]
        
        Parameters
        ----------
        paths: List of type Path
        
        Returns
        -------
        List[List[List[Path]]]
        """
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
        """
        Calculate the Starting angle and ending angle of the wedge
        e.g.
            Starting angle of the root is 0
            Ending angle of the root is 360
            
            If root has 2 nodes of the same value, 
            starting and ending angles of the node 1 is 0 and 180
            starting and ending angles of the node 2 is 180 and 360
            
            and so on
        
        Parameters
        ----------
        structured_paths: list of paths and groups the paths first by length (empty path length 0) and then by the parent (path[:len(path) - 1]).
        path_values: Dict[Path, Value] must be in completed_pv
        
        Returns
        -------
        Dict[Path, Angles]
            
        """
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
    
    def __prepare_data(self):
        """
        Sets up variables used for computing  such as, 
            _completed_pv
            _completed_path
            _max_level
            _structured_paths
            _angles
            
        Parameters
        ----------
        This function has no parameters
        
        Returns
        -------
        None
        """
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
                print("Warning: path values are of type dict. can not keep the order of path values")
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

    def __is_outmost(self, path: Path):
        """
        Checks whether thewedge corresponding to the path is the outmost wedge
        return True if there is no descendant of the path
        
        Parameters
        ----------
        path: Path of a node
        
        Returns
        -------
        bool
        """
        level = len(path)
        if level == self._max_level:
            return True
        for group in self._structured_paths[level + 1]:
            for p in group:
                if p.startswith(path):
                    return False
                continue
        return True
    
    def __wedge_width(self):
        """
        The width of the wedge corresponding to `path`
        sets to 0.4
        
        Parameters
        ----------
        None
        
        Returns
        float
        """
        return self.base_wedge_width
    
    def __wedge_spacing(self):
        """
        The radial space before and after the wedge
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Tuple[float, float]
        """
        return 0, 0

    def __wedge_inner_radius(self, path: Path):
        """
        The inner radius of the wedge corresponding to the path
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        float
        """
        start = 0 if self.plot_center else 1
        ancestors = [path[:i] for i in range(start, len(path))]
        return (
            sum(
                self.__wedge_width() + sum(self.__wedge_spacing())
                for ancestor in ancestors
            )
            + self.__wedge_spacing()[0]
        )
    
    def __wedge_outer_radius(self, path: Path):
        """
        The outer radius of the wedge corresponding to the path
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        float
        """
        return self.__wedge_inner_radius(path) + self.__wedge_width()
        
    def __wedge_mid_radius(self, path: Path) -> float:
        """
        The radius of the middle of the wedge corresponding to a path.
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        float
        """
        return (
            self.__wedge_outer_radius(path) + self.__wedge_inner_radius(path)
        ) / 2
        
    def __edge_color(self):
        """
        The line color of the wedge
        sets to (0,0,0,1)
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Tuple[float, float, float, float]
        """
        return self.base_edge_color
    
    def __line_width(self):
        """
        The line width of the wedge
        sets to 0.75
        
        Parameters
        ----------
        None
        
        Returns
        -------
        float
        """
        return self.base_line_width;
    
    def __face_color(self, path: Path):
        """
        The color of the wedge corresponding to the path
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        Tuple[float, float, float, float]
        """
        if len(path) == 0:
            color: List[float] = [1, 1, 1, 1]
        else:
            
            color: List[float] = []
            angle = (self._angles[path].theta1 + self._angles[path].theta2) / 2
            
            colormap = mpl.colormaps[self.chart_properties['colormap']]
            # colormap = plt.get_cmap(self.chart_properties["colormap"])
            if angle < 270:
                color = colormap(angle/360)
            else:   color = colormap(angle/720)
        return tuple(color)
    
    def __format_path_text(self, path):
        """
        Returns a string which represent the path of the corresponding wedge
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        str
        """
        return path[-1] if path else ""
    
    def __format_value_text(self, value: float):
        """
        Returns a string which represent the value of the corresponding wedge
        
        Parameters
        ----------
        value: float
        
        Returns
        -------
        str
        """
        return "{0:.2f}".format(value)
    
    def __format_text(self, path: Path):
        """
        Returns a string which represent the corresponding wedge
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        str
        """
        path_text = self.__format_path_text(path)
        value_text = self.__format_value_text(self._completed_pv[path])
        if path_text and value_text:
            return "{} ({})".format(path_text, value_text)
        return path_text
    
    def __radial_text(self, path: Path):
        """
        Adds a radially rotated annotation for the wedge corresponding to `path` to the axes
        
        e.g.
        if the angle is between 0 and 90 do not rotate text angle
        if the angle is between 90 and 270 rotate text by 180
        if the angle is between 270 and 360, flip the text
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        None
        """
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        radius = self.__wedge_mid_radius(path)
        if self.__is_outmost(path):
            radius = self.__wedge_inner_radius(path)

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
        
        # to avoid the clashes with below levels, move the text further out
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

        font = {
            "family": self.chart_properties["chart_font_family"],
            "size": self.chart_properties["chart_font_size"]
        }
        
        text = self.__format_text(path)
        self.axes.text(
            mid_x,
            mid_y,
            text,
            ha=ha,
            va=va,
            rotation=rotation,
            fontdict=font,
            # bbox=self.__textbox_props(),
        )
    
    def __tangential_text(self, path: Path):
        """
        Adds a tangentially rotated annotation for the wedge corresponding to `path` to the axes
        
        e.g.
        if the angle is between 0 and 180 rotate by 90
        if the angle is 180, rotate by 180 
        if the angle is between 180 and 360, rotate by 270
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        None
        """
        theta1, theta2 = self._angles[path].theta1, self._angles[path].theta2
        angle = (theta1 + theta2) / 2
        radius = self.__wedge_mid_radius(path)
        mid_x = self.origin[0] + radius * np.cos(np.deg2rad(angle))
        mid_y = self.origin[1] + radius * np.sin(np.deg2rad(angle))

        if 0 <= angle < 180:
            rotation = angle - 90
        elif angle == 180:
            rotation = angle - 180
        elif 180 < angle < 360:
            rotation = angle - 270
        else:
            raise ValueError

        font = {
            "family": self.chart_properties["chart_font_family"],
            "size": self.chart_properties["chart_font_size"]
        }
        
        text = self.__format_text(path)
        self.axes.text(
            mid_x,
            mid_y,
            text,
            ha="center",
            va="center",
            rotation=rotation,
            fontdict=font,
            # bbox=self.__textbox_props(),
        )
    
    def __add_annotation(self, path):
        """
        Add the radial or tangential text to the wedge
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        None
        """
        angle = self._angles[path].theta2 - self._angles[path].theta1

        if not angle > self.label_minimal_angle:
            return  # no text

        if len(path) * angle > 90:
            self.__tangential_text(path)
        else:
            self.__radial_text(path)
            
    def __plot(self, setup_axes=False, interactive=False)-> None:
        """
        Combines all the necesesary preperations and add the plot to the axes
        
        Parameters
        ----------
        
        None
        
        Returns
        -------
        None
        """    
        
        if not self.wedges:
            self.__prepare_data()
        
        for path, wedge in self.wedges.items():
            self.axes.add_patch(wedge)
            self.__add_annotation(path)
        
        self.axes.autoscale()
        self.axes.set_aspect("equal")
        self.axes.autoscale_view(True, True, True)
        self.axes.axis("off")
        self.axes.margins(x=0.1, y=0.1)
            
    
    def __wedge(self, path: Path) -> Wedge:
        """
        Generates the wedges corresponding to the path
        
        Parameters
        ----------
        path: Path
        
        Returns
        -------
        Wedge
        """
        return Wedge(
            (self.origin[0], self.origin[1]),
            self.__wedge_outer_radius(path),
            self._angles[path].theta1,
            self._angles[path].theta2,
            width = self.__wedge_width(),
            label = self.__format_text(path),
            facecolor = self.__face_color(path),
            edgecolor = self.__edge_color(),
            linewidth = self.__line_width(),
            fill = True,
            alpha = 1,
        )
    
    def __customize_chart(self) -> None:
        """
        Customize title, title font family, and title font size
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        
        if self.chart_properties:
            if "title" in self.chart_properties and self.chart_properties["title"]:
                self.figure.suptitle(self.chart_properties["title"], fontsize=20)
            if self.chart_properties["title"] and self.chart_properties["title_font_family"] and self.chart_properties["title_font_size"]:
                self.figure.suptitle(self.chart_properties["title"], fontsize=self.chart_properties["title_font_size"], fontfamily=self.chart_properties["title_font_family"])