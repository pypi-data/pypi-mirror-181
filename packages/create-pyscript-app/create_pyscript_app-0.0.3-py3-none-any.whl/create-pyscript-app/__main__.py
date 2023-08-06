import os
import argparse
import shutil


def main():
    parser = argparse.ArgumentParser(prog="create-pyscript-app")
    parser.add_argument(dest="project_directory",
                        help="name of project directory")
    parser.add_argument("-V", "--version", action="version",
                        version="%(prog)s v0.0.3")
    args = parser.parse_args()

    try:
        print(
            f'Creating a new PyScript app at "{os.getcwd()}/{args.project_directory}" ...\n')
        shutil.copytree(f"{os.path.dirname(os.path.realpath(__file__))}/app",
                        f"{os.getcwd()}/{args.project_directory}")
        print(
            f'Successfully created PyScript app in "{os.getcwd()}/{args.project_directory}"\n')
        print('Inside that directory, you can run command\n\n\tpython -m http.server\n\nand open http://localhost:8000/ in your browser.')
    except FileExistsError as e:
        print(e)
        print('Run "python -m create-pyscript-app --help" to see all options.')


if __name__ == '__main__':
    main()
