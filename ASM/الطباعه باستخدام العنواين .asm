.model small
.stack 20h
.data
num db "CYBER$"
num2 db 1,2,3,0
.code
main proc             
    
    
    
         mov dx,712h
         mov ds,dx
         mov si,0
        ;mov [0125h],'*'
         
     
        mov ah,2   
        mov dl,[si] 
        cmp dl,'$'
        
        je ex
        int 21h 
        inc si 
        jmp 08h
                ex:
  
        
        
        
        
        
        
        
        
        
        
    main endp   
    endm