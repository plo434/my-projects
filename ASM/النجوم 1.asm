.data 
num db "0"
macro print 
    
    
   
       mov dl,'*'
       mov ah,2
       int 21h
    
endm
macro newline
        mov ah,2
        mov dl,0ah
        int 21h
        mov dl,0dh
        int 21h
endm
     mov dx,@data
    mov ds,dx
mov ah,1      
    int 21h        
     
    mov num, al    

    
   newline                                                        
      
 
    
mov si,0
mov cl,num
sub cl,30h
lop:

cmp si,cx
ja next
mov di,0                


lop2:
print
inc di 
cmp di,si
ja endline
jmp lop2  
endline:
inc si
newline
jmp lop
next:  

    ;================================================
lopp: 
cmp si,0
je exit
mov di,0                


lopp2:
print
inc di 
cmp di,si
je endline2
jmp lopp2
  
endline2:
dec si
newline
jmp lopp
exit:  

