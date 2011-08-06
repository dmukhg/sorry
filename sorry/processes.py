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


