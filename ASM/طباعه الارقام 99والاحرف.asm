macro print x
    
    
    mov ax,x
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
       int 21h
    
endm
macro newline
        mov ah,2
        mov dl,0ah
        int 21h
        mov dl,0dh
        int 21h
endm 

mov si,0
lop:
print si
inc si 
newline
cmp si,99
ja exit
jmp lop

exit: