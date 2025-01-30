# sea-crawler

C++ build system that uses Python and the GNU compiler (g++).

### how to use

example:
```
python crawler.py -p [path towards root of project folder] -t [one of the following: run, build, clean]
```

### todo
- [ ] make it create a build file that you can then use
- [ ] build object for each file instead of one executable in one command
    - [ ] take into account time of modification for files
    - [ ] maybe make it an argument?
- [ ] fine-tune the file selection and header association
- [ ] implement the `clean` target functionality
