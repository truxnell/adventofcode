with open('2a.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

h = 0
d = 0

for i in range(0, len(lines)):
    a = lines[i].split()
    a[1] = int(a[1])
    if a[0] == "forward":
        h += a[1]
    elif a[0] == "down":
        d += a[1]
    elif a[0] == "up":
        d -= a[1]

print(f"h={h}")
print(f"d={d}")
print(f"\nresult={h*d}")
