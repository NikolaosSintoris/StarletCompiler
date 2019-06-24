import sys

program_tk,endprogram_tk,declare_tk="program","endprogram","declare"
if_tk,then_tk,else_tk,endif_tk="if","then","else","endif"
dowhile_tk,enddowhile_tk,while_tk,endwhile_tk="dowhile","enddowhile","while","endwhile"
loop_tk,endloop_tk,exit_tk="loop","endloop","exit"
forcase_tk,endforcase_tk,incase_tk,endincase_tk="forcase","endforcase","incase","endincase"
when_tk,endwhen_tk,default_tk,enddefault_tk="when","endwhen","default","enddefault"
function_tk,endfunction_tk,return_tk="function","endfunction","return"
in_tk,inout_tk,inandout_tk="in","inout","inandout"
and_tk,or_tk,not_tk="and","or","not"
input_tk,print_tk="input","print"
plus_tk,minus_tk,mul_tk,div_tk="plus","minus","mul","div"
lower_tk,greater_tk,equal_tk,lowerequal_tk,greaterequal_tk,dif_tk="lower","greater","equal","lowerequal","greaterequal","dif"
assign_tk,semi_tk,comma_tk,colon_tk="assign","semi","comma","colon"
leftpar_tk,rightpar_tk,leftbr_tk,rightbr_tk="leftpar","rightpar","leftbracket","rightbracket"
startcomm_tk,endcomm_tk,linecomm_tk="startcomment","endcomment","linecomment"
constant_tk,variable_tk="constant","variable"

commitedwords = {"program":program_tk, "endprogram":endprogram_tk,"declare":declare_tk,"if":if_tk, 
"then":then_tk, "else" :else_tk,"endif":endif_tk,
"dowhile":dowhile_tk, "enddowhile":enddowhile_tk, "while":while_tk, "endwhile":endwhile_tk,
"loop":loop_tk, "endloop":endloop_tk, "exit":exit_tk,
"forcase":forcase_tk, "endforcase":endforcase_tk, "incase":incase_tk, "endincase":endincase_tk,
"when":when_tk, "endwhen":endwhen_tk, "default":default_tk, "enddefault":enddefault_tk,
"function":function_tk, "endfunction":endfunction_tk, "return":return_tk, 
"in":in_tk, "inout":inout_tk, "inandout":inandout_tk,
"and":and_tk, "or":or_tk, "not":not_tk,
"input":input_tk, "print":print_tk}

symbols={"+":plus_tk,"-":minus_tk,"*":mul_tk,"=":equal_tk,";":semi_tk,"(":leftpar_tk,")":rightpar_tk,"[":leftbr_tk,"]":rightbr_tk,",":comma_tk}

mylist = ["*","/"]
errors = ["!","@","$","#","^","&","_","{","}","`","~",".","'"]


char = ""

fd = open(str(sys.argv[1]))
first = True
row = 1


token = ""
tokenid = ""


program_name = ""
next_quad_number = 0
program_list = []
new_temp_index = 0
exitloop = []
exitflag = []
returnFlag = False
declarelist = []
declarestring = ""


symbol_table = []
offset = 8
indexScope = -1
argumentList = []
checkArgumentList = []
subProgramNameList = []
mainFrameLength = 0


finalCodeTable = []
cpList = []
cpFlag = False
functionLabel = ""
parameterList = []


def gnlvcode(nonLocalVariable,label):
	global indexScope, symbol_table, finalCodeTable

	if (label == ""):
		finalCodeTable.append("\tlw, $t0, -4($sp)")
	else:
		finalCodeTable.append(label+"\n"+"\tlw, $t0, -4($sp)")	
	tempIndexScope = indexScope - 1

	pos = -1
	gnlvcodeFlag = False
	while (gnlvcodeFlag == False):
		# Search inside the current Scope.If you find this variable, save its position 
		for j in range(0, len(symbol_table[tempIndexScope]), 1):
			if (symbol_table[tempIndexScope][j][0] == nonLocalVariable):
				gnlvcodeFlag = True
				pos = j
		# If you did not find the variable, go to the next(previous) scope
		if (gnlvcodeFlag == False):
			finalCodeTable.append("\tlw, $t0, -4($sp)")
			tempIndexScope = tempIndexScope - 1

	finalCodeTable.append("\taddi $t0, $t0, -"+str(symbol_table[tempIndexScope][pos][1]))
		
def loadvr(variable, register, label):
	global indexScope, symbol_table, finalCodeTable

	
	if(variable.isdigit()):		# If variable is immidiate then i store its value to the register
		if (label == ""):
			finalCodeTable.append("\tli $t"+str(register)+", "+str(variable))
		else:
			finalCodeTable.append(label+"\n"+"\tli $t"+str(register)+", "+str(variable))	
	else:
		(x, y) = searchEntity(variable)

		if ((x == 0) and (symbol_table[x][y][0].find("T_") == -1)):	# If the variable is global
			if (label == ""):
				finalCodeTable.append("\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($s0)")
			else:
				finalCodeTable.append(label+"\n"+"\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($s0)")
		elif (x == indexScope):
			if (symbol_table[x][y][0].find("T_") != -1):
				if (label == ""):
					finalCodeTable.append("\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
				else:
					finalCodeTable.append(label+"\n"+"\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
			elif (len(symbol_table[x][y]) == 2) :
				if (label == ""):
					finalCodeTable.append("\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
				else:
					finalCodeTable.append(label+"\n"+"\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
			elif (symbol_table[x][y][2] in ["in", "inandout"]):	
				if (label == ""):
					finalCodeTable.append("\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
				else:
					finalCodeTable.append(label+"\n"+"\tlw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")	
			elif (symbol_table[x][y][2] == "inout"):
				if (label == ""):		
					finalCodeTable.append("\tlw $t0, -"+str(symbol_table[x][y][1])+"($sp)")
				else:
					finalCodeTable.append(label+"\n"+"\tlw $t0, -"+str(symbol_table[x][y][1])+"($sp)")	
				finalCodeTable.append("\tlw $t"+str(register)+", 0($t0)")
			else:
				None					
		else:
			if (symbol_table[x][y][0].find("T_") != -1):
				gnlvcode(variable,label)
				finalCodeTable.append("\tlw $t"+str(register)+", 0($t0)")	
			elif (len(symbol_table[x][y]) == 2):
				gnlvcode(variable,label)
				finalCodeTable.append("\tlw $t"+str(register)+", 0($t0)")	
			elif (symbol_table[x][y][2] in ["in", "inandout"]): 	
				gnlvcode(variable,label)
				finalCodeTable.append("\tlw $t"+str(register)+", 0($t0)")
			elif (symbol_table[x][y][2] == "inout"):		
				gnlvcode(variable,label)
				finalCodeTable.append("\tlw $t0, 0($t0)")	
				finalCodeTable.append("\tlw $t"+str(register)+", 0($t0)")
			else:
				None
	
def storerv(register, variable):
	global finalCodeTable

	(x, y) = searchEntity(variable)

	if ((x == 0) and (symbol_table[x][y][0].find("T_") == -1)):	# If the variable is global
		finalCodeTable.append("\tsw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($s0)")
	elif (x == indexScope):
		if (symbol_table[x][y][0].find("T_") != -1):
			finalCodeTable.append("\tsw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
		elif (len(symbol_table[x][y]) == 2):
			finalCodeTable.append("\tsw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
		elif (symbol_table[x][y][2] in ["in", "inandout"]):
			finalCodeTable.append("\tsw $t"+str(register)+", -"+str(symbol_table[x][y][1])+"($sp)")
		elif (symbol_table[x][y][2] == "inout"):	
			finalCodeTable.append("\tlw $t0"+", -"+str(symbol_table[x][y][1])+"($sp)")
			finalCodeTable.append("\tsw $t"+str(register)+", "+"0($t0)")
		else:
			None	
	else: 
		if (symbol_table[x][y][0].find("T_") != -1):
			gnlvcode(variable,"")
			finalCodeTable.append("\tsw $t"+str(register)+", "+"0($t0)")
		elif (len(symbol_table[x][y]) == 2):
			gnlvcode(variable,"")
			finalCodeTable.append("\tsw $t"+str(register)+", "+"0($t0)")	
		elif (symbol_table[x][y][2] in ["in", "inandout"]): 	
			gnlvcode(variable,"")
			finalCodeTable.append("\tsw $t"+str(register)+", "+"0($t0)")
		elif (symbol_table[x][y][2] == "inout"):	
			gnlvcode(variable,"")	
			finalCodeTable.append("\tlw $t0"+", "+"0($t0)")
			finalCodeTable.append("\tsw $t"+str(register)+", "+"0($t0)")
		else:
			None

def createFinalCodeTable(aTable, functionName):
	global finalCodeTable, indexScope, symbol_table, program_name, cpList, cpFlag, functionLabel, parameterList

	parameterFlag = False
	parameterCount = -1

	for l2 in aTable:
		if(l2[1] == "jump"):
			finalCodeTable.append("L"+str(l2[0])+":"+"\n"+"\tj "+"L"+str(l2[4]))
		elif (l2[1] in ["equal", "<>", ">", "<", "<=", ">="]):
			loadvr(l2[2],1,"L"+str(l2[0])+": ")
			loadvr(l2[3],2,"")
			if (l2[1] == "equal"):
				finalCodeTable.append("\tbeq $t1, $t2, "+l2[4])
			elif (l2[1] == "<>"):
				finalCodeTable.append("\tbne $t1, $t2, "+l2[4])
			elif (l2[1] == ">"):
				finalCodeTable.append("\tbgt $t1, $t2, "+l2[4])
			elif (l2[1] == "<"):
				finalCodeTable.append("\tblt $t1, $t2, "+l2[4])
			elif (l2[1] == ">="):
				finalCodeTable.append("\tbge $t1, $t2, "+l2[4])
			else:
				finalCodeTable.append("\tble $t1, $t2, "+l2[4])	
		elif (l2[1] == ":="):
			loadvr(l2[2],1,"L"+str(l2[0])+": ")	
			storerv(1,l2[4])
		elif (l2[1] in ["+", "-", "*", "/"]):
			loadvr(l2[2],1,"L"+str(l2[0])+": ")	
			loadvr(l2[3],2,"")
			if (l2[1] == "+"):
				finalCodeTable.append("\tadd $t1, $t1, $t2")
			elif (l2[1] == "-"):
				finalCodeTable.append("\tsub $t1, $t1, $t2")
			elif (l2[1] == "*"):
				finalCodeTable.append("\tmul $t1, $t1, $t2")
			else:
				finalCodeTable.append("\tdiv $t1, $t1, $t2")
			storerv(1,l2[4])
		elif (l2[1] == "out"):
			finalCodeTable.append("L"+str(l2[0])+":"+"\n"+"\tli $v0, 1")
			loadvr(l2[2],0,"")			
			finalCodeTable.append("\tmove $a0, $t0")
			finalCodeTable.append("\tsyscall")
		elif (l2[1] == "inp"):
			finalCodeTable.append("L"+str(l2[0])+":"+"\n"+"\tli $v0, 5")
			finalCodeTable.append("\tsyscall")
			finalCodeTable.append("\tmove $t0, $v0")
			storerv(0,l2[2])						
		elif (l2[1] == "retv"):
			loadvr(l2[2],1,"L"+str(l2[0])+": ")
			finalCodeTable.append("\tlw $t0, -8($sp)")
			finalCodeTable.append("\tsw $t1, 0($t0)")
		elif (l2[1] == "par"):
			if(l2[3] == "RET"):
				x2,y2 = searchEntity(l2[2])
				of=symbol_table[x2][y2][1]
				l=l2[:]
				l.append(of)
				parameterList.append(l)
			else:	
				parameterList.append(l2)	
		elif (l2[1] == "call"):
			for l7 in parameterList:
				firstTimePar = False 	#Gia ta label
				parameterCount = parameterCount + 1
				address = 12+(4*parameterCount)
				if (parameterFlag == False):
					parameterFlag = True
					x,y = searchEntity(l2[2])
					finalCodeTable.append("L"+str(l7[0])+":"+"\n"+"\taddi $fp, $sp, "+str(symbol_table[x][y][2]))
					firstTimePar = True
				if (l7[3] == "CV"):
					if (firstTimePar == True):
						loadvr(l7[2],0,"")
						firstTimePar = False
					else:
						loadvr(l7[2],0,"L"+str(l7[0])+": ")	
					finalCodeTable.append("\tsw $t0, -"+str(address)+"($fp)")
				elif (l7[3] == "CP"):
					if (firstTimePar == True):
						loadvr(l7[2],0,"")
						firstTimePar = False
					else:
						loadvr(l7[2],0,"L"+str(l7[0])+": ")	
					finalCodeTable.append("\tsw $t0, -"+str(address)+"($fp)")
					cpList.append([l7[2],parameterCount])
					cpFlag = True	
				elif (l7[3] == "REF"):
					x,y = searchEntity(l7[2])
					if (x == indexScope):
						if (len(symbol_table[x][y]) == 2):
							if (firstTimePar == True):
								finalCodeTable.append("\taddi $t0, $sp, -"+str(symbol_table[x][y][1]))
								firstTimePar = False
							else:
								finalCodeTable.append("L"+str(l7[0])+":"+"\n"+"\taddi $t0, $sp, -"+str(symbol_table[x][y][1]))
						elif (symbol_table[x][y][2] == "in"):
							if (firstTimePar == True):
								finalCodeTable.append("\taddi $t0, $sp, -"+str(symbol_table[x][y][1]))
								firstTimePar = False
							else:
								finalCodeTable.append("L"+str(l7[0])+":"+"\n"+"\taddi $t0, $sp, -"+str(symbol_table[x][y][1]))
						elif (symbol_table[x][y][2] == "inout"):
							if (firstTimePar == True):
								finalCodeTable.append("\tlw $t0, -"+str(symbol_table[x][y][1])+"($sp)")
								firstTimePar = False
							else:
								finalCodeTable.append("L"+str(l7[0])+":"+"\n"+"\tlw $t0, -"+str(symbol_table[x][y][1])+"($sp)")
						else:
							None
					else:
						if (len(symbol_table[x][y]) == 2):
							if (firstTimePar == True):
								gnlvcode(l7[2],"")
								firstTimePar = False
							else:
								gnlvcode(l7[2],"L"+str(l7[0])+": ")
						elif (symbol_table[x][y][2] == "in"):
							if (firstTimePar == True):
								gnlvcode(l7[2],"")
								firstTimePar = False
							else:
								gnlvcode(l7[2],"L"+str(l7[0])+": ")
						elif (symbol_table[x][y][2] == "inout"):
							if (firstTimePar == True):
								gnlvcode(l7[2],"")
								firstTimePar = False
							else:	
								gnlvcode(l7[2],"L"+str(l7[0])+": ")
							finalCodeTable.append("\tlw $t0, 0($t0)")
						else:
							None
					finalCodeTable.append("\tsw $t0, -"+str(address)+"($fp)")
				elif (l7[3] == "RET"):
					if (firstTimePar == True):
						finalCodeTable.append("\taddi $t0, $sp, -"+str(l7[5]))
						firstTimePar = False
					else:	
						finalCodeTable.append("L"+str(l7[0])+":"+"\n"+"\taddi $t0, $sp, -"+str(l7[5]))
					finalCodeTable.append("\tsw $t0, -8($fp)")
				else: 
					None
			x,y = searchEntity(l2[2])
			if (x+1 == indexScope):	
				finalCodeTable.append("L"+str(l2[0])+":"+"\n"+"\tlw $t0, -4($sp)")
				finalCodeTable.append("\tsw $t0, -4($fp)")
			else:
				finalCodeTable.append("L"+str(l2[0])+":"+"\n"+"\tsw $sp, -4($fp)")	
			finalCodeTable.append("\taddi $sp, $sp, "+str(symbol_table[x][y][2]))
			x3,y3 = searchEntity(l2[2])
			functionLabel = str(symbol_table[x3][y3][1])
			finalCodeTable.append("\tjal "+"L"+functionLabel)
			if (cpFlag == True):
				cpFlag = False
				finalCodeTable.append("\tmove $s1, $sp")
				finalCodeTable.append("\taddi $sp, $sp, -"+str(symbol_table[x][y][2]))
				for cpEntity in cpList:
					a = 12 + (4*cpEntity[1])
					finalCodeTable.append("\tlw $t7, -"+str(a)+"($s1)")	
					storerv(7,cpEntity[0])	
			else:		
				finalCodeTable.append("\taddi $sp, $sp, -"+str(symbol_table[x][y][2]))
			cpList = []	
			parameterList = []
		elif (l2[1] == "begin_block"):
			if (functionName != program_name):
				finalCodeTable.append("L"+str(l2[0])+":"+"\n"+"\tsw $ra, 0($sp)")
		elif (l2[1] == "end_block"):	
			if (functionName != program_name):
				finalCodeTable.append("L"+str(l2[0])+":"+"\n"+"\tlw $ra, 0($sp)")
				finalCodeTable.append("\tjr $ra")
		else:		
			None


def newscope():
	global symbol_table, offset, indexScope

	indexScope = indexScope + 1
	offset = 8
	symbol_table.append([])

def newEntity(tokenString, tokenidString, firstQuad, framelength, listArgument):
	global offset

	if (tokenString == variable_tk):
		offset = offset + 4
		if(len(firstQuad) > 0):
			return [tokenidString, offset,firstQuad]
		else:
			return [tokenidString, offset]	
	elif (tokenString == function_tk):
		return [tokenidString, firstQuad, framelength, listArgument]
	else:	
		offset = offset + 4
		return[tokenidString, offset]	

def insertEntity(aList):
	global symbol_table, indexScope, row

	for q in symbol_table[indexScope]:
		if (q[0] == aList[0]):
			print("\nThis variable name is already declared in line: ", row)
			sys.exit(0)

	symbol_table[indexScope].append(aList)

def searchEntity(name):
	global symbol_table

	for i in range(indexScope, -1, -1):
		for j in range(0, len(symbol_table[i]), 1):
			if (symbol_table[i][j][0] == name):
				return i,j

def deleteScope():
	global symbol_table, indexScope,offset

	indexScope = indexScope - 1
	del symbol_table[-1]

	if (indexScope>-1):
		for entity in symbol_table[indexScope]:
			if (len(entity)<=3):
				offset=entity[1]


def nextquad():
	global next_quad_number

	return str(next_quad_number)

def genquad(op, x, y, z):
	global next_quad_number

	number = next_quad_number
	next_quad_number = next_quad_number + 1
	temp = [str(number), op, x, y, z]
	program_list.append(temp)

def newtemp():
	global new_temp_index
	
	new_temp_index = new_temp_index + 1
	temp_value = "T_"+str(new_temp_index)

	myList = newEntity("", temp_value, "", "", [])
	insertEntity(myList)

	return temp_value		

def emptylist():

	return []

def makelist(x):
	new_list = []
	new_list.append(x)
	return new_list

def mergelist(l1, l2):

	return l1 + l2

def backpatch(alist, z):
	global program_list

	for list1 in program_list:
		if (list1[0] in alist):
			list1[4] = z

			
def read_char():	#A function that reads the next character of the file
	global char,row, fd
	char = fd.read(1)
	#Checks if the file has one of the forbidden characters.If it has then exit.
	if (char in errors):
		print("Forbidden character %s" %(char))
		sys.exit(0)
	if(char == "\n"):
		row = row + 1
	return char
	
def lex():
	global token,tokenid,first,char,row
	string = ""
	final_string = ""
	
	#Reads the first character of the file.Only the first time
	if(first == True):
		read_char()
		first = False
	
	#Ignore the white spaces of the file
	while char.isspace():
		read_char()
			
	#check if we have div or a comment	
	if (char == '/'):
		#We have div
		read_char()
		if (char not in mylist): 
			#print(div_tk)
			tokenid = div_tk
			return (div_tk)		
		#We have comments
		elif (char == "*"):
			read_char()
			while (char != "*"):
				read_char()
				#checks if it starts comments inside comments
				if(char == "/"):
					read_char()
					if(char in mylist):
						print("Wrong syntax.Comments in comments in line: ",row)
						sys.exit(0)
			read_char()	
			if (char == "/"):
				#print("/* Comment")
				read_char()
				return(lex())
			else:
				print("Wrong syntax.Comments never closed")
				sys.exit(0)	
		elif (char == "/"):
			read_char()
			while (char != "\n"):
				read_char()
				#checks if it starts comments inside comments
				if(char == "/"):
					read_char()
					if(char in mylist):
						print("Wrong syntax.Comments in comments in line: ",row)
						sys.exit(0)		
			#print("// comments")
			read_char()
			return (lex())
	#Check the lowercase			
	elif (char == "<"):
		read_char()
		if(char == "="):
			read_char()
			#print(lowerequal_tk)
			tokenid = "<=" #tokenid = lowerequal_tk
			return (lowerequal_tk)
		elif(char == ">"):
			read_char()
			#print(dif_tk)
			tokenid = "<>"	#tokenid = dif_tk
			return (dif_tk)
		else:
			tokenid = "<"	#tokenid = lower_tk
			#print(lower_tk)
			return (lower_tk)
	#check the greater case		
	elif (char == ">"):
		read_char()
		if (char == "="):
			read_char()
			#print(greaterequal_tk)
			tokenid = ">="	#tokenid = greaterequal_tk
			return (greaterequal_tk)
		else:
			#print(greater_tk)
			tokenid = ">"	#tokenid = greater_tk
			return (greater_tk)
	elif (char == ":"):
		if(read_char() == "="):
			read_char()
			#print(assign_tk)
			tokenid = ":="	#tokenid = assign_tk
			return (assign_tk)
		else:
			read_char()
			#print(colon_tk)
			tokenid = colon_tk
			return (colon_tk)
	#Check if it is a symbol
	elif (char in symbols):
		temp = symbols[char]
		read_char()
		#print(temp)
		tokenid = temp
		return (temp)
	else:
		#Reads until it finds sth that it is not a char or a number
		while (char.isalnum()):
			string = string + char
			read_char()
		#Saves only the 30 first characters of a string	
		if (len(string) > 30 ):
			final_string = string[0:30]
		else:
			final_string = string
		#Checks if it is a constant	
		if (final_string.isdigit()):
			if (int(final_string) in range (-32767,32768)):
				#print(constant_tk)
				tokenid = final_string
				return (constant_tk)
			else:
				print("Number out of range in line: ",row)
				sys.exit(0)	
		#Checks if the first char of the string is number		
		elif (final_string[0].isdigit()):
			print("Wrong syntax because the string starts with digit in line: ",row)
			sys.exit(0)
		#Checks if the string is a commited word	
		elif (final_string in commitedwords):
			#print(commitedwords[final_string])
			tokenid = commitedwords[final_string]
			return (commitedwords[final_string])
		else:
			#print(variable_tk)
			tokenid = final_string	
			return (variable_tk)

				
def program ():
	global token,tokenid,program_name, returnFlag, row, finalCodeTable
	
	token=lex()
	if (token==program_tk):
		token=lex()
		if (token==variable_tk):
			newscope()
			program_name = tokenid
			finalCodeTable.append("j L"+program_name)
			token=lex()
			block(program_name)
			if (token==endprogram_tk):
				#Checks if a return exists outside a function
				if (returnFlag == True):
					print("\nIt is not allowd a return statement outside a function\n")
					sys.exit(0)
				#Checks if it has sth after endprogram
				read_char()
				if(not char):
					print("\nThe program compiled succesfully \n")
				else:
					print("Wrong Syntax.After endprogram there is a character")	
					sys.exit(0)
			else:	
				print("The keyword 'endprogram' was expected in line: ",row)
				sys.exit(0)	
		else:
			print("Program name was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'program' was expected in line: ",row)
		sys.exit(0)

def block(name):
	global program_name, symbol_table, argumentList, mainFrameLength, next_quad_number, indexScope, program_list, finalCodeTable

	declarations()
	subprograms()
	if (name == program_name):
		
		genquad("begin_block", name, "_", "_")
		statements()

		for q in symbol_table[0]:
			if (len(q) <= 3):
				mainFrameLength = q[1] + 4

		genquad("halt", "_", "_", "_")
		genquad("end_block", name, "_", "_")	

		#print("\nUntil Scope: ", indexScope)
		#print(symbol_table)

		finalCodeTable.append("L"+program_name+":"+"\n"+"\taddi $sp, $sp, "+str(mainFrameLength))
		finalCodeTable.append("\tmove $s0, $sp")

		flag = False
		temporaryList = []
		for l1 in program_list:
			if(l1[2] == program_name):
				if(flag == True):
					flag = False
					break
				else:
					flag = True	
				continue
			if(flag == True):
				temporaryList.append(l1)	

		createFinalCodeTable(temporaryList,name)

		deleteScope()
	else:
		genquad("begin_block", name, "_", "_")

		x,y = searchEntity(name)
		symbol_table[x][y][1] = next_quad_number - 1

		statements()

		tempFrameLength = 0
		for q in symbol_table[x+1]:
			if (len(q) <= 3):
				tempFrameLength = q[1] + 4
		symbol_table[x][y][2] = tempFrameLength

		genquad("end_block", name, "_", "_")

		#print("Until Scope: ", indexScope)
		#for q in symbol_table:
			#print(q)
		#print("\n")

		flag = False
		temporaryList = []
		for l1 in program_list:
			if(l1[2] == name):
				temporaryList.append(l1)
				if(flag == True):
					flag = False
					break
				else:
					flag = True	
				continue
			if(flag == True):
				temporaryList.append(l1)			

		createFinalCodeTable(temporaryList,name)

		deleteScope()
			
def declarations():
	global token
	
	while (token == declare_tk):
		token = lex()
		varlist()
		if(token != semi_tk):
			print("Wrong syntax.Semi colon ';' was expected in line: ",row)
			sys.exit(0)
		token = lex()	

def varlist():
	global token,tokenid
	
	if (token == variable_tk):
		myList = newEntity(token, tokenid, "", "", [])
		insertEntity(myList)
		token = lex()
		while (token == comma_tk):
			token = lex()
			if (token == variable_tk):
				myList = newEntity(token, tokenid, "", "", [])
				insertEntity(myList)
				token = lex()
			else:
				print("Variable name was expected in line: ",row)
				sys.exit(0)		
	
def subprograms():
	global token
	
	while (token == function_tk):
		subprogram()
	
def subprogram():
	global token, tokenid, returnFlag, program_name, subProgramNameList
	
	if (token==function_tk):
		token=lex()
		if (token==variable_tk):
			subprogram_name = tokenid  # Store the subprogram name an pass it to the funcbody
			#Checks if a function name is already used
			if(subprogram_name in subProgramNameList):
				print("\nThis function name is already used\n")
				sys.exit(0)
			else:
				subProgramNameList.append(subprogram_name)	
			#Check if a function name has the same name as he main program
			if(subprogram_name == program_name):
				print("\nYou can not use as a function name, the name of the main program\n")
				sys.exit(0)

			myList = newEntity(function_tk, subprogram_name, "", "", [])
			insertEntity(myList)
			newscope()

			token=lex()
			funcbody(subprogram_name)
			if(token==endfunction_tk):
				if (returnFlag == False):
					print("\nA function must have a return statement\n")
					sys.exit(0)
				else:
					returnFlag = False	
					token=lex()
			else:
				print("The keyword 'endfunction' was expected in line: ",row)
				sys.exit(0)
		else:
			print("Subprogram name was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'function' was expected in line: ",row)
		sys.exit(0)		

def funcbody(name):
	formalpars(name)
	block(name)

def formalpars(name):
	global token, symbol_table, argumentList
	if (token==leftpar_tk):
		token=lex()
		formalparlist()
		if (token==rightpar_tk):
			x,y = searchEntity(name)
			symbol_table[x][y][3] = argumentList
			argumentList = []
			token=lex()
		else:
			print("Right parenthesis ')' was expected in line: ",row)
			sys.exit(0)
	else:
		print("Left parenthesis '(' was expected in line: ",row)
		sys.exit(0)

def formalparlist():
	global token

	if (token in [in_tk,inout_tk,inandout_tk]):
		formalparitem()
		while (token == comma_tk):
			token = lex()
			formalparitem()

def formalparitem():
	global token, tokenid, argumentList
	
	myformallist = [in_tk,inout_tk,inandout_tk]
	if (token in myformallist):
		argumentList.append(tokenid)
		temp = tokenid
		token = lex()
		if (token == variable_tk):
			myList = newEntity(token, tokenid, temp, "", [])
			insertEntity(myList)
			token = lex()
		else:
			print ("Variable name was expected in line: ",row)
			sys.exit(0)
	else:
		print("One of the following keywords was expected ",myformallist,"in line",row)
		sys.exit(0)
		
def statements():
	global token
	
	statement()
	while (token == semi_tk):
		token = lex()
		statement()
				
def statement():
	global token, exitflag, repeatFlag, row
	
	if (token==variable_tk):
		assignment_stat()
	elif (token == if_tk):
		if_stat()
	elif (token == while_tk):
		exitflag.append(False)
		while_stat()
	elif (token == dowhile_tk):
		exitflag.append(False)
		do_while_stat()
	elif (token == loop_tk):
		exitflag.append(True)
		loop_stat()
	elif (token == exit_tk):
		if(len(exitflag) > 0):
			if(exitflag[-1] == True):
				exit_stat()
			else:	
				print("\nWrong syntax. Wrong use of exit statement in line: ", row)
				sys.exit(0)
		else:
			print("\nWrong syntax. Wrong use of exit statement in line: ", row)	
			sys.exit(0)	
	elif (token == forcase_tk):
		exitflag.append(False)
		forcase_stat()
	elif (token == incase_tk):
		exitflag.append(False)
		incase_stat()
	elif (token == return_tk):
		return_stat()
	elif (token == input_tk):
		input_stat()
	elif (token == print_tk):
		print_stat()

def assignment_stat():
	global token
	
	if (token == variable_tk):
		id_name = tokenid
		token = lex()
		if (token == assign_tk):
			token = lex()
			ex1 = expression()
			genquad(":=", ex1, "_", id_name)
		else:
			print("The assignment symbol ':=' was expected in line: ",row)
			sys.exit(0)
	else:
		print("Variable name was expected in line: ",row)
		sys.exit(0)		

def if_stat():
	global token
	
	condition_true = []
	condition_false = []

	if (token == if_tk):
		token = lex()
		if(token == leftpar_tk):
			token = lex()
			condition_true,condition_false = condition()
			if(token == rightpar_tk):
				token = lex()
			else:
				print("Right parenthesis ')' was expected in line: ",row)
				sys.exit(0)
		else:
			print("Left parenthesis '(' was expected in line: ",row)
			sys.exit(0)
		if (token == then_tk):
			token = lex()
			backpatch(condition_true, nextquad())
			statements()
			if_list = makelist(nextquad())
			genquad("jump", "_", "_", "_")
			backpatch(condition_false, nextquad())
			elsepart()
			backpatch(if_list, nextquad())
			if (token == endif_tk):
				token = lex()
			else:
				print("The keyword 'endif' was expected in line: ",row)
				sys.exit(0)
		else:
			print("The keyword 'then' was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'if' was expected in line: ",row)	
		sys.exit(0)

def elsepart():
	global token
	
	if (token == else_tk):
		token = lex()
		statements()

def while_stat():
	global token, exitflag
	
	if (token == while_tk):
		token = lex()
		if (token == leftpar_tk):
			token = lex()
			begin = nextquad()
			condition_true,condition_false = condition()
			backpatch(condition_true, nextquad())
			if (token == rightpar_tk):
				token = lex()
			else:
				print("Right parenthesis was expected in line: ",row)
				sys.exit(0)
		else:
			print("Left parenthesis '(' was expected in line: ",row)
			sys.exit(0)
		statements()
		genquad("jump", "_", "_", begin)
		backpatch(condition_false, nextquad())
		if(token == endwhile_tk):
			exitflag = exitflag[:-1]
			token = lex()
		else:
			print("The keyword 'endwhile' was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'while' was expected in line: ",row)
		sys.exit(0)
		
def do_while_stat():
	global token, exitflag
	
	if (token == dowhile_tk):
		token = lex()
		begin = nextquad()
		statements()
		if (token == enddowhile_tk):
			token = lex()
			if (token == leftpar_tk):
				token = lex()
				condition_true,condition_false = condition()
				backpatch(condition_true, begin)
				backpatch(condition_false, nextquad())
				if (token == rightpar_tk):
					exitflag = exitflag[:-1]
					token = lex()
				else:
					print("Right parenthesis was expected in line: ",row)
					sys.exit(0)
			else:		
				print("Left parenthesis '(' was expected in line: ",row)
				sys.exit(0)
		else:
			print("the keyword 'enddowhile' was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'dowhile' was expected in line: ",row)
		sys.exit(0)

def loop_stat():
	global token, exitloop
	
	if (token == loop_tk):
		token = lex()
		exitloop.append([])
		begin = nextquad()
		statements()
		genquad("jump", "_", "_", begin)
		if(exitloop):
			backpatch(exitloop[-1], nextquad())
		exitloop.pop()
		if (token == endloop_tk):
			token = lex()
		else:
			print("The keyword 'endloop' was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'loop' was expected in line: ",row)
		sys.exit(0)
		
def exit_stat():
	global token, exitloop, exitflag
	
	if(token == exit_tk):
		token = lex()
		t = makelist(nextquad())
		genquad("jump", "_", "_", "_")
		exitloop[-1] = t
		exitflag = exitflag[:-1]
	else:
		print("The keyword exit was expected in line: ",row)
		sys.exit(0)

def forcase_stat():
	global token, exitflag
	
	if (token == forcase_tk):
		token = lex()
		if(token == when_tk):
			exitlist = emptylist()	#create an empty list that holds the exit numbers
			begin = nextquad()	#keep the first tag so that i can came back
			while (token == when_tk):
				token = lex()
				if (token == leftpar_tk):
					token = lex()
					condition_true,condition_false = condition()				
					if (token == rightpar_tk):
						token = lex()
					else:
						print("Right parenthesis was expected in line: ",row)
						sys.exit(0)
				else:		
					print("Left parenthesis '(' was expected in line: ",row)
					sys.exit(0)
				if (token == colon_tk):
					token = lex()
					backpatch(condition_true, nextquad())
					statements()
					# collects all the exit jumps so that can do exit
					whenlist = makelist(nextquad())
					genquad("jump","_", "_", "_")
					backpatch(condition_false, nextquad())
					exitlist = mergelist(exitlist, whenlist)
				else:
					print ("The symbol ':' was expected in line: ",row)
					sys.exit(0)
		if (token == default_tk):
			token = lex()
			if (token == colon_tk):
				token = lex()
				backpatch(condition_false, nextquad())
				statements()
				genquad("jump", "_", "_", begin)
				if(token == enddefault_tk):
					token = lex()
				else:
					print("The keyword 'enddefault' was expected in line: ",row)
					sys.exit(0)
			else:
				print("Colon ':' was expected in line: ",row)
				sys.exit(0)		
		else:
			print("The keyword 'default' was expected in line: ",row)
			sys.exit(0)
		if(token == endforcase_tk):
			exitflag = exitflag[:-1]
			token = lex()
			
			backpatch(exitlist, nextquad()) 
		else:
			print("The keyword 'endforcase' was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'forcase' was expected in line: ",row)
		sys.exit(0)

def incase_stat():
	global token, exitflag
	
	if(token == incase_tk):
		token = lex()
		var_temp = newtemp()
		begin = nextquad()
		genquad(":=", "1", "_", var_temp)
		while (token == when_tk):
			token = lex()
			if (token == leftpar_tk):
				token = lex()
				condition_true,condition_false = condition()
				
				if (token == rightpar_tk):
					token = lex()
				else:
					print("Right parenthesis was expected in line: ",row)
					sys.exit(0)
			else:		
				print("Left parenthesis '(' was expected in line: ",row)
				sys.exit(0)
			if (token == colon_tk):
				token = lex()
				backpatch(condition_true, nextquad())
				genquad(":=", "0", "_", var_temp)
				statements()
				backpatch(condition_false, nextquad())
			else:
				print ("The symbol ':' was expected in line: ",row)
				sys.exit(0)
		if(token == endincase_tk):
			exitflag = exitflag[:-1]
			token = lex()
			genquad("=", var_temp, "0", begin)
		else:
			print("The keyword 'endincase' was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'incase' was expected in line: ",row)
		sys.exit(0)

def return_stat():
	global token, returnFlag
	
	if(token == return_tk):
		returnFlag = True
		token = lex()
		ex1 = expression()
		genquad("retv", ex1, "_", "_")
	else:
		print("The keyword 'return' was expected in line: ",row)
		sys.exit(0)		

def print_stat():
	global token
	
	if(token == print_tk):
		token = lex()
		ex1 = expression()
		genquad("out", ex1, "_", "_")
	else:
		print("The keyword 'print' was expected in line: ",row)
		sys.exit(0)
		
def input_stat():
	global token
	
	if(token == input_tk):
		token = lex()
		if(token == variable_tk):
			input_value = tokenid
			token = lex()
			genquad("inp", input_value, "_", "_")
		else:
			print("Variable name was expected in line: ",row)
			sys.exit(0)
	else:
		print("The keyword 'input' was expected in line: ",row)
		sys.exit(0)		

def actualpars(functionName):
	global token, checkArgumentList, row
	
	if(token == leftpar_tk):
		token = lex()
		actualparlist()
		if(token == rightpar_tk):
			#Checks the parameters matched to the function parameters
			x,y = searchEntity(functionName)
			if(symbol_table[x][y][3] != checkArgumentList):
				print("\nWrong Syntax. Wrong parameter types in the call of a function in line: ", row)
				sys.exit(0)
			checkArgumentList = []
			token = lex()
			return True
		else:
			print("Right parenthesis ')' was expected in line: ",row)
			sys.exit(0)
	else:
		print("Left parenthesis '(' was expected in line: ",row)		
		sys.exit(0)
				
def actualparlist():
	global token
	
	if (token in [in_tk,inout_tk,inandout_tk]):
		actualparitem()
		while (token == comma_tk):
			token = lex()
			actualparitem()
		
def actualparitem():
	global token, checkArgumentList
	
	if (token == in_tk):
		checkArgumentList.append(in_tk)
		token=lex()
		ex1 = expression()
		genquad("par", ex1, "CV", "_")
	elif(token == inout_tk):
		checkArgumentList.append(inout_tk)
		token=lex()
		if(token == variable_tk):
			id_par = tokenid
			token=lex()
			genquad("par", id_par, "REF", "_")
		else:
			print("Variable name was expected in line: ",row)
			sys.exit(0)
	elif(token == inandout_tk):
		checkArgumentList.append(inandout_tk)
		token=lex()
		if(token == variable_tk):
			id_par = tokenid
			token=lex()
			genquad("par", id_par, "CP", "_")
		else:
			print("Variable name was expected in line: ",row)
			sys.exit(0)
	else:
		print("One of the following keywords was expected ",[in_tk,inout_tk,inandout_tk],"in line: ",row)		
		sys.exit(0)
		
def condition():
	global token
	
	boolterm1_true,boolterm1_false = boolterm()
	condition_true,condition_false = boolterm1_true,boolterm1_false
	while (token == or_tk):
		backpatch(condition_false, nextquad()) 	# If you find or and its is false go to the next one
		token = lex()
		boolterm2_true,boolterm2_false = boolterm()
		condition_true = mergelist(condition_true, boolterm2_true)
		condition_false = boolterm2_false 	# Get the false list from the last boolterm
	return condition_true,condition_false	

def boolterm():
	global token
	
	boolfactor1_true,boolfactor1_false = boolfactor()
	boolterm_true,boolterm_false = boolfactor1_true,boolfactor1_false
	while (token == and_tk):
		backpatch(boolterm_true, nextquad())
		token = lex()
		boolfactor2_true,boolfactor2_false = boolfactor()
		boolterm_false = mergelist(boolterm_false, boolfactor2_false)
		boolterm_true = boolfactor2_true
	return boolterm_true,boolterm_false 	
		
def boolfactor():
	global token
	
	boolfactor_true = []
	boolfactor_false = []

	if (token == not_tk):
		token = lex()
		if (token == leftbr_tk):
			token = lex()
			boolfactor_false,boolfactor_true = condition()
			if (token == rightbr_tk):
				token = lex()
			else:
				print ("Right bracket ']' was expected in line: ",row)
				sys.exit(0)
		else:
			print ("Left bracket ']' was expected in line: ",row)
			sys.exit(0)
	elif (token == leftbr_tk):
		token = lex()
		boolfactor_true,boolfactor_false = condition()
		if (token == rightbr_tk):
			token = lex()
		else:
			print ("Right bracket ']' was expected in line: ",row)
			sys.exit(0)
	else:
		ex1 = expression()
		relop = tokenid
		relational_oper()
		ex2 = expression()
		boolfactor_true = makelist(nextquad())
		genquad(relop, ex1, ex2, "_")
		boolfactor_false = makelist(nextquad())
		genquad("jump", "_", "_", "_")

	return boolfactor_true,boolfactor_false	
		
def expression():
	global token
	
	optional_sign()
	t1 = term()
	while (token in [plus_tk, minus_tk]):
		previous_token = token
		var = newtemp()
		add_oper()
		t2 = term()
		if(previous_token == plus_tk):
			genquad("+", t1, t2, var) # var = t1 + t2
		else:
			genquad("-", t1, t2, var)
		t1 = var 	# the result is stored in t1
	return t1		
	
def term():
	global token
	
	f1 = factor()
	while (token in [mul_tk, div_tk]):
		previous_token = token
		var = newtemp()
		mul_oper()
		f2 = factor()
		if(previous_token == mul_tk):
			genquad("*", f1, f2, var)
		else:
			genquad("/", f1, f2, var)
		f1 = var
	return f1		
			
def factor():
	global token, tokenid
	
	return_value = ""
	if(token == constant_tk):
		return_value = tokenid
		token = lex()
	elif (token == leftpar_tk):
		token = lex()
		return_value = expression()
		if(token == rightpar_tk):
			token = lex()
		else:
			print("Right parenthesis ')' was expected in line: ",row)
			sys.exit(0)
	elif (token == variable_tk):															#prepei na to kanw else.tha ta brethi to lathos parakatw
		function_name = tokenid # name of the function maybe
		token = lex()
		my_tail = idtail(function_name)
		if (my_tail != None):
			temp_value = newtemp() # i need a value to return
			genquad("par", temp_value, "RET", "_")
			genquad("call", function_name, "_", "_")
			return_value = temp_value # i save the value that needs to be returned
		else:
			return_value = function_name	
	else:
		print("Constant or right parenthesis '(' or variable name was expected in line: ",row)
		sys.exit(0)	

	return return_value	

def idtail(functioName):
	global token
	
	if (token == leftpar_tk):
		return actualpars(functioName)

def relational_oper():
	global token
	if(token in [equal_tk,lowerequal_tk,greaterequal_tk,greater_tk,lower_tk,dif_tk]):
		token = lex()
	else:
		print("A comparative operator was expected in line: ",row)
		sys.exit(0)		
		
def add_oper():
	global token
	
	if(token in [plus_tk,minus_tk]):
		token = lex()
	else:
		print("An add operator was expected in line: ",row)
		sys.exit(0)
		
def mul_oper():
	global token
	
	if(token in [mul_tk,div_tk]):
		token = lex()
	else:
		print("A mul operator was expected in line: ",row)
		sys.exit(0)		
		
def optional_sign():
	global token
	
	if(token in [plus_tk,minus_tk]):
		add_oper()
		

def C_Code(mylist):
	global program_name

	if (mylist[1] == "begin_block"):
		if (mylist[2] == program_name):
			return "int main() \n{"	
	elif (mylist[1] == "end_block"):
		if (mylist[2] == program_name):
			return "}\n"	
	elif (mylist[1] == "jump"):
		return "\tL_" + mylist[0] + ":" + " " + "goto L_" + mylist[4]
	elif (mylist[1] == "halt"):
		return "\tL_" + mylist[0] + ":" + " " + "return 0"	 	
	elif (mylist[1] == "retv"):
		return "\tL_" + mylist[0] + ":" + " " + "return" + " " + mylist[2]
	elif (mylist[1] == "out"):
		return "\tL_" + mylist[0] + ":" + " " + "printf(" + mylist[2] + ")"
	elif (mylist[1] == "inp"):
		return "\tL_" + mylist[0] + ":" + " " + "scanf(" + mylist[2] + ")"
	elif (mylist[1] == ":="):
		return "\tL_" + mylist[0] + ":" + " " + mylist[4] + "=" + mylist[2]
	elif (mylist[1] in ["+", "-", "*", "/"]):
		return "\tL_" + mylist[0] + ":" + " " + mylist[4] + "=" + mylist[2] + mylist[1] + mylist[3]
	elif (mylist[1] in ["<", ">", "<=", ">="]):
		return "\tL_" + mylist[0] + ":" + " " + "if(" + mylist[2] + mylist[1] + mylist[3] + ")" + "goto L_" + mylist[4]
	elif (mylist[1] == "="):
		return "\tL_" + mylist[0] + ":" + " " + "if(" + mylist[2] + "==" + mylist[3] + ")" + "goto L_" + mylist[4]	
	elif (mylist[1] == "<>"):
		return "\tL_" + mylist[0] + ":" + " " + "if(" + mylist[2] + "!=" + mylist[3] + ")" + "goto L_" + mylist[4] 
	else:
		return None					


def create_declarelist(alist):
	if (alist[1] == ":="):
		if (alist[4] not in declarelist):
			declarelist.append(alist[4])
	elif(alist[1] in ["+", "-", "*", "/", "<", ">", "<=", ">=", "<>"]):
		if (alist[2].isdigit() ==False):
			if (alist[2] not in declarelist):
				declarelist.append(alist[2])	
		if (alist[3].isdigit() ==False):
			if (alist[3] not in declarelist):
				declarelist.append(alist[3])
		if (alist[4].isdigit() ==False):
			if (alist[4] not in declarelist):
				declarelist.append(alist[4])


def main():
	global declarestring, declarelist, mainFrameLength, symbol_table

	program()	

	print("The array of the intermediate code is:")
	for l in program_list:
		print("%-5s %-15s %-10s %-10s %s" %(l[0],l[1],l[2],l[3],l[4]))
		create_declarelist(l)

			

	for declare in declarelist:
		declarestring = declarestring + declare + ", "
	declarestring = declarestring[:-2]		

	# Create the int file
	intFile = open("test.int", "w")	
	for l1 in program_list:
		for string in l1:
			intFile.write(string + " ")
		intFile.write("\n")	
	intFile.close()	

	# Create the C file
	cFile = open("test.c", "w")
	for l2 in program_list:
		string = C_Code(l2)
		if (string != None):
			if(string == "int main() \n{"):
				cFile.write(string + "\n")
				cFile.write("\tint " + declarestring + "\n")
			else:
				cFile.write(string + "\n")	
	cFile.close()	

	# Create the assembly file
	assemblyFile = open("test.asm", "w")	
	for l3 in finalCodeTable:
		assemblyFile.write(l3)
		assemblyFile.write("\n")	
	assemblyFile.close()		


main()