from fractions import Fraction
import math

def triangle(num):
    return int(num * (num + 1) / 2)

def antiTri(num):
    return (math.sqrt((8 * num) + 1) - 1) / 2

def rationalToInteger(fraction: Fraction):
    if fraction.numerator == 0:
        return 0

    sign = 1
    if fraction.numerator < 0:
        sign = -1
        fraction = abs(fraction)
    fracRat = fraction.as_integer_ratio()

    if fracRat[0] == 1:
        return triangle(fracRat[1])

    numOnDenom = 0
    for i in range(fracRat[0]):
        if Fraction(i+1, fracRat[1]).as_integer_ratio() == (i+1, fracRat[1]):
            numOnDenom += 1

    return (triangle(fracRat[1] + numOnDenom - 2) + fracRat[1]) * sign

def integerToRational(integer: int):
    if integer == 0:
        return Fraction(0, 1)

    sign = 1
    if integer < 0:
        integer = abs(integer)
        sign = -1

    section = math.floor(antiTri(integer))
    unit = integer - triangle(section)

    if unit == 0:
        return Fraction(sign, section)

    numOnDenom = section - unit + 2
    numerator = 0
    for i in range(numOnDenom):
        numerator += 1
        while Fraction(numerator, unit).as_integer_ratio() != (numerator, unit):
            numerator += 1

    return Fraction(numerator * sign, unit)