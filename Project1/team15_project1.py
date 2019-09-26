import sys  # reads input file lines 9-11

# read a binary file containing arm program in machine code
# generate assembly code for the given arm code.
#
# * Input file contains a 32-bit instruction words.
#   - assume you will start your program on memory location 96, incrementing by 4 bytes

# with open(sys.argv[1], 'r') as f:
#     contents: str = f.read()
# print(contents)


def readFile(inputFile):
    pass
    # placeholder

def writeFile(outputFile):
    pass
    # placeholder

#
def convertBinaryToDecimal(n):
    return int(n, 2)

def findOpCode(opcodeRange):
    opcode = ['','']

    if opcodeRange >= 160 and opcodeRange <= 191:
        opcode[0] = 'B'
        opcode[1] = 'B'
    elif opcodeRange == 1104:
        opcode[0] = 'AND'
        opcode[1] = 'R'
    elif opcodeRange == 1112:
        opcode[0] = 'ADD'
        opcode[1] = 'R'
    elif opcodeRange >= 1160 and opcodeRange <= 1161:
        opcode[0] = 'ADDI'
        opcode[1] = 'I'
    elif opcodeRange == 1360:
        opcode[0] = 'ORR'
        opcode[1] = 'R'
    elif opcodeRange >= 1440 and opcodeRange <= 1447:
        opcode[0] = 'CBZ'
        opcode[1] = 'CB'
    elif opcodeRange >= 1448 and opcodeRange <= 1455:
        opcode[0] = 'CBNZ'
        opcode[1] = 'CB'
    elif opcodeRange == 1624:
        opcode[0] = 'SUB'
        opcode[1] = 'R'
    elif opcodeRange >= 1672 and opcodeRange <= 1673:
        opcode[0] = 'SUBI'
        opcode[1] = 'I'
    elif opcodeRange >= 1684 and opcodeRange <= 1687:
        opcode[0] = 'MOVZ'
        opcode[1] = 'IM'
    elif opcodeRange >= 1940 and opcodeRange <= 1943:
        opcode[0] = 'MOVK'
        opcode[1] = 'IM'
    elif opcodeRange == 1690:
        opcode[0] = 'LSR'
        opcode[1] = 'R'
    elif opcodeRange == 1691:
        opcode[0] = 'LSL'
        opcode[1] = 'R'
    elif opcodeRange == 1984:
        opcode[0] = 'STUR'
        opcode[1] = 'D'
    elif opcodeRange == 1986:
        opcode[0] = 'LDUR'
        opcode[1] = 'D'
    elif opcodeRange == 1692:
        opcode[0] = 'ASR'
        opcode[1] = 'R'
    elif opcodeRange == 0:
        opcode[0] = 'NOP'
        opcode[1] = 'N/A'
    elif opcodeRange == 1872:
        opcode[0] = 'EOR'
        opcode[1] = 'R'
    else:
        opcode[0] = 'ERROR'
        opcode[1] = 'ERROR'
    
    return opcode

def findRegisters():
    pass
    # placeholder

print(findOpCode(convertBinaryToDecimal('10001010000')))