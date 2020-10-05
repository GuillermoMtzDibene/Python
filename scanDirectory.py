import sys, os, pprint

def normalise_path(path):
    """
    Normalises the path with os.path.normpath and then normalise the case with os.path.normcase.
    """
    return os.path.normcase(os.path.normpath(path))

def scanDirectory(directory = os.curdir, extension = '.py', in_here = True):
    """
    Find the largest file with a given extension in a given directory if in_here is true (default).
    Else search the entire directory starting in the passed directory.
    """
    visited = set()
    allsizes = []
    if in_here:
        os.chdir(directory)
        allsizes = [(os.path.getsize(f), normalise_path(os.path.join(directory, f))) for f in os.listdir('.') if os.path.isfile(f)] #Get all files in the CWD with the correct extension
        allsizes = [(size, file) for (size, file) in allsizes if file.endswith(extension)]
        visited = {directory: True} #The CWD is the only directory visited
    else:
        for (thisDir, subDir, filesHere) in os.walk(directory): #walk through the subdirectories of directory, starting in directory
            fixcase = normalise_path(thisDir)
            if fixcase in visited: #if a directory has already been visited, ignore it
                continue
            else:
                visited.add(fixcase)
            for filename in filesHere:
                if filename.endswith(extension):
                    path = os.path.join(thisDir, filename)
                    try:
                        size = os.path.getsize(path)
                    except os.error:
                        print('skipping', path, sys.exc_info()[0])
                    else:
                        allsizes.append((size, path))
    allsizes.sort()
    return (visited, allsizes)
