import bestModuleProfilMot as mot
import bestModuleProfilHexad as hexad
from collections import OrderedDict
import csv
import test as test

def recommandModule(idStudent):
    vecTmpH, modulesH = hexad.bestModuleProfilHexad(idStudent)
    vecTmpM, modulesM = mot.bestModuleProfilMot(idStudent)

    vecAffinityHexad = OrderedDict(sorted(vecTmpH.items(), key=lambda t: t[1]))
    vecAffinityMot = OrderedDict(sorted(vecTmpM.items(), key=lambda t: t[1]))
    recommandationHexad = next(reversed(vecAffinityHexad.items()))
    recommandationMot = next(reversed(vecAffinityMot.items()))   

    #Si les 2 recommandations sont les mêmes
    if recommandationHexad[0] == recommandationMot[0]:
        return vecAffinityHexad
    else:
        dictAvgRank = dict()
        rankHexad = 6
        for tH in vecAffinityHexad:
            rankMot = 6
            for tM in vecAffinityMot:
                if tM == tH:
                    avgRank = (rankMot + rankHexad) / 2
                    dictAvgRank[tM] = avgRank
                    break
                rankMot -= 1
            rankHexad -= 1

        dictAvgRank = sorted(dictAvgRank.items(), key=lambda t: t[1])
        bestModuleAvgRank = dictAvgRank[0]
        secondBestModuleAvgRank = dictAvgRank[1]
        if (bestModuleAvgRank[1] - secondBestModuleAvgRank[1]) >= 1:
            return dictAvgRank
        else:
            domHexad, domMot = dominante(idStudent)
            if domHexad is None or domMot is None:
                return dictAvgRank
            else: 
                affDomHexadBest = hexad.affinityDominance(idStudent, domHexad, bestModuleAvgRank, modulesH)
                affDomHexadSecondBest = hexad.affinityDominance(idStudent, domHexad, secondBestModuleAvgRank, modulesH)

                affDomMotBest = mot.affinityDominance(idStudent, domMot, bestModuleAvgRank, modulesM)
                affDomMotSecondBest = mot.affinityDominance(idStudent, domMot, secondBestModuleAvgRank, modulesM)

                avgBest = (affDomHexadBest + affDomMotBest) / 2
                avgSecond = (affDomMotSecondBest + affDomHexadSecondBest) / 2

                if avgBest > avgSecond:
                    return dictAvgRank
                else:
                    dictAvgRank[0] = secondBestModuleAvgRank
                    dictAvgRank[1] = bestModuleAvgRank
                    return dictAvgRank

def dominante(idStudent):
    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";")
        
        idRow = 0
        vecAff = [0] * 6

        for row in students:
            if idRow == idStudent:
                hexad = dict()
                hexad['achiever'] = row['achiever']
                hexad['player'] = row['player']
                hexad['socialiser'] = row['socialiser']
                hexad['freeSpirit'] = row['freeSpirit']
                hexad['disruptor'] = row['disruptor']
                hexad['philanthropist'] = row['philanthropist']

                mot = dict()
                mot['MI'] = float(row['micoI']) + float(row[' miacI']) + float(row[' mistI'])
                mot['ME'] = float(row[' meidI']) + float(row[' meinI']) + float(row[' mereI'])
                amotI = float(row[' amotI'])

                bestHexad = 'achiever'
                for i in hexad:
                    if float(hexad[i]) >= float(hexad[bestHexad]):
                        bestHexad = i
                
                bestMot = 'MI'
                for i in mot:
                    if float(mot[i]) >= float(mot[bestMot]):
                        bestMot = i

            idRow += 1

    # On regarde si'l y a une réel dominance
    for i in hexad:
        if i != bestHexad:
            if float(hexad[bestHexad]) - 3 < float(hexad[i]):
                return None, None

    for i in mot:
        if i != bestMot:
            if float(mot[bestMot]) - 10 < float(mot[i]):
                return None, None
    
    if float(hexad[bestHexad]) >= 8 and float(mot[bestMot]) >= 45: 
        return bestHexad, bestMot
    else:
        return None, None

def displayDictMotAndHexad(dictA):
    if isinstance(dictA, dict):
        displayDict(dictA)
    else :
        for i in range(len(dictA)):
            print(str(len(dictA) - i) + ") " + dictA[len(dictA) - i - 1][0] + " " + str(dictA[len(dictA) - i - 1][1]))

def displayDict(dictA):
    i = 6
    for a in dictA:
        print(str(i) + ") " + a + " " + str(dictA.get(a)))
        i -= 1

if __name__ == "__main__":
    moduleName = {0: "avatar", 1: "badges", 2: "progress", 3: "rank", 4: "score", 5: "timer"}

    goodElement = test.getStudentWithGoodElement()
    badElement = test.getStudentWithBadElement()

    nbGoodStudent = 0

    avgGoodRecommandationHexad = 0
    avgGoodRecommandationMot = 0
    avgGoodRecommandationMotAndHexad = 0
    for student in goodElement:
        element = goodElement.get(student)
        recommandationHexad, _ = hexad.bestModuleProfilHexad(student)
        recommandationHexad = OrderedDict(sorted(recommandationHexad.items(), key=lambda t: t[1]))
        recommandationMot, _ = mot.bestModuleProfilMot(student)
        recommandationMot = OrderedDict(sorted(recommandationMot.items(), key=lambda t: t[1]))
        recommandationMotAndHexad = recommandModule(student)

        i = 6
        for m in recommandationMot:
            if m == element:
                avgGoodRecommandationMot += i
                break
            i -= 1

        i = 6
        for m in recommandationHexad:
            if m == element:
                avgGoodRecommandationHexad += i
                break
            i -= 1

        if isinstance(recommandationMotAndHexad, dict):
            i = 6
            for m in recommandationMotAndHexad:
                if m == element:
                    avgGoodRecommandationMotAndHexad += i
                    break
                i -= 1
        else :
            for i in range(len(recommandationMotAndHexad)):
                if recommandationMotAndHexad[len(recommandationMotAndHexad) - i - 1][0] == element:
                    avgGoodRecommandationMotAndHexad += len(recommandationMotAndHexad) - i
                    break
        
        nbGoodStudent += 1

    avgGoodRecommandationHexad /= nbGoodStudent
    avgGoodRecommandationMot /= nbGoodStudent
    avgGoodRecommandationMotAndHexad /= nbGoodStudent

    print("----------------Conclusion-----------------")
    print("Sur " + str(nbGoodStudent) + " qui ont eu un element adapte a leur profil, en moyenne notre algorithme utilisant uniquement le "+ 
                "profil Motivation recommande l'element adapte au rang " + str(avgGoodRecommandationMot) +".")

    print("Sur " + str(nbGoodStudent) + " qui ont eu un element adapte a leur profil, en moyenne notre algorithme utilisant uniquement le "+ 
                "profil HEXAD recommande l'element adapte au rang " + str(avgGoodRecommandationHexad) +".")

    print("Sur " + str(nbGoodStudent) + " qui ont eu un element adapte a leur profil, en moyenne notre algorithme utilisant le "+ 
                "profil Motivation et le profil Hexad recommande l'element adapte au rang " + str(avgGoodRecommandationMotAndHexad) +".")

    #####################################################################################################

    nbBadStudent = 0

    avgBadRecommandationHexad = 0
    avgBadRecommandationMot = 0
    avgBadRecommandationMotAndHexad = 0
    for student in badElement:
        element = badElement.get(student)
        recommandationHexad, _ = hexad.bestModuleProfilHexad(student)
        recommandationHexad = OrderedDict(sorted(recommandationHexad.items(), key=lambda t: t[1]))
        recommandationMot, _ = mot.bestModuleProfilMot(student)
        recommandationMot = OrderedDict(sorted(recommandationMot.items(), key=lambda t: t[1]))
        recommandationMotAndHexad = recommandModule(student)
        #print("Pour l'eleve " + str(student + 1) + " les meilleurs modules selon son profil Motivation sont les suivants :")
        #displayDict(recommandationMot)
        #print("Pour l'eleve " + str(student + 1) + " les meilleurs modules selon son profil HEXAD sont les suivants :")
        #displayDict(recommandationHexad)
        #print("Pour l'eleve " + str(student + 1) + " les meilleurs modules selon son profil HEXAD et Motivation sont les suivants :")
        #displayDictMotAndHexad(recommandationMotAndHexad)
        #print("L'element qui a marche lors de l'experimentation est " + element)

        i = 6
        for m in recommandationMot:
            if m == element:
                avgBadRecommandationMot += i
                break
            i -= 1

        i = 6
        for m in recommandationHexad:
            if m == element:
                avgBadRecommandationHexad += i
                break
            i -= 1

        if isinstance(recommandationMotAndHexad, dict):
            i = 6
            for m in recommandationMotAndHexad:
                if m == element:
                    avgBadRecommandationMotAndHexad += i
                    break
                i -= 1
        else :
            for i in range(len(recommandationMotAndHexad)):
                if recommandationMotAndHexad[len(recommandationMotAndHexad) - i - 1][0] == element:
                    avgBadRecommandationMotAndHexad += len(recommandationMotAndHexad) - i
                    break
        
        nbBadStudent += 1

    avgBadRecommandationHexad /= nbBadStudent
    avgBadRecommandationMot /= nbBadStudent
    avgBadRecommandationMotAndHexad /= nbBadStudent

    print("----------------Conclusion-----------------")
    print("Sur " + str(nbBadStudent) + " qui n'ont pas eu un element adapte a leur profil, en moyenne notre algorithme utilisant uniquement le "+ 
                "profil Motivation recommande l'element non adapte au rang " + str(avgBadRecommandationMot) +".")

    print("Sur " + str(nbBadStudent) + " qui n'ont pas eu un element adapte a leur profil, en moyenne notre algorithme utilisant uniquement le "+ 
                "profil HEXAD recommande l'element non adapte au rang " + str(avgBadRecommandationHexad) +".")

    print("Sur " + str(nbBadStudent) + " qui n'ont pas eu un element adapte a leur profil, en moyenne notre algorithme utilisant le "+ 
                "profil Motivation et le profil Hexad recommande l'element non adapte au rang " + str(avgBadRecommandationMotAndHexad) +".")
