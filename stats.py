import csv
f = open("gen9.txt", "r")
content = f.readlines()
stats_array = []
for line in content:
    if 'Max Position' in line:
        stats_array.append(line)

stats = [[],[],[],[]]

with open('dkstats.csv', 'w+', newline='') as csvfile:
		filewrite = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewrite.writerow(['"generation"', '"genome"', '"fitness"', '"maxposx"'])

for i in stats_array:
    if 'Running' in i:
        gen = i.split('generation', 1)[(- 1)].split('*', 1)[0].strip()
    if 'Max Position' in i:
        genome = i.split('Genome:', 1)[(- 1)].split('F', 1)[0].strip()
        fitness = i.split('Fitness:', 1)[(- 1)].split('M', 1)[0].strip()
        maxpos = i.split('X:', 1)[(- 1)].split('  ', 1)[0].strip()

    with open('dkstats.csv', 'w+', newline='') as csvfile:
        filewrite = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewrite.writerow([gen, genome, fitness, maxpos])
