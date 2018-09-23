class RSSResponse:
    def __init__(self, title, items, paginations=None):
        self._title = title
        self._items = items
        self._paginations = paginations

    def title(self):
        return self._title

    def items(self):
        return self._items

    def paginations(self):
        return self._paginations