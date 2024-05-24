from imports import *
from files import *
from constants import *
from directory import *
from defs import *



def download_iso():
    if not os.path.exists(ISO_PATH):
        print(f"{COLOR_YELLOW}Descargando ISO...{COLOR_RESET}")
        subprocess.run(["wget", "-O", ISO_PATH, ISO_URL], check=True)
        print(f"{COLOR_GREEN}ISO descargado y almacenado en {ISO_PATH}.{COLOR_RESET}")
    else:
        print(f"{COLOR_GREEN}ISO ya descargado previamente en {ISO_PATH}.{COLOR_RESET}")

def check_7z_installed():
    try:
        subprocess.run(["7z"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{COLOR_GREEN}7z está instalado.{COLOR_RESET}")
    except FileNotFoundError:
        print(f"{COLOR_YELLOW}7z no está instalado. Instálalo e inténtalo de nuevo.{COLOR_RESET}")
        sys.exit(1)


def extract_iso(version_dir):
    source_files_dir = os.path.join(version_dir, "source-files")
    os.makedirs(source_files_dir)
    print(f"{COLOR_YELLOW}Extrayendo ISO en '{source_files_dir}'...{COLOR_RESET}")
    subprocess.run(["7z", "x", ISO_PATH, f"-o{source_files_dir}", "-y"], check=True)
    print(f"{COLOR_GREEN}ISO extraído en '{source_files_dir}'.{COLOR_RESET}")


def create_auto_install_file(server_dir, gui_option):
    config_content = f"""#cloud-config
autoinstall:
  version: 1
  identity:
    hostname: doncom
    username: admin
    password: $6$A8TPSoM/hhcc6jkv$5WAmDVk6JP0xj76DmeO711VC2grPZJAXmS88tiG13kowziCM1U0zZKNPkMhPv3HiSNV6c2JslSpsfA.UbmlQV1
  storage:
    layout:
      name: direct
  ssh:
    install-server: yes
  locale: es_ES.UTF-8
  keyboard: {{layout: es, variant: ''}}
  packages:
    - {gui_option}
  user-data:
    packages:
    - dbus-x11
    runcmd:
     - wget https://github.com/DonComProject/arenita/raw/main/src/deb-files/veyon_4.8.3.0-ubuntu.jammy_amd64.deb -O /tmp/veyon.deb
     - dpkg -i /tmp/veyon.deb
     - apt-get install -f -y
     - wget https://raw.githubusercontent.com/DonComProject/arenita/main/img/doncom_banner.jpg -O /usr/share/backgrounds/doncom_banner.jpg
     - sudo -u admin dbus-launch gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/backgrounds/doncom_banner.jpg'
"""
    with open(os.path.join(server_dir, "user-data"), 'w') as file:
        file.write(config_content)

    print(f"{COLOR_GREEN}Archivo de configuración 'user-data' creado automáticamente.{COLOR_RESET}")

def create_personalized_install_file(server_dir, gui_option):
    hostname = input("Introduce el hostname: ")
    username = input("Introduce el nombre de usuario: ")
    password = input("Introduce la contraseña: ")
    encrypted_password = subprocess.run(
        ["openssl", "passwd", "-6", password], capture_output=True, text=True).stdout.strip()

    config_content = f"""#cloud-config
autoinstall:
  version: 1
  identity:
    hostname: {hostname}
    username: {username}
    password: {encrypted_password}
  storage:
    layout:
      name: direct
  ssh:
    install-server: yes
  locale: es_ES.UTF-8
  keyboard: {{layout: es, variant: ''}}
  packages:
    - {gui_option}
"""
    with open(os.path.join(server_dir, "user-data"), 'w') as file:
        file.write(config_content)

    print(f"{COLOR_GREEN}Archivo de configuración 'user-data' personalizado creado.{COLOR_RESET}")

def create_meta_data_file(server_dir, gui_option):
    # URL base para los archivos meta-data
    base_url = "https://raw.githubusercontent.com/DonComProject/arenita/main/src/iso-conf/meta-data"

    # Obtener la lista de versiones disponibles
    meta_data_list_url = f"{base_url}/000"
    try:
        response = requests.get(meta_data_list_url)
        response.raise_for_status()
        versions = response.text.splitlines()
    except requests.exceptions.RequestException:
        print(f"{COLOR_RED}Error al obtener la lista de versiones disponibles.{COLOR_RESET}")
        sys.exit(1)

    # Mostrar las versiones disponibles
    print("Versiones disponibles:")
    for i, version in enumerate(versions, start=1):
        print(f"{i}. {version}")

    # Solicitar al usuario que seleccione una versión
    selected_version_index = input("Selecciona el número de la versión de meta-data: ").strip()
    try:
        selected_version_index = int(selected_version_index)
        if selected_version_index < 1 or selected_version_index > len(versions):
            raise ValueError
    except ValueError:
        print(f"{COLOR_YELLOW}Número de versión no válido. Saliendo del programa.{COLOR_RESET}")
        sys.exit(1)

    selected_version = versions[selected_version_index - 1]

    # Construir la URL completa para el archivo meta-data seleccionado
    meta_data_url = f"{base_url}/{selected_version}"

    # Ruta al archivo meta-data local
    meta_data_path = os.path.join(server_dir, "meta-data")

    # Descargar el archivo meta-data
    print(f"{COLOR_YELLOW}Descargando 'meta-data' desde {meta_data_url}...{COLOR_RESET}")
    try:
        response = requests.get(meta_data_url)
        response.raise_for_status()
        with open(meta_data_path, 'w') as file:
            file.write(response.text)
        print(f"{COLOR_GREEN}Archivo 'meta-data' descargado y almacenado en '{meta_data_path}'.{COLOR_RESET}")
    except requests.exceptions.RequestException:
        print(f"{COLOR_RED}Error al descargar el archivo 'meta-data'.{COLOR_RESET}")
        sys.exit(1)

    # Leer el contenido del archivo meta-data
    with open(meta_data_path, 'r') as file:
        content = file.read()

    # Reemplazar las variables
    content = content.replace("{hostname}", "doncom")
    content = content.replace("{username}", "admin")
    
    # Encriptar la contraseña 'davidtomas'
    encrypted_password = subprocess.run(["openssl", "passwd", "-6", "davidtomas"], capture_output=True, text=True).stdout.strip()
    content = content.replace("{password}", encrypted_password)

    # Reemplazar {gui} si se proporcionó la opción -g
    if gui_option:
        content = content.replace("{gui}", gui_option)

    # Guardar el archivo modificado
    with open(meta_data_path, 'w') as file:
        file.write(content)

    print(f"{COLOR_GREEN}Archivo 'meta-data' modificado y guardado en '{meta_data_path}'.{COLOR_RESET}")



def build_iso(source_files_dir, iso_name):
    iso_output_path = os.path.join(os.path.dirname(source_files_dir), f"{iso_name}.iso")
    boot_dir = os.path.join(os.path.dirname(source_files_dir), "BOOT")
    os.chdir(source_files_dir)
    subprocess.run([
        "xorriso", "-as", "mkisofs", "-r",
        "-V", "Ubuntu 22.04 LTS AUTO (EFIBIOS)",
        "-o", iso_output_path,
        "--grub2-mbr", os.path.join(boot_dir, "1-Boot-NoEmul.img"),
        "-partition_offset", "16",
        "--mbr-force-bootable",
        "-append_partition", "2", "28732ac11ff8d211ba4b00a0c93ec93b", os.path.join(boot_dir, "2-Boot-NoEmul.img"),
        "-appended_part_as_gpt",
        "-iso_mbr_part_type", "a2a0d0ebe5b9334487c068b6b72699c7",
        "-c", "/boot.catalog",
        "-b", "/boot/grub/i386-pc/eltorito.img",
        "-no-emul-boot", "-boot-load-size", "4", "-boot-info-table",
        "--grub2-boot-info",
        "-eltorito-alt-boot",
        "-e", "--interval:appended_partition_2:::",
        "-no-emul-boot", "."
    ], check=True)
    print(f"{COLOR_GREEN}ISO creada en '{iso_output_path}'.{COLOR_RESET}")
