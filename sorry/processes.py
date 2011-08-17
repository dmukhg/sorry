def list_of_files(directory):
    # returns a list of files open for reading
    # from within a argumented directory
    import os
    ls = os.listdir(directory)
    return [ open(os.path.join(directory, fname)) for fname in ls ]

def post_from_file(fileobject):
    # parses metadata from file, creaates a new Post object and
    # returns it. 
    def parse_meta_data(data):
        # parses metadata in the form key:value\nkey2:value2
        rtn = {}
        for line in data.split('\n'):
            if len(line.split(':', 1)) is 2:
                # to escape \n s from being parsed
                k, v = [ _.strip() for _ in line.split(':', 1) ]
                rtn[k] = v
        return rtn

    from objects import Post

    filetext = fileobject.read().split('\n---\n')
    text = filetext[1]
    metadata = parse_meta_data(filetext[0])
    
    return Post(text, metadata)


def render_html(posts, title, footlinks, template):
    # takes a list of post objects a title, 2 footlinks and the
    # template and converts it all into a full HTML string ready
    # to be written to a file.

    from mako.runtime import Context
    from StringIO import StringIO
    
    buff = StringIO()
    ctx = Context(buff, posts = posts, title = title, footlinks = footlinks)

    template.render_context(ctx)

    return buff.getvalue()


def create_indices(directory):
    # creates a dictionary of entire html pages that are indices. the
    # key serves as the name of the file for eg, index or page-2
    # while the values are complete HTML strings that can be written
    # straight away to files.

    # the directory argument must be a filepath to the directory
    # containing the posts
    
    ls = list_of_files(directory)
    posts = [ post_from_file(fobj) for fobj in ls ]

    posts_count = len(posts)


