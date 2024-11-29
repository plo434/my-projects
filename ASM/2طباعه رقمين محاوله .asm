.model small
.data 
num dw '7' 
msg db "the num : $"
.code
mymo proc
 mov ax,data
 mov ds,ax   
     
mov ax,num
mov bx ,10
mov cx,0

save:

mov dx ,0
div bx 
 push dx 
inc cx 
cmp al,0
jne save 

mov ah,2h

prent:
 pop dx
 
 add dx,30h
 int 21h
 sub cx,1 
 jnz prent
  aaa
   or ax,3030h 
 mov ax,2
 int 21h  
              
  
              mymo endp
end mymo