#! /usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import *
import openpyxl
import csv
import sys
from pylab import *

path = '/wrk/gcao/Dataset/government_award/'

def toCSV(year):
    wb = openpyxl.load_workbook(path + 'data/' + year + '.xlsx')
    sh = wb.get_active_sheet()
    with open(path + 'data/'+ year + '.csv', 'wb') as f:
        c = csv.writer(f)
        for r in sh.rows:
            string = [] 
            for cell in r:
                if cell.value < u'\u9fff' and cell.value > u'\u4e00':
                    print cell.value
                    string.append(cell.value.encode('utf-8'))
                else:
                    string.append(cell.value)
            c.writerow(string)

# from countries
def getLookup(year):
    lookup = {}
    countries = []
    if year == '2011':
        name = 'lookup2.txt'
    else:
        name = 'lookup.txt'
    with open(path + 'info/'+ name) as fr:
        for line in fr:
            #print line
            countries.append(line.split()[1]) 
            lookup[line.split()[0]] = line.split()[1]
    return lookup, countries

# from embassies 
def buildLookup2():
    countries = []
    with open(path + 'data/'+ '2011.csv') as fr:
        for line in fr:
            #print line.split(',')[2]
            countries.append(line.split(',')[2])
    countries = set(countries)
    for c in countries:
        print c.decode('utf8')

def analysis(year):
    year = str(year)
    countries = []
    lookup, countries = getLookup(year)
    freq = {}; fracs = {}
    total = 0
    for c in countries:
        freq[c] = 0
        fracs[c] = 0
    with open(path + 'data/' + year + '.csv') as fr:
        for line in fr:
            if year== '2010' or year == '2011':
                idx = 2
            else:
                idx = 3
            freq[lookup[line.split(',')[idx]]] = freq[lookup[line.split(',')[idx]]] + 1
            total = total + 1
    for c in countries:
        fracs[c] = (double(freq[c]) / total) * 100
    countries_sorted = sorted(fracs, key=lambda key: fracs[key], reverse=True) 
    #print fracs 
    return fracs, freq, countries_sorted

def writeFreq(freq, year):
    filename = path + 'info/'  + year + '_record.txt'
    with file(filename, 'w') as outfile:
        for c in countries:
            line = c + ' ' +  str(freq[c]) + '\n'
            outfile.write(line)
    outfile.close()

def plotPie(fracs, countries, year):

    # make a square figure and axes
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])

    # The slices will be ordered and plotted counter-clockwise.
        
    labels = countries
    fracs_new = []; 
    countries_new = []
    rest_frac = 0.0
    for idx, c in enumerate(countries):
        if fracs[c] > 3.0:
            fracs_new.append(fracs[c])
            countries_new.append(c)
        else:
            rest_frac = rest_frac + fracs[c]
    fracs_new.append(rest_frac)
    countries_new.append('rest')

    explode= zeros((len(countries_new), 1))
    explode[0] = .05
    print len(countries_new)
    print len(explode)
    pie(fracs_new, labels=asarray(countries_new),
    #pie(fracs_new, explode=explode, labels=asarray(countries_new),
                    autopct='%1.1f%%', shadow=True, startangle=90)
                    # The default startangle is 0, which would start
                    # the Frogs slice on the x-axis.  With startangle=90,
                    # everything is rotated counter-clockwise by 90 degrees,
                    # so the plotting starts on the positive y-axis.
    title('The fractions of awarded students by country in ' + year, bbox={'facecolor':'0.8', 'pad':5})
    #show()
    savefig(path + 'info/' + year + '.png')

def plotBar():
    nordic = ('finland', 'sweden', 'norway', 'denmark')
    N = 4
    ind = arange(N)
    width = .2
    rects = []
    #for 
    rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

def recordNordic():
    nordic_countries = ('finland', 'sweden', 'norway', 'denmark')
    nordic_freq = {}
    for c in nordic_countries:
        nordic_freq[c] = []
    for year in range(2010, 2016):
        fracs, freq, countries = analysis(year)
        for c in nordic_countries:
            nordic_freq[c].append(freq[c])
    print nordic_freq

def main():
    #year = sys.argv[1]
    #buildLookup()
    #buildLookup2()
    # toCSV(year)
    #fracs, freq, countries = analysis(year)
    #plotStat(fracs, countries, year)
    recordNordic()

if __name__ == '__main__':
    main()