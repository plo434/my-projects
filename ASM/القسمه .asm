.model small
.stack 20h
.data
x db ?
y db ?
q db ?
r db ?   
msg1 db "Enter first value:$"
msg2 db "Enter second value:$"
msg3 db "The Qutient is:$"
msg4 db "The remainder is:$"
.code 
macro saleh
    mov dl,0ah
    mov ah,2
    int 21h
    mov dl,0dh
    int 21h
    endm
main proc
      mov dx,@data
      mov ds,dx
      
    
    lea dx,msg1
    mov ah,9
    int 21h 
    
    mov ah,1
    int 21h  
    sub al,30h
    mov x,al
     saleh
     lea dx,msg2
     mov ah,9
     int 21h
     
    mov ah,1
    int 21h  
    sub al,30h
    mov y,al
    saleh
   lea dx,msg3
   mov ah,9
   int 21h 
    mov al,x
    mov ah,0
   div y
   
   push ax
         
   mov dl,al
   add dl,30h
   mov ah,2
   int 21h
         
         ;------
         
        saleh
        lea dx,msg4
        mov ah,9
        int 21h
   ;------------
    pop dx
      
    mov dl,dh
   add dl,30h
   mov ah,2
   int 21h
    
    main endp
end main