import unittest
import time
from cpu6502 import Cpu6502

from unittest.mock import patch, Mock
from memory_controller import MemoryController
from registers import Registers


class TestMemoryController(MemoryController):

    def __init__(self):

        self.interrupted = False
        super(TestMemoryController, self).__init__(65536)

    def read(self, address):
        #print("read:{0}".format(address))
        if address == 0xfffe:
            self.interrupted = True

        return super(TestMemoryController, self).read(address)

    def is_signalled(self):
        return self.interrupted

class cpu6502Tests(unittest.TestCase):

    # at 0x0600
    mult10_instructions = [ 0x0a, 0x8d, 0x0b, 0x06, 0x0a, 0x0a, 0x18, 0x6d, 0x0b, 0x06, 0x0 ]

    # code is fast mult10:
    #  ASL
    #  STA temp
    #  ASL
    #  ASL
    #  CLC
    #  ADC temp
    #  BRK
    # temp:
    #############################################

    def test_execute_mult10_function_10x10(self):

        test_memory_controller = TestMemoryController()
        for byte in range(len(self.mult10_instructions)):
            test_memory_controller.buffer[0x600+byte] = self.mult10_instructions[byte]

        cpu = Cpu6502(test_memory_controller)
        cpu.registers.pc = 0x0600

        cpu.registers.accumulator = 10

        start = time.perf_counter()
        total_clocks = cpu.run_until_signalled(test_memory_controller.is_signalled)
        print("Clocks:{0}".format(total_clocks))
        print("Time:{0}".format(time.perf_counter() - start))

        self.assertEqual(cpu.registers.accumulator, 100)

    def test_execute_mult10_function_10xminus10(self):

        test_memory_controller = TestMemoryController()
        for byte in range(len(self.mult10_instructions)):
            test_memory_controller.buffer[0x600+byte] = self.mult10_instructions[byte]

        cpu = Cpu6502(test_memory_controller)
        cpu.registers.pc = 0x0600

        cpu.registers.accumulator = 0xf6
        start = time.perf_counter()
        total_clocks = cpu.run_until_signalled(test_memory_controller.is_signalled)
        print("Clocks:{0}".format(total_clocks))
        print("Time:{0}".format(time.perf_counter() - start))

        self.assertEqual(cpu.registers.accumulator, 0x9c)

    #############################################

    sqrt_instructions = [
        0xa9, 0x00, 0x85, 0xf2, 0x85, 0xf3, 0x85, 0xf6, 0xa2, 0x08, 0x06, 0xf6, 0x06, 0xf0, 0x26, 0xf1, 
        0x26, 0xf2, 0x26, 0xf3, 0x06, 0xf0, 0x26, 0xf1, 0x26, 0xf2, 0x26, 0xf3, 0xa5, 0xf6, 0x85, 0xf4, 
        0xa9, 0x00, 0x85, 0xf5, 0x38, 0x26, 0xf4, 0x26, 0xf5, 0xa5, 0xf3, 0xc5, 0xf5, 0x90, 0x16, 0xd0, 
        0x06, 0xa5, 0xf2, 0xc5, 0xf4, 0x90, 0x0e, 0xa5, 0xf2, 0xe5, 0xf4, 0x85, 0xf2, 0xa5, 0xf3, 0xe5, 
        0xf5, 0x85, 0xf3, 0xe6, 0xf6, 0xca, 0xd0, 0xc2, 0x00 
    ]
    # Calculates the 8 bit root and 9 bit remainder of a 16 bit unsigned integer in
    # Numberl/Numberh. The result is always in the range 0 to 255 and is held in
    # Root, the remainder is in the range 0 to 511 and is held in Reml/Remh
    #
    # partial results are held in templ/temph
    #
    # This routine is the complement to the integer square program.
    #
    # Destroys A, X registers.
    # variables - must be in RAM

    #Numberl     = $F0       ; number to find square root of low byte
    #Numberh     = Numberl+1 ; number to find square root of high byte
    #Reml        = $F2       ; remainder low byte
    #Remh        = Reml+1    ; remainder high byte
    #templ       = $F4       ; temp partial low byte
    #temph       = templ+1   ; temp partial high byte
    #Root        = $F6       ; square root
    #
    #    *= $0x600        ; can be anywhere, ROM or RAM
    #
    #SqRoot
    #    LDA #$00        ; clear A
    #    STA Reml        ; clear remainder low byte
    #    STA Remh        ; clear remainder high byte
    #    STA Root        ; clear Root
    #    LDX #$08        ; 8 pairs of bits to do
    #Loop
    #    ASL Root        ; Root = Root * 2
    #
    #    ASL Numberl     ; shift highest bit of number ..
    #    ROL Numberh     ;
    #    ROL Reml        ; .. into remainder
    #    ROL Remh        ;
    #
    #    ASL Numberl     ; shift highest bit of number ..
    #    ROL Numberh     ;
    #    ROL Reml        ; .. into remainder
    #    ROL Remh        ;
    #
    #    LDA Root        ; copy Root ..
    #    STA templ       ; .. to templ
    #    LDA #$00        ; clear byte
    #    STA temph       ; clear temp high byte
    #
    #    SEC         ; +1
    #    ROL templ       ; temp = temp * 2 + 1
    #    ROL temph       ;
    #
    #    LDA Remh        ; get remainder high byte
    #    CMP temph       ; comapre with partial high byte
    #    BCC Next        ; skip sub if remainder high byte smaller
    #
    #    BNE Subtr       ; do sub if <> (must be remainder>partial !)
    #
    #    LDA Reml        ; get remainder low byte
    #    CMP templ       ; comapre with partial low byte
    #    BCC Next        ; skip sub if remainder low byte smaller
    #
                    #; else remainder>=partial so subtract then
                    #; and add 1 to root. carry is always set here
    #Subtr
    #    LDA Reml        ; get remainder low byte
    #    SBC templ       ; subtract partial low byte
    #    STA Reml        ; save remainder low byte
    #    LDA Remh        ; get remainder high byte
    #    SBC temph       ; subtract partial high byte
    #    STA Remh        ; save remainder high byte
    #
    #    INC Root        ; increment Root
    #Next
    #    DEX         ; decrement bit pair count
    #    BNE Loop        ; loop if not all done
    #
    #    BRK

    def test_execute_sqrt_function_1(self):

        test_memory_controller = TestMemoryController()
        for byte in range(len(self.sqrt_instructions)):
            test_memory_controller.buffer[0x600+byte] = self.sqrt_instructions[byte]

        test_memory_controller.buffer[0xf0] = 0x11
        test_memory_controller.buffer[0xf1] = 2

        cpu = Cpu6502(test_memory_controller)
        cpu.registers.pc = 0x0600

        start = time.perf_counter()
        total_clocks = cpu.run_until_signalled(test_memory_controller.is_signalled)
        print("Clocks:{0}".format(total_clocks))
        print("Time:{0}".format(time.perf_counter() - start))

        print("Sqrt(25)={0} remainder {1}".format(
                test_memory_controller.read(0xf6),
                (test_memory_controller.read(0xf3) * 256) + test_memory_controller.read(0xf2)))

    #############################################

    # at 0x0600
    fibonacci_instructions = [ 0xa9, 0x00, 0x85, 0xf0, 0xa9, 0x01, 0x85, 0xf1, 0xa2, 0x00, 
                               0xa5, 0xf1, 0x9d, 0x1b, 0x0f, 0x85, 0xf2, 0x65, 0xf0, 0x85, 
                               0xf1, 0xa5, 0xf2, 0x85, 0xf0, 0xe8, 0xe0, 0x0a, 0x30, 0xec, 0x0 ]

    # code is

    #   LDA  #0
    #   STA  $F0     ; LOWER NUMBER
    #   LDA  #1
    #   STA  $F1     ; HIGHER NUMBER
    #   LDX  #0
#LOOP:  LDA  $F1
    #   STA  $0F1B,X
    #   STA  $F2     ; OLD HIGHER NUMBER
    #   ADC  $F0
    #   STA  $F1     ; NEW HIGHER NUMBER
    #   LDA  $F2
    #   STA  $F0     ; NEW LOWER NUMBER
    #   INX
    #   CPX  #$0A    ; STOP AT FIB(10)
    #   BMI  LOOP
    #   BRK      

    def test_execute_fibonacci_function_1(self):

        test_memory_controller = TestMemoryController()
        for byte in range(len(self.fibonacci_instructions)):
            test_memory_controller.buffer[0x600+byte] = self.fibonacci_instructions[byte]

        cpu = Cpu6502(test_memory_controller)
        cpu.registers.pc = 0x0600

        cpu.registers.accumulator = 10

        start = time.perf_counter()
        total_clocks = cpu.run_until_signalled(test_memory_controller.is_signalled)
        print("Clocks:{0}".format(total_clocks))
        print("Time:{0}".format(time.perf_counter() - start))

        for result in range(0, 9):
            print("F({0}) = {1}".format(result, test_memory_controller.read(0xf1b + result)))

    #############################################

    # at 0x0600
    divide_instructions = [ 0xA9, 0x00, 0x8D, 0x5C, 0x00, 0x8D, 0x5D, 0x00, 0xA2, 0x10,
                            0x0E, 0x5A, 0x00, 0x2E, 0x5B, 0x00, 0x2E, 0x5C, 0x00, 0x2E,
                            0x5D, 0x00, 0xAD, 0x5C, 0x00, 0x38, 0xED, 0x58, 0x00, 0xA8,
                            0xAD, 0x5D, 0x00, 0xED, 0x59, 0x00, 0x90, 0x09, 0x8D, 0x5D,
                            0x00, 0x8C, 0x5C, 0x00, 0xEE, 0x5E, 0x00, 0xCA, 0xD0, 0xD8, 0x00 ] 

    # code is

    # divisor = $58     ;$59 used for hi-byte
    # dividend = $5a    ;$5b used for hi-byte
    # remainder = $5c   ;$5d used for hi-byte
    # result = $5e      ;$5e to store the result
    # 
    # divide:  lda #0          ;preset remainder to 0
    #          sta remainder
    #          sta remainder+1
    #          ldx #16         ;repeat for each bit: ...
    # 
    # divloop: asl dividend    ;dividend lb & hb*2, msb -> Carry
    #          rol dividend+1  
    #          rol remainder   ;remainder lb & hb * 2 + msb from carry
    #          rol remainder+1
    #          lda remainder
    #          sec
    #          sbc divisor ;substract divisor to see if it fits in
    #          tay         ;lb result -> Y, for we may need it later
    #          lda remainder+1
    #          sbc divisor+1
    #          bcc skip    ;if carry=0 then divisor didn't fit in yet
    # 
    #          sta remainder+1 ;else save substraction result as new remainder,
    #          sty remainder   
    #          inc result  ;and INCrement result cause divisor fit in 1 times
    # 
    # skip:    dex
    #          bne divloop 
    #          rts
    
    def test_execute_16bit_divide_function_1(self):

        test_memory_controller = TestMemoryController()
        for byte in range(len(self.divide_instructions)):
            test_memory_controller.buffer[0x600+byte] = self.divide_instructions[byte]

        cpu = Cpu6502(test_memory_controller)
        cpu.registers.pc = 0x0600

        cpu.registers.accumulator = 10

        test_memory_controller.buffer[0x58] = 8
        test_memory_controller.buffer[0x59] = 0

        test_memory_controller.buffer[0x5a] = 32
        test_memory_controller.buffer[0x5b] = 0

        start = time.perf_counter()
        total_clocks = cpu.run_until_signalled(test_memory_controller.is_signalled)
        print("Clocks:{0}".format(total_clocks))
        print("Time:{0}".format(time.perf_counter() - start))

        print("32 / 8 = {0} remainder {1}".format(test_memory_controller.read(0x5e) + (test_memory_controller.read(0x5f) * 256),
                test_memory_controller.read(0x5c) + (test_memory_controller.read(0x5d) * 256)))

    #############################################

    # at 0x0600
    subtract_16bit_instructions = [ 0x38, 0xA5, 0x20, 0xE5, 0x22, 0x85, 0x24, 0xA5,
        0x21, 0xE5, 0x23, 0x85, 0x25, 0x00, ] 

    # code is [0x24,0x25] = [0x20,0x21] - [0x22,0x23]

    #       SEC
    #       LDA *$20
    #       SBC *$22
    #       STA *$24
    #       LDA *$21
    #       SBC *$23     
    #       STA *$25 
    #       brk    
    
    def test_execute_16bit_subtract_function(self):

        test_memory_controller = TestMemoryController()
        for byte in range(len(self.subtract_16bit_instructions)):
            test_memory_controller.buffer[0x600+byte] = self.subtract_16bit_instructions[byte]

        subtractions = [
            (5000, 3000, 2000),
            (15000, 2000, 13000),
            (35000, 4000, 31000),
            (25000, 12000, 13000),
            (2000, 3000, 0xfc18),
            (20000, 26000, 0xe890),
            (3000, 32000, 0x8eb8),
        ]

        cpu = Cpu6502(test_memory_controller)
        start = time.perf_counter()
        total_clocks = 0
        for subtraction in subtractions:
            cpu.registers.pc = 0x0600
            test_memory_controller.interrupted = False

            test_memory_controller.buffer[0x20] = subtraction[0] & 0xff
            test_memory_controller.buffer[0x21] = (subtraction[0] >> 8) & 0xff

            test_memory_controller.buffer[0x22] = subtraction[1] & 0xff
            test_memory_controller.buffer[0x23] = (subtraction[1] >> 8) & 0xff

            total_clocks += cpu.run_until_signalled(test_memory_controller.is_signalled)

            result = test_memory_controller.read(0x24) + (test_memory_controller.read(0x25) * 256)
            print("{0} - {1} = {2}".format(test_memory_controller.read(0x20) + (test_memory_controller.read(0x21) * 256),
                    test_memory_controller.read(0x22) + (test_memory_controller.read(0x23) * 256),
                    result))

            self.assertEqual(result, subtraction[2])

        print("Clocks:{0}".format(total_clocks))
        print("Time:{0}".format(time.perf_counter() - start))

if __name__ == '__main__':
    unittest.main()