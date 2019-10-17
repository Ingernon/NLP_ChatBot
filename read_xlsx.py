import xlrd 
  
path = ("Trivia-Printable.xlsx") 
wb = xlrd.open_workbook(path) 
  
Q = []
A = []

for k in range(3):
	sheet = wb.sheet_by_index(k) 
	for j in range(3):
		for i in range(1, sheet.nrows):
			if sheet.cell_value(i, j*3) and sheet.cell_value(i, j*3 + 1):
				Q.append(sheet.cell_value(i, j*3))
				A.append(sheet.cell_value(i, j*3 + 1))

trivial = [[],[],[]]

sheet = wb.sheet_by_index(3)
for j in range(3):
	for i in range(1, sheet.nrows):
		if sheet.cell_value(i, j*4) and sheet.cell_value(i, j*4 + 1) and sheet.cell_value(i, j*4 + 2):
			trivial[0].append(sheet.cell_value(i, j*4))
			trivial[1].append(sheet.cell_value(i, j*4 + 1))
			trivial[2].append(sheet.cell_value(i, j*4 + 2))

