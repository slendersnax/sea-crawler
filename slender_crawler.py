import os
import glob
import subprocess

'''
MVP Project.

Works on Linux.

Assumes that:
- all C++ files end in .cpp or .h
- if the filename is the same for a .cpp and .h file, then it's the same object and the .h file is included in the .cpp file
- rebuilds all files everytime the 'build' target is run
'''

def get_pure_filename(path: str):
    '''
    Returns the filename without the full path or file extension
    '''
    full_name: str = path.split("/")[-1]
    dot_index: int = full_name.index(".")

    return full_name[:dot_index]

class CPP_File:
    def __init__(self, path: str):
        self.path: str = path
        self.included_files: List[str] = []

    def add_included_files(self, filename: str) -> None:
        self.included_files.append(filename)

    def __repr__(self):
        string: str = '''Path: {}
Included headers: {}
        '''.format(self.path, self.included_files)

        return string

class Slender_Crawler:
    def __init__(self, path: str):
        self.cpp_files: Dict[str, CPP_File] = {}
        self.build_order: List[str] = []
        self.project_path: str = path
        self.executable_name: str = "test2"

    def find_files(self) -> None:
        file_types: List[str] = ["*.cpp", "*.h"]
        files: List[str] = []

        for extension in file_types:
            files.extend(glob.glob(self.project_path + "/**/{}".format(extension), recursive=True))

        # getting all the cpp files and what headers can be found in them

        for filepath in files:
            print(filepath)
            filename: str = get_pure_filename(filepath)

            # replace with cpp file location sometime
            if filename not in self.cpp_files:
                self.cpp_files[filename] = CPP_File(filepath)

            with open(filepath) as file:
                lines = [line.rstrip() for line in file]

                for line in lines:
                    if line.find("#include") > -1:
                        quote_index = line.find("\"")
                        if quote_index > -1:
                            header_name = get_pure_filename(line[quote_index + 1:])

                            if header_name != filename:
                                self.cpp_files[filename].add_included_files(header_name)

                            print(header_name)

        # sorting the cpp files into a dependency order
        # kind of a naive way but oh well
        # check this sometime: https://medium.com/@fgnowhtHnidd/a-comprehensive-analysis-of-dependency-sorting-algorithms-ff4215b0b930

        # we go through every file and check if it appears as another file's header
        # if it doesn't, we put it in the build order

        # at the moment, it's going to be most dependant -> most independent
        temp_cpp_files = [item[0] for item in self.cpp_files.items()]

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

        print("\nFinal order:\n")
        for key in self.build_order:
            print(key)
            print(self.cpp_files.get(key))

    def build_project(self) -> None:
        self.find_files()

        command: List[str] = ["g++"]

        for filename in self.build_order:
            command.append(self.cpp_files.get(filename).path)

        command.append("-o{}".format(self.executable_name))

        subprocess.run(command)

    def run_project(self):
        subprocess.run("./{}".format(self.executable_name), shell=True)

    def delete_object_files(self):
        pass