def a_ord(sim):
    if '0' <= sim <= '9':
        return ord(sim) - ord('0')
    elif 'a' <= sim <= 'z':
        return ord(sim) - ord('a') + 21

def metrics(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return abs(a-b)
    if isinstance(a, int) and isinstance(b, str):
    	return metrics(str(a), b)
    if isinstance(a, str) and isinstance(b, str):
        if (a.isdigit()) and (b.isdigit()):
            return abs(int(a)-int(b))
        elif (len(a) == 1) and (len(b) == 1):
            return abs(a_ord(a) - a_ord(b))
        elif (len(a) == len(b)):
            sum = 0
            for sim, i in enumerate(a):
                sum += metrics(sim, b[i])**2
            return sum**(1/2)
        else:
            diff = abs(len(a)-len(b))
            return metrics('0'*diff + a, b) if (len(b) > len(a)) else metrics(a, '0'*diff+b)
    if isinstance(a, str) and isinstance(b, list):
        sum = 0
        for attr in b:
            sum += metrics(a, attr)^2
        return (sum**(1/2))/len(b)
    if instance(a, list) and isinstance(b, list):
        sum = 0
        for attr in a:
            sum += metrics(attr, b)**2
        return sum**(1/2)
    return metrics(b,a)