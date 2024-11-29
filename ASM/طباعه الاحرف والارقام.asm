macro line 
    mov ah,2
    mov dl,0ah
    int 21h
    mov dl,0dh
    int 21h
endm 

macro charC
    mov si,65
    agee:
    mov dx,si 
    mov ah,2
    int 21h
    inc si
    cmp si,90
    line
    jg exx
    jmp agee
endm

macro charM
    add si,6
    ageee:
    mov dx,si
    mov ah,2
    int 21h
    inc si
    cmp si,122
    jg exxx
    line
    jmp ageee    

endm

charC
exx:

charM 
exxx:
line
mov si,00
    age:
    mov ax,si
    mov bl,10
    div bl

    push ax
    mov dl,al
    add dl,30h
    mov ah,2
    int 21h

    pop dx
    mov dl,dh
    add dl,30h
    mov ah,2
    int 21h

    line

    cmp si,99 
    je ex
    inc si
    jmp age    
ex: 