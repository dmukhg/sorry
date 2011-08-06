
def is_filter(apparent_filter):
    # this function checks whether the apparent_filter quacks like a
    # filter or not. I am not sure whether this is the right way to go
    # to implement a "interface" like Class in python but I am so hung
    # up on three months of java coding that I find interfaces
    # necessary.
    #
    # In any way, this is better than not having any check at all or
    # the AbstractBaseClass way. I found the syntax ugly.
    # http://docs.python.org/library/abc.html

    # TODO  
    if hasattr(apparent_filter, "apply_filter"):
        return True
    else:
        return False


class MarkdownFilter:
    # A filter that converts markdown text into html.
    def __init__(self):
        pass

    def apply_filter(self, text):
       import markdown 
       return markdown.markdown(text)

class PygmentsFilter:
    # converts code into formatted html using the language argument
    # passed in the constructor
    def __init__(self, language=None):
        self._language = language

    def apply_filter(self, text):
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments import lexers

        try:
            lexer = getattr(lexers, "%sLexer" %(self._language.capitalize()) )
        except AttributeError:
            print "That is a weird language to code in: %s" %(self._language)
            raise SystemExit

        return highlight(text, lexer(), HtmlFormatter())
