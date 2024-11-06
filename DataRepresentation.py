'''
Data Representation
for converting specific types of data to strings for printing to a console
-PaiShoFish49
'''

'''
┌─┬─┐  ╔═╦═╗  ╭─╮
│ │ │  ║ ║ ║  │ │
├─┼─┤  ╠═╬═╣  │ │
└─┴─┘  ╚═╩═╝  ╰─╯
'''
box = {
    'sh': '─', 'sv': '│', 'sm': '┼',
    'sl': '├', 'sr': '┤', 'st': '┬', 'sb': '┴',
    'stl': '┌', 'str': '┐', 'sbl': '└', 'sbr': '┘',

    'dh': '═', 'dv': '║', 'dm': '╬',
    'dl': '╠', 'dr': '╣', 'dt': '╦', 'db': '╩',
    'dtl': '╔', 'dtr': '╗', 'dbl': '╚', 'dbr': '╝',

    'ctl': '╭', 'ctr': '╮', 'cbl': '╰', 'cbr': '╯'
}

def vizDataToString(data, stringify = True):
    if isinstance(data, str) and stringify:
        return '"' + data + '"'
    else:
        return str(data)

def arrayToString(inputArray, horizontal: bool = True):
    retStr = ''
    inputAsStrings = [vizDataToString(i) for i in inputArray]

    if horizontal:
        topStr = box['dtl']
        middleStr = box['dv']
        for i in inputAsStrings:
            topStr += box['dh'] * (len(i) + 2)
            topStr += box['dt']
            middleStr += f' {i} {box['dv']}'

        topStr = topStr[:-1] + box['dtr']
        retStr = topStr + '\n' + middleStr + '\n' + topStr.replace(box['dtl'], box['dbl']).replace(box['dt'], box['db']).replace(box['dtr'], box['dbr'])

    else:
        longest = max(inputAsStrings, key = len)
        retStr += box['dtl'] + (box['dh'] * (longest + 2)) + box['dtr'] + '\n'
        for i, j in enumerate(inputAsStrings):
            retStr += f'{box['dh']} {j} {box['dh']}\n'
            if i + 1 < len(inputAsStrings):
                retStr += box['dl'] + (box['h'] * (longest + 2)) + box['dr'] + '\n'
        retStr += box['dbl'] + (box['dh'] * (longest + 2)) + box['dbr']

    return retStr

def bytesToBraille(data: bytearray):
    retStr = ''
    for i in data:
        retStr += chr(0x2800 + i) + ' '
    return retStr

with open('Apollonius.py', 'br') as file:
    print(bytesToBraille(bytearray(file.read())))