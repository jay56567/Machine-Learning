fh = ['a','b','c','d','e','a','b','c','d','e']
lst = list()

for word in fh:
    if word not in lst:
        lst.append(word)

print lst
