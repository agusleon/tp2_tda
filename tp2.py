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

def disponerCajas(cajas, L, n):
    max_alturas = [0] * (n+1)
    estantes = [0] * (n+1)

    for i in range(1,n+1):
        print(max_alturas)
        print(estantes)
        largo = cajas[i-1].largo
        altura = cajas[i-1].altura
        print("Largo: " + str(largo))
        print("Altura: " + str(altura))
        max_alturas[i] = max_alturas[i-1] + altura
        estantes[i] = estantes[i-1]+1
        for j in range(i-1,0,-1):
            print(j)
            if (largo + cajas[j-1].largo <= L):
                altura = max(altura, cajas[j-1].altura)
                largo = largo + cajas[j-1].largo
                if (altura + max_alturas[j-1] <= max_alturas[i]):
                    max_alturas[i] = altura + max_alturas[j-1]
                    estantes[j] = estantes[i]
    return max_alturas, estantes

    


# Main

if __name__=="__main__":

    archivo, n, L = readArguments()
    cajas = readFile(archivo)
    max_alturas, estantes = disponerCajas(cajas, L, n)
    print("Maxima altura: " + str(max_alturas[n]))
    for i in range(1,n+1):
        print("Caja " + str(cajas[i-1].cod) + " en estante " + str(estantes[i]))


