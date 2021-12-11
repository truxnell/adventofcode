
f = open('1a.txt', 'r').read().split()
f = [int(x) for x in f]
i = 0
c = 1

for i in range(0, len(f)-4):
    if sum(f[i:i+3]) < sum(f[i+1:i+4]):
        c += 1

print(c)
