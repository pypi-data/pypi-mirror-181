# allways_truncate specifies whether the significant digits should be truncated to the given precision after each operation
class BigDecimal:
    __PRECISION = 50

    def __init__(self, mantissa, exponent, precision=__PRECISION, allways_truncate = False) -> None:
        self.precision = precision
        self.allways_truncate = allways_truncate
        self.__mantissa = mantissa
        self.__exponent = exponent

    @staticmethod
    def from_number(val, prec = 50):
        if isinstance(val, int):
            return BigDecimal(val, 0, prec)
        elif isinstance(val, float):
            mantissa = int(val)
            exponent = 0
            scalefactor = 1
            while abs(val*scalefactor - mantissa) > 0:
                exponent -=1
                scalefactor *=10
                mantissa = int(val * scalefactor)

            return BigDecimal(mantissa, exponent, prec)

    def to_float(self):
        return self.__mantissa * pow(10, self.__exponent)

    def __str__(self) -> str:
        self.normalize()
        # rec = self.__is_recurring()
        return str(self.__mantissa) + "E" + str(self.__exponent)

    def __is_recurring(self):
        man = str(self.__mantissa)[1:]
        for i in range(1,BigDecimal.__PRECISION // 2):
            substring = man[:i]
            for j in range(i,BigDecimal.__PRECISION // 2):
                if substring != man[j+i:j+i*2]:
                    break
            return i
        return -1



    # removes trailing zeros on the mantissa
    def normalize(self):
        if self.__mantissa == 0:
            self.__exponent = 0
        else:
            reminder = 0
            while reminder == 0:
                shortened, reminder = divmod(self.__mantissa,10)
                if reminder == 0:
                    self.__mantissa = shortened
                    self.__exponent +=1


    # Truncate the number to the given precision by removing the least significant digits
    def truncate(self, precision:int):
        d = self.copy()
        d.normalize()
        while BigDecimal.number_of_digits(d.__mantissa) > precision:
            d.__mantissa //= 10
            d.__exponent +=1
        return d

    
    @staticmethod
    def number_of_digits(n): return len(str(BigDecimal.sign(n)*n))

    sign = lambda x: copysign(1,x)

    @staticmethod
    def align_exponent(value, reference):
        return value.__mantissa * pow(10, value.__exponent - reference.__exponent)

    @staticmethod
    def negate(bigdecimal):
        bigdecimal.__mantissa *= -1
        return bigdecimal

    @staticmethod
    def add(left, right): 
        if left.__exponent > right.__exponent:
            return BigDecimal(BigDecimal.align_exponent(left, right) + right.__mantissa, right.__exponent)
        else:
            return BigDecimal(BigDecimal.align_exponent(right, left) + left.__mantissa, left.__exponent)

    @staticmethod
    def subtract(left, right): return BigDecimal.add(left, BigDecimal.negate(right))

    @staticmethod
    def mult(left, right): return BigDecimal(left.__mantissa * right.__mantissa, left.__exponent + right.__exponent) 

    @staticmethod
    def divide(dividend, divisor):
        tmp = dividend.copy()
        prec = dividend.precision if dividend.precision <= divisor.precision else divisor.precision
        exponent_change = prec - (BigDecimal.number_of_digits(dividend.__mantissa) - BigDecimal.number_of_digits(divisor.__mantissa))
        if exponent_change < 0:
            exponent_change = 0
        tmp.__mantissa *= pow(10, exponent_change)
        return BigDecimal(tmp.__mantissa // divisor.__mantissa, tmp.__exponent - divisor.__exponent - exponent_change, prec)


    @staticmethod
    def exp(exponent):
        tmp = BigDecimal.from_number(1)
        while abs(exponent) > 100:
            diff = 100 if exponent > 0 else -100
            tmp = BigDecimal.mult(tmp, exp(diff))
            exponent -= diff
        return BigDecimal.mult(tmp,pow(exponent))

    @staticmethod
    def pow(basis, exponent):
        tmp = BigDecimal.from_number(1)
        while abs(exponent) > 100:
            diff = 100 if exponent > 0 else -100
            tmp = BigDecimal.mult(tmp, pow(basis,diff))
            exponent -= diff
        return BigDecimal.mult(tmp,pow(basis, exponent))

    def copy(self):
        d = BigDecimal(self.precision, self.allways_truncate)
        d.__exponent = self.__exponent
        d.__mantissa = self.__mantissa
        return d

 