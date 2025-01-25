import argparse, os
from slender_crawler import Slender_Crawler

def dir_path(path: str) -> bool:
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)

def get_arguments() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path",
                        metavar="PATH",
                        help="path to the project directory",
                        type=dir_path,
                        required=True)

    parser.add_argument("-t", "--target",
                        choices=["run", "build", "clean"],
                        metavar="TARGET",
                        help="the objective of the current command - 'run' runs the executable (if it has been built), 'build' builds the executable, 'clean' deletes all the built object files",
                        required=True)

    return parser

def main():
    parser = get_arguments()
    args = parser.parse_args()

    crawler_handler = Slender_Crawler(args.path)

    if args.target == "run":
        crawler_handler.run_project()
    elif args.target == "build":
        crawler_handler.build_project()
    elif args.target == "clean":
        crawler_handler.delete_object_files()

if __name__ == "__main__":
    main()