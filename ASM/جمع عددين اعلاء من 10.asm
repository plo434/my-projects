.model small
.data 
num db 87h 
msg db "the sum is  : $"
.code
mymo proc
    mov ax,@data
    mov ds,ax
    
    lea dx,msg
    mov ah,9
    int 21h 
    
        mov ah ,0
        mov al, 9h
        add al,7h
        
         
        aaa
        or ax,3030h
        
        mov bx,ax
        mov dl,bh
        
        mov ah,2h
        int 21h
        
        mov dl,bl
        mov ah,2h
        int 21h
        
   
              
mymo endp
end mymo