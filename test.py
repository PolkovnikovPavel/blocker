import psutil

l = list(psutil.process_iter())
l.sort(key=lambda x: x.name())

for p in l:
    try:
        print(p.name())
    except Exception:
        print(123)