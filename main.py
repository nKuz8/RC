from math import log2
n = []
table_phi = []
table_ksi = []


def phi_ksi_fun(vec, x, mode):
    number = 0
    vec.append(x)
    for i in range(len(vec) - 1, -1, -1):
        number += 2 ** (len(vec) - 1 - i) * vec[i]
    if mode == "phi":
        return table_phi[number]
    elif mode == "ksi":
        return table_ksi[number]


def h_fun(vec, x):
    xn = phi_ksi_fun(vec.copy(), x, "phi")

    for i in range(0, len(vec) - 1):
        vec[i] = vec[i + 1]
    vec.pop(-1)
    vec.append(xn)

    return vec


def f_fun(vec, x):
    return phi_ksi_fun(vec.copy(), phi_ksi_fun(vec.copy(), x, "phi"), "ksi")


def dec_to_bin(number):
    global n
    res_vec = []
    for i in range(0, n):
        res_vec.append(number % 2)
        number //= 2
    res_vec.reverse()
    return res_vec

def bin_to_dec(vec):
    number = 0
    for i in range(len(vec) - 1, -1, -1):
        number += 2 ** (len(vec) - 1 - i) * vec[i]
    return number



def make_reach_table():
    global n
    reach_table = []
    for  i in range(0, 2 ** n):
        table_line = [0] * 2 ** n
        table_line[bin_to_dec(h_fun(dec_to_bin(i), 0))] = 1
        table_line[bin_to_dec(h_fun(dec_to_bin(i), 1))] = 1
        reach_table.append(table_line)
    return reach_table


def depth_first_search(reach_table, mode):
    global n
    stack = []
    marked = []
    result = []

    for i in range(0, 2**n):
        flag = False
        for item in result:
            if i in item:
                flag = True
            break

        if flag:
            continue
        else:
            marked.append(i)
            stack.append(i)

            for j in range(0, reach_table[i]):
                if reach_table[i][j] == 1 and i != j:



def main():
    with open("params.txt", 'r') as file:
        lines = file.readlines()
        global table_phi, table_ksi, n
        n = int(lines[0])
        table_phi = list(map(lambda x: int(x), lines[2].replace("\n", "").split(" ")))
        table_ksi = list(map(lambda x: int(x), lines[4].replace("\n", "").split(" ")))

    for line in make_reach_table():
        print(line)
    # print(make_reach_table())
    print("Enter s: ")
    s = list(map(lambda x: int(x), input().split(" ")))

    while True:
        x = int(input("Enter x: "))
        s_save = s.copy()
        s = h_fun(s, x)
        print("Next state: {}".format(s))
        print("Output: {}".format(f_fun(s_save, x)))


if __name__ == "__main__":
    main()





