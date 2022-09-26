class BaseChart:
    def __init__(self, data):
        self.data = data
        self.figure = None

    def get_figure(self):
        return self.figure