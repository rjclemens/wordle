import statistics as stats

with open('results/exp_stg1_raw.txt') as file:
    data = file.read().split('\n')

data = [(e.split(':')[0], float(e.split(':')[1][1:])) for e in data]

data = list(sorted(data, key=lambda x: x[1], reverse=True))

avg = sum([x[1] for x in data])/len(data)
med = stats.median([x[1] for x in data])

print(f'Average:\t{avg}\t\tMedian:\t{med}')
for x in data:
    print(f'{x[0]}:\t{x[1]}')
