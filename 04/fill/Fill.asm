// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@PIXELCOLOUR
M=0

@16384
D=A
@CURRENTBYTE
M=D

(LOOP) //start of infinite loop

    @KBD
    D=M
    @BLACK
    D;JNE
    
    @PIXELCOLOUR //Prepare to write white to pixels
    M=0
    @SCREENWRITE
    0;JMP

    (BLACK) //Prepare to write black to pixels
    @PIXELCOLOUR
    M=-1

    
    (SCREENWRITE)
    //write to screen
    @PIXELCOLOUR
    D=M
    @CURRENTBYTE
    A=M
    M=D
    
    @CURRENTBYTE //Increment pointer
    MD=M+1
    //RESET ONCE 24575 is reached
    @24575
    D=D-A
    @SKIPPOINTERRESET   
    D;JLE
    @16384
    D=A
    @CURRENTBYTE
    M=D
    (SKIPPOINTERRESET)

@LOOP
0;JMP