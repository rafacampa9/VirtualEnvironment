######################################### PACKAGES ##############################################################
from subprocess import check_call, call
from os.path import exists
from os import chdir
from sys import executable
from pkg_resources import require, DistributionNotFound, VersionConflict


######################################### METHODS ##########################################################################

# Activate the virtual environment
def call_activate():
    try:
        call('activate.bat', shell=True)
        print('Virtual environment activated (only affects this subprocess)\n')
    except Exception as e:
        print(f'Error to activate the virtual environment: {e}\n')


# creates and activates the virtual environment venv
def manage_and_activate_env():
    venv_path = 'venv/Scripts'
    if exists(venv_path):
        chdir(venv_path)
        call_activate()
        chdir('../../')
    else:
        print(f"The package {venv_path} doesn't exist.\nInstalling venv...\n")
        call([executable, '-m', 'venv', 'venv'])
        if exists(venv_path):
            chdir(venv_path)
            call_activate()
            chdir('../../')


# Function to install a package
def check_and_install_package(package):
    try:
        require(package)
        print(f'Package already installed.\n')
    except DistributionNotFound:
        print(f"The package {package} doesn't exist.\nInstalling package...\n")
        check_call([executable, '-m', 'pip', 'install', package])
    except VersionConflict as vc:
        installed_version = vc.dist.version
        required_version = vc.req
        print(f"A version's conflict detected:\n"
              f"Version installed: {installed_version}"
              f"Version required: {required_version}"
              "Trying to install the package required\n")
        check_call([executable, '-m', 'pip', 'install', '--upgrade', package])


# Function to install all packages written in requirements.txt
def check_and_install_packages(file):
    with open(file, 'r') as packages:
        for package in packages.readlines():
            check_and_install_package(package)

    packages.close()


######################################### MAIN ############################################################################
if __name__ == '__main__':
    manage_and_activate_env()

    while True:
        selection = input('1. Install an only package\n'
                          '2. Install all packages written to the requirements.txt type file\n'
                          '(Other). Exit\n'
                          'Enter the option: ')

        if selection == '1':
            package = input('Enter the package which you want to install: ')
            check_and_install_package(package)
        elif selection == '2':
            file = input('Enter your file with the packages to install (requirements.txt): ')
            check_and_install_packages(file)
        else:
            break

