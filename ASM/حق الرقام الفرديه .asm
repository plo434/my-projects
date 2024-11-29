mov cx,0
ag:
mov ah,1
int 21h
cmp al,0dh
je ex
sub al,30h
mov ah,0
push ax
inc cx
jmp ag


ex:
mov bl,2h
pop dx
mov bh,dl
mov al,dl
mov ah,0
div bl
cmp ah,0
je ex
mov bl,al 
mov ah,2
mov dl,0ah
int 21h
mov dl,0dh
int 21h
cmp bh,0
je exx
add bh,30h
mov dl,bh
int 21h
loop ex

      exx:
 
