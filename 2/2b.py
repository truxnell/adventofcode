with open('2a.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

h = 0
d = 0
a = 0

for i in range(0, len(lines)):
    w = lines[i].split()
    w[1] = int(w[1])
    if w[0] == "forward":
        h += w[1]
        d += w[1]*a
    elif w[0] == "down":
        a += w[1]
    elif w[0] == "up":
        a -= w[1]

print(f"h={h}")
print(f"d={d}")
print(f"\nresult={h*d}")
