# Software Engineering Assignment 1

## Tools
1. Language Used: Python 3.10
2. Target Language: Python
3. Editor Used: PyCharm
4. Dependencies: sys, ast, re libraries

## Execution
On the terminal type:
python3 main.py <Name_of_input_file.py> <name_of_output_file>

To run the code with the files uploaded use:
python3 main.py Test.py results.txt


# Logic Used

## Blank Lines
Pseudocode:
1. Open the file
2. Read a line
3. Initialize no_blank = 0
4. Check if the line is blank using the inbuilt function isspace()
5. If the line is blank increment no_blank by 1
6. Repeat from step 2 till the end of file is reached
7. return no_blank

## LOC
1. Count the number of blank lines using the above procedure (Blank Lines)
2. return total_number_of_lines - no_blank - no_comment

## eLOC
1. Count the number of blank lines using the above procedure (Blank Lines)
2. return total_number_of_lines - no_blank - no_comment

### Note: LOC and eLOC will be the same since python does not use stand alone curly braces

## Functions
1. Open the file
2. Get the parse tree of the file
3. Initialize no_func = 0
4. For each item in the parse tree use the ast library to check if it is an instance of a function.
5. If it is an instance of a function increment no_func by 1.
6. Return no_func


## Comments
### Note: We have counted the single line as well as multiple line comments.

1. Open the file
2. Read line by line
3. Initialize num_single_comments = 0 and num_mul_comments = 0
4. To count single line comments:
   4.1 We check if a # is in the line
   4.2 To make sure it is not part of a print statement or string we check the position of the # in the line
   4.3 When we encounter a " or a ' in the line we alternatively increment and decrement 2 counter variables
   4.4 When the # character is encountered, if the counter value for ' and " is 0 it is a comment.
   4.5 If the counter value of ' or " is 1 then it is not a comment.

> ````print("# This is not a comment")   # This is a comment ```` </br>
> ````var = "# This is not a comment" ````

5. To count multiple line comments:
   5.1 We check if there is a """ or ''' in the line
   5.2 We increment a counter till the next """ or ''' is encountered
   5.3 If a blank line is encountered in a multiple line comment it is ignored.

### Note: In python multiple line comments always start on a new line

6. Add no_single_comments and no_mul_comments
7. return the sum of comments

### Note: A # in a multiple line comment is considered as part of multiple line comment. This way we do not count the same line twice.
