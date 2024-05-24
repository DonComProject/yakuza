from imports import *
from defs import *

COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_LIGHT_PURPLE = "\033[95m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

ISO_URL = "https://cdimage.ubuntu.com/ubuntu-server/jammy/daily-live/current/jammy-live-server-amd64.iso"
CONFIG_DIR = os.path.expanduser("~/yakuza/.config")
ISO_PATH = os.path.join(CONFIG_DIR, "jammy-live-server-amd64.iso")
