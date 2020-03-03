import sys
import itertools


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
    cf.remove(cf[0])
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
                    s += '+' + str(i)
                else:
                    s += '+/' + str(i)
            s += ' |'
            bad.append(s)
    return bad


def minim(values, dnf, cf, bad):
    for el in values:
        out = ''
        elstr = ''.join(str(x) for x in el)
        if elstr not in dnf:
            continue
        for coef in cf:
            s = "| "
            for i in coef:
                if elstr[5 - int(i)] == '0':
                    s += '+' + str(i)
                else:
                    s += '+/' + str(i)
            s += ' |'
            if s in bad:
                continue
            else:
                out += s + '+'
        out = out[:-1]
        print(out + '=1 for' + str(el) + '\n')


dnf = list()
for st in sys.stdin:
    st = st.strip('\n')
    dnf.append(st)
n = 6
cf = formCoefVect()
values = list(itertools.product(range(2), repeat=6))

bad = findBadMonoms(values, dnf, cf)
minim(values, dnf, cf, bad)
