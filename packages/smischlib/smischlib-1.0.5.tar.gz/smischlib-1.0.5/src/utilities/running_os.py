from platform import system as snames
def running_os():
    if snames() == 'Windows': return "win"
    else: return "lin"