"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initCatalog():
    catalog = {'events': None,
               'content_features': None,
               'sentiment_values': None,
               'listening_events': None,
               'genres': None}
    
    catalog['events'] = lt.newList('ARRAY_LIST')
    catalog['content_features'] = mp.newMap(20, maptype='PROBING', loadfactor=0.5)
    catalog['listening_events'] = mp.newMap()
    catalog['genres'] = mp.newMap(10, maptype='PROBING', loadfactor=0.5)
    catalog['hashtags'] = mp.newMap(maptype='PROBING', loadfactor=0.5)
    return catalog


# Funciones para agregar informacion al catalogo
def addHashtag(catalog, hashtag):
    if(hashtag['vader_avg'] != ''):
        mp.put(catalog['hashtags'], hashtag['hashtag'], float(hashtag['vader_avg']))


def addGenre(catalog, genrename, mintempo, maxtempo):
    genre = newGenre(genrename, mintempo, maxtempo)
    mp.put(catalog['genres'], genrename, genre)


def addUserGenre(catalog, genrename, mintempo, maxtempo):
    genre = newGenre(genrename, mintempo, maxtempo)
    mp.put(catalog['genres'], genrename, genre)
    pass


def assignGenre(catalog, event):
    for genre in lt.iterator(mp.valueSet(catalog['genres'])):
        if float(event['tempo']) >= genre['min_tempo'] and float(event['tempo']) <= genre['max_tempo']:
            lt.addLast(genre['events'], event)


def addEvent(catalog, event):
    lt.addLast(catalog['events'], event)
    updateFeatures(catalog['content_features'], event)


def updateFeatures(table, event):
    '''Todos los features estan en una tabla de Hash, el key es el feature y el value es un rbt
    este rbt tiene key un valor de instrumentalness (por ejemplo) y como valor un diccionario
    el diccionario tiene dos elementos:
        el elemento ['valueevents'] que contiene una array list con todos los eventos de reproduccion
        el elemento ['track_ids'] que contiene un hash table con key = track_id y value = evento con ese track id

    el anadido fue el segundo elemento. 
    Lo hice de esta manera para poder completar los requerimientos 2 y 3, que piden reproducciones unicas y comparar diccionarios.

    Otra cosa es que ahora solo se crean RBTs para features con valores que tiene sentido comparar, antes se creaba para todo feature

    Ademas hice cambios para que los keys de los RBT sean floats, antes eran strings.
    '''
    i = 1
    for feature in event:
        
        if mp.size(table) < 9:
            print(mp.size(table))
            tree = om.newMap(omaptype='RBT', comparefunction=cmpFunction)
            dict = {'valueevents' : None, 'track_ids':None}

            dict['valueevents'] = lt.newList(datastructure='ARRAY_LIST')
            dict['track_ids'] = mp.newMap(maptype='PROBING', loadfactor=0.5)

            lt.addLast(dict['valueevents'], event)
            mp.put(dict['track_ids'], event['track_id'], event)
            
            om.put(tree, float(event[feature]), dict)
            mp.put(table, feature, tree)
        else:
            tree = me.getValue(mp.get(table, feature))
            if om.contains(tree, float(event[feature])):
                dict = me.getValue(om.get(tree, float(event[feature])))
                lt.addLast(dict['valueevents'], event)
                mp.put(dict['track_ids'], event['track_id'], event)
            else:
                dict = {'valueevents' : None, 'track_ids':None}
                dict['track_ids'] = mp.newMap(maptype='PROBING', loadfactor=0.5)
                dict['valueevents'] = lt.newList(datastructure='ARRAY_LIST')

                lt.addLast(dict['valueevents'], event)
                mp.put(dict['track_ids'], event['track_id'], event)

                om.put(tree, float(event[feature]), dict)
        if i == 9:
            break
        i += 1


# Funciones para creacion de datos
def newGenre(name, mintempo, maxtempo):
    genre = {'name': name.lower(),
             'min_tempo': mintempo,
             'max_tempo': maxtempo,
             'events': lt.newList(datastructure='ARRAY_LIST')}
    return genre


# Funciones de consulta
def getCharacteristicReproductions(catalog, characteristic, minrange, toprange):
    tree = me.getValue(mp.get(catalog['content_features'], characteristic))
    total = 0
    artists = lt.newList('ARRAY')
    for value in lt.iterator(om.values(tree, minrange, toprange)):
        events = value['valueevents']
        total += lt.size(events)
    
        for event in lt.iterator(events):
            if not lt.isPresent(artists, event['artist_id']):
                lt.addLast(artists, event['artist_id'])
    total2 = lt.size(artists)
    artists.clear()
    return total, total2

def getPartyMusic(catalog, minEne, maxEne, minDan, maxDan):
    EneValues = om.values(me.getValue(mp.get(catalog['content_features'], 'energy')),minEne, maxEne)
    DanValues = om.values(me.getValue(mp.get(catalog['content_features'], 'danceability')), minDan, maxDan)
    lstEnergyDance = lt.newList(datastructure='ARRAY_LIST')

    for dictDance in lt.iterator(DanValues):
        trackIdsList_Dance = mp.valueSet(dictDance['track_ids'])
        for dictEnergy in lt.iterator(EneValues):
            for event in lt.iterator(trackIdsList_Dance):
                if(mp.contains(dictEnergy['track_ids'], event['track_id']) == True):
                    lt.addLast(lstEnergyDance, event)

    return lstEnergyDance
    


        


def getStudyMusic(catalog, mininst, maxinst, mintempo, maxtempo):
    pass


# Funciones utilizadas para comparar elementos dentro de una lista
def cmpFunction(data1, data2):
    if data1 == data2:
        return 0
    elif data1 > data2:
        return 1
    else:
        return -1


# Funciones de ordenamiento
