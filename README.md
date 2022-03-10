# TaskJoiner
This is a program for creating Join commands in a database

*main.py* is the code that is executed when the program is started. It uses code contained in *functions.py*. 
The tests were performed in the file test.py. File */dist/main/main.exe* is executable file. By typing e.g. a command 
 "join SmallTable1.csv SmallTable2.csv key2to1 inner" into it you can get the database. Database is safed in file *NewTable.csv*.
 
 Example:
"join SmallTable1.csv SmallTable2.csv key2to1 right"

![after_join](https://user-images.githubusercontent.com/78937784/157584073-98250f5f-0695-4cef-94b8-c407368f21c4.JPG)

where, SmallTable1.csv:
![smalltable1](https://user-images.githubusercontent.com/78937784/157584336-674275f1-e50c-4b31-975d-bcedbf53a740.JPG)

and SmallTable2.csv:
![smalltable2](https://user-images.githubusercontent.com/78937784/157584344-43b5fe89-4643-4c64-993f-7754f6b2ced8.JPG)
