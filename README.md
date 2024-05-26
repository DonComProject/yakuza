# 🕵️‍♂️ Yakuza

## Description
Yakuza is a tool designed to automate the customization and creation of a customized Ubuntu ISO. It downloads the base Ubuntu ISO, extracts it, modifies configuration files, and creates a new ISO with the desired changes.

## Features
- 📥 Downloads the base Ubuntu ISO if it's not already downloaded.
- 📦 Extracts the ISO and performs modifications.
- 🛠 Modifies configuration files like `grub.cfg` and creates `user-data` and `meta-data` files for cloud-init.
- 🏗 Builds a new ISO with the customized configurations.

## Usage
To use Yakuza, simply run the `yakuza.py` script. It will guide you through the process of customizing and creating your Ubuntu ISO.

```bash
python3 yakuza.py
```

## Installation
There's no installation required for Yakuza. Simply clone the repository and run the `yakuza.py` script.

## License
Yakuza is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
