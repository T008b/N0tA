import os
import re
import time
import shutil
import platform
import sys


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

plist_path = "/rootfs/var/mobile/Library/Application Support/Flex3/patches.plist"
txt_path = "/rootfs/var/mobile/Library/Application Support/Flex3/patches.txt"
verbose_folder = "/var/mobile/N0tA/_verboseIndex/"
info_file = os.path.join(verbose_folder, "_infoplist")
read_puaf_file = os.path.join(verbose_folder, "_readPuafPages")
status_puaf_file = os.path.join(verbose_folder, "_statusPuaf")
apps_bundles_file = os.path.join(verbose_folder, "_AppsBundles")
_installedx = "/var/mobile/N0tA/_installed.jjK"


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

if not os.path.exists(verbose_folder):
    os.makedirs(verbose_folder)
    with open(info_file, 'w'): pass
    with open(read_puaf_file, 'w'): pass
    with open(status_puaf_file, 'w'): pass
    with open(apps_bundles_file, 'w'): pass


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

apps_bundles = {}
if os.path.exists(apps_bundles_file):
    with open(apps_bundles_file, 'r') as file:
        for line in file:
            bundle, app_name = line.strip().split('=')
            apps_bundles[bundle] = app_name


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

default_bundles = {
    "net.whatsapp.WhatsApp": "WhatsApp",
    "ph.telegra.Telegraph": "Telegram",
    "com.google.ios.youtube": "YouTube",
    "net.whatsapp.WhatsAppSMB": "WA Business",
    "com.tigisoftware.Filza": "Filza",
    "com.burbn.instagram": "Instagram"
}

for bundle, app_name in default_bundles.items():
    if bundle not in apps_bundles:
        with open(apps_bundles_file, 'a') as file:
            file.write(f"{bundle}={app_name}\n")

        apps_bundles[bundle] = app_name


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def clear():
    os.system("clear")

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def clean_tag(text):
    return re.sub(r'<[^>]*>', '', text)

def find_app(bundle_id):
    if bundle_id in apps_bundles:
        return apps_bundles[bundle_id]
    else:
        with open(status_puaf_file, 'a') as file:
            file.write(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: '{bundle_id}' is not found | input_appName: ")
        return input(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: '{bundle_id}' is not found | input_appName: ")

def refresh_app(app_name):
    os.system(f"killall {app_name}")

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def log(message):
    print(f"[+] {message}")


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def x():
    if not os.path.exists(_installedx):
        clear()
        log("_installed.jjK not installed - installing modules... ")
        os.system("sh _install.sh")
        return


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
clear()
x()
if len(sys.argv) < 2:
    print("[+] Use: [ -r (readOnly) | -s (start) ]\n       [+]: [ -l (language) ]")
    sys.exit()

if sys.argv[1] == "-l":
    print("coming soon...")
    sys.exit()

if sys.argv[1] == "-r":
    iOS = platform.machine()
    vrs = platform.version()
    print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: Machine: {iOS}")
    print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: kernel_version: {vrs}")
    with open(plist_path, 'a') as file:
            print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: {plist_path} :200: open\n\n")
    sys.exit()

if sys.argv[1] == "-s":
    while True:
        
        shutil.copy(plist_path, txt_path)

        with open(info_file, 'a') as file:
            file.write(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: {txt_path} :200: open\n\n")

        with open(txt_path, 'r') as file:
            lines = file.readlines()

        with open(read_puaf_file, 'a') as file:
            file.write(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: readPuafLines: {len(lines)} - :200:\n\n")

        with open(txt_path + ".old", 'r') as old_file:
            old_lines = old_file.readlines() if os.path.exists(txt_path + ".old") else []

        if lines != old_lines:
            changed_line = None
            for i, (new_line, old_line) in enumerate(zip(lines, old_lines)):
                if new_line != old_line:
                    changed_line = i
                    break

            if changed_line is not None:
                app_identifier_line = None
                for i in range(changed_line, 0, -1):
                    if "<key>appIdentifier</key>" in lines[i]:
                        app_identifier_line = i + 1
                        break

                if app_identifier_line is not None:
                    bundle_id = clean_tag(lines[app_identifier_line].strip())
                    app_name = find_app(bundle_id)
                    if app_name:
                        refresh_app(app_name)
                        with open(status_puaf_file, 'a') as file:
                            file.write(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: :200: {app_name} -r :success:\n\n")

        shutil.copy(txt_path, txt_path + ".old")
        time.sleep(1)
else:
    print("[+] Use: [ -r (readOnly) | -s (start) ]\n       [+]: [ -l (language) ]")
    sys.exit()

