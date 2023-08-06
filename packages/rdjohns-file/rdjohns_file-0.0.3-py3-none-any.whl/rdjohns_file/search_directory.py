import os
def getDirectories(url:str =""):
    if os.path.isdir(url) and len(url)>0:
        os.chdir(url)
    parent = []
    data = os.listdir()
    for filename in data:
        if os.path.isdir(filename):
            parent += [filename]
    return parent


def getDataDirectory(data: list ):
    parent_, res = [], []
    for filename in data:
        if os.path.isdir(filename):
            os.chdir(filename)
            parent_ = getDirectories()
            for item in parent_:
                res +=[filename+'/'+item]
            for i in range(len(filename.split('/'))):
                os.chdir('..')
    return res

def getAllDirectory(inc: int = 10, racine: str =""):
    """Get all directory of deep inc and with racine location

    Args:
        inc (int, optional): Number of deep. Defaults to 10.
        racine (str, optional): Location start. Defaults to "".

    Returns:
        list: list directory name
    """
    data1 = getDirectories(racine)
    resultat = []

    while inc >0:
        data1 = getDataDirectory(data1)
        resultat += data1
        inc -=1
    return resultat
