
class b_Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




def print_yellow(x):
    print(b_Colours.WARNING, x, b_Colours.ENDC)

def print_red(x):
    print(b_Colours.FAIL, x, b_Colours.ENDC)

def print_result(x):
    print(b_Colours.WARNING, x, b_Colours.BOLD)

def print_error(x):
    print(b_Colours.FAIL, x, b_Colours.BOLD)

