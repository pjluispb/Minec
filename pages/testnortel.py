
lista_original = [['4262875517'], ['04242432267', '4123908500'], [], ['04246057507 '], ['(0416) 0532080', '4160532080'], ['0426-5543006', '0426-5543006'], ['4121482956'], ['04246309923', '4246309923']]

def normalizar_elemento(elemento):
    # Eliminar espacios en blanco al principio y al final
    elemento = elemento.strip()

    # Verificar si el elemento comienza con '0'
    if not elemento.startswith('0'):
        elemento = '0' + elemento

    # Verificar si el código después del '0' es válido
    codigos_validos = ['416', '426', '414', '424', '412']
    codigo = elemento[1:4]
    if codigo not in codigos_validos:
        # Si no es válido, usar '416' como código predeterminado
        elemento = '0' + '416' + elemento[4:]

    # Asegurar que la longitud total sea 12
    elemento = elemento[:12]

    return elemento

# Normalizar cada sublista en la lista original
lista_normalizada = [list(map(normalizar_elemento, sublista)) for sublista in lista_original]

# Imprimir la lista normalizada
for sublista in lista_normalizada:
    print(sublista)

ln1 = normalizar_elemento('0426-5543006')
print(ln1)
