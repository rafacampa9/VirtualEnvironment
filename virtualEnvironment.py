######################################### PACKAGES ##############################################################
from subprocess import check_call, call, CalledProcessError, run as runSubprocess
from os.path import exists
from os import chdir, getenv
from sys import executable, modules
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
        print(f'\nPackage already installed.\n')
    except DistributionNotFound:
        print(f"\nThe package {package} doesn't exist.\nInstalling package...\n")
        check_call([executable, '-m', 'pip', 'install', package])
    except VersionConflict as vc:
        installed_version = vc.dist.version
        required_version = vc.req
        print(f"\nA version's conflict detected:\n"
              f"Version installed: {installed_version}"
              f"Version required: {required_version}"
               "Trying to install the package required\n")
        check_call([executable, '-m', 'pip', 'install', '--upgrade', package])
    except CalledProcessError as cp:
        print(f"\nAn error occurred: {cp.returncode}\n")
        check_call(([executable, '-m', 'pip', 'install', '--upgrade', package]))
        check_call([executable, '-m', 'pip', 'install', package])



# Function to install all packages written in requirements.txt
def check_and_install_packages(file, STANDARD_PACKAGE):
    with open(file, 'r') as packages:
        for package in packages.readlines():
            if package.strip() in STANDARD_PACKAGE:
                print(f"Package {package.strip()} already installed!\n")
            else:
                check_and_install_package(package.strip())

    packages.close()

def run_script(file):
    try:
        runSubprocess(['python', f'{file}.py'])
    except CalledProcessError as e:
        print(f'An error occurred: {e.stderr.decode()}')



def upload_docker():
    username = getenv('DOCKER_USERNAME', default='default_username')
    pwd = getenv('DOCKER_PASSWORD', default='default_password')
    try:
        runSubprocess(['docker', 'login', '--username', username, '--password', pwd], check=True)

        dockerfile_contents = """
#Use the official image of Python
FROM python:3.11.0-slim

#Establised your work directory
WORKDIR /app

# Install venv and create a virtual environment
RUN python -m venv /app/venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements file (assuming you're using a requirements.txt for dependencies)
COPY requirements.txt /app/

# Install dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Install Jupyter
RUN pip install jupyter ipykernel

# Copy all the files
COPY . /app

# Expose the port 8888 for Jupyter
EXPOSE 8888

# Environment variable (optional)
ENV NAME VirtualEnvironment

# Command to run the application, ensure it runs within the virtual environment
CMD ["python", "virtualEnvironment.py"]
"""
    
        image_name = input('Enter the name of your image: ')

        print('\nWriting Dockerfile\n')
        with open('Dockerfile', 'w') as file:
            file.write(dockerfile_contents)
            file.close()
        print('\nBuilding image...\n')
        runSubprocess(f'docker build -t {image_name}:latest .', shell=True, check=True)
        print('\nImage built.\n')
        runSubprocess(f'docker push {image_name}', shell=True, check=True)
        print('\nImage uploaded to DockerHub.\n')


    except CalledProcessError as cp:
        print(f'CalledProcessError: {cp.stderr}')
    except Exception as e:
        print(f'Exception: {e}')

def upload_github():
    try:
        email = getenv("GITHUB_EMAIL", default='default_email')
        runSubprocess(f'git config --global user.email "{email}"',
                      shell=True, check=True)
        print('\nname')
        username = getenv("GITHUB_USERNAME", default='default_username')
        runSubprocess(f'git config --global user.name "{username}"',
                      shell=True, check=True)
        runSubprocess('git init', shell=True, check=True)
        print('\nInitializing Github & git status\n')
        runSubprocess('git status', shell=True, check=True)
        print('\ngit add .\n')
        runSubprocess('git add .', shell=True, check=True)
        commit = input('Enter commit message: ')
        runSubprocess(f'git commit -m "{commit}"', shell=True, check=True)

        print('\ngit branch\n')
        runSubprocess('git branch -M main', shell=True, check=True)
        first_upload = ''
        while first_upload not in ['Y', 'y', 'N', 'n']:
            first_upload = input('Enter if it is your first commit: ')
            if first_upload not in ['Y', 'y', 'N', 'n']:
                print('\nInvalid option\n')
        
        if first_upload in ['Y', 'y']:
            my_git = input('Enter repository name: ')
            print('\nremote add origin\n')
            #
            runSubprocess(f'git remote add origin https://github.com/rafacampa9/{my_git}.git',
                shell=True, check=True, capture_output=True)
        else:
            runSubprocess('git pull origin main', shell=True, check=True)
        print('\npush\n')
        runSubprocess(f'git push -u origin main', shell=True, check=True)
        print('\nProject uploaded to GitHub\n')
    except CalledProcessError as cp:
        print(f'\nCalledProcessError: {cp.stderr}\n')
    except Exception as e:
        print(f'Exeption: {e}')


def run():
    STANDARD_PACKAGE = []

    manage_and_activate_env()
    for key in modules.keys():
        STANDARD_PACKAGE.append(key.strip())
    """for package in STANDARD_PACKAGE:
        print(package)
    breakpoint()"""
    selection = '1'
    while selection in ['1', '2']:
        selection = input('1. Install an only package\n'
                          '2. Install all packages written to the requirements.txt type file\n'
                          '(Other). Exit\n'
                          'Enter the option: ')

        if selection == '1':
            package = input('Enter the package which you want to install: ')
            if package in STANDARD_PACKAGE:
                print('Package already installed!\n')
            else:
                check_and_install_package(package)
        elif selection == '2':
            file = input('Enter your file with the packages to install (requirements.txt): ')
            check_and_install_packages(file, STANDARD_PACKAGE)

    file = input('\nEnter file name: ')
    from dotenv import load_dotenv
    load_dotenv()
    run_script(file)

    docker_option = '9'
    while docker_option not in ['Y', 'y', 'N', 'n']:
        docker_option = input('Do you want to upload this project to Docker? [Y/N]: ')
        if docker_option not in ['Y', 'y', 'N', 'n']:
            print('\nInvalid option\n')
    if docker_option in ['Y', 'y']:
        upload_docker()
    else:
        print('\nDocker pass...\n')

    git_option = '9'
    while git_option not in ['Y', 'y', 'N', 'n']:
        git_option = input('Do you want to upload this project to GitHub? [Y/N]: ')
        if git_option not in ['Y', 'y', 'N', 'n']:
            print('\nInvalid option\n')
    if git_option in ['Y', 'y']:
        upload_github()
    else:
        print('\nGit pass...\n')


######################################### MAIN ############################################################################
if __name__ == '__main__':
    run()