import os
import glob
import subprocess
import datetime
import pathlib

def get_last_updated(path: str):
    '''
    Returns a datetime object which shows the last time the file was modified
    '''
    fname = pathlib.Path(path)
    mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime, tz=datetime.timezone.utc)

    return mtime

def get_filename_details(path: str):
    '''
    Returns a tuple formed of (file name without extension, file extension)
    '''
    full_name: str = path.split("/")[-1]
    dot_index: int = full_name.index(".")

    return (full_name[:dot_index], full_name[dot_index + 1:])

class CPP_File:
    def __init__(self, path: str):
        self.path: str = path
        self.object_path: str = ""
        self.included_files: List[str] = []
        # https://stackoverflow.com/a/52858040 -> see for time for update

        self.last_updated = None

    def add_included_files(self, filename: str) -> None:
        self.included_files.append(filename)

    def __repr__(self):
        string: str = '''Path: {}
Included headers: {} '''.format(self.path, self.included_files)

        return string

class Slender_Crawler:
    def __init__(self, path: str, exe: str = ""):
        self.cpp_files: Dict[str, CPP_File] = {}
        self.build_order: List[str] = []
        self.project_path: str = path
        self.executable_name: str = exe

    def crawl(self) -> None:
        file_types: List[str] = ["*.cpp", "*.h"]
        files: List[str] = []

        for extension in file_types:
            files.extend(glob.glob(self.project_path + "/**/{}".format(extension), recursive=True))

        # getting all the cpp files and what headers can be found in them
        for filepath in files:
            print("Found {}".format(filepath))
            filename, file_extension = get_filename_details(filepath)

            if filename not in self.cpp_files:
                print("Adding file to list of project files...")
                self.cpp_files[filename] = CPP_File(filepath)
            # so that we keep the location of the .cpp file, not the header file
            elif file_extension == "cpp":
                self.cpp_files[filename].path = filepath
            else:
                print("File already in list of project files.")

            print("Checking headers...")
            with open(filepath) as file:
                lines = [line.rstrip() for line in file]

                for line in lines:
                    if line.find("#include") > -1:
                        quote_index = line.find("\"")
                        if quote_index > -1:
                            header_name = get_filename_details(line[quote_index + 1:])[0]

                            if header_name != filename:
                                self.cpp_files[filename].add_included_files(header_name)

                print("Current header files: {}\n".format(self.cpp_files[filename].included_files))

        # sorting the cpp files into a dependency order
        # kind of a naive way but oh well
        # check this sometime: https://medium.com/@fgnowhtHnidd/a-comprehensive-analysis-of-dependency-sorting-algorithms-ff4215b0b930

        # we go through every file and check if it appears as another file's header
        # if it doesn't, we put it in the build order

        # at the moment, it's going to be most dependent -> most independent
        temp_cpp_files = [item[0] for item in self.cpp_files.items()]

        print("Sorting files ASC in order of dependency...\n")

        while len(temp_cpp_files) > 0:
            for dependency in temp_cpp_files:
                independent: bool = True
                for dependant in temp_cpp_files:
                    if dependency in self.cpp_files.get(dependant).included_files:
                        independent = False
                        break

                if independent:
                    self.build_order.append(dependency)
                    temp_cpp_files.remove(dependency)

        print("Final order:\n")
        for key in self.build_order:
            print(key)
            print("Last time of modification: {}".format(get_last_updated(self.cpp_files.get(key).path)))
            print(self.cpp_files.get(key), "\n")

    # compiling and linking all source files
    def build_project_all(self) -> None:
        command: List[str] = ["g++"]

        for filename in self.build_order:
            command.append(self.cpp_files.get(filename).path)

        if self.executable_name:
            command.append("-o{}".format(self.executable_name))

        subprocess.run(command)

    # compiling each individual object file and linking them in the executable
    def build_project_individual(self) -> None:
        pass

    def run_project(self):
        subprocess.run("./{}".format(self.executable_name), shell=True)

    def delete_object_files(self):
        pass