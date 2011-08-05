class Link:
    # encapsulates a link type object
    def __init__(self, href, title):
        self._href = href
        self._title = title
        self.href = property(get_href, set_href)
        self.title = property(get_title, set_title)

    def get_href(self):
        return self._href

    def set_href(self, href):
        self._href = href


    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title


class Block:
    # encapsulates a block of text that will have a single filter
    # applied to it. eg. A block of markdown text or a text of python
    # code that needs to be pygmentized
    # A block is created externally. Block doesn't offer any functions
    # to decompose text into blocks.

    def __init__(self, text, _filters):
        # filters is an ordered list of filter objects that will be
        # applied to the block when it is being rendered. All filters 
        # must pass the is_filter function as defined in filters
        # module

        self._text = text

        from filters import is_filter
        self._filters = filter(is_filter, _filters)
        # this may seem confusing. It filters out any such TextFilters
        # that aren't quacking like a filter

    def render(self):
        rendered = self._text 
        for f in self._filters:
            rendered = f.apply_filter(rendered)
            # apply the filters in the order specified

        return rendered

