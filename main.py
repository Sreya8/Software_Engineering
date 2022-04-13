import sys
import ast
import re

def parse_file(filepath):
    with open(filepath, 'r') as f:
        return ast.parse(f.read(), filename=filepath)

# Counting the Number of Functions
def count_function(filepath):
    ptree = parse_file(filepath)

    num_func = 0
    for item in ast.walk(ptree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            num_func += 1

    return num_func

# Counting the LOC
def count_lines_of_code(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Read blank lines
    num_blank = 0
    for aline in lines:
        if aline.isspace():
            num_blank += 1

    return len(lines) - num_blank, num_blank

# Counting the number of single line and multiple line comments
def count_comments(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    num_comment = 0
    num_mul_comment = 0

    state = True
    flag_multiple = 0
    start_count = False

    for aline in lines:
        scounter = 0
        dcounter = 0
        flag_d = 0
        flag_s = 0

        if state:
            if "#" in aline:
                for char in aline:
                    if char == "\"":
                        if flag_d == 0:
                            dcounter += 1
                            flag_d = 1
                        else:
                            dcounter -= 1
                            flag_d = 0

                    if char == "\'":
                        if flag_s == 0:
                            scounter += 1
                            flag_s = 1
                        else:
                            scounter -= 1
                            flag_s = 0

                    if char == "#":
                        if scounter == 0 and dcounter == 0:
                            num_comment += 1
                            break

        if '"""' in aline:

            if ([] != re.findall(r"\s*\"{3}.*\"{3}", aline)):
                num_mul_comment += 1
                continue

            if aline.endswith('"""'):
                num_mul_comment += 1
                break

            if flag_multiple == 0:
                flag_multiple = 1
                start_count = True
                state = False

            else:
                flag_multiple = 0
                start_count = False
                num_mul_comment += 1
                state = True

        if start_count:
            if aline.isspace():
                continue
            else:
                num_mul_comment += 1

    return num_comment, num_mul_comment

# Counting the number of lines having only comments and no code
def count_only_comments(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        num_comment = 0
        for aline in lines:
            aline = aline.strip()
            if aline.startswith('#'):
                num_comment += 1

    return  num_comment


def main():
    filepath = sys.argv[1]
    writepath = sys.argv[2]
    num_codelines, blank_lines = count_lines_of_code(filepath)
    num_of_func = count_function(filepath)
    num_comments, num_mul_com = count_comments(filepath)
    num_only_plain_comments = count_only_comments(filepath)
    lines_of_code = num_codelines - num_mul_com - num_only_plain_comments

    with open(writepath, "w") as f:
        f.write(f"LOC: {lines_of_code}\n")
        f.write(f"eLOC: {lines_of_code}\n")
        f.write(f"Comment: {num_comments}\n")
        f.write(f"Blank: {blank_lines}\n")
        f.write(f"No. of Functions: {num_of_func}\n")

if __name__ == "__main__":
    main()
