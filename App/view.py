"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf
from DISClib.ADT import list as lt
import random

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Reproducciones por rango de característica")
    print("3- Música para festejar")
    print("4- Música para estudiar")
    print("5- Canciones y artistas por géneros")
    print("6- Género más escuchado en un tiempo")
    print("Presione cualquier otra tecla para salir")

catalog = None

def printRandomSongs(result):
    size = lt.size(result)
    i = 0
    while i < 5:
        posicion = random.randint(1, size)
        evento = lt.getElement(result, posicion)
        print('track 1: ', evento['track_id'],' with energy of ', evento['energy'],' and danceability of ', evento['danceability'])
        i +=1

def printReq5(generos, genero, total, arbol):
    print('En el rango de horas dado hay un total de ', total, ' Reproducciones...')
    print('Reggae tiene ', generos[0], ' Reproducciones')
    print('Chill Out tiene ', generos[2], ' Reproducciones')
    print('Hip-Hop tiene ', generos[3], ' Reproducciones')
    print('Jazz and Funk tiene ', generos[4], ' Reproducciones')
    print('Pop tiene ', generos[5], ' Reproducciones')
    print('R&B tiene ', generos[6], ' Reproducciones')
    print('Rock tiene ', generos[7], ' Reproducciones')
    print('Metal tiene ', generos[8], ' Reproducciones')
    print('Down Tempo tiene ', generos[1], ' Reproducciones')
    print('El genero con más reproducciones es ', genero, '!\n\n')
    print('3 Tracks con su respectivo Vader son:')
    Req5Anexo(arbol)
    

def Req5Anexo(arbol):
    i = 0
    while i < 3:
        mayorVader = om.maxKey(arbol)
        evento = me.getValue(om.get(arbol, mayorVader))
        print('El evento con track_id: ', evento['track_id'], ' con un Vader de ', mayorVader)
        om.deleteMax(arbol)
        i+=1



def initCatalog():
    return controller.initCatalog()



def loadData(catalog):
    return controller.loadData(catalog)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)


    elif int(inputs[0]) == 2:
        characteristic = input("Nombre de la característica de contenido: ")
        minrange = float(input("Valor mínimo de la característica: "))
        toprange = float(input("Valor máximo de la característica: "))
        result = controller.getCharacteristicReproductions(catalog, characteristic, minrange, toprange)
        print("\nReproducciones totales:", result[0], "\nArtistas únicos:", result[1])

    elif int(inputs[0]) == 3:
        minEne = float(input("Valor mínimo de Energy: "))
        maxEne = float(input("Valor mínimo de Energy: "))
        minDan = float(input("Valor mínimo de Dance: "))
        maxDan = float(input("Valor mínimo de Dance: "))
        result = controller.getPartyMusic(catalog, minEne, maxEne, minDan, maxDan)
        print('++++++ Req No. 2 results... ++++++')
        print('Energy is between ', minEne, ' and ', maxEne)
        print('Danceability is between', minDan,  ' and ', maxDan)
        print('total of unique track in events: ', lt.size(result), '\n')
        printRandomSongs(result)


    elif int(inputs[0]) == 4:
        mininst = float(input("Valor mínimo de instrumentalness: "))
        maxinst = float(input("Valor máximo de instrumentalness: "))
        mintempo = float(input("Valor mínimo de tempo: "))
        maxtempo = float(input("Valor máximo de tempo: "))
        result = controller.getStudyMusic(catalog, mininst, maxinst, mintempo, maxtempo) 

    elif int(inputs[0]) == 5:
        genreslist = input("Nombre de los géneros (separados por coma): ").lower().split(',')
        #totalcount = 0
        #countlist = lt.newList('ARRAY_LIST')
        for genrename in genreslist:
            if not mp.contains(catalog['genres'], genrename):
                mintempo = float(input("Valor mínimo de tempo del género " + genrename + ": "))
                maxtempo = float(input("Valor máximo de tempo del género" + genrename + ": "))
                controller.addUserGenre(catalog, genrename, mintempo, maxtempo)
            #result = controller.getGenreReproductions(catalog, genrename)
            #totalcount += result[0]
            #lt.addLast(countlist, result[0])


    elif int(inputs[0]) == 6:
        minhour = input("Hora inicial del rango de tiempo: ")
        maxhour = input("Hora final del rango de tiempo: ")
        result = controller.generosEnRango(catalog, minhour, maxhour)
        printReq5(result[0], result[1], result[2], result[3])

    else:
        catalog.clear()
        sys.exit(0)
sys.exit(0)