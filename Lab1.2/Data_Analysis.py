from matplotlib import pyplot
from openpyxl import load_workbook

wb = load_workbook('data_analysis_lab.xlsx')
sheet = wb['Data']

def getvalue(x):
    return x.value

years = list(map(getvalue, wb['Data']['A'][1:]))
tempr = list(map(getvalue, wb['Data']['C'][1:]))
act = list(map(getvalue, wb['Data']['D'][1:]))

pyplot.plot(years, tempr, label="Graf_1")
pyplot.plot(years, act, label="Graf_2")
pyplot.show()
