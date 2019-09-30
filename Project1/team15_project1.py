import sys

def file_input():
    for i in range(len(sys.argv)):
        if "bin.txt" in str(sys.argv[i]):
            inputFileName = str(sys.argv[i])

    try:
        instruction = [line.rstrip() for line in open(inputFileName, 'r')]
    except IOError:
        print("Could not open input file")

    return instruction

def file_output():
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '-o' and i < (len(sys.argv) - 1):
            outputFileName = sys.argv[i + 1]
    return outputFileName


def twos_compliment(bits):
    newbits = ""
    if (bits[0] == "0"):
        return convertBinaryToDecimal(bits)
    else:
        for i in bits:
            newbits += str(int(not int(i)))
        newbits = (int(newbits, 2) + int(1))
        return -newbits

def convertBinaryToDecimal(n):
    return int(n, 2)

def findOpCode(opcodeRange):
    opcode = ['', '']

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
        opcode[1] = 'NOP'
    elif opcodeRange == 1872:
        opcode[0] = 'EOR'
        opcode[1] = 'R'
    elif opcodeRange == 2038:
        opcode[0] = 'BREAK'
        opcode[1] = 'BREAK'
    elif opcodeRange == 2047:   # doesnt account for positive numbers
        opcode[0] = 'data'
        opcode[1] = 'data'
    else:
        opcode[0] = 'ERROR'
        opcode[1] = 'ERROR'

    return opcode


def write_to_file(inst, opcode, memoryLocation):  # print out by opcode
    f = open(file_output() + ".txt", "a+")
    if opcode[1] == "B":
        # B format: (Opcode - 6), (Offset (W) - 26)
        f.write(inst[0:6] + " " + inst[6:32])
        f.write("\t%d\t%s" % (memoryLocation, opcode[0]))
        f.write("\t%s%d" % ("#", twos_compliment(inst[6:32])))

    elif opcode[1] == "R":
        # R format: (Opcode - 11), (Rm - 5), (Shamt - 6), (Rn - 5), (Rd - 5)
        f.write(inst[0:11] + " " + inst[11:16] + " " + inst[16:22] + " " + inst[22:27]
                + " " + inst[27:32])
        f.write("\t%d\t%s" % (memoryLocation, opcode[0]))
        f.write("%s%d," % ("\tR", convertBinaryToDecimal(inst[27:32])))
        f.write("%s%d," % (" R", convertBinaryToDecimal(inst[22:27])))
        if opcode[0] == "LSL" or opcode[0] == "LSR" or opcode[0] == "ASR":
            f.write("%s%d" % (" #", convertBinaryToDecimal(inst[16:22])))
        else:
            f.write("%s%d" % (" R", convertBinaryToDecimal(inst[11:16])))

    elif opcode[1] == "D":
        # D format: (Opcode - 11), (Immediate - 9), (Rn - 5), (Rd - 5)
        f.write(inst[0:11] + " " + inst[11:20] + " " + inst[20:22] + " " + inst[22:27]
                + " " + inst[27:32])
        f.write("\t%d\t%s" % (memoryLocation, opcode[0]))
        f.write("%s%d," % ("\tR", convertBinaryToDecimal(inst[27:32])))
        f.write("%s%d, #%d]" % (" [R", convertBinaryToDecimal(inst[22:27]), convertBinaryToDecimal(inst[11:20])))

    elif opcode[1] == "I":
        # I format: (Opcode - 10), (Immediate - 12), (Rn - 5), (Rd - 5)
        # NOTE: The Immediate field is zero extended.
        f.write(inst[0:10] + " " + inst[10:22] + " " + inst[22:27] + " " + inst[27:32])
        f.write("\t%d\t%s" % (memoryLocation, opcode[0]))
        f.write("%s%d," % ("\tR", convertBinaryToDecimal(inst[27:32])))
        f.write("%s%d," % (" R", convertBinaryToDecimal(inst[22:27])))
        f.write(" #%d" % (convertBinaryToDecimal(inst[10:22])))

    elif opcode[1] == "CB":
        # CB Format: (Opcode - 8), (Offset (W) - 19), (Conditional - 5)
        f.write(inst[0:8] + " " + inst[8:27] + " " + inst[27:32])
        f.write("\t%d\t%s" % (memoryLocation, opcode[0]))
        f.write("%s%d," % ("\tR", convertBinaryToDecimal(inst[27:32])))
        f.write(" #%d" % (twos_compliment(inst[8:27])))

    elif opcode[1] == "IM":
        # IM Format: (Opcode - 9), (Shift - 2), (Field - 16), (Rd - 5)
        f.write(inst[0:9] + " " + inst[9:11] + " " + inst[11:27] + " " + inst[27:32])
        f.write("\t%d\t%s" % (memoryLocation, opcode[0]))
        f.write("%s%d," % ("\tR", convertBinaryToDecimal(inst[27:32])))
        f.write(" %d,%s%d" % (convertBinaryToDecimal(inst[11:27]), " LSL ", convertBinaryToDecimal(inst[9:11]) * 16))

    elif  opcode[1] == "BREAK":
        f.write(inst[0:8] + " " + inst[8:11] + " " + inst[11:16] + " " + inst[16:21] + " " + inst[21:26]
                + " " + inst[26:32])
        f.write("\t%d\t%s" % (memoryLocation, opcode[0]))
    elif opcode[1] == "NOP":
        f.write(inst[0:8] + " " + inst[8:11] + " " + inst[11:16] + " " + inst[16:21] + " " + inst[21:26]
                + " " + inst[26:32])
    elif opcode[1] == "data":
        f.write("%s\t%d\t%d" % (inst[0:32], memoryLocation, twos_compliment(inst)))
    elif opcode[1] == "ERROR":
        print("ERROR: Invalid input")
    else:
        print("ERROR: Invalid input")
    memoryLocation += 4
    f.write("\n")
    f.close()

def main():
    memory_location = 96
    instructions = file_input()
    f = open(file_output() + ".txt", "w+")
    f.close()

    for i in instructions:
        op_code = findOpCode(convertBinaryToDecimal(i[0:11]))
        write_to_file(i, op_code, memory_location)
        memory_location += 4

if __name__ == "__main__":
    main()
