from os import name as osnam
def running_os():
    if osnam() == 'nt': return "win"
    else: return "lin"
