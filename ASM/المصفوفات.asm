.model small
.stack 10h
.data    
num2 db ?
num db ?
res db ?
.code 
macro line
    mov dl,0ah
    mov ah,2
    int 21h
    mov dl,0dh
    int 21h
    endm 
main proc             
      mov dx,712h
      mov ds,dx
      mov si,0
     age: 
      mov ah,1     
      int 21h
      mov bl,al
      cmp bl,0Dh
      je ex
      
      mov num2[si],al
      inc si
      jmp age
      ex:
      line
      mov cx,si
      mov si,0 
      mov al,num2[0]
      sub al,30h
      mov bl,10
      mul bl
      mov bh,al
      mov al,num2[1]
      sub al,30h
      add al,bh
      mov bl,al 
      mov bh,0     
      push bx
      
      line
     agee: 
      mov ah,1     
      int 21h
      mov bl,al
      cmp bl,0Dh
      je exx 
      mov num[si],al
      inc si
      jmp agee
      exx:
      line
      mov cx,si
      mov si,0 
      mov al,num[0]
      sub al,30h
      mov bl,10
      mul bl
      mov bh,al
      mov al,num[1]
      sub al,30h
      add al,bh
   
      pop bx
      add al,bl
     
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