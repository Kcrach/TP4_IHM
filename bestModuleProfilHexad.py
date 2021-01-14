import csv
import sys

def calcMotivationVar(mat):
    toReturn = 6 * [0] #One per Hexad's profil
    idRow = 0
    #MotivationVar = MI + ME - Amot
    for row in mat:
        if idRow == 2 :
            toReturn[0] -= float(row['achiever'])
            toReturn[1] -= float(row['player'])
            toReturn[2] -= float(row['socialiser'])
            toReturn[3] -= float(row['freeSpirit'])
            toReturn[4] -= float(row['disruptor'])
            toReturn[5] -= float(row['philanthropist'])
        else:
            toReturn[0] += float(row['achiever'])
            toReturn[1] += float(row['player'])
            toReturn[2] += float(row['socialiser'])
            toReturn[3] += float(row['freeSpirit'])
            toReturn[4] += float(row['disruptor'])
            toReturn[5] += float(row['philanthropist'])
        idRow += 1
    return toReturn

def bestModuleProfilHexad(idStudent):
    modules = [] # ["avatar", "badges", "progress", "rank", "score", "timer"]
    moduleName = {0: "avatar", 1: "badges", 2: "progress", 3: "rank", 4: "score", 5: "timer"}

    # Load all csv
    with open('./R Code/PLS/Hexad/avatarPathCoefs.csv', newline='') as csvfile:
        avatar = csv.DictReader(csvfile, delimiter =";")
        motAvatar = calcMotivationVar(avatar)
        modules.append(motAvatar)

    with open('./R Code/PLS/Hexad/badgesPathCoefs.csv', newline='') as csvfile:
        badges = csv.DictReader(csvfile, delimiter =";")
        motBadges = calcMotivationVar(badges)
        modules.append(motBadges)

    with open('./R Code/PLS/Hexad/progressPathCoefs.csv', newline='') as csvfile:
        progress = csv.DictReader(csvfile, delimiter =";")
        motProgress = calcMotivationVar(progress)
        modules.append(motProgress)

    with open('./R Code/PLS/Hexad/rankingPathCoefs.csv', newline='') as csvfile:
        ranking = csv.DictReader(csvfile, delimiter =";")
        motRanking = calcMotivationVar(ranking)
        modules.append(motRanking)

    with open('./R Code/PLS/Hexad/scorePathCoefs.csv', newline='') as csvfile:
        score = csv.DictReader(csvfile, delimiter =";")
        motScore = calcMotivationVar(score)
        modules.append(motScore)
    
    with open('./R Code/PLS/Hexad/timerPathCoefs.csv', newline='') as csvfile:
        timer = csv.DictReader(csvfile, delimiter =";")
        motTimer = calcMotivationVar(timer)
        modules.append(motTimer)

    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";")
        
        idRow = 0
        modulePref = [0] * 6 # ["avatar", "badges", "progress", "rank", "score", "timer"]

        for row in students:
            if idRow == idStudent:
                for i in range(len(modules)) :
                    modulePref[i] += float(row['achiever']) * modules[i][0]
                    modulePref[i] += float(row['player']) * modules[i][1]
                    modulePref[i] += float(row['socialiser']) * modules[i][2]
                    modulePref[i] += float(row['freeSpirit']) * modules[i][3]
                    modulePref[i] += float(row['disruptor']) * modules[i][4]
                    modulePref[i] += float(row['philanthropist']) * modules[i][5]
                break
            idRow += 1

        print(modulePref)

        # Find the best
        indexMax = 0

        for i in range(len(modulePref)):
            if modulePref[i] > modulePref[indexMax]:
                indexMax = i

        print("Le module le plus adapte au profil HEXAD l'etudiant " + str(idStudent) + " semble etre le module '" + 
                moduleName.get(indexMax) + "' avec un score d'affinite de " + str(modulePref[indexMax]) + ".")



    