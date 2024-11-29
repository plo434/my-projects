 
    mov cx,9
   li:
    add ax,cx
      LOOP li
      
      mov bl,10
      div bl 
      mov bh,ah
      add bh,30h
      mov bl,al
      add bl,30h
      mov dl,bl
      
      mov ah,2
      int 21h
       
      
      mov dl,bh
      mov ah,2
      int 21h
                        