class Fraction:
    def __init__(self, numerator, denominator) -> None:
        if not isinstance(numerator, int):
            raise Exception("numerator must be of type int")
        if not isinstance(denominator, int):
            raise Exception("denominator must be of type int")
        if denominator == 0:
            raise Exception("Denominator cannot be assigned a zero value")
        self.numerator = numerator
        self.denominator = denominator
        self.__reduce()

    def __str__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return str(self.numerator) + "/" + str(self.denominator)

    def __eq__(self, __o: object) -> bool:
        return self.numerator == __o.numerator and self.denominator == __o.denominator

    def __add__(self, __o:object): return Fraction.add(self, __o)

    def __mul__(self, __o:object): return Fraction.multiply(self, __o)
        
    __rmul__ = __mul__

    
    @staticmethod
    def add(frac1, frac2):
        if frac1 == Fraction.__zero():
            return frac2
        if frac2 == Fraction.__zero():
            return frac1
        
        num = frac1.numerator * frac2.denominator + frac2.numerator * frac1.denominator
        den = frac1.denominator * frac2.denominator
        return Fraction(num, den)

    @staticmethod
    def multiply(frac1, frac2):
        num = frac1.numerator * frac2.numerator
        den = frac1.denominator * frac2.denominator
        return Fraction(num, den)

    @staticmethod
    def negate(frac): return Fraction(frac.numerator * -1, frac.denominator)

    @staticmethod
    def from_int(n): return Fraction(n,1)

    @staticmethod
    def from_float(d): return Fraction.to_fraction(d)

    # The function takes an string as an argument and returns its corresponding reduced fraction
    # the string can be an in the form of and integer, double or fraction:
    # like "123" or "123.321" or "123/456"
    @staticmethod
    def from_string(str):
        ix = 0
        for c in str:
            if c == '/':
                break
            else:
                ix+=1
        if ix == len(str):
            return Fraction.from_float(float(str))
        else:
            return Fraction(int(str[0:ix]), int(str[ix+1:]))


        pass

    @staticmethod
    def to_fraction(d):
        if not isinstance(d, float):
            raise Exception("to_fraction requires float argument")
        if  d % 1 == 0.0:
            return Fraction.from_int(int(d))

        d_tmp = d
        multiple = 1
        str_tmp = str(d)
        while 'E' in str_tmp: # if in the form like 12E-9
            d_tmp *= 10
            multiple *= 10
            str_tmp = str(d_tmp)
        i = 0
        while str_tmp[i] != '.':
            i+=1
        digits_after_decimal = len(str_tmp)-i-1
        while digits_after_decimal > 0:
            d_tmp *=10
            multiple *=10
            digits_after_decimal -=1
        return Fraction(int(d_tmp), multiple)

    def __reduce(self):
        if self.numerator == 0:
            self.denominator = 1
        else:
            gcd = Fraction.__gcd(self.numerator, self.denominator)
            self.numerator //= gcd
            self.denominator //= gcd

            if self.denominator < 0:
                self.numerator *= -1
                self.denominator *= -1
            
    @staticmethod
    def __gcd(n1, n2):
        if n1 < 0:
            n1 *= -1
        if n2 < 0:
            n2 *= -1
        
        while True:
            if n1<n2:
                n1,n2 = n2,n1

            n1 = n1 % n2
            if n1 == 0:
                break
        return n2

    @staticmethod
    def __lcm(m, n):
        if m < 0:
            m *= -1
        if n < 0:
            n *= -1
        return m * (n // Fraction.__gcd(m,n)) # parentheses important to avoid overflow if working whith fixed length ints
    
    @staticmethod
    def __zero(): return Fraction(0,1)

    def copy(self): return Fraction(self.numerator, self.denominator)


def main():
    f1 = Fraction(2,4)
    f2 = Fraction.from_float(317.128923872386248)
    f3 = Fraction.from_string("2/8")


    print(f1)
    print(f2)
    print(f3)
    print(f1 == f3+f3)
    print(f1*f1 == f3)
    print(f1*f2*f3)
   
if __name__ == "__main__":
    main()