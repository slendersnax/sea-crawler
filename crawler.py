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
                        choices=["run", "build-all", "build-ind", "crawl", "clean"],
                        metavar="TARGET",
                        help="the objective of the current command - 'run' runs the executable (if it has been built), 'build' builds the executable, 'clean' deletes all the built object files",
                        required=True)

    parser.add_argument("-e", "--executable",
                        metavar="EXECUTABLE",
                        help="the name of the generated executable file",
                        type=str,
                        required=False)

    return parser

def main():
    parser = get_arguments()
    args = parser.parse_args()

    crawler_handler = Slender_Crawler(args.path, args.executable)

    if args.target == "run":
        crawler_handler.run_project()
    elif args.target == "build-all":
        crawler_handler.crawl()
        crawler_handler.build_project_all()
    elif args.target == "build-ind":
        crawler_handler.crawl()
        crawler_handler.build_project_individual()
    elif args.target == "clean":
        crawler_handler.delete_object_files()

if __name__ == "__main__":
    main()