#  @PRERAK  instructions     -> instructions for which binary to be generated
#  @PRERAK  var_instructions -> variable declarations only
#  @PRERAK  address          -> tells us the instruction's address
#  @PRERAK  opcode           -> dictionary ..stores opcode for each key (say 'mul')
#  @PRERAK  register_code    -> dictionary..stores code for each register as key
###############################################################################################
import sys
l=list(sys.stdin.read().split('\n'))

var_instructions=[]
instructions=[]
labels={}
count=0; var_count=0;

for i in range(len(l)):
	if(l[i]==''):
		continue

	temp = l[i].split(' ') #  @PRERAK  temp=['label2:' , 'mov' , 'R1' , '$5']
	if(temp[0][-1]==':'):
		label_str = temp[0][:-1]
		if(temp[1]=='var'):
			labels[label_str]=[var_count,-1]  #  @PRERAK  -1 is dummmy to identify var labels
			var_count += 1
		else:
			labels[label_str]=count
			count += 1
		temp = temp[1:] #  @PRERAK  temp=['mov' , 'R1' , '$5'], if more than one lable ERROR
		buff=""
		for x in temp[0:-1]:
		    buff=buff+x+" "
		buff+=temp[-1]      #  @PRERAK  now its as if label was never there
		if(buff[0:3]!="var"):
			instructions.append(buff)
			instructions[-1]=instructions[-1].split(' ')
		else:
			var_instructions.append(buff)
			var_instructions[-1]=var_instructions[-1].split(' ')


	else:
		if(l[i][0:3]!="var"):
			count += 1
			instructions.append(l[i])
			instructions[-1]=instructions[-1].split(' ')
		else:
			var_count += 1
			var_instructions.append(l[i])
			var_instructions[-1]=var_instructions[-1].split(' ')


for x in labels.keys():
	if(type(labels[x])==type([])):
		labels[x]=len(instructions)+labels[x][0]


# @PRERAK													(TARGET INSTRUCTION)
# @PRERAK instruc address i -> if i<len(instructions) => instructions[address[i]]
# @PRERAK				   ->     >                  => var_instructions[address[i]]
address = list(range(0,len(instructions))) + list(range(0,len(var_instructions)))


#  @PRERAK 
##############################################################################################
#print("instructions     -> ",instructions);print();print("var_instructions -> ",var_instructions);print();print("address          -> ",address);print();print("labels           -> ",labels);
##############################################################################################


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

#	@PRERAK						  V  L  G  E
FLAGS = [0,0,0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0]


def binary(current_instruction,current_instruction_type): #  @PRERAK  return binary eq. as string
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
		s+=register_code[current_instruction[1]]
		s+=register_code[current_instruction[2]]

	
	elif(current_instruction_type=='D'):
		s+=register_code[current_instruction[1]]
		for i in range(len(var_instructions)):
			if(var_instructions[i][-1]==current_instruction[2]):
				addr=len(instructions)+i
				s1=str(bin(addr))[2:]
				if(len(s1)<8):
					for i in range(8-len(s1)):
						s+="0"
				s+=s1
				break
		

	elif(current_instruction_type=='E'):  #  @PRERAK  JUMP TO LABEL
		s+="000"
		goto_label=current_instruction[1]
		for x in labels.keys():
			if(x==goto_label):
				addr=labels[x]
				s1=str(bin(addr))[2:]
				if(len(s1)<8):
					for i in range(8-len(s1)):
						s+="0"
				s+=s1
				break
	

	elif(current_instruction_type=='F'):
		s+="00000000000"


	return s


def instruction_type(current_instruction):    #  @PRERAK  tell type of passed instrcn.

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
	if(current_instruction[0]=='mov'):       # @PRERAK  we deal with 'mov' separately
		if(current_instruction[-1][0]=='$'):
			return 'B'
		else:
			return 'C'




for i in range(len(instructions)):  #  @PRERAK  simply iterate on instructions
	print(binary(instructions[i],instruction_type(instructions[i])))



