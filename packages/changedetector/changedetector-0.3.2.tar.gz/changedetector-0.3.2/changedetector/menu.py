import sys
import inquirer
from colors import Colors
def menu(options:list, title:str, key:str):
    """
    A simple menu for the user to choose from.
    :param options: The options the user can choose from.
    :param title: The title of the menu.
    :return: The option the user chose.
    """
    try:
        res = inquirer.prompt(
            [
                inquirer.List(
                    key,
                    message=title,
                    choices=options,
                    carousel=True
                )
            ]
        )[key]

    except Exception as e:
        print(f"{Colors.BOLD}{Colors.RED}An error occured: {e}{Colors.END}")
        print(f"\n{Colors.BOLD}{Colors.GREEN}Program Exited{Colors.END}")
        sys.exit(1)
    return res

if __name__ == "__main__":
    MODE = menu(["Watch and Run Self (WRS)", "Watch and Run Other (WRO)"],
            "Choose the mode you want to use", "mode")
    print(MODE)

