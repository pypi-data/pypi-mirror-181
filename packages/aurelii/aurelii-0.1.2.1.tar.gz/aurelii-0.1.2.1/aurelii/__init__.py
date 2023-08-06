import aopen
def readme():
    with aopen('README.rst', 'r') as f:
        return f.read()

def info():
    '''Prints info for Aurelii package'''
    print("This is the Python package for Aurelii.")