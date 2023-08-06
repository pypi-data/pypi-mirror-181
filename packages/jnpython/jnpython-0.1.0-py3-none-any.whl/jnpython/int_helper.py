from functools import reduce
import math
import multiprocessing
import random
from math import ceil, copysign, isqrt, sqrt
from sorting import q_sort

_rand = random.SystemRandom()

def sign(x): return copysign(1,x)

# concat 10 11 returns 1011
def concat(a, b):
    c = b
    while c > 0:
        a *= 10
        c //= 10
    return a + b
        
def bitlength(n):
    if n == 0:
        return 1
    nbits = 0
    while n != 0:
        nbits+=1
        n //=2
    return nbits

# Greatest Common Divisor (a.k.a. gcd, gcf, hcf, gcm, sgd)
def gcd(a, b):
        while b != 0:
            a,b = b, a%b
        return a

# Least Common Multiple
def lcm(a, b): return (a*b) // gcd(a,b)

def are_relatively_prime(a,b) -> bool:
    while True:
        a %=b
        if a == 0:
            return b == 1
        b %= a
        if b == 0:
            return a == 1

#################### COMBINATORICS ####################

# binom(n,r) = (n "over" r) or "choose r from n" = n!/(r!*(n-r)!)
def binom(n, r):
    if n < r:
        return 0
    elif n == r:
        return 1
    if r > n -r:
        r = n-r
    ret = 1
    for i in range(r):
        ret = ret * (n-i)//(i+1)
    return ret

# pick/choose (permutation = ordered combination)
def combinations(n, r, with_repetition:bool):
    if with_repetition: # n+r-1 over k = (n+k-1)! / k!(n-1)!
        return binom(n+r-1,r)
    else: # n! / k!(n-k)! = n over r = n over n-r
        return binom(n, r)

# arrange or arrange and pick when k!=n (variation). N is the number of things to choose from, and we choose k of them
def permutations(n, k, with_repetition:bool):
    if with_repetition: # n^k
        return pow(n,k) # n possibilities for the first choice, n possibilites for the second choice etc.
    else: #n! /(n-k)!
        res = 1
        for i in range(k):
            res *=n-i # n possibilities for the first choice,  n-1 possibilites for the second choice etc.
        return res

#################### MODULAR ARITHMETIC ####################

# Euler's totient function
# Number of positive integers less than or equal to n that are relatively prime to n
def phi(n, primes_limit = None):
    if n < 1:
        raise Exception("Euler's totient function is not defined for n < 1")
    elif n <= 2:
        return 1
    elif is_prime(n):
        return n-1
    
    phi = n
    i = 0
    ps = primes_sieve(primes_limit if primes_limit is not None else n)
    p = ps[0]
    while i <= len(ps) and p*p <=n:
        if n%p == 0:
            phi = phi - phi//p
            while n%p == 0:
                n = n//p
        i+=1
        p = ps[i]
    if n>1:
        phi = phi - phi //n
    return phi

def phi_sieve(exclusive_max)->list:
    phis = [n for n in range(0,exclusive_max)]
    for n in range(2,exclusive_max):
        if phis[n] == n: # n is a prime, for all multiples of n multiply with (1-1/n)
            m = n
            while m < exclusive_max:
                phis[m] = phis[m] - phis[m]//n
                m += n
    return phis

# compute (a * b) % mod
def mul_mod(a,b,mod):
    while a < 0:
        a+=mod
    while b < 0:
        b+=mod
    res = 0
    a %= mod
    while b > 0:
        if b%2 == 1:
            t = (res+a)%mod
            res = t
        t2 = a*2 % mod
        a = t2
        b //=2
    return res % mod

# modular multiplicative inverse
def mod_inverse(a, mod):
    dividend = a%mod
    divisor = mod
    last_x = 1
    curr_x = 0
    while divisor > 0:
        quotient = dividend // divisor
        remainder = dividend % divisor
        if remainder <= 0:
            break
        next_x = last_x - curr_x * quotient
        last_x = curr_x
        curr_x = next_x
        dividend = divisor
        divisor = remainder

    if divisor != 1:
        raise Exception("Numbers a and b are not relatively primes")

    return curr_x + mod if sign(curr_x) < 0 else curr_x

# Modular multiplicative inverse
def inverse_modulo(a, mod):
    ans = None
    for i in range(mod-1):
        if (a*i) % mod == 1:
            ans = i
            break
    return ans

# nThRoot=2 >= sqRoot
def modular_root(a, n, nth_root = 2):
    if n % 4 == 3 and nth_root == 2:
        return pow(a,(n+1)//4)%n
    elif is_prime(n) and gcd(nth_root, n-1)==1: # the "easy case".
        return pow(a, inverse_modulo(nth_root, n)) % n
    elif is_prime(n):
        for i in range(n):
            if pow(i, nth_root) % n == a:
                return i
        return None
    else:
        return None # factor n and work from there...

# a*x^2+bx+c=d in Zn
def quad_solve_modulo(a ,b ,c, d, n):
    x0 = None
    x1 = None
    c = c-d
    # res: x = (-b +- srt(b^2-4ac) / 2a
    i = inverse_modulo(2*a,n)
    j = pow(b,2)-4*a*c
    k = modular_root(j, n)
    if k is not None:
        x0 = to_normal_modular_form((-b+k)*i,n)
        x1 = to_normal_modular_form((-b-k)*i,n)
    return x0,x1

# ToNormalModularForm
def to_normal_modular_form(i, mod):
    while i<0 or i>mod:
        if i < 0:
            i+=mod
        else:
            i-=mod
    return i

def count_inverses(n):
    res = 0
    for i in range(n-1):
        if inverse_modulo(i,n) is not None:
            res += 1
    return res + 1

def generate_group(g, n):
    elems = []
    order = 0
    for i in range(n):
        j = pow(g,i)
        if i == 0 or i > 0 and j % n != 1:
            elems.append(j%n)
        elif i != 0:
            order = i
            break
    return elems, order

# A unit g is a generator or primitive root of Z_n
# if for every a in Z_n, g^k=a for some integer k
# if we start with g and keep multiplying with g, eventually we se every element
def is_generator(g, n):
    _, order = generate_group(g,n)
    return n-1 == order

def discrete_log(a, logbase, n):
    for i in range(n):
        if pow(logbase, i, n) == a:
            return i
    return None

#################### PRIMES ####################

def primes_sieve(exclusive_limit:int):
    sievebound = exclusive_limit // 2 # last index of sieve
    sieve = bytearray(b'\x01') * sievebound # bytearray(sievebound+1)
    crosslimit = ((math.isqrt(exclusive_limit)-1) // 2)+1
    for i in range(1, crosslimit):
        if sieve[i]: # 2*i+1 is prime, mark multiples
            # print(sieve[2*i*(i+1):sievebound:2*i+1]) # debug
            sieve[2*i*(i+1):sievebound:2*i+1] = bytes(len(sieve[2*i*(i+1):sievebound:2*i+1]))
    res = list(2*i+1 for i, flag in enumerate(sieve) if flag)
    res[0] = 2
    return res

def is_prime(n:int):
    if (n <= 1): 
        return False
    elif (n < 4): 
        return True # 2,3
    elif (n % 2 == 0): 
        return False
    elif (n < 9): 
        return True # 5,7
    elif (n % 3 == 0): 
        return False
    elif(pseudo_prime(n)):
            if (miller_rabin(n, 40)):
                return True
    return False

# pseudo primality testing using Fermat's theorem, can report false primes, but never false negatives
pseudo_prime = lambda n: modular_exponentiation(n) == 1

modular_exponentiation = lambda n: pow(2,n-1,n)

def miller_rabin(n:int, k:int):
    # write n as 2^s·d + 1 with d odd (by factoring out powers of 2 from n − 1)
    s, d = 0, n-1
    while not (d & 1): # while even
        d >>= 1 # d // 2
        s +=1
    for _ in range(0,k): # witness loop
        a = _rand.randrange(2, n-1) # random integer in the range [2, n − 2]
        x = pow(a,d,n)
        if(x==1 or x == n-1): 
            continue
        for _ in range(0,s-1):
            x = pow(x,2,n)
            if(x == n-1): break
        else:
            return False
    return True

def aks(n):
    if n < 2:
        return False
    if len(str(n)) > 30:
        raise Exception("Float maximum precision reached")
    if __step1(n):
        r = __step2(n)
        return __step3(n, r) and (n <= r or __step5(n, r))
    return False

def __step1(n):
    for b in range(2, math.floor(math.log2(n) + 1)):
        a = n ** (1 / b)
        if a.is_integer():
            return False
    return True

def __step2(n):
    mk = math.floor(math.log2(n) ** 2)
    nexr = True
    r = 1
    while nexr:
        r += 1
        nexr = False
        k = 0
        while k <= mk and not nexr:
            k += 1
            if pow(n, k, r) in (0, 1):
                nexr = True
    return r

def __step3(n, r):
    for a in range(1, r + 1):
        if 1 < math.gcd(a, n) < n:
            return False
    return True

def __step5(n, r):
    max = math.sqrt(__phi(r))
    rn = math.floor(max * math.log2(n))
    if rn > n:
        rn = n
    threads = []
    ran = rn / 8
    ran = math.floor(ran)
    if ran == 0:
        ran = 1

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    for a in range(0, rn, ran):
        process = multiprocessing.Process(
            target=__step5_check, args=(n, a, a + ran, return_dict)
        )
        process.start()
        threads.append(process)
    for i in threads:
        i.join()

    return False not in return_dict.values()

def __step5_check(n, bot, top, return_dict):
    x = bot / (top - bot)
    if bot == 0:
        bot = 1
    for a in range(bot, top):
        b = pow(a, n, n)
        if b - a != 0:
            return_dict[x] = False
            return False
    return_dict[x] = True
    return True

def __phi(n):
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(k, n) == 1:
            amount += 1
    return amount
    
#################### FACTORS AND DIVISORS ####################

# Uses trial division e.g. getNextFactor to find small factors up to 3 digits
# Uses PollardFactor to find factors between 4 and 12 digits
# Uses Pollard_p_1_Factor for larger factors
def factor(n:int):
    l = len(str(n))
    if l < 4:
        return factors(n)
    if l < 13:
        s, t, = pollard_rho(n)
    else:
        if is_prime(n):
            return [n]
        else:
            s,t = pollard_p_1(n)
    if s is None or t is None:
        return None
    else:
        return [s] + factor(t)

def factors(n:int):
    if(n<2): 
        return []
    elif n % 2 == 0: 
        return [2] + factors(n//2)
    elif n % 3 == 0: 
        return [3] + factors(n//3)
    elif is_prime(n): 
        return [n]
    else:
        limit = ceil(sqrt(n))
        i=5
        while i < limit:
            if n%i == 0: 
                return [i] + factors(n//i)
            elif n%(i+2) == 0: 
                return [i+2] + factors(n//(i+2))
            else:
                i+=6
    return [n]

# Fermat factorization, good when N=pq and |p-q| is small or one factor is close to sqrt(n)
def fermat_factor(n:int):
    sq_root = isqrt(n)
    y2 = y = root = 0
    x = sq_root
    while x<n:
        y2 = abs(x*x-n)
        root = isqrt(y2)
        if y2==root*root:
            y = root
            s = x-y
            t = x+y
            if s != 1 and s != n:
                return s,t
        x+=1
    return None, None

def pollard_rho(n:int, lim = 1000000000):
    if n%2 == 0:
        return 2
    limit = 1000
    while limit < lim:
        xi = 2
        x2i = 2
        for _ in range(1,limit):
            xi_prime = xi*xi+1
            x2i_prime = x2i*x2i+1
            x2i_prime = x2i_prime * x2i_prime +1
            xi = xi_prime % n
            x2i = x2i_prime % n
            s = abs(gcd(xi-x2i, n))
            if s != 1 and s != n:
                t = n//s
                return s,t
        if is_prime(n):
            return None, None
        elif limit < lim:
            limit *=10
    raise Exception("Max limit reached")

def pollard_p_1(n:int):
    two_k_fact = 2 # Initial value 2^(k!) for k = 0
    cnt = 0
    while True:
        #Calculate 2^(k!) (mod N) from 2^((k-1)!)
        rk = gcd(two_k_fact-1, n)
        if rk != 1 and rk != n:
            s = rk
            t = n // rk
            return s, t
        elif rk == n:
            break
        cnt+=1
        two_k_fact = pow(two_k_fact, cnt, n)
    return None, None

# Given two integers expressed as lists of prime factors, returns the product as primefactors
def multiply_prime_factors(lhs:list, rhs:list)->list:
    product = [x for x in lhs] + [x for x in rhs] 
    q_sort(product)
    return product

# Given two integers expressed as lists of prime factors, returns the quotient as primefactors
# (this function is only useful where the result is known to be an integer)
def divide_prime_factors(numerator:list, denominator:list)->list:
    quotient = [x for x in numerator]
    for prime in denominator:
        if prime in quotient:
            quotient.remove(prime)
        else:
            raise Exception("divide_prime_factors can only be used when the result is an integer")
    return quotient

def evaluate_prime_factors(factors:list)->int:
    return reduce(lambda x,y: x*y, factors)

def divisors(n:int, only_proper_devisors = False):
    res = [1]
    divisors = []
    limit = n//2 # isqrt(n)
    if(n == 1): 
        return res
    divisors = [x for x in range(2,limit+1) if n % x == 0]
    divisors.insert(0,1)
    if not only_proper_devisors:
        divisors.append(n)
    return divisors

def divisors_b(n:int):
    res = [1]
    divisors = []
    if(n == 1): return res
    #divisors = list(filter(lambda x: n%x==0,range(2,n)))
    with multiprocessing.Pool(6) as p:
        divisors += list(filter(lambda x: n%x==0,range(2,n)))
    divisors.insert(0,1)
    divisors.append(n)
    return divisors

def proper_divisors(n): return divisors_b(n)[:-1]

# Uses the fact that an integer N can be expressed as p_1^a_1 * p_2^a_2 * ..., 
# where p_n is a distinct prime and a_n it's exponent.
# Then the number of divisors can be calculated by (a_1 + 1)*(a_2 + 1) * ...
# for example 28 = 2^2 * 7^1 -> (2 + 1) * (1 + 1) = 6
def no_of_divisors(n:int):
    ps = primes_sieve(max((2*math.isqrt(n),3)))
    #ps = primes_sieve(1000000)
    if n == 1:
        return 1
    cnt = 1
    for p in ps:
        if p*p > n: # When the prime divisor would be greater than the residual tt, that residual tt is the last prime factor with an exponent=1
            cnt = 2*cnt
            break
        exp = 1
        while n % p == 0:
            exp +=1
            n = n//p
        if exp > 1:
            cnt *=exp
        if n == 1:
            break
    return cnt

#################### MISC ####################

# high performance implementation
def is_square(n:int):
    if n < 0: 
        return False
    elif n == 0: 
        return True

    while n&3 == 0:  # reduction by powers of 4   
        n >>=2

    # all perfect squares, in binary, end in 001, when powers of 4 are factored out
    if n&7 != 1: 
        return False

    if n==1: 
        return True  # org. n was 4 or 2
    
    # modulo equivalency test
    c = n%10
    if n%10 in {3, 7}:
        return False  # Not 1,4,5,6,9 in mod 10
    if n % 7 in {3, 5, 6}:
        return False  # Not 1,2,4 mod 7
    if n % 9 in {2,3,5,6,8}:
        return False  
    if n % 13 in {2,5,6,7,8,11}:
        return False  
    
    # other patterns
    if c == 5:  # if it ends in a 5
        if (n//10)%10 != 2:
            return False    # then it must end in 25
        if (n//100)%10 not in {0,2,6}: 
            return False    # and in 025, 225, or 625
        if (n//100)%10 == 6:
            if (n//1000)%10 not in {0,5}:
                return False    # that is, 0625 or 5625
    else:
        if (n//10)%4 != 0:
            return False    # (4k)*10 + (1,9)

    ## Babylonian Algorithm, finding the integer square root (root extraction).
    s = (len(str(n))-1) // 2
    x = (10**s) * 4

    A = {x, n}
    while x * x != n:
        x = (x + (n // x)) >> 1
        if x in A:
            return False
        A.add(x)
    return True

# Count fractions in Stern-Brocot tree between 1/left and 1/right,
def count_fractions_sb(denominator_limit, left, right):
    c = 0
    top = 0
    stack = [x for x in range(0, denominator_limit//2)]
    while True:
        med = left + right
        if med > denominator_limit:
            if top > 0:
                left = right
                top -=1
                right = stack[top]
            else:
                break
        else:
            c+=1
            stack[top] = right
            top +=1
            right = med
    return c

def get_fractions(n, limit):
    sb = __stern_brocot(n)
    fracs = []
    for i in range(1,len(sb)):
        if sb[i-1] < sb[i] and sb[i] <= limit:
            fracs.append((sb[i-1],sb[i]))
    return fracs

def __stern_brocot(n):
    seq = [0]*n
    seq[0]=1
    seq[1]=1
    consider = 1
    i=2
    while i < n:
        seq[i]=seq[consider] + seq[consider-1]
        if i < n-1:
            seq[i+1] = seq[consider]
        consider+=1
        i+=2
    return seq