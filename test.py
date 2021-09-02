import psutil

l = list(psutil.process_iter())
l.sort(key=lambda x: x.name())

for p in l:
    print(p.name())