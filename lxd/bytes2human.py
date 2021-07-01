def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8KB'
    # >>> bytes2human(100001221)
    # '95.4MB'
    symbols = ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    prefix = {s: 1 << (i + 1) * 10 for i, s in enumerate(symbols)}
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n
