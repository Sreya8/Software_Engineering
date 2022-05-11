import math
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

# Counting the Cyclomatic Number
def count_cyclo(filepath):
    ptree = parse_file(filepath)
    flag = 0
    func_array = []
    cyclo_array = []

    for item in ast.walk(ptree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):

            func_array.append(item.name)
            flag = 1

            continue

    count = 0
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for aline in lines:
            words = aline.split()
            if words:
                for more_words in words:
                    refined_words = more_words.split('(')
                    if refined_words[0] == "def":
                        count = 0
                        flag = 1
                    elif flag == 1 and (refined_words[0] == "for" or refined_words[0] == "while" or refined_words[0] == "if" or refined_words[0] == "elif"):
                            count = count + 1
                    elif flag == 1 and refined_words[0] == "return":
                        count = count + 1
                        cyclo_array.append(count)
                        flag = 0
                        count = 0

    return func_array, cyclo_array


# Counting the IFC
def count_ifc(filepath):
    in_array = []
    out_array = []

    ptree = parse_file(filepath)
    for item in ast.walk(ptree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            arguments = [a.arg for a in item.args.args]
            in_array.append(len(arguments))

    with open(filepath, 'r') as f:
        lines = f.readlines()
        for aline in lines:
            words = aline.split()
            for word in words:
                if word == "return":
                    out_array.append(len(words)-1)

        out_array.append(0)
        return in_array, out_array



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

        if '"""' in aline or "'''" in aline:

            if ([] != re.findall(r"\s*\"{3}.*\"{3}", aline)):
                num_mul_comment += 1
                continue

            if ([] != re.findall(r"\s*\'{3}.*\'{3}", aline)):
                num_mul_comment += 1
                continue

            if aline.endswith('"""') or aline.endswith("'''"):
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
    name, cyclo = count_cyclo(filepath)
    num_comments, num_mul_com = count_comments(filepath)
    num_only_plain_comments = count_only_comments(filepath)
    lines_of_code = num_codelines - num_mul_com - num_only_plain_comments
    in_arr, out_arr = count_ifc(filepath)

    with open(writepath, "w") as f:
        # f.write(f"LOC: {lines_of_code}\n")
        # f.write(f"eLOC: {lines_of_code}\n")
        # f.write(f"Comment: {num_comments+num_mul_com}\n")
        # f.write(f"Blank: {blank_lines}\n")
        cyclo.append(1)
        for i in range(num_of_func):
            f.write(f"{name[i]}:\n")
            f.write(f"   - cyclomatic: {cyclo[i]}\n")
            ifc = int(math.pow((in_arr[i]*out_arr[i]), 2))
            f.write(f"   - ifc: {ifc}\n")

if __name__ == "__main__":
    main()
