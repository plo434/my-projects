.model 
.stack 
.data
msg1 db "Enter onely NUMBER : $" 
msg2 db "It is number : $"
msg3 db "*It is not number.#PLEASE ENTER NUMBER# $" 
.code
macro line 
    mov dl,0ah
    mov ah,2
    int 21h
    mov dl,0dh
    int 21h
        endm
mymo proc
    mov dx,@data
    mov ds,dx
   
  agen:  
    lea dx,msg1
    mov ah,9
    int 21h
    
    mov ah,1
    int 21h
    
    
    mov bl,al
    
    cmp bl,30h
     jnae lesnum:
    
    cmp bl,3Ah 
     jnb  gretnum:
    
     line
     line 
     line
    lea dx,msg2
    mov ah,9
    int 21h
    
    mov dl,bl
    mov ah,2
    int 21h
       jmp endd:
  
    lesnum:
        gretnum:
          mov dl,0ah
          mov ah,2
          int 21h
          lea dx,msg3
          mov ah,9
          int 21h
          line
          jmp agen:
    
    
    
    
    
    
    endd:
    mymo endp
end mymo