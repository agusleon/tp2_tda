import argparse

MENOS_INFINITO = -999

# Objeto que representa a una caja y sus propiedades

class Caja:
     def __init__(self, cod, largo, altura):
        self.cod = cod
        self.largo = int(largo)
        self.altura = int(altura)

# Funcion que lee un archivo linea por linea y crea la lista de objetos de tipo Caja

def readFile(path):
    with open(path) as f: lines = [ line.strip() for line in f ]
    cajas = []
    for line in lines:
        arr_caja = line.split(',')
        caja = Caja(arr_caja[0], arr_caja[1], arr_caja[2])
        cajas.append(caja)

    return cajas

# Funcion que lee los parametros del programa por línea de comando y devuelve el nombre del archivo que contiene la informacion, la cantidad de cajas y
# el largo de las repisas

def readArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path del archivo que contiene la información de las cajas')
    parser.add_argument('largo',  type=int, help='cantidad de cajas')
    parser.add_argument('n',  type=int, help='largo de las repisa')
    args = parser.parse_args()

    return args.path, args.n, args.largo

# Funcion para crear matriz de seleccionados, va a ser una lista de listas que a su vez contendrá una lista que 
# tendrá los elementos que aporten a esa ganancia en particular

def crear_matriz_seleccionados(L, n):

    lista = []

    for i in range(n+1):
        lista_de_listas = []

        for i in range(L+1):
            lista_de_listas.append([])

        lista.append(lista_de_listas)

    return lista

# Funcion para crear la matriz de ganancia por cada vez que se evalúe la caja i contra el peso restante j
# El elemento matriz[i][j] contendrá la ganancia acumulada de los elementos seleccionados[i][j]

def crear_matriz_ganancia(L, n):

    matriz = []

    for i in range(n+1):
        lista = []

        for i in range(L+1):
            lista.append(0)

        matriz.append(lista)
    
    return matriz

# Algoritmo que emplea programacion dinamica para encontrar la mejor disposición de las cajas en estantes tales que la altura total sea mínima

def programacion_dinamica(cajas, alturas, seleccionados, L, n):

    max_altura_estante = 0

    for i in range(0,n):
        for j in range(1,L+1):
            altura_temporal = MENOS_INFINITO

            if cajas[i].largo <= j:
                altura_temporal = cajas[i].altura + alturas[i][j-cajas[i].largo]

            altura_historica = alturas[i][j]

            if altura_temporal > altura_historica:
                alturas[i+1][j] = altura_temporal
                seleccionados[i+1][j] = seleccionados[i][j-cajas[i].largo].copy()
                seleccionados[i+1][j].append(cajas[i])

                if max_altura_estante < cajas[i].altura:
                    max_altura_estante = cajas[i].altura
            else:
                alturas[i+1][j] = altura_historica
                seleccionados[i+1][j] = seleccionados[i][j].copy()

    return seleccionados[n][L], max_altura_estante

# Funcion que repite el algoritmo de programación dinámica hasta que no haya más cajas que ubicar

def disponer_cajas(cajas, L, n):

    num_estantes = 1
    altura_acumulada = 0

    while n > 0:
        seleccionados = crear_matriz_seleccionados(L, n)
        alturas = crear_matriz_ganancia(L, n)

        seleccionados_final, max_altura_estante = programacion_dinamica(cajas, alturas, seleccionados, L, n)

        print("En el estante "+str(num_estantes)+": Se dispondrán las cajas", end=" ")

        for caja_seleccionada in seleccionados_final:
            print(caja_seleccionada.cod,end=" ")
            cajas.remove(caja_seleccionada)

        
        print("con una altura máxima de "+str(max_altura_estante)+"\n")

        n = len(cajas)

        num_estantes+=1
        altura_acumulada+=max_altura_estante

    print("La altura de todos los estantes será: "+str(altura_acumulada)+"\n")

# Main

if __name__=="__main__":

    archivo, n, L = readArguments()
    cajas = readFile(archivo)
    disponer_cajas(cajas, L, n)
