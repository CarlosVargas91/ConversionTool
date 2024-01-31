# Class to allow printing warnings and errors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# Function to print header
def printHeader(msg):
    print(bcolors.OKCYAN + msg + bcolors.ENDC)

# Function to print info
def printInfo(msg, sameLine=False):
    if sameLine:
        print('\r   ' + msg, end ='', flush = True)
    else:
        print('   ' + msg)

# Function to print a success
def printSuccess(msg):
    print('   ' + bcolors.OKGREEN + msg + bcolors.ENDC)

# Function to print a warning
def printWarning(msg):
    print('   ' + bcolors.WARNING + msg + bcolors.ENDC)

# Function to print a error
def printError(msg):
    print('   ' + bcolors.FAIL + msg + bcolors.ENDC)