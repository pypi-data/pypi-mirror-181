from colorama import Fore, Style
from pathlib import Path

def color_str(string, color='cyan', bold=True):
    r"""Returns stylized string with coloring and bolding for printing.
    
    Example::
    
        >>> print(color_str('lagom', 'green', bold=True))
        
    Args:
        string (str): input string
        color (str): color name
        bold (bool, optional): if ``True``, then the string is bolded. Default: ``False``
    
    Returns:
        out: stylized string
    
    """
    if isinstance(string, Path): string = string.as_posix()
    elif isinstance(string, (float, int)): string = str(string)
    colors = {'red': Fore.RED, 'green': Fore.GREEN, 'blue': Fore.BLUE, 'cyan': Fore.CYAN, 
              'magenta': Fore.MAGENTA, 'black': Fore.BLACK, 'white': Fore.WHITE}
    style = colors[color]
    if bold:
        style += Style.BRIGHT
    out = style + string + Style.RESET_ALL
    return out