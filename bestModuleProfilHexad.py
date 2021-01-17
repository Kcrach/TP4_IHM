import csv
import sys
from collections import OrderedDict

moduleName = {0: "avatar", 1: "badges", 2: "progress", 3: "ranking", 4: "score", 5: "timer"}
modules = [] # ["avatar", "badges", "progress", "rank", "score", "timer"] 

def calcMotivationVar(m, p):
    toReturn = 6 * [0] #One per Hexad's profil
    idRow = 0
    precision = 0.1

    pvals = convertDictReaderToArray(p)
    mat = convertDictReaderToArray(m)

    #MotivationVar = MI + ME - Amot
    for i in range(len(mat)):
        for j in range(len(pvals)):
            if i == j:
                if i == 2 : 
                    if float(pvals[i]['achiever']) < precision:      
                        toReturn[0] -= float(mat[i]['achiever'])
                    if float(pvals[i]['player']) < precision:      
                        toReturn[1] -= float(mat[i]['player'])
                    if float(pvals[i]['socialiser']) < precision:      
                        toReturn[2] -= float(mat[i]['socialiser'])
                    if float(pvals[i]['freeSpirit']) < precision:      
                        toReturn[3] -= float(mat[i]['freeSpirit'])
                    if float(pvals[i]['disruptor']) < precision:      
                        toReturn[4] -= float(mat[i]['disruptor'])
                    if float(pvals[i]['philanthropist']) < precision:      
                        toReturn[5] -= float(mat[i]['philanthropist'])
                else:      
                    if float(pvals[i]['achiever']) < precision:      
                        toReturn[0] += float(mat[i]['achiever'])
                    if float(pvals[i]['player']) < precision:      
                        toReturn[1] += float(mat[i]['player'])
                    if float(pvals[i]['socialiser']) < precision:      
                        toReturn[2] += float(mat[i]['socialiser'])
                    if float(pvals[i]['freeSpirit']) < precision:      
                        toReturn[3] += float(mat[i]['freeSpirit'])
                    if float(pvals[i]['disruptor']) < precision:      
                        toReturn[4] += float(mat[i]['disruptor'])
                    if float(pvals[i]['philanthropist']) < precision:      
                        toReturn[5] += float(mat[i]['philanthropist'])
                break  

    return toReturn

def convertDictReaderToArray(dictReader):
    toReturn = [0] * 3

    i = 0
    for row in dictReader:
        toReturn[i] = row
        i += 1

    return toReturn


def bestModuleProfilHexad(idStudent):
    modules = []

    # Load all csv
    with open('./R Code/PLS/Hexad/avatarPathCoefs.csv', newline='') as csvfile:
        avatar = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Hexad/avatarpVals.csv', newline='') as csvfilepVals:
            pvalsAvatar = csv.DictReader(csvfilepVals, delimiter =";")
            motAvatar = calcMotivationVar(avatar, pvalsAvatar)
            modules.append(motAvatar)

    with open('./R Code/PLS/Hexad/badgesPathCoefs.csv', newline='') as csvfile:
        badges = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Hexad/badgespVals.csv', newline='') as csvfilepVals:
            pvalsBadges = csv.DictReader(csvfilepVals, delimiter =";")
            motBadges = calcMotivationVar(badges, pvalsBadges)
            modules.append(motBadges)


    with open('./R Code/PLS/Hexad/progressPathCoefs.csv', newline='') as csvfile:
        progress = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Hexad/progresspVals.csv', newline='') as csvfilepVals:
            pvalsProgress = csv.DictReader(csvfilepVals, delimiter =";")
            motProgress = calcMotivationVar(progress, pvalsProgress)
            modules.append(motProgress)

    with open('./R Code/PLS/Hexad/rankingPathCoefs.csv', newline='') as csvfile:
        ranking = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Hexad/rankingpVals.csv', newline='') as csvfilepVals:
            pvalsRanking = csv.DictReader(csvfilepVals, delimiter =";")
            motRanking = calcMotivationVar(ranking, pvalsRanking)
            modules.append(motRanking)

    with open('./R Code/PLS/Hexad/scorePathCoefs.csv', newline='') as csvfile:
        score = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Hexad/scorepVals.csv', newline='') as csvfilepVals:
            pvalsScore = csv.DictReader(csvfilepVals, delimiter =";")
            motScore = calcMotivationVar(score, pvalsScore)
            modules.append(motScore)
    
    with open('./R Code/PLS/Hexad/timerPathCoefs.csv', newline='') as csvfile:
        timer = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Hexad/timerpVals.csv', newline='') as csvfilepVals:
            pvalsTimer = csv.DictReader(csvfilepVals, delimiter =";")
            motTimer = calcMotivationVar(timer, pvalsTimer)
            modules.append(motTimer)

    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";")
        
        idRow = 0
        vecAff = [0] * 6 # ["avatar", "badges", "progress", "rank", "score", "timer"]

        for row in students:
            if idRow == idStudent:
                for i in range(len(modules)) :
                    vecAff[i] += float(row['achiever']) * modules[i][0]
                    vecAff[i] += float(row['player']) * modules[i][1]
                    vecAff[i] += float(row['socialiser']) * modules[i][2]
                    vecAff[i] += float(row['freeSpirit']) * modules[i][3]
                    vecAff[i] += float(row['disruptor']) * modules[i][4]
                    vecAff[i] += float(row['philanthropist']) * modules[i][5]
                break
            idRow += 1

        dictAff = dict()
        for i in range(len(vecAff)):
            dictAff[moduleName.get(i)] = vecAff[i]

        return dictAff, modules

def affinityDominance(idStudent, dominanceHexad, module, modulesVar):
    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";")
        hexadType = ['achiever', 'player', 'socialiser', 'freeSpirit', 'disruptor', 'philanthropist']
            
        idRow = 0
        vecAff = [0] * 6 # ["avatar", "badges", "progress", "rank", "score", "timer"]
        idModule = 0
        idHexadType = 0
        affinity = 0

        for i in range(len(moduleName)):
            if moduleName.get(i) == module:
                idModule = i
                break

        for i in range(len(hexadType)):
            if hexadType[i] == dominanceHexad:
                idHexadType = i
                break

        for row in students:
            if idRow == idStudent:
                affinity += float(row[dominanceHexad]) * modulesVar[idModule][idHexadType]
                break
            idRow += 1

        return affinity