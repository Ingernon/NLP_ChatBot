import xlrd 
  
path = ("data/Trivia-Printable.xlsx") 
wb = xlrd.open_workbook(path) 

def get_trivial(BAN_WORD, BAN_TAG, MAX_SIZE):
	trivial = [[],[],[]]
	for k in range(3):
		sheet = wb.sheet_by_index(k) 
		for j in range(3):
			for i in range(1, sheet.nrows):
				if sheet.cell_value(i, j*3) and sheet.cell_value(i, j*3 + 1):
					trivial[0].append("none")
					trivial[1].append(sheet.cell_value(i, j*3))
					trivial[2].append(sheet.cell_value(i, j*3 + 1))


	sheet = wb.sheet_by_index(3)
	for j in range(3):
		for i in range(1, sheet.nrows):
			if sheet.cell_value(i, j*4) and sheet.cell_value(i, j*4 + 1) and sheet.cell_value(i, j*4 + 2):
				trivial[0].append(sheet.cell_value(i, j*4))
				trivial[1].append(sheet.cell_value(i, j*4 + 1))
				trivial[2].append(sheet.cell_value(i, j*4 + 2))
	i = 0
	while i in range(len(trivial[0])):
		if (any(x in trivial[1][i] for x in BAN_WORD) or len(trivial[1][i]) > MAX_SIZE):
			for j in range(3):
				del trivial[j][i]
		else :
			i+=1
	return trivial

#tmp = get_trivial(["_", "'", "&", '"', ":", "(", ")"], [], 100)
#print(len(tmp[0]))
#for i in range(len(tmp[0])):
#	print(i, " : " , tmp[1][i], ":", tmp[2][i])
