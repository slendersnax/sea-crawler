# sea-crawler

C++ build system that uses Python and the GNU compiler (g++).

### status

Not ready for release - can be used for standalone local projects (i.e. projects that don't depend on anything external, only local source files (most university projects are probably included in this category)).

Also it only works on Linux at the moment.

Assumes that:
- all C++ files end in .cpp or .h
- if the filename is the same for a .cpp and .h file, then it's the same object and the .h file is included in the .cpp file

### how to use

example:
```
python crawler.py -p [path towards root of project folder] -t [one of the following: run, build-all, build-ind, clean]
```

### todo
- [ ] make it create a build file that you can then use
    - [ ] actually two files: one made by the program, one by the user
    - [ ] add `flags` argument - flags for g++
- [ ] build object for each file instead of one executable in one command
    - [ ] take into account time of modification for files
    - [x] maybe make it an argument? - Done, functionality not implemented yet
- [ ] fine-tune the file selection and header association
- [ ] implement the `clean` target functionality
- [ ] display g++ build process output
- [ ] Windows and OS X support?