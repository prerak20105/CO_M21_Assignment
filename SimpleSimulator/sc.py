opcode = { "00000":"add","00001":"sub","00110":"mul","01010":"xor","01011":"or","01100":"and",   # @ VINEET
           "00010":"movB","01000":"rs","01001":"ls",
           "00011":"movC","00111":"div","01101":"not","01110":"cmp",
           "00100":"ld","00101":"st",
           "01111":"jmp","10000":"jlt","10001":"jgt","10010":"je",
           "10011":"hlt"}   

register_code = {"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}

register_values = {
    "R0"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # @ VINEET
    "R1"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R2"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R3"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R4"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R5"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R6"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

#  @ VINEET                             V  L  G  E  
    "FLAGS" : [0,0,0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0]
}


def list_to_decimal(l): #[0,0,...]
    res=0; i=0;
    for j in range(len(l)-1,-1,-1):
        res+=l[j]*pow(2,i)
        i+=1
    return res
def decimal_to_list(val):    # @PRERAK  overflow will be dealt with overflow function
    res=[]
    s=bin(val); s1=s[2:]; 
    if(len(s1)>=16):
        for i in range(-1,-17,-1):
            res.append(int(s1[i]))
        res.reverse()
    else:
        for i in range(16-len(s1)):
            res.append(0)
        for x in s1:
            res.append(int(x))
    return res
def string_to_decimal(s):
    res=0; i=0;
    for j in range(len(s)-1,-1,-1):
        res+=int(s[j])*pow(2,i)
        i+=1
    return res





import sys
memory=list(sys.stdin.read().split('\n'))
memory.pop(-1)
for i in range(len(memory)):
    temp=[]
    for j in range(16):
        temp.append(int(memory[i][j]))    
    memory[i]=temp
for i in range(256-len(memory)):
    memory.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

### @PRERAK memory created  -> memory
pc = [0,0,0,0,0,0,0,0]

def MEM(index):              # @PRERAK return list (element of memory)
    return memory[index]

def RF(reg_name): #as string
    return list_to_decimal(register_values[reg_name])


def EE():                     @ PRERAK  @ VINEET
	while True:
		global pc
		global memory
		global register_values
		global register_code
		global opcode
		index=list_to_decimal(pc)
		current_instruction=MEM(index) 
		verdict=execute(current_instruction) 
		if(verdict==1):
			pc=decimal_to_list(list_to_decimal(pc)+1)
			pc=pc[8:]
		if(verdict==-1):
			break


def execute(current_instruction):   @ ABINAV    @ PRERAK   @ VINEET  
	global pc
	global memory
	global register_values
	global register_code
	global opcode
	opc=""
	for i in range(5):
		opc+=str(current_instruction[i])
	current_instruction_name=opcode[opc]
	if current_instruction_name=='add':
		add_instruction(current_instruction)
		return 1
	elif current_instruction_name=='sub':
		sub_instruction(current_instruction)
		return 1
	elif current_instruction_name=='mul':
		mul_instruction(current_instruction)
		return 1
	elif current_instruction_name=='xor':
		xor_instruction(current_instruction)
		return 1
	elif current_instruction_name=='or':
		or_instruction(current_instruction)
		return 1
	elif current_instruction_name=='and':
		and_instruction(current_instruction)
		return 1

	elif current_instruction_name=='movB':
		movB_instruction(current_instruction)
		return 1
	elif current_instruction_name=='rs':
		rs_instruction(current_instruction)
		return 1
	elif current_instruction_name=='ls':
		ls_instruction(current_instruction)
		return 1

	elif current_instruction_name=='movC':
		movC_instruction(current_instruction)
		return 1
	elif current_instruction_name=='div':
		div_instruction(current_instruction)
		return 1
	elif current_instruction_name=='not':
		not_instruction(current_instruction)
		return 1
	elif current_instruction_name=='cmp':
		cmp_instruction(current_instruction)
		return 1

	elif current_instruction_name=='ld':
		ld_instruction(current_instruction)
		return 1
	elif current_instruction_name=='st':
		st_instruction(current_instruction)
		return 1

	elif current_instruction_name=='jmp':
		jmp_instruction(current_instruction)
		return 0
	elif current_instruction_name=='jlt':
		jlt_instruction(current_instruction)
		return 0

	elif current_instruction_name=='jgt':
		jgt_instruction(current_instruction)
		return 0

	elif current_instruction_name=='je':
		je_instruction(current_instruction)
		return 0

	elif current_instruction_name=='hlt':
		return -1
		


EE()

