.model small
.stack 20h
.data
nam db ?
.code  
macro line 
    mov dl,0ah
    mov ah,2
    int 21h
    mov dl,0dh
    int 21h
        endm
main proc             
    
   mov dx,@data
   mov ds,dx 
   mov si,0
ent: 
   mov ah,1
   int 21h
   mov bl,al
   cmp bl,0Dh
   je prin
   mov [si],al 
   inc si
   jmp ent
 
 
 prin: 
 line 
      push si
      mov cx,si
      inc si  
      mov [si],'$'
      mov si,0
     
prin2:
      mov ah,2
      mov dl,[si] 
      int 21h
      inc si
      loop prin2  
                 
line        
         lea dx,nam
         mov ah,9
         int 21h
line
    
        pop si
    re:
     
     mov ah,2
     mov dl,[si]
     int 21h
     cmp si,0
     je ex 
     dec si
     jmp re
              
         ex:
                 
    main endp   
    endm