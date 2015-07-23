from urllib import request
import zipfile
from os import system, path

PROGRAM_PATH = path.realpath(__file__).replace("update.py", "")
ZIP_DIRECTORY = "astroConverter-master"
IGNORED_FILES = (".gitattributes",
                 ".gitignore",
                 ".idea",
                 "__pycache__",
                 "virtualenv")


def get_version_from_data(data):
    data = data.split("\n")
    data = data[1]
    data = data.split("=")
    version = data[1]
    return version.replace("\n", "")


def get_remote_version():
    r = request.urlopen("https://github.com/laszlowaty/astroConverter/raw/master/settings.py")
    data = r.read()
    r.close()
    return get_version_from_data(data.decode())


def get_local_version():
    try:
        file = open("settings.py")
    except FileNotFoundError:
        print("Couldn't find setting.py file. Forcing update...")
        return "0"
    data = file.read()
    file.close()
    return get_version_from_data(data)


def check_versions():
    print("checking versions...")
    return get_local_version() == get_remote_version()


def fetch_file():
    print("downloading files...")
    r = request.urlopen("https://github.com/laszlowaty/astroConverter/archive/master.zip")
    data = r.read()
    file = open("temp.zip", "wb")
    file.write(data)
    file.close()


def read_zip():
    print("Extracting zip file...")
    data = zipfile.ZipFile("temp.zip")
    data.extractall()


def clean_after():
    print("cleaning up...")
    system("rmdir " + ZIP_DIRECTORY + " /S /Q")
    system("del temp.zip")


def copy_files():
    print("Coping files...")
    cmd = "xcopy /Q /S /Y "
    cmd += PROGRAM_PATH + ZIP_DIRECTORY + "\\*"
    cmd += " " + PROGRAM_PATH
    system(cmd)


def update():
    fetch_file()
    read_zip()
    copy_files()
    clean_after()
    print("Updates were installed")
    input("Press enter key to exit")


def do_not_update():
    print("Nothing to update.")
    input("Press enter key to exit.")


controller = {False: update,
              True: do_not_update}


def main():
    controller[check_versions()]()


if __name__ == '__main__':
    main()
