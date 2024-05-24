
from imports import *
from directory import *
from defs import *
from constants import *
from files import *

def create_yakuza_directory():
    yakuza_dir = os.path.expanduser("~/yakuza")
    if not os.path.exists(yakuza_dir):
        os.makedirs(yakuza_dir)
        print(f"{COLOR_GREEN}Directorio 'yakuza' creado en el hogar del usuario.{COLOR_RESET}")
    return yakuza_dir

def create_config_directory():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        print(f"{COLOR_GREEN}Directorio '.config' creado dentro de 'yakuza'.{COLOR_RESET}")

def create_yakuza_version_directory(yakuza_dir):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    version_dir = os.path.join(yakuza_dir, f"yakuza-{now}-version")
    os.makedirs(version_dir)
    print(f"{COLOR_GREEN}Directorio '{version_dir}' creado.{COLOR_RESET}")
    return version_dir

def move_boot_directory(version_dir):
    source_files_dir = os.path.join(version_dir, "source-files")
    boot_source = os.path.join(source_files_dir, "[BOOT]")
    boot_target = os.path.join(version_dir, "BOOT")
    if os.path.exists(boot_source):
        os.rename(boot_source, boot_target)
        print(f"{COLOR_GREEN}Carpeta '[BOOT]' movida a '{boot_target}'.{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}Carpeta '[BOOT]' no encontrada.{COLOR_RESET}")
        
def create_server_directory(source_files_dir):
    server_dir = os.path.join(source_files_dir, "server")
    os.makedirs(server_dir)
    print(f"{COLOR_GREEN}Directorio 'server' creado en '{source_files_dir}'.{COLOR_RESET}")
    return server_dir

