.model small
.stack 10h
.data 
msg1 db "It is number : $"
msg2 db "It is captel char : $"
msg3 db "It is small char : $"
msg4 db "It is not number or char : $" 
msg5 db "Enter any key : $"
.code 
mymo proc
     mov dx,@data
     mov ds,dx 
     
     lea dx,msg5
     mov ah,9
     int 21h
     
     mov ah,01h
     int 21h 
     mov bl, al
    
       ;-----
    mov dl,0ah
    mov ah,2
    int 21h
    mov dl,0dh
    int 21h
    ;------  
   
    
           ;------1------
           mov al,3Ah
           cmp al,bl
           jc notnum:
           
           mov al,2Fh
           cmp al,bl
           jnc notchar: 
          
           lea dx,msg1
           mov ah,9
           int 21h
          
           mov ah,02h
           mov dl,bl  
           int 21h
                  
                  jmp endd:
           
            ;prenit is number 
        

     notnum:    
           ;------2------
            mov al,5Bh
            cmp al,bl
            jc notcaptel:
            
            mov al,40h
            cmp  al,bl
            jnc notchar:
            
           lea dx,msg2
           mov ah,9
           int 21h
           
           mov ah,02h
           mov dl,bl  
           int 21h
               
                jmp endd:
                      ;prent it is captel
                
  notcaptel:    
               ;------3------
                mov al,7Bh
                cmp al,bl
                jc notchar: 
                
                mov al,60h
                cmp al,bl
                jnc notchar:
                
           lea dx,msg3
           mov ah,9
           int 21h
           
           mov ah,02h
           mov dl,bl  
           int 21h
                 jmp endd:
                  ;prent it is small 
                 
 notchar:      
           ;------4------
           lea dx,msg4
           mov ah,9
           int 21h
           
           mov ah,02h
           mov dl,bl  
           int 21h
                ;ptent not char 
               
               endd:
mymo endp
end mymo
