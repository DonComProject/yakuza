import argparse
from imports import *
from files import *
from directory import *
from defs import *
from constants import *

def main():
    """
    Entry point of the Yakuza program.
    Performs various tasks to create a customized Ubuntu ISO.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Crear una ISO personalizada de Ubuntu.")
    parser.add_argument("-g", "--gui", choices=[
        "ubuntu-desktop",
        "xubuntu-desktop",
        "lubuntu-desktop",
        "ubuntu-mate-desktop",
        "cinnamon-desktop-environment",
        "ubuntu-budgie-desktop"
    ], default="ubuntu-desktop", help="Selecciona el entorno de escritorio para {gui}")
    args = parser.parse_args()

    print(f"{COLOR_YELLOW}Iniciando programa Yakuza...{COLOR_RESET}")

    # Crear directorio principal yakuza
    yakuza_dir = create_yakuza_directory()

    # Crear directorio .config dentro de yakuza y descargar ISO si no existe
    create_config_directory()
    download_iso()

    # Verificar si 7z está instalado
    check_7z_installed()

    # Crear directorio yakuza-diaHora-version
    version_dir = create_yakuza_version_directory(yakuza_dir)

    # Extraer ISO en el directorio creado
    extract_iso(version_dir)

    # Mover la carpeta '[BOOT]'
    move_boot_directory(version_dir)

    # Modificar grub.cfg
    source_files_dir = os.path.join(version_dir, "source-files")
    modify_grub_file(source_files_dir)

    # Crear directorio server
    server_dir = create_server_directory(source_files_dir)

    # Crear archivo de instalación automática con el entorno de escritorio seleccionado
    create_auto_install_file(server_dir, args.gui)
    create_meta_data_file(server_dir, args.gui)

    # Copiar user-data a meta-data
    copy_meta_to_user_data(server_dir)

    # Crear la ISO final
    iso_name = f"ubuntu-22.04-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    build_iso(source_files_dir, iso_name)

    print(f"{COLOR_GREEN}Proceso completado.{COLOR_RESET}")

if __name__ == "__main__":
    main()

