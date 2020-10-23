from stdnum import iso6346
import re

def checkDigitNum(text):
    number =  text
    num = number[0:-1]
    dig = number[-1]
    # csqu3054383
    test1 = iso6346.calc_check_digit(num)
    
    return 'valid' if test1 == dig else 'not valid'