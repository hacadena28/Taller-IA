import numpy as np
from pesosYUmbrales import matrizUmbrales,matrizPesos

# numeroDeIteraciones =int( input("Numero de iteraciones: \n"))
numeroDeIteraciones=500
errorMaximoPermitido =float(  input("Error maximo permitido: \n"))
rataDeAprendizaje =float( input("Rata de aprendizaje: \n"))
patrones=3 #**patrones falsos
entradas=3
salidas = 2



MatrizPatrones = [[1,2,3],[4,5,6],[7,8,9]]


#**Salida Falsa
s=[1,2]

#**Comprobar los valores del umbral
u = matrizUmbrales(2)
# print(u)

#**Comprobar los valores de los pesos
w = matrizPesos(3,2)
# print(b)

Yr = np.empty(salidas)
El = np.empty(salidas)
EpTotal=np.empty(patrones)

for iteracion in range(0,numeroDeIteraciones):
    print("iteracion: ",iteracion)

    for patron in range(0,patrones):
        
        #**Patron falso
        a = MatrizPatrones[patron]
        print("patron: ",patron)
        print(a)
        print("\n")
        print("\n")
        print("\n")
        print("\n")


        Ep=0
        for i in range(0,salidas): 
            aux=0
            print("valor de i:" ,i)
            for j in range(0,entradas):
                print("valor de j:",j)
                print("valor de a[j]:",a[j])
                print("valor de b[i][j]:",w[i][j])
                aux+=(a[j])*(w[i][j])
                print(aux)
            print("umbral : ",i)
            print(u[i])
            print("salida: ",i)
            Yr[i]=aux+u[i]
            
            print(Yr[i])
            El[i] = s[i]-Yr[i]
            print("error por salida: ",El[i])
            #!agregar el valor absoluto 
            if(El[i])<0:
                El[i] = El[i]*-1
                Ep+=El[i]
            print("error: por patron: ",Ep)

        Ep/=salidas

        EpTotal[patron]=Ep
        print(Yr)
        print(El)
        print("error: por patron: ",Ep)
        


        #!Segunda parte del algoritmo
        #**Modificacion de PESOS Y UMBRALES

        print("Modificacion de pesos y umbrales")

        print("Pesos viejos")
        print(w)
        print("Umbrales viejos")
        print(u)
        for i in range(0,salidas): 
            aux = w[i]
            print("valor de i:" ,i)
            for j in range(0,entradas):
                print("valor de j:",j)
                print(w[i][j])
                print(rataDeAprendizaje)
                print(float(El[i]))
                print(float(a[j]))
                print(aux)
                aux[j] = rataDeAprendizaje*El[i]*a[j]
                print(aux[j])
                print(aux)
            w[i]= aux
            u[i]+=rataDeAprendizaje*El[i]*1
                
        print("Pesos Nuevos")
        print(w)
        print("Umbrales Nuevos")
        print(u)


    Erms = sum(EpTotal)/patrones
    if(Erms <= errorMaximoPermitido):
        print("\nError maximo alcanzado\n")
        print("\n",Erms)
        break
    print("\n\n")
    print("\n\n")
    print("ERMS")
    print(Erms)
    print("\n\n")
    print("\n\n")
