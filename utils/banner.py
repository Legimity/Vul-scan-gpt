import random
from termcolor import colored

banner_1 = colored(
    """          
██╗   ██╗██╗   ██╗██╗      ███████╗ ██████╗ █████╗ ███╗   ██╗       ██████╗ ██████╗ ████████╗
██║   ██║██║   ██║██║      ██╔════╝██╔════╝██╔══██╗████╗  ██║      ██╔════╝ ██╔══██╗╚══██╔══╝
██║   ██║██║   ██║██║█████╗███████╗██║     ███████║██╔██╗ ██║█████╗██║  ███╗██████╔╝   ██║   
╚██╗ ██╔╝██║   ██║██║╚════╝╚════██║██║     ██╔══██║██║╚██╗██║╚════╝██║   ██║██╔═══╝    ██║   
 ╚████╔╝ ╚██████╔╝███████╗ ███████║╚██████╗██║  ██║██║ ╚████║      ╚██████╔╝██║        ██║   
  ╚═══╝   ╚═════╝ ╚══════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝       ╚═════╝ ╚═╝        ╚═╝ 
                      """,
    "cyan",
)

banner_2 = colored(
    r"""
                                +---------------+
 How to find vulnerabilities?   | vul-scan-gpt  |
                                +---------------+ 
  (╯▔＾▔)╯                        \ (•◡ •) / 
   \   |                            |   /
￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣""",
    "yellow",
)


def banner():
    o_o = random.choice(range(10))
    if o_o < 9:
        return banner_1
    else:
        return banner_2


if __name__ == "__main__":
    print(banner())
