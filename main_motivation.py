# Load all csv
import csv
import copy

if __name__ == "__main__":

    csv_root = './Motivation/'

    csv_path = [
        'avatarPathCoefs.csv',
        'badgesPathCoefs.csv',
        'progressPathCoefs.csv',
        'rankingPathCoefs.csv',
        'scorePathCoefs.csv',
        'timerPathCoefs.csv'
    ]

    mat = dict()

    for path in csv_path:
        with open(csv_root + path, newline='') as csv_file:
            content = csv.reader(csv_file, delimiter=';')
            ME_sum = 0
            MI_sum = 0
            amot_sum = 0
            first = True
            for row in content:
                if first:
                    first = False
                else:
                    ME_sum += float(row[1])
                    MI_sum += float(row[2])
                    amot_sum -= float(row[3])

        mat[path] = [ME_sum / 3, MI_sum / 3, amot_sum / 3]

    best_module_ME = ["", None]
    best_module_MI = ["", None]
    best_module_amot = ["", None]

    for m in mat.keys():
        value = mat[m]
        print(m, value)
        if best_module_ME[1] is None or value[0] > best_module_ME[1]:
            best_module_ME = [m, value[0]]
        if best_module_MI[1] is None or value[1] > best_module_MI[1]:
            best_module_MI = [m, value[1]]
        if best_module_amot[1] is None or value[2] > best_module_amot[1]:
            best_module_amot = [m, value[2]]

    print("best ME:", best_module_ME)
    print("best MI:", best_module_MI)
    print("best amot:", best_module_amot)

