
f = open('1a.txt', 'r').read().split()
i = 0
c = 1

for i in range(1, len(f)):
    if f[i] > f[i-1]:
        c += 1
        # print("({0}){1} - {2}".format(i, f[i-1], f[i]))

print(c)
