def agregar_producto(lista,id,nombre,precio,cantidad):
    diccionario={
        'id':id,
        'nombre':nombre,
        'precio':precio,
        'cantidad':cantidad
    }
    lista.append(diccionario)
aa = []
agregar_producto(aa,'00','Pimpoyo',100,99999999999)
print(aa)
