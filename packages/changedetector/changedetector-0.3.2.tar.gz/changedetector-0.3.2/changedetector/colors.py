class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    GRAY = '\033[0;49;90m'
    WHITE = '\033[97m'

    @staticmethod
    def clr(text, color, bold=False):
        if bold:
            return f"{color}{Colors.BOLD}{text}{Colors.END}"
        else:
            return f"{color}{text}{Colors.END}"

    @staticmethod
    def bold(text, color=None):
        if color:
            return Colors.clr(text, color, bold=True)
        else:
            return Colors.clr(text, Colors.WHITE, bold=True)

    @staticmethod
    def underline(text, color=None):
        if color:
            return f"{color}{Colors.UNDERLINE}{text}{Colors.END}"
        else:
            return f"{Colors.UNDERLINE}{text}{Colors.END}"
