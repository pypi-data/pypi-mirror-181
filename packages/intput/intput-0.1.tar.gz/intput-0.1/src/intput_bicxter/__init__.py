def intput(prompt='', errorMsg=None):
	inpt=None
	while type(inpt) != int:
		try:
			inpt = int(input(prompt))
		except ValueError:
			if errorMsg != None:
				print(errorMsg)
			else:
				pass
	return inpt