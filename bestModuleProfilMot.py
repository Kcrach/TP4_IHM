import csv
import sys

def calcMotivationVar(mat, pvals):
    toReturn = 3 * [0] #One per motivation's profil
    idRowMat = 0
    idRowPVals = 0
    # MotivationVar = MI + ME - Amot
    for row in mat:
        for rowP in pvals:
            if idRowMat == idRowPVals:
                if idRowMat == 2 : 
                    if float(rowP['MI']) < 0.1:      
                        toReturn[0] -= float(row['MI'])
                    if float(rowP['ME']) < 0.1:      
                        toReturn[1] -= float(row['ME'])
                    if float(rowP['amotI']) < 0.1:      
                        toReturn[2] -= float(row['amotI'])
                else:      
                    if float(rowP['MI']) < 0.1:      
                        toReturn[0] += float(row['MI'])
                    if float(rowP['ME']) < 0.1:      
                        toReturn[1] += float(row['ME'])
                    if float(rowP['amotI']) < 0.1:      
                        toReturn[2] += float(row['amotI'])
            idRowPVals += 1
        idRowMat += 1
    return toReturn

def bestModuleProfilMot(idStudent):
    modules = [] # ["avatar", "badges", "progress", "rank", "score", "timer"]
    moduleName = {0: "avatar", 1: "badges", 2: "progress", 3: "rank", 4: "score", 5: "timer"}

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
        with open('./R Code/PLS/Motivation/rankingpVals.csv', newline='') as csvfilepVals:
            pvalsScore = csv.DictReader(csvfilepVals, delimiter =";")
            motScore = calcMotivationVar(score, pvalsScore)
            modules.append(motScore)
    
    with open('./R Code/PLS/Motivation/timerPathCoefs.csv', newline='') as csvfile:
        timer = csv.DictReader(csvfile, delimiter =";")
        with open('./R Code/PLS/Motivation/rankingpVals.csv', newline='') as csvfilepVals:
            pvalsTimer = csv.DictReader(csvfilepVals, delimiter =";")
            motTimer = calcMotivationVar(timer, pvalsTimer)
            modules.append(motTimer)

    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";")
        
        idRow = 0
        vecAff = [0] * 6

        for row in students:
            if idRow == idStudent:
                for i in range(len(modules)) :
                    vecAff[i] += (float(row['micoI']) + float(row[' miacI']) + float(row[' mistI'])) * modules[i][0]
                    vecAff[i] += (float(row[' meidI']) + float(row[' meinI']) + float(row[' mereI'])) * modules[i][1]
                    vecAff[i] += float(row[' amotI']) * modules[i][2]
                break
            idRow += 1

        print(vecAff)

        # Find the best
        indexMax = 0

        for i in range(len(vecAff)):
            if vecAff[i] > vecAff[indexMax]:
                indexMax = i

        print("Le module le plus adapte au profil motivation de l'etudiant " + str(idStudent) + " semble etre le module '" + 
                moduleName.get(indexMax) + "' avec un score d'affinite de " + str(vecAff[indexMax]) + ".")

        return vecAff



    