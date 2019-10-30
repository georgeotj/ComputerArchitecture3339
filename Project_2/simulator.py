from helper import SetUp
import os
import masking_constants as MASKs
import sys


class State:
    dataval = []    # don't really need but makes clear this is part of state
    pc = 96
    cycle = 1
    R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, opcode, dataval, address, arg1, arg2, arg3, numInstructions, opcodeStr, arg1Str, arg2Str, arg3Str):
        self.opcode = opcode
        self.dataval = dataval
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.numInstructions = numInstructions
        self.opcodeStr = opcodeStr
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str

    def getIndexOfMemAddress(self, currAddr):   # this figures out which "i" is associated with a mem address like 96
        #   find the address and return the instruction associated with it
        index = 0
        for i in self.address:
            if i == currAddr:
                return index
            index += 1

    def incrementPC(self):
        self.pc = self.pc + 4

    def printState(self):
        oFileName = SetUp.get_output_filename()

        with open(oFileName + "_sim.txt", "a") as outFile:

            i = self.getIndexOfMemAddress(self.PC)
            outFile.write("=====================\n")
            outFile.write("Cycle:" + str(self.cycle) + "\t" + str(self.PC) + "\t" + self.opcodeStr[i] + self.arg1Str[i] +
                          self.arg2Str[i] + self.arg3Str[i] + "\n" + "\n")
            outFile.write("Registers:\n")

            outStr = "r00:"
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r08:"
            for i in range(8, 16):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r16:"
            for i in range(16, 24):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r24:"
            for i in range in range(24, 32):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n\nData:\n")
            outStr = "\n"

            for i in range(len(self.dataval())):
                if i % 8 == 0 and i != 0 or i == len(self.dataval):
                    outFile.write(outStr + "\n")
                if i % 8 == 0:
                    outStr = str(self.address[i + self.numInstructions]) + ":" + str(self.dataval[i])
                if i % 8 == 0:
                    outStr = outStr + "\t" + str(self.dataval[i])

            outFile.write(outStr + "\n")
            outFile.close()


class Simulator:
    def __init__(self, opcode, dataval, address, arg1, arg2, arg3, numInstructions, opcodeStr, arg1Str, arg2Str, arg3Str):
        self.opcode = opcode
        self.dataval = dataval
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.numInstructions = numInstructions
        self.opcodeStr = opcodeStr
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.specialMask = MASKs.specialMask

    def run(self):
        foundBreak = False
        armState = State(self.opcode, self.dataval, self.address, self.arg1, self.arg2, self.arg3,
                         self.numInstructions, self.opcodeStr, self.arg1Str, self.arg2Str, self.arg3Str)
        while not foundBreak:
            jumpAddr = armState.pc
            #   get next instruction
            i = armState.getIndexOfMemAddress(armState.pc)
            # His comment
            # Test and delete the need for instructions
            #   NOP
            if self.opcode[i] == 0:
                armState.printState()
                armState.incrementPC()
                armState.cycle += 1
                continue
            #   B
            elif 160 <= self.opcode[i] <= 191:
                jumpAddr = jumpAddr + ((self.arg2[i] * 4) - 4)  # -4 takes care of incrementing PC later
            #   ADD
            elif self.opcode[i] == 1112:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] + armState.R[self.arg2[i]]
            #   AND
            elif self.opcode[i] == 1104:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] & armState.R[self.arg2[i]]
            #   ADDI
            elif 1160 <= self.opcode[i] <= 1161:
                armState.R[self.arg2[i]] = armState.R[self.arg1[i]] + self.arg3[i]
            #   ORR
            elif self.opcode[i] == 1360:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] | armState.R[self.arg2[i]]
            #   CBZ
            elif 1440 <= self.opcode[i] <= 1447:
                if armState.R[self.arg2[i]] == 0:
                    jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)
            #   CBNZ
            elif 1448 <= self.opcode[i] <= 1455:
                if armState.R[self.arg2[i]] != 0:
                    jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)
            #   SUB
            elif self.opcode[i] == 1624:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] + armState.R[self.arg2[i]]
            #   SUBI
            elif 1672 <= self.opcode[i] <= 1673:
                armState.R[self.arg2[i]] = armState.R[self.arg1[i]] - self.arg3[i]
            #   MOVZ
            elif 1684 <= self.opcode[i] <= 1687:
                # depending on arg1, the 2 digit code determins if its * 0, 16, 32, 48
                armState.R[self.arg3[i]] = self.arg1[i] << (self.arg2[i] * 16)
            #   MOVK
            elif 1940 <= self.opcode[i] <= 1943:
                pass # TODO armState.R[self.arg3[i]] = self.arg1[i] <<
            #   LSR
            elif self.opcode[i] == 1690:
                armState.R[self.arg3[i]] = self.arg1[i] >> self.arg2[i]
                pass
            #   LSL
            elif self.opcode[i] == 1691:
                armState.R[self.arg3[i]] = self.arg1[i] << self.arg2[i]
                pass
            #   STUR
            elif self.opcode[i] == 1984:
                pass    # TODO
            #   LDUR
            elif self.opcode[i] == 1986:
                pass    # TODO
            #   ASR
            elif self.opcode[i] == 1692:
                pass    # TODO
            #   EOR
            elif self.opcode[i] == 1872:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] ^ armState.R[self.arg2[i]]
            #   Break
            elif self.opcode[i] == 2038:
                foundBreak = True
            else:
                print("IN SIM - UNKNOWN INSTRUCTION -------------!!!!")

            print("instruction @ ", i, " complete")
            armState.printState()
            armState.pc = jumpAddr
            armState.incrementPC()
            armState.cycle += 1
