;x^2  + 3x +9


.model small
.stack 10h
.data 
x db ?
res db ? 
.code
 macro newline
        mov ah,2
        mov dl,0ah
        int 21h
        mov dl,0dh
        int 21h
endm 
main proc
       mov dx,@data
       mov ds,dx
       
       mov ah,1
       int 21h
       sub al,30h
       mov x,al
       mul x
      
       mov bh,al
       
       mov al,x
       mov bl,3
       mul bl
       
       add al,bh
       add al,9
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
       
       
       
       
       
       
       
       
       
   
   main endp
   endm