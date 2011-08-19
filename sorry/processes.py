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


def create_indices(directory, sitename, template):
    # creates a dictionary of entire html pages that are indices. the
    # key serves as the name of the file for eg, index or page-2
    # while the values are complete HTML strings that can be written
    # straight away to files.

    # the directory argument must be a filepath to the directory
    # containing the posts
    from objects import Link 
    
    posts_per_index = 3
    # reflects the number of posts that will be in each index

    ls = list_of_files(directory)
    posts = [ post_from_file(fobj) for fobj in ls ]
    posts.sort(key = lambda post : post.uid)

    remaining_post_count = len(posts)
     
    index_map = {}
    
    def _decompose(posts, posts_per_index):
        while (posts):
            yield posts[:posts_per_index]
            posts = posts[posts_per_index:]
     
    k = "index"
    i = 1
    for few_posts in _decompose(posts, posts_per_index) :
        remaining_post_count -= posts_per_index
        # keeps track of the number of posts remaining in the post
        # stack

        # will now construct the links and title etc.
        title = sitename 
        template = template

        # footlink generation requires knowledge of remaining posts
        footlinks = [Link("", ""), Link("", "")] # degenerate case

        if i == 1:
            footlinks[0] = Link("", "")
        elif i == 2:
            footlinks[0] = Link("index", "newer")
        else :
            footlinks[0] = Link("page-%d" %(i-1), "newer")
        if remaining_post_count > 0:
            footlinks[1] = Link("page-%d" %(i+1), "older")

        # footlink generation complete

        if i > 1:
            k = "page-%d" %i

        index_map[k] = render_html(few_posts, title, footlinks, template)

        # update keys for the index map
        i += 1 

    return index_map

