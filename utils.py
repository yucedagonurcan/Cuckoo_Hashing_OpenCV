COLORS = {"green" : "\33[92m",
          "red"   : "\33[91m",
          "yellow" : "\33[93m",
          "endc"    : "\33[0m" ,
          "bold" : '\033[1m',
          "underline" : '\033[4m'}

def print_green(msg):
    """Prints msg in green text."""
    print("{0}{1}{2}".format(COLORS["green"], msg, COLORS["endc"]))


def print_yellow(msg):
    """Prints msg in yellow text."""
    print("{0}{1}{2}".format(COLORS["yellow"], msg, COLORS["endc"]))


def print_red(msg):
    """Prints msg in red text."""
    print("{0}{1}{2}".format(COLORS["red"], msg, COLORS["endc"]))


# BOLD print functions.
def print_green_bold(msg):
    """Prints msg in green text."""
    print("{0}{1}{2}{3}".format(COLORS["green"], COLORS['bold'], msg, COLORS["endc"]))


def print_yellow_bold(msg):
    """Prints msg in yellow text."""
    print("{0}{1}{2}{3}".format(COLORS["yellow"], COLORS['bold'], msg, COLORS["endc"]))


def print_red_bold(msg):
    """Prints msg in red text."""
    print("{0}{1}{2}{3}".format(COLORS["red"], COLORS['bold'], msg, COLORS["endc"]))