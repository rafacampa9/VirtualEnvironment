#################################################### IMPORTS ###################################################################
from subprocess import check_call, call
from os.path import exists
from os import chdir
from sys import executable
#from time import sleep
from pkg_resources import require, DistributionNotFound, VersionConflict

##################################################### METHODS ###################################################################################################################################################################
#Activate the virtual environment venv
def call_activate():
    try:
        call("activate.bat", shell=True)
        print("Virtual environment: Activated (only affects this subprocess)")
    except Exception as e:
        print(f'Error al activar el entorno virtual: {e}')

#create and activates the virtual environment
def manage_and_activate_venv():
    venv_path = 'venv/Scripts'
    if exists(venv_path):
        call_activate()
    else:
        print('El directorio venv/Scripts no existe.\nCreando entorno virtual...\n')
        call([executable, '-m', 'venv', 'venv'])
        #sleep(30)
        if exists(venv_path):
            chdir(venv_path)
            call_activate()
            chdir('../../')

#Installing the package check by parameter
def check_and_install_package(package):
    try:
        require(package)
        print(f'El paquete {package} está instalado. Continuando...')
    except DistributionNotFound:
        print(f'{package} no existe. Instalándolo...')
        check_call([executable, "-m", "pip", "install", package])
    except VersionConflict as vc:
        installed_version = vc.dist.version
        required_version = vc.req
        print(f'Conflicto de versión detectado para el paquete {package}:\n'
              f'Versión instalada: {installed_version}\n'
              f'Versión requerida: {required_version}\n'
              f'Intentando actualizar el paquete...')
        check_call([executable, '-m', 'pip', 'install', '--upgrade', package])


#Installing the packages checks in requirements.txt
def check_and_install_packages(file):
    with open(file, 'r') as packages:
        packs = packages.readlines()
        for package in packs:
            check_and_install_package(package)



############################################### MAIN ###########################################################################
if __name__ == "__main__":
    manage_and_activate_venv()

    while True:
        selection = input('Enter the option:\n'
                          '1. Import an only package\n'
                          '2. Import all packages in requirements.txt\n'
                          '(Other). Exit\n')
        if selection == '1':
            package = input('Enter the package which you want to install: ')
            check_and_install_package(package)
        elif selection == '2':
            file = input('Enter your file with packages to install (requirements.txt): ')
            check_and_install_packages(file)
        else:
            break