import csv
import sys
from collections import OrderedDict

moduleName = {0: "avatar", 1: "badges", 2: "progress", 3: "ranking", 4: "score", 5: "timer"}
modules = [] # ["avatar", "badges", "progress", "rank", "score", "timer"]

def calcMotivationVar(m, p):
    precision = 0.1
    toReturn = 3 * [0] #One per motivation's profil

    pvals = convertDictReaderToArray(p)
    mat = convertDictReaderToArray(m)

    # MotivationVar = MI + ME - Amot

    for i in range(len(mat)):
        for j in range(len(pvals)):
            if i == j:
                if i == 2 : 
                    if float(pvals[i]['MI']) < precision:      
                        toReturn[0] -= float(mat[i]['MI'])
                    if float(pvals[i]['ME']) < precision:      
                        toReturn[1] -= float(mat[i]['ME'])
                    if float(pvals[i]['amotI']) < precision:      
                        toReturn[2] -= float(mat[i]['amotI'])
                else:      
                    if float(pvals[i]['MI']) < precision:      
                        toReturn[0] += float(mat[i]['MI'])
                    if float(pvals[i]['ME']) < precision:   
                        toReturn[1] += float(mat[i]['ME'])
                    if float(pvals[i]['amotI']) < precision:      
                        toReturn[2] += float(mat[i]['amotI'])

    return toReturn

def convertDictReaderToArray(dictReader):
    toReturn = [0] * 3

    i = 0
    for row in dictReader:
        toReturn[i] = row
        i += 1

    return toReturn

def bestModuleProfilMot(idStudent):
    modules = []

    # Load all csv
    with open('./R Code/PLS/Motivation/avatarPathCoefs.csv', newline='') as csvfile:
        avatar = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Motivation/avatarpVals.csv', newline='') as csvfilepVals:
            pvalsAvatar = csv.DictReader(csvfilepVals, delimiter =";")
            motAvatar = calcMotivationVar(avatar, pvalsAvatar)
            modules.append(motAvatar)

    with open('./R Code/PLS/Motivation/badgesPathCoefs.csv', newline='') as csvfile:
        badges = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Motivation/badgespVals.csv', newline='') as csvfilepVals:
            pvalsBadges = csv.DictReader(csvfilepVals, delimiter =";")
            motBadges = calcMotivationVar(badges, pvalsBadges)
            modules.append(motBadges)


    with open('./R Code/PLS/Motivation/progressPathCoefs.csv', newline='') as csvfile:
        progress = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Motivation/progresspVals.csv', newline='') as csvfilepVals:
            pvalsProgress = csv.DictReader(csvfilepVals, delimiter =";")
            motProgress = calcMotivationVar(progress, pvalsProgress)
            modules.append(motProgress)

    with open('./R Code/PLS/Motivation/rankingPathCoefs.csv', newline='') as csvfile:
        ranking = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Motivation/rankingpVals.csv', newline='') as csvfilepVals:
            pvalsRanking = csv.DictReader(csvfilepVals, delimiter =";")
            motRanking = calcMotivationVar(ranking, pvalsRanking)
            modules.append(motRanking)

    with open('./R Code/PLS/Motivation/scorePathCoefs.csv', newline='') as csvfile:
        score = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Motivation/scorepVals.csv', newline='') as csvfilepVals:
            pvalsScore = csv.DictReader(csvfilepVals, delimiter =";")
            motScore = calcMotivationVar(score, pvalsScore)
            modules.append(motScore)
    
    with open('./R Code/PLS/Motivation/timerPathCoefs.csv', newline='') as csvfile:
        timer = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Motivation/timerpVals.csv', newline='') as csvfilepVals:
            pvalsTimer = csv.DictReader(csvfilepVals, delimiter =";")
            motTimer = calcMotivationVar(timer, pvalsTimer)
            modules.append(motTimer)

    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";")
        
        idRow = 0
        vecAff = [0] * 6

        for row in students:
            if idRow == idStudent:
                MI = (float(row['micoI']) + float(row[' miacI']) + float(row[' mistI']))
                ME = (float(row[' meidI']) + float(row[' meinI']) + float(row[' mereI']))
                for i in range(len(modules)) : 
                    vecAff[i] += (float(row['micoI']) + float(row[' miacI']) + float(row[' mistI'])) * modules[i][0]
                    vecAff[i] += (float(row[' meidI']) + float(row[' meinI']) + float(row[' mereI'])) * modules[i][1]
                    vecAff[i] += float(row[' amotI']) * modules[i][2]
                break
            idRow += 1

        dictAff = dict()
        for i in range(len(vecAff)):
            dictAff[moduleName.get(i)] = vecAff[i]

        return dictAff, modules

def affinityDominance(idStudent, dominanceMot, module, modulesVar):
    with open('./userStats.csv', newline='') as csvfile:
            students = csv.DictReader(csvfile, delimiter =";")
            motType = ['MI', 'ME', 'amotI']
            
            idRow = 0
            idModule = 0
            idMotType = 0
            affinity = 0

            for i in range(len(moduleName)):
                if moduleName.get(i) == module:
                    idModule = i
                    break

            for i in range(len(motType)):
                if motType[i] == dominanceMot:
                    motType = i
                    break

            for row in students:
                if dominanceMot == "MI":
                    m = (float(row['micoI']) + float(row[' miacI']) + float(row[' mistI']))
                elif dominanceMot == "ME":
                    m = (float(row[' meidI']) + float(row[' meinI']) + float(row[' mereI']))
                else:
                    m = float(row[' amotI'])

                if idRow == idStudent:
                    affinity += m * modulesVar[idModule][idMotType]
                    break
                idRow += 1

            return affinity