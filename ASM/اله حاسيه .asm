.model small
.stack 100h
.data
    msg1 db "Enter first number: $"
    msg2 db "Enter operator (+, -, *, /): $"
    msg3 db "Enter second number: $"
    msg4 db "Result: $"
    msg5 db "Invalid input. Try again.$"
    msg6 db "*It is not number.#PLEASE ENTER NUMBER# $" 
    msg7 db "*It is not operator (+, -, *, /) .#PLEASE ENTER OPERATOR (+, -, *, /)# $" 
    num1 db 0
    num2 db 0
    operator db 0
    result dw 0

macro line 
    mov ah, 2
    mov dl, 0Dh
    int 21h
    mov dl, 0Ah
    int 21h
    endm                            -
.code 

mymo proc
    mov ax, @data
    mov ds, ax

    ; frst number
agenfir:    

    lea dx, msg1
    mov ah, 9
    int 21h
    
    mov ah, 1
    int 21h    
   
    cmp al,30h
      jnae invalid:
    cmp al,3Ah 
      jnb invalid :
     
    sub al, 30h
    mov num1, al


line 
line
line
    agenop:
    ; oprat
    lea dx, msg2
    mov ah, 9
    int 21h
    
    mov ah, 1
    int 21h
     
    mov operator, al

 line
 line
 line
 
 agensie:
    ; Read second number
    lea dx, msg3
    mov ah, 9
    int 21h
    mov al ,0
    mov ah, 1
    int 21h
    

     
    
    sub al, 30h
    mov num2, al

line
line
line 
    ; Calculate
    mov al, num1
    mov bl, num2
    mov cl, operator

    cmp cl, 2Bh ;+
    je addd
    cmp cl, 2Dh   ;-
    je subb
    cmp cl, 2Ah     ;*
    je mull
    cmp cl, 2fh     ;\
    je divv
     jmp invalid_opr
    
   

addd:
    add al, bl
    mov ah, 0
    mov result, ax
    jmp print

subb:
    sub al, bl
    mov ah, 0
    mov result, ax
    jmp print

mull:
    mul bl
    mov result, ax
    jmp print

divv:
    mov ah, 0
    div bl
    mov result, ax
    jmp print
invalid_opr: 

          mov dl,0ah
          mov ah,2
          int 21h
          
          lea dx, msg5
          mov ah, 9
          int 21h
          
        line 
        line 
        
          lea dx,msg7
          mov ah,9
          int 21h
           line
           jmp agenop
          
          
invalid:    
line
          mov bl,al    
          mov dl,0ah
          mov ah,2
          int 21h
          
          lea dx, msg5
          mov ah, 9
          int 21h
          
       
     line   
          
            line
            line
          lea dx,msg6
          mov ah,9
          int 21h
           line
           line
           
          jmp agenfir:
          cmp num2,00h
          je agensie:

print:
    lea dx, msg4
    mov ah, 9
    int 21h

    mov ax, result
    mov cx, 0
    mov dx, 0
    
    cmp ax,0
    jge positev
    
    push ax
    mov dl, '-'
    mov ah, 2
    int 21h
    pop ax                                                             
    neg ax
    mov dl,al
    add dl,30h
    mov ah,2
    int 21h
    jmp endd

positev:
    mov bx, 10
    div bx
    push dx
    inc cx
    mov dx, 0
    cmp ax, 0
    jne positev
    
printres:
    pop dx
    add dl, 30h
    mov ah, 2
    int 21h
    dec cx
    jnz printres

endd:
  
        mymo endp
end mymo