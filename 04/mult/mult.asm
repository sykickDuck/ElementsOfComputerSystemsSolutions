// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

    @R2 //ensure destination of product is 0
    M=0
    @i //initialise iteration counter
    M=0

(LOOP)
    @R1 //line 17-22 is check that loop should continue
    D=M
    @i
    D=M-D
    @END
    D;JGE

    @R0 //add R0 to r2 again
    D=M
    @R2
    M=D+M

    @i //increment i
    M=M+1

    @LOOP //jump to beginning of loop
    0;JMP


(END)
    @END
    0;JMP
