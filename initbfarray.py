import re
import json

def findPrimeFactors(num):
    if num == 1:
        return (1,)

    pfacs = []
    i = 2
    while(i <= num):
        while(num % i == 0):
            num //= i
            pfacs.append(i)
        i += 1

    return pfacs

def getSmallestFactors(pfacs):
    if pfacs == []:
        return (0,)

    a, b = 1, 1
    pfacs = sorted(pfacs, reverse = True)
    for i in pfacs:
        if a > b:
            b *= i
        else:
            a *= i

    if b == 1:
        return (a,)

    return a, b

if False:
    allPaths = []
    for i in range(256):
        currentPath = getSmallestFactors(findPrimeFactors(i))
        currentPathSum = sum(currentPath)

        allPaths.append((i, currentPath, currentPathSum))

    adjustedPaths = []
    for i in allPaths:
        tempAll = []
        for j in allPaths:
            cost = j[2] + abs(i[0] - j[0]) + (7 if len(j[1]) == 2 else 0)
            tempAll.append((j[0], j[1], cost))

        lowestCost = 1000
        lowestCostInd = 0
        for j in range(len(tempAll)):
            if tempAll[j][2] < lowestCost:
                lowestCost = tempAll[j][2]
                lowestCostInd = j

        adjustedPaths.append((tempAll[lowestCostInd][0], tempAll[lowestCostInd][1], tempAll[lowestCostInd][2]))

    finalPaths = []
    for i in range(len(adjustedPaths)):
        comp = 255-i
        if (adjustedPaths[comp][2] + 1) < adjustedPaths[i][2]:
            finalPaths.append((True, adjustedPaths[comp][0], adjustedPaths[comp][1], (adjustedPaths[comp][2] + 1)))
        else:
            finalPaths.append((False, adjustedPaths[i][0], adjustedPaths[i][1], adjustedPaths[i][2]))

    strings = []
    for i, j in enumerate(finalPaths):
        curPath = j[2]
        if j[0] == True:
            addon = (255 - j[1]) - i
            if addon < 0:
                addStr = '+'
                addon = abs(addon)
            else:
                addStr = '-'

            if len(j[2]) == 1:
                apStr = f'-{'-'*j[2][0]}{addStr*addon}'
            else:
                apStr = f'->{'+'*j[2][0]}[<{'-'*j[2][1]}>-]<{addStr*addon}'

        else:
            addon = i - j[1]
            if addon < 0:
                addStr = '-'
                addon = abs(addon)
            else:
                addStr = '+'

            if len(j[2]) == 1:
                apStr = f'{'+'*j[2][0]}{addStr*addon}'
            else:
                apStr = f'>{'+'*j[2][0]}[<{'+'*j[2][1]}>-]<{addStr*addon}'

        strings.append(apStr)

    for i in range(len(strings)):
        print(i, strings[i])

    with open('results.json', 'w') as file:
        json.dump(strings, file, indent=4)

else:
    with open('results.json', 'r') as file:
        strings = json.load(file)

    # strings = sorted(strings, key=(lambda x: len(x)))
    # print(len(strings[-1]))

    if input('use string? >>').lower() in ('y', 'yes', 'true', 't'):
        encode = [ord(i) for i in input('>>')]
    else:
        encode = [int(i) for i in input('>>').replace(' ', '').split(',')]

    finalString = ''
    for i, j in enumerate(encode):
        curString: str = strings[j]

        if (i + 1) < len(encode):
            if curString.endswith('<'):
                curString = curString[:-1]
            else:
                curString += '>'

        curString = curString.ljust(35)
        curString += f'load {j}\n'
        finalString += curString

    finalString += ('<' * (len(encode)-1)) + '  reset to 0'

print(finalString)