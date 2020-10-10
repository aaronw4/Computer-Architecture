"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.PC = 0
        self.FL = 0b00000000
        self.reg = [0] * 8
        self.reg[7] = 0xF4

    def load(self):
        """Load a program into memory."""

        if (len(sys.argv)) != 2:
            print("remember to pass the second file name")
            print("usage: python3 fileio.py <second_file_name.py>")
            sys.exit()

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    possible_number = line[:line.find('#')]
                    if possible_number == '':
                        continue
                    instruction = int(possible_number, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, index):
        print(self.ram[index])

    def ram_write(self, index, data):
        self.ram[index].append(data)

    def run(self):
        """Run the CPU."""
        running = True
        # Stack Pointer
        SP = self.reg[7]

        while running:
            command = self.ram[self.PC]

            # LDI
            if command == 0b10000010:
                index = self.ram[self.PC + 1]
                value = self.ram[self.PC + 2]
                self.reg[index] = value
                self.PC += 2

            # PRN
            elif command == 0b01000111:
                index = self.ram[self.PC + 1]
                print(self.reg[index])
                self.PC += 1

            # MUL
            elif command == 0b10100010:
                reg_index_1 = self.ram[self.PC + 1]
                reg_index_2 = self.ram[self.PC + 2]
                first_value = self.reg[reg_index_1]
                second_value = self.reg[reg_index_2]
                self.reg[reg_index_1] = first_value * second_value
                self.PC += 2

            # PUSH
            elif command == 0b01000101:
                SP -= 1
                reg_index_1 = self.ram[self.PC + 1]
                value = self.reg[reg_index_1]
                self.ram[SP] = value
                self.PC += 1

            # POP
            elif command == 0b01000110:
                value = self.ram[SP]
                reg_index_1 = self.ram[self.PC + 1]
                self.reg[reg_index_1] = value
                SP += 1
                self.PC += 1

            # CALL
            elif command == 0b01010000:
                return_address = self.PC + 2
                SP -= 1
                self.ram[SP] = return_address
                reg_index_1 = self.ram[self.PC + 1]
                subroutine_address = self.reg[reg_index_1]
                self.PC = subroutine_address

            # RET
            elif command == 0b00010001:
                return_address = self.ram[SP]
                self.PC = return_address
                SP += 1

            # CMP
            elif command == 0b10100111:
                reg_index_1 = self.ram[self.PC + 1]
                reg_index_2 = self.ram[self.PC + 2]
                value1 = self.reg[reg_index_1]
                value2 = self.reg[reg_index_2]

                if value1 < value2:
                    self.FL = 0b00000100
                elif value1 > value2:
                    self.FL = 0b00000010
                elif value1 == value2:
                    self.FL = 0b00000001
                
                self.PC += 2

            # JEQ
            elif command == 0b01010101:
                reg_index_1 =  self.ram[self.PC + 1]
                address = self.reg[reg_index_1]

                if self.FL == 0b00000001:
                    self.PC = address
                    continue
                else:
                    self.PC += 1

            # JNE
            elif command == 0b01010110:
                reg_index_1 = self.ram[self.PC + 1]
                address = self.reg[reg_index_1]
                result = self.FL & 0b00000001

                if result == 0:
                    self.PC = address
                    continue
                else:
                    self.PC += 1

            # JMP
            elif command == 0b01010100:
                reg_index_1 = self.ram[self.PC + 1]
                address = self.reg[reg_index_1]
                self.PC = address
                continue

            # HLT
            elif command == 0b00000001:
                running = False

            else:
                print(f'unknown command: {command:b} on line {self.PC}!')
                running = False

            self.PC += 1

if __name__ == '__main__':
    CPU = CPU()
    CPU.run()
