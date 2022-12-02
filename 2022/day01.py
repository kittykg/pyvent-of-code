with open("input/day01", "r") as f:
    s = f.read()

groups = s.split("\n\n")
e_sum = [sum([int(i) for i in e.split()]) for e in groups]

# Task 1
print(max(e_sum))

# Task 2
print(sum(sorted(e_sum, reverse=True)[:3]))
