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

# Counting the wmc value
def count_wmc(filepath):
    class_names_array = []
    wmc_array = []
    with open(filepath) as file:
        node = ast.parse(file.read())

    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    for class_name in classes:
        class_names_array.append(class_name.name)

    for class_ in classes:
        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        wmc_array.append(len(methods))

    return class_names_array, wmc_array

# Counting the cbo value
def count_cbo(filepath):
    cbo_array = []

    with open(filepath) as f:
        data = f.read()
        module = ast.parse(data)

        classes = [obj for obj in module.body if isinstance(obj, ast.ClassDef)]
        class_names = [obj.name for obj in classes]

        dependencies = {name: [] for name in class_names}

        for cls in classes:
            for node in ast.walk(cls):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id != cls.name and node.func.id in class_names:
                            dependencies[cls.name].append(node.func.id)

        values = [0] * len(classes)
        list_dict = {k: v for k, v in zip(class_names, values)}

        for class_name, dependency in dependencies.items():
            for d in dependency:
                list_dict[d] = list_dict[d] + 1

        for class_name, dependency in dependencies.items():
            cbo_array.append(len(dependency) + list_dict[class_name])

    return cbo_array

# Counting the rfc value
def count_rfc(filepath):
    rfc_array = []
    dep_array = []
    num_func_array = []
    dependencies = []

    with open(filepath) as file:
        node = ast.parse(file.read())

    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    class_names = [obj.name for obj in classes]

    for class_ in classes:
        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        num_func_array.append(len(methods))

    dependencies = {name: [] for name in class_names}

    for cls in classes:
        for node in ast.walk(cls):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id != cls.name and node.func.id in class_names:
                        dependencies[cls.name].append(node.func.id)

    for class_name, dependency in dependencies.items():
        dep_array.append(len(dependency))

    for i in range(len(class_names)):
        rfc_array.append(num_func_array[i] + dep_array[i])

    return rfc_array

# Counting the lcom value
def count_lcom(filepath):
    lcom_array = []
    P = []
    Q = []
    dict = {}
    with open(filepath) as file:
        node = ast.parse(file.read())

    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    class_names = [obj.name for obj in classes]

    for class_ in classes:
        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        P.append(len(methods))

    for class_ in classes:
        count_pairs = 0
        for node in ast.walk(class_):
            if isinstance(node, ast.Attribute):
                if node.attr in dict.keys():
                    dict[node.attr] = dict[node.attr] + 1
                else:
                    dict[node.attr] = 1
        for key in dict:
            if dict[key] > 1:
                count_pairs = count_pairs + 1

        Q.append(count_pairs)
        dict = {}

    for i in range(len(class_names)):
        if P[i] > Q[i]:
            lcom_array.append(P[i] - Q[i])
        else:
            lcom_array.append(0)

    return lcom_array

def main():
    filepath = sys.argv[1]
    writepath = sys.argv[2]
    # num_codelines, blank_lines = count_lines_of_code(filepath)
    # num_of_func = count_function(filepath)
    # name, cyclo = count_cyclo(filepath)
    # num_comments, num_mul_com = count_comments(filepath)
    # num_only_plain_comments = count_only_comments(filepath)
    # lines_of_code = num_codelines - num_mul_com - num_only_plain_comments
    # in_arr, out_arr = count_ifc(filepath)
    classes, wmc = count_wmc(filepath)
    cbo = count_cbo(filepath)
    rfc = count_rfc(filepath)
    lcom = count_lcom(filepath)


    with open(writepath, "w") as f:
        for i in range(len(classes)):
            f.write(f"{classes[i]}:\n")
            f.write(f"   - wmc: {wmc[i]}\n")
            f.write(f"   - cbo: {cbo[i]}\n")
            f.write(f"   - rfc: {rfc[i]}\n")
            f.write(f"   - lcom: {lcom[i]}\n")

    #     # f.write(f"LOC: {lines_of_code}\n")
    #     # f.write(f"eLOC: {lines_of_code}\n")
    #     # f.write(f"Comment: {num_comments+num_mul_com}\n")
    #     # f.write(f"Blank: {blank_lines}\n")
    #     cyclo.append(1)
    #     for i in range(num_of_func):
    #         f.write(f"{name[i]}:\n")
    #         f.write(f"   - cyclomatic: {cyclo[i]}\n")
    #         ifc = int(math.pow((in_arr[i]*out_arr[i]), 2))
    #         f.write(f"   - ifc: {ifc}\n")

if __name__ == "__main__":
    main()
