.model small
.stack 10h
.data 
num db ?
.code 

mov dx,@data
mov ds,dx
mov si,0

enter:
mov ah,1
int 21h
cmp al,0Dh
je print
mov [si],dl
inc si
jmp enter

print:





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    mov ax,12
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