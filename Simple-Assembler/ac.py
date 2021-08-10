# @p instructions     -> instructions for which binary to be generated
# @p var_instructions -> variable declarations only
# @p address          -> 
# opcode              -> 
##############################################################################################
import sys
l=list(sys.stdin.read().split('\n'))

var_instructions=[]
instructions=[]

for i in range(len(l)):
	if(l[i]==''):
		continue
	if(l[i][0:3]!="var"):
		instructions.append(l[i])
		instructions[-1]=instructions[-1].split(' ')
	else:
		var_instructions.append(l[i])
		var_instructions[-1]=var_instructions[-1].split(' ')

# @p													(TARGET INSTRUCTION)
# @p instruc address i -> if i<len(instructions) => instructions[address[i]]
# @p				   ->     >                  => var_instructions[address[i]]
address = list(range(0,len(instructions))) + list(range(0,len(var_instructions)))

##############################################################################################
##############################################################################################

memory = {}

opcode = { "add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100",
		   "movB":"00010","rs":"01000","ls":"01001",
		   "movC":"00011","div":"00111","not":"01101","cmp":"01110",
		   "ld":"00100","st":"00101",
		   "jmp":"01111","jlt":"10000","jgt":"10001","je":"10010",
		   "hlt":"10011"}	
register_code = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
R0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R5 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#							      V  L  G  E
FLAGS = [0,0,0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0]


def binary(current_instruction,current_instruction_type): # return binary eq. as string
	if(current_instruction[0]=='mov'):
		if(current_instruction_type=='B'):
			s = opcode["movB"]
		else:
			s = opcode["movC"]
	else:
		s = opcode[current_instruction[0]]

	if(current_instruction_type=='A'):
		s+="00"
		s+=register_code[current_instruction[1]]
		s+=register_code[current_instruction[2]]
		s+=register_code[current_instruction[3]]

	

	elif(current_instruction_type=='B'):
		s+=register_code[current_instruction[1]]
		n=int(current_instruction[2][1:])
		s1=str(bin(n))[2:]
		if(len(s1)<8):
			for i in range(8-len(s1)):
				s+="0"
		s+=s1


	elif(current_instruction_type=='C'):
		s+="00000"
		if(current_instruction[0]=='mov'):
			s+=register_code["movC"]
		else:
			s+=register_code[current_instruction[1]]

		if(current_instruction[0]=='mov'):
			s+=register_code["movC"]
		else:
			s+=register_code[current_instruction[2]]

	
	elif(current_instruction_type=='D'):
		s+=register_code[current_instruction[1]]
		####

	elif(current_instruction_type=='E'):
		s+="000"
		####

	

	elif(current_instruction_type=='F'):
		s+="00000000000"

	return s


def instruction_type(current_instruction): 
	if(current_instruction[0]=='add' or current_instruction[0]=='sub' or current_instruction[0]=='mul' or current_instruction[0]=='or' or current_instruction[0]=='xor' or current_instruction[0]=='and'):
		return 'A'
	if(current_instruction[0]=='rs' or current_instruction[0]=='ls'):
		return 'B'
	if(current_instruction[0]=='div' or current_instruction[0]=='not' or current_instruction[0]=='cmp'):
		return 'C'
	if(current_instruction[0]=='st' or current_instruction[0]=='ld'):
		return 'D'
	if(current_instruction[0]=='je' or current_instruction[0]=='jgt' or current_instruction[0]=='jlt' or current_instruction[0]=='jmp'):
		return 'E'
	if(current_instruction[0]=='hlt'):
		return 'F'
	if(current_instruction[0]=='mov'):
		if(current_instruction[-1][0]=='$'):
			return 'B'
		else:
			return 'C'
