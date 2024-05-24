from imports import *
from directory import *
from defs import *
from constants import *
from files import *

def modify_grub_file(source_files_dir):
    grub_file_path = os.path.join(source_files_dir, "boot/grub/grub.cfg")
    with open(grub_file_path, 'r') as file:
        grub_content = file.readlines()

    for i in range(len(grub_content)):
        if "set menu_color_normal" in grub_content[i]:
            grub_content[i] = grub_content[i].replace("white", "yellow")
        if "set menu_color_highlight" in grub_content[i]:
            grub_content[i] = grub_content[i].replace("light-gray", "yellow")

    new_menuentry = """menuentry "DonCom Ubuntu Server" {
        set gfxpayload=keep
        linux   /casper/vmlinuz quiet autoinstall ds=nocloud\\;s=/cdrom/server/ ---
        initrd  /casper/initrd
}\n"""
    for i in range(len(grub_content)):
        if grub_content[i].startswith("menuentry"):
            grub_content.insert(i, new_menuentry)
            break

    with open(grub_file_path, 'w') as file:
        file.writelines(grub_content)

    print(f"{COLOR_GREEN}Archivo 'grub.cfg' modificado correctamente.{COLOR_RESET}")


def copy_meta_to_user_data(server_dir):
    meta_data_path = os.path.join(server_dir, "meta-data")
    user_data_path = os.path.join(server_dir, "user-data")
    
    try:
        with open(meta_data_path, 'r') as meta_file:
            content = meta_file.read()
        
        with open(user_data_path, 'w') as user_file:
            user_file.write(content)
        
        print(f"{COLOR_GREEN}Archivo 'meta-data' copiado a 'user-data' en '{user_data_path}'.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_RED}Error al copiar 'meta-data' a 'user-data': {e}{COLOR_RESET}")
        sys.exit(1)
