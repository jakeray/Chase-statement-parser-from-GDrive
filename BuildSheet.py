from distutils.command.build import build
from openpyxl import Workbook

def BuildSheet():
    wb = Workbook()
    ws = wb.active
    d = ws.cell(row=4, column=2, value=10)

    print(ws)

BuildSheet()