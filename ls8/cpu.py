"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
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
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
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
            command = self.ram[self.pc]
            # LDI
            if command == 0b10000010:
                index = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[index] = value
                self.pc += 2
            # PRN
            elif command == 0b01000111:
                index = self.ram[self.pc + 1]
                print(self.reg[index])
                self.pc += 1
            # MUL
            elif command == 0b10100010:
                reg_index_1 = self.ram[self.pc + 1]
                reg_index_2 = self.ram[self.pc + 2]
                first_value = self.reg[reg_index_1]
                second_value = self.reg[reg_index_2]
                self.reg[reg_index_1] = first_value * second_value
                self.pc += 2
            # PUSH
            elif command == 0b01000101:
                SP -= 1
                reg_index_1 = self.ram[self.pc + 1]
                value = self.reg[reg_index_1]
                self.ram[SP] = value
                self.pc += 1
            # POP
            elif command == 0b01000110:
                value = self.ram[SP]
                reg_index_1 = self.ram[self.pc + 1]
                self.reg[reg_index_1] = value
                SP += 1
                self.pc += 1
            # HLT
            elif command == 0b00000001:
                running = False

            self.pc += 1

if __name__ == '__main__':
    CPU = CPU()
    CPU.run()