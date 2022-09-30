from chart.sunburst import Sunburst
from chart.treemap import Treemap

class ChartGenerator:
    def __init__(self):
        self.chart_type = None
        self.file_obj = None

    def generate_chart(self, chart_type, data):
        figure = None
        match chart_type:
            case "Treemap":
                treemap = Treemap(data)
                figure = treemap.get_figure()
            case "Sunburst":
                sunburst = Sunburst(data)
                figure = sunburst.get_figure()
        return figure
