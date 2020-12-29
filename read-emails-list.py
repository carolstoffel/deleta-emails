d = {}

with open('lista_de_emails.txt', 'r') as arquivo:
    em = arquivo.read().split(',')
    for e in em:
        if e not in d.keys():
            d[e] = 1
        else:
            d[e] += 1

for key, value in d.items():
    if value > 5:
        print(key)
