﻿"""
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
 """

import config as cf
import model
import csv
from DISClib.ADT import map as mp

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de canciones
def initCatalog():
    return model.initCatalog()


# Funciones para la carga de datos
def loadData(catalog):
    loadGenres(catalog)
    loadFeatures(catalog)
    loadHashtags(catalog)
    loadUserHashtags(catalog)
    

def loadGenres(catalog):
    genres = [("Reggae", 60, 90),
              ("Down-tempo", 70, 100),
              ("Chill-out", 90, 120),
              ("Hip-hop", 85, 115),
              ("Jazz and Funk", 120, 125),
              ("Pop", 100, 130),
              ("R&B", 60, 80),
              ("Rock", 110, 140),
              ("Metal", 100, 160)]
    for genre in genres:
        model.addGenre(catalog, genre[0], genre[1], genre[2])
    genres.clear()


def addUserGenre(catalog, genrename, mintempo, maxtempo):
    return model.addUserGenre(catalog, genrename, mintempo, maxtempo)


def loadFeatures(catalog):
    featuresfile = cf.data_dir + "context_content_features-small.csv"
    input_file = csv.DictReader(open(featuresfile, encoding='utf-8'))
    for event in input_file:
        model.assignGenre(catalog, event)
        model.addEvent(catalog, event)
        model.updateHour_Tree(catalog, event)


def loadHashtags(catalog):
    hashtagsfile = cf.data_dir + 'sentiment_values.csv'
    input_file = csv.DictReader(open(hashtagsfile, encoding='utf-8'))
    for hashtag in input_file:
        model.addHashtag(catalog, hashtag)


def loadUserHashtags(catalog):
    userHashtagsFile = cf.data_dir + 'user_track_hashtag_timestamp-small.csv'
    input_file = csv.DictReader(open(userHashtagsFile, encoding='utf-8'))
    for event in input_file:
        model.updateUserHashtags(catalog, event)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getCharacteristicReproductions(catalog, characteristic, minrange, toprange):
    return model.getCharacteristicReproductions(catalog, characteristic, minrange, toprange)

def getMusic(catalog, min1, max1, min2, max2, name1, name2):
    return model.getMusic(catalog, min1, max1, min2, max2, name1, name2)

def getGenreReproductions(catalog, genrename):
    return model.getGenreReproductions(catalog, genrename)

def generosEnRango(catalog, minHour, maxHour):
    return model.generosEnRango(catalog, minHour, maxHour)