from filters import *

class Link:
    # encapsulates a link type object
    def __init__(self, href, title):
        self._href = href
        self._title = title

    def get_href(self):
        return self._href

    def set_href(self, href):
        self._href = href

    href = property(get_href, set_href)

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    title = property(get_title, set_title)

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
        # TODO this doesn't notify on a filter being a wrong filter

    def render(self):
        rendered = self._text 
        for f in self._filters:
            rendered = f.apply_filter(rendered)
            # apply the filters in the order specified

        return rendered


class Post:
    # encapsulates a post mostly consists of an ordered list of blocks
    # and some metadata the uid must be a number. This makes it easy
    # to identify and order. No date-fu required.

    def __init__(self, text, metadata):
        self._text = text
        self.feed_meta_data(metadata)

    def decompose(self):
        lines = self._text.split('\n')

        def _internal_block(content):

            """
            Possible algorithm for decomposing:
             > have an empty buffer.
             > set buffer_type to default ( buffer_filter is Markdown or
               Pygments)
             > for each line
                > if line has no marker, add to buffer.
                > if line has ::code marker, yied and clear previous 
                  buffer and set buffer_filter to the ::code language
                > if line has ::endcode marker, yield and clear
                  previous buffer set buffer_filter to default
             > yield the final buffer
            """
            DEFAULT_FILTER = MarkdownFilter()

            block_buffer = ""
            block_filter = DEFAULT_FILTER

            for line in content:
                if not line.startswith("::"):
                    block_buffer += '\n'+ line
                if line.startswith("::code"):
                    if not block_buffer == "":
                        # sometimes, when a code block succeeds
                        # another code block, we need to ensure that
                        # an empty markdown block isn't yielded
                        yield Block(block_buffer, [block_filter])
                    block_buffer = ""
                    language = line.rsplit(":", 1)[1]
                    block_filter = PygmentsFilter(language)
                if line.startswith("::endcode"):
                    yield Block(block_buffer, [block_filter])
                    block_buffer = ""
                    block_filter = DEFAULT_FILTER 
            
            if not block_buffer == "":
                # do not yield an empty block
                yield Block(block_buffer, [block_filter])

        
        blocks = [ _ for _ in _internal_block(lines)]
        return blocks

    def render(self):
        blocks = self.decompose()
        rendered = ""

        for block in blocks:
            rendered += block.render()

        return rendered

    def feed_meta_data(self, metadata):
        self.uid = metadata['uid']
        self.date = metadata['date']
        self.author = metadata['author']
        self.title = metadata['title']
        self.draft = metadata['draft']
        try:
            self.page = metadata['page']
            self.page = True
        except KeyError:
            self.page = False


class Page:
    # Represents the contents of an actual page. Responsible for
    # creating the Post objects for any page and also for rendering
    # the final HTML. Will not do any file-handling. That should be
    # handled by specialized functions. There will be however,
    # considerable number of init arguments. There is a lot of
    # metadata around.

    def __init__(self, posts = [], title = "", footlinks = []):
        # create the context right away.
        from mako.runtime import Context
        from StringIO import StringIO

        self.buffered = StringIO()

        self.context = Context(self.buffered,  
                                posts = posts,
                                title = title,
                                footlinks = footlinks)

    def render(template):
        if template is None:
            print "No template provided"
            raise SystemExit

        template.render(self.context)
        return self.buffered.getvalue()

