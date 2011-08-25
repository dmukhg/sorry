import os
from mako.template import Template

from processes import *
from objects import Link

def cleardirectory(directory):
    # clears the non-hidden contents of the supplied directory
    import subprocess

    try:
        command = 'rm -rf %s/*' %directory
        subprocess.call(command, shell=True)
    except OSError:
        print "Error executing %s" %command
        raise SystemExit

def mediacopy(source, destination):
    # copies the contents of source directory to a destination
    # directory. This creates the destination directory if required
    # and then copies all the files. eg. mediacopy('a', 'b') will copy
    # all files *within* a to a folder named 'b'
    import subprocess
    import os 

    try:
        os.makedirs(destination)
        # try to create the destination directory
    except OSError:
        pass # Already exists. nothing to do
    
    try:
        command = 'cp -rf %s/* %s' %(source, destination)
        subprocess.call(command, shell=True)
    except:
        print "Error executing %s" %command
        raise SystemExit

def sitegen(directory, sitename = "Posts"):
    # sitegen takes a single directory path as an argument and spews
    # out complete deployable directories in the deploy sub-directory 
    # of the calling directory. Uses template 'base.html' from the
    # layout sub-directory.

    # declare and initialize the variables
    deploy_dir = os.path.join(directory, 'deploy')
    posts_dir = os.path.join(directory, 'posts')
    layout_dir = os.path.join(directory, 'layout')

    try:
        os.makedirs(deploy_dir)
        print "Created deploy dir in : %s" %deploy_dir
        # create the deploy_dir in case it doesn't exist
    except OSError:
        # Already exists
        print "Deploy dir already exists in : %s" %deploy_dir 
    
    try:
        layout_file = open(os.path.join(layout_dir, 'base.html'))
        base_template = Template(layout_file.read())
        # try to open the base.html template
    except IOError:
        # There is no such file. 
        print "No template named 'base.html' in %s" % layout_dir
        raise SystemExit

     
    # initialize deploy sub-directories  
    archive_dir = os.path.join(deploy_dir, 'archive')
    page_dir = os.path.join(deploy_dir, 'pages')

    try:
        os.makedirs(archive_dir)
        print "Created archive dir in : %s" %archive_dir
        # create the archive_dir in case it doesn't exist
    except OSError:
        # Already exists
        print "Archive dir already exists in : %s" %archive_dir

    try:
        os.makedirs(page_dir)
        print "Created standalone post dir in : %s" %page_dir
        # create the archive_dir in case it doesn't exist
    except OSError:
        # Already exists
        print "Standalone post dir already exists in : %s" %page_dir
    



    """Begin generating indices"""
    # generate the indices via the processes.create_indices function
    index_map = create_indices(posts_dir, sitename, base_template)

    for key in index_map:
        # the return value of create_indices, if you remember is a
        # dictionary. The keys of this dict are filenames like index,
        # page-2 etc. the values of this dict are complete rendered
        # HTML strings ready to be written to files.
        filename = os.path.join(deploy_dir, '%s.html' %key)
        fhandle = open(filename, 'w') # create a handle for the file

        fhandle.write(index_map[key])
        fhandle.close()
        # write to and close the file handle
        # with this, the generation of indices is done.

    
    """Begin Generating archive"""
    # now, to generate the archive entries.
    all_posts = [post_from_file(_) for _ in  list_of_files(posts_dir)]
    posts = filter(lambda post : not post.page, all_posts)
    # creates a list of posts using the list_of_files and
    # post_from_file functions of the processes module.
    posts.sort(key = lambda post : post.uid )
    posts.reverse()
    # this sorts the posts so that prev next links work like they
    # should

    for post in posts:
        filename = os.path.join(archive_dir, "%s.html" %post.uid)
        fhandle = open(filename, 'w')
    
        # in this block, the variables with names starting with c_ are
        # contextual pertaining to the currently processed post file
        c_posts = [post]
        c_title = post.title
        c_link_prev = Link("", "") # degenerate case
        c_link_next = Link("", "") # degenerate case

        if posts.index(post) != 0:
            # this isn't the first post
            prev_post = posts[posts.index(post) - 1]
            prev_post_location = "%s.html" %prev_post.uid
            c_link_prev = Link(prev_post_location, prev_post.title)

        if posts.index(post) != ( len(posts) - 1 ):
            # this isn't the last post
            next_post = posts[posts.index(post) + 1]
            next_post_location = "%s.html" %next_post.uid
            c_link_next = Link(next_post_location, next_post.title)

        c_footlinks = [c_link_prev, c_link_next]

        fhandle.write(render_html(c_posts, c_title, c_footlinks, base_template))
        fhandle.close()

    """ Begin generating standalones """
    pages = filter(lambda post : post.page, all_posts)

    for page in pages:
        filename = os.path.join(page_dir, "%s.html" %page.uid)
        fhandle = open(filename, 'w')
        
        # in this block, the variables with names starting with c_ are 
        # contextual pertaining to the currently processed page
        c_page = [page]
        c_title = page.title
        c_footlinks = [Link("", ""),
                       Link("", "")]

        fhandle.write(render_html(c_page, c_title, c_footlinks, base_template))
        fhandle.close()
