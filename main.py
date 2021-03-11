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


def main():
    with open("params.txt", 'r') as file:
        lines = file.readlines()
        global table_phi, table_ksi
        table_phi = list(map(lambda x: int(x), lines[2].replace("\n", "").split(" ")))
        table_ksi = list(map(lambda x: int(x), lines[4].replace("\n", "").split(" ")))

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





