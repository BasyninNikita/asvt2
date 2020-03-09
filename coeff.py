import sys
import itertools
from collections import defaultdict
import re


def formCoefVect():
    cf = list(itertools.combinations_with_replacement(range(n), n))
    j = 0
    while j < len(cf):
        for i in range(n - 1):
            if cf[j][i] == cf[j][i + 1] and cf[j][i] != 0:
                cf.remove(cf[j])
                j -= 1
                break
        j += 1
    coef_vect = list()
    for el in cf:
        coef = ""
        for i in range(len(el) - 1):
            if el[i] == el[i + 1]:
                continue
            else:
                coef += str(el[i])
        coef += str(el[len(el) - 1])
        coef_vect.append(coef)
        coef_vect.append(coef[1:])
    coef_vect.remove(coef_vect[1])
    return coef_vect


def findBadMonoms(values, dnf, cf):  # , cf, dnf):
    bad = list()
    for el in values:
        elstr = ''.join(str(x) for x in el)
        if elstr in dnf:
            continue
        for coef in cf:
            s = "| "
            for i in coef:
                if elstr[5 - int(i)] == '0':
                    s += '+/' + str(i)
                else:
                    s += '+' + str(i)
            s += ' |'
            bad.append(s)
    return bad


def minim(values, dnf, cf, bad):
    numb = defaultdict(int)
    system = list()
    for el in values:
        ur = list()
        out = ''
        elstr = ''.join(str(x) for x in el)
        if elstr not in dnf:
            continue
        for coef in cf:
            s = "| "
            for i in coef:
                if elstr[5 - int(i)] == '0':
                    s += '+/' + str(i)
                else:
                    s += '+' + str(i)
            s += ' |'
            if s in bad:
                continue
            else:
                ur.append(s)
                a = numb.setdefault(s, 0)
                a += 1
                numb[s] = a
                out += s + '+'
        system.append(ur)
        out = out[:-1]
        print(out + '=1 for' + str(el))
    numb.pop('| +0+/1+/2+/3 |')
    sred = sorted(numb.items(), key=lambda value: value[1], reverse=True)
    sred.sort(key=lambda k: len(re.sub(r"[+/|]", "", k[0])))
    needed_coef = list()
    while system:
        for ur in system:
            if sred[0][0] in ur:
                needed_coef.append(sred[0][0])
                j = 0
                while j < len(system):
                    if sred[0][0] in system[j]:
                        system.remove(system[j])
                    else:
                        j += 1
                sred.remove(sred[0])
                dd = defaultdict(int)
                for uravn in system:
                    for coeff in uravn:
                        a = numb.setdefault(coeff, 0)
                        a += 1
                        dd[coeff] = a
                sred = sorted(dd.items(), key=lambda value: value[1], reverse=True)
                sred.sort(key=lambda k: len(re.sub(r"[+/|]", "", k[0])))
                break
    return needed_coef


dnf = list()
for st in sys.stdin:
    st = st.strip('\n')
    dnf.append(st)
n = 6
cf = formCoefVect()
values = list(itertools.product(range(2), repeat=6))
bad = findBadMonoms(values, dnf, cf)
minim(values, dnf, cf, bad)
