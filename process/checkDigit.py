from stdnum import iso6346
import re

def checkDigitNum(text):
<<<<<<< HEAD
    try:
        number =  text
        num = number[0:-1]
        dig = number[-1]
        # csqu3054383
        test1 = iso6346.calc_check_digit(num)
        
        return 'valid' if test1 == dig else 'not valid'
    except TypeError:
        return 'not valid'
=======
    number =  text
    num = number[0:-1]
    dig = number[-1]
    # csqu3054383
    test1 = iso6346.calc_check_digit(num)
    
    return 'valid' if test1 == dig else 'not valid'
>>>>>>> b75979ed493d7f8bfa25ba2180190d6f3a72020f
