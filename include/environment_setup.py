# In this, we create all the folders necessary to recreate our desired portage filestructure.
def create_output_directory_structure(filepaths : List[str]):
    for fpath in filepaths: 
        #if debug:
        print('File ' + fpath)
        expanded_fpath = fpath.split('/')
        #if debug:
        print(expanded_fpath)
        print('Expanded fpath (list) length = ' + str(len(expanded_fpath)))
        prefix = output_path
        if len(expanded_fpath) > 1: # If we're still considering a directory and not a file
            #if debug:
            print('Going deeper into the filestructure') # TODO: Make more sense
            for p in expanded_fpath: # The last element is the filename itself
                prefix += '/'
                prefix += p
                print('prefix = ' + prefix)
                if not os.path.isdir(prefix):
                    #if debug:
                    print('Making directory ' + prefix)
                    os.mkdir(prefix) # Now we finally make our directory. Is there a better way to do this???
