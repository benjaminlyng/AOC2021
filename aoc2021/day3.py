from operator import itemgetter
with open("inputs/day3.txt") as f:
    diagnostics = f.readlines()

def columns(diagnostics, l):
    report_length = len(diagnostics)

    gamma = []
    epsilon = []
    for i in range(l):
        column = map(itemgetter(i), diagnostics)
        column = map(int,column)
        s = sum(column)
        gamma.append(1 if s>=report_length/2 else 0)
        epsilon.append(0 if s>report_length/2 else 1)
    return gamma, epsilon


def power_consumption(diagnostics:list, l:int) -> int:
    """
    >>> t = [ "00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]
    >>> power_consumption(t, 5)
    198
    """
    
    gamma, epsilon = columns(diagnostics, l)
    gamma = int("".join(str(g) for g in gamma), 2)
    epsilon= int("".join(str(g) for g in epsilon), 2)
    return gamma*epsilon

def life_support(diagnostics, l):
    """
    3>>> t = [ "00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]
    #>>> life_support(t, 5)
    #198
    """
    oxygen = []
    co2 = []
    gamma, epsilon = columns(diagnostics, l)
    
    
    for i in range(l):
        o = list(filter(lambda x: x[i] == gamma[i], diagnostics))
        gamma, _ = columns(gamma, l)
        epsilon = list(filter(lambda x: x[i] == epsilon[i], diagnostics))
        epsilon, _ = columns(epsilon, l)
        print(list(o), list(c))
    # print(diagnostics)
    # print(diagnostics[0], diagnostics[-1] )
    

    

# print(power_consumption(diagnostics, 12))
life_support(diagnostics, 12)
