import csv

def getStudentWithGoodElement():
    studentsDict = dict() # {idStudent : "GoodElement"}

    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";") 

        idStudent = 0

        for row in students:
            if float(row['Time'].split(":")[0]) >= 1:
                questionRatio = float(row['CorrectCount']) / float(row['QuestionCount'])
                if questionRatio >= 0.60:
                    MIVar = (float(row[' micoVar']) + float(row[' miacVar']) + float(row[' mistVar']))
                    MEVar = (float(row[' meidVar']) + float(row[' meinVar']) + float(row[' mereVar']))
                    varMotGlobal = MIVar + MEVar - float(row[' amotVar']) 
                    if varMotGlobal >= 0:
                        studentsDict[idStudent] = row['GameElement']
            idStudent += 1

    return studentsDict

def getStudentWithBadElement():
    studentsDict = dict() # {idStudent : "GoodElement"}

    with open('./userStats.csv', newline='') as csvfile:
        students = csv.DictReader(csvfile, delimiter =";") 

        idStudent = 0

        for row in students:
            if float(row['Time'].split(":")[0]) < 1:
                questionRatio = float(row['CorrectCount']) / float(row['QuestionCount'])
                if questionRatio < 0.60:
                    MIVar = (float(row[' micoVar']) + float(row[' miacVar']) + float(row[' mistVar']))
                    MEVar = (float(row[' meidVar']) + float(row[' meinVar']) + float(row[' mereVar']))
                    varMotGlobal = MIVar + MEVar - float(row[' amotVar']) 
                    if varMotGlobal < 0:
                        studentsDict[idStudent] = row['GameElement']
            idStudent += 1

    return studentsDict