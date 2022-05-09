
def abc(X, Y):
    print(X + Y)
    if True:
        print("a")
    return 0

if 1 == 1:
    print("a")

def xyz(X):
    print(abc)
    if True:
        print("a")

    while True:
        print("b")
        break;
    return 0


def another_function(Y):
    print("abc")
    val = 2
    if True:
        print("a")
    if 1==val:
        print("c")
    else:
        print("b")

    while True:
        print("b")
        break;
    return 0

def one_more_function(X, Y, Z):
    print(abc)
    val = 2
    if val>2:
        print("a")
    elif val==2:
        print("b")
    else:
        print("c")

    while True:
        print("b")
        break;
    return 0, 1

def main():
    x = 5
    y = 10
    p = xyz(x,y)
    if True:
        print("a")
    while True:
        break
    return 0
