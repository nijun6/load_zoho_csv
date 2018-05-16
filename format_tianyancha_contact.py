# -*- coding:utf-8 -*-

from sys import argv
if __name__ == '__main__':
    if len(argv) >= 2:
        ls = open(argv[1]).readlines()
        for l in ls:
            cns = l.replace("，",",").replace("、",",").replace("；",",").replace(";",",").replace("\n","").replace("/",",").replace(" ",",").replace('"', '').replace('\t', '')
            cns = cns.split(',')
            print ';'.join([e if not e.startswith('0') or '-' in e  else e[:4]+'-'+e[4:] for e in cns]).strip(';')