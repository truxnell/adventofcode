with open('3a.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

l = [0]*len(lines[0])

for line in lines:
    for i in range(0, len(line)):
        l[i] += int(line[i])
n = len(lines)/2
for i in range(0, len(l)):
    if l[i] > n:
        l[i] = 1
    else:
        l[i] = 0

g = int(''.join(map(str, l)), 2)
e = 2**len(lines[0])-g-1

print(f"Gamma: {g}")
print(f"Epsilon: {e}")
print(f"Result: {g*e}")
