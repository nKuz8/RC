from math import log2
from sys import setrecursionlimit

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

    for i in range(len(vec) - 1):
        vec[i] = vec[i + 1]
    vec.pop(-1)
    vec.append(xn)

    return vec


def f_fun(vec, x):
    return phi_ksi_fun(vec.copy(), phi_ksi_fun(vec.copy(), x, "phi"), "ksi")


def dec_to_bin(number):
    global n
    res_vec = []
    for i in range(n):
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
    for i in range(2 ** n):
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

    for i in range(2 ** n):
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

            while len(stack) != 0:
                for j in range(len(reach_table[i])):
                    if (((reach_table[i][j] == 1 or reach_table[j][i] == 1) and mode == "normal") or (reach_table[i][j] == 1 and mode == "strong")) and i != j:
                        flag = False
                        for item in result:
                            if j in item:
                                flag = True
                                break

                        if flag or j in marked:
                            continue
                        else:
                            marked.append(j)
                            stack.append(j)
                            dps_rec(reach_table, j, marked, stack, result, mode)
                            stack.pop(-1)
                stack.pop(-1)
            result.append(marked)
            marked = []
    return result


def dps_rec(reach_table, i, marked, stack, result, mode):
    for j in range(len(reach_table[i])):
        if (((reach_table[i][j] == 1 or reach_table[j][i] == 1) and mode == "normal") or (reach_table[i][j] == 1 and mode == "strong")) and i != j:
            flag = False
            for item in result:
                if j in item:
                    flag = True
                    break

            if flag or j in marked:
                continue
            else:
                marked.append(j)
                stack.append(j)
                dps_rec(reach_table, j, marked, stack, result, mode)
                stack.pop(-1)


def equal_prep():
    global n
    equal_array = []
    state_info = []
    for i in range(2**n):
        state = dec_to_bin(i)
        for j in [0, 1]:
            state_info.append(bin_to_dec(h_fun(state, j)))
            state_info.append(f_fun(state, j))
        equal_array.append(state_info)
        state_info = []
    return equal_array


def equal_search(equal_array):
    equal_classes = []
    equal_class = []
    for i in range(len(equal_array) - 1):
        flag = False
        for item in equal_classes:
            if i in item:
                flag = True
                break
        if flag:
            continue
        else:
            equal_class.append(i)
            for j in range(i + 1, len(equal_array)):
                if equal_array[i][1] == equal_array[j][1] and equal_array[i][3] == equal_array[j][3]:
                    equal_class.append(j)
            equal_classes.append(equal_class)
            equal_class = []
    return equal_classes


def main():
    with open("params.txt", 'r') as file:
        lines = file.readlines()
        global table_phi, table_ksi, n
        n = int(lines[0])
        table_phi = list(map(lambda x: int(x), lines[2].replace("\n", "").split(" ")))
        table_ksi = list(map(lambda x: int(x), lines[4].replace("\n", "").split(" ")))
    setrecursionlimit(2**n + 10)
    reach_table = make_reach_table()
    links = depth_first_search(reach_table, "normal")
    print("Automat is linked") if len(links) == 1 else print("Automat is not linked")
    print("Linked components: {}".format(links))
    strong_links = depth_first_search(reach_table, "strong")
    print("Automat is strongly linked") if len(strong_links) == 1 else print("Automat is not strongly linked")
    print("Strongly linked components: {}".format(strong_links))
    print("{}".format(equal_search(equal_prep())))
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
