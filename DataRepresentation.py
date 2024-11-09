'''
Data Representation
for converting specific types of data to strings for printing to a console
-PaiShoFish49
'''

import math

'''
┌─┬─┐  ╔═╦═╗  ╭─┴─╮       ╭┴┴┴┴┴╮ ┴┴┴┴┴┬┴┴┴┴┴╬╬
│ │ │  ║ ║ ║  ┤   ├     ┼┼┤ ╬ ╬ ├┼┼    ├──────╬╬╬╬
├─┼─┤  ╠═╬═╣  ┤   ├       ╰─────╯ ─────╯
└─┴─┘  ╚═╩═╝  ╰─┬─╯        ┼   ┼    ┼ ┼
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

def arrayToString(inputArray: list, horizontal: bool = True):
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

def gridToString(inputGrid: list[list]):
    retStr = ''
    longest = 0
    inputAsStrings = []
    for x in inputGrid:
        row = []
        for y in x:
            row.append(str(y))
            if len(str(y)) > longest:
                longest = len(str(y))
        inputAsStrings.append(row)

    retStr += box['dtl'] + (((box['dh'] * (longest + 2)) + box['dt']) * len(inputGrid[0]))[:-1] + box['dtr'] + '\n'

    for xi, x in enumerate(inputAsStrings):
        row = box['dv']
        for y in x:
            row += f' {y} {box['dv']}'

        retStr += row + '\n'

        if xi + 1 < len(inputAsStrings):
            retStr += box['dl'] + (((box['dh'] * (longest + 2)) + box['dm']) * len(inputGrid[0]))[:-1] + box['dr'] + '\n'
        else:
            retStr += box['dbl'] + (((box['dh'] * (longest + 2)) + box['db']) * len(inputGrid[0]))[:-1] + box['dbr']

    return retStr

def chessToString(fen: str):
    # input chess notation in Forsyth-Edwards Notation
    boardStr, _, _, _, _, _ = fen.split()
    boardList = [['#', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
    row = [1]
    rowInd = 2
    boxInd = 0
    for i in boardStr:
        if i == '/':
            boardList.append(row)
            row = [rowInd]
            rowInd += 1
        elif i.isdecimal():
            for j in range(int(i)):
                row.append("#" if boxInd % 2 == 1 else ' ')
                boxInd += 1
        else:
            row.append({
                'K': '♔', 'k': '♚',
                'Q': '♕', 'q': '♛',
                'B': '♗', 'b': '♝',
                'N': '♘', 'n': '♞',
                'R': '♖', 'r': '♜',
                'P': '♙', 'p': '♟'
            }[i])
            boxInd += 1
    boardList.append(row)

    return gridToString(boardList[::-1])

def bytesToBraille(data: bytearray):
    retStr = ''
    for i in data:
        retStr += chr(0x2800 + i) + ' '
    return retStr

