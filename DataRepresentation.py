'''
Data Representation
for converting specific types of data to strings for printing to a console
-PaiShoFish49
'''

class Shapes():
    @staticmethod
    def box(peice):
        '''
        ┌─┬┐
        │ ││
        ├─┼┤
        └─┴┘
        '''
        return


def arrayToString(inputArray, horizontal: bool = True):
    retStr = ""
    inputAsStrings = [str(i) for i in inputArray]

    if horizontal:
        totalLength = 

    maxLength = max(inputAsStrings, key = lambda x: len(x))