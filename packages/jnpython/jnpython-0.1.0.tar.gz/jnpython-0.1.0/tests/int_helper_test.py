from random import randint
import int_helper
import pytest
from functools import reduce

p_10 = 9576890767
p_30 = 362736035870515331128527330659
p_100 = 6513516734600035718300327211250928237178281758494417357560086828416863929270451437126021949850746381
p_200 = 58021664585639791181184025950440248398226136069516938232493687505822471836536824298822733710342250697739996825938232641940670857624514103125986134050997697160127301547995788468137887651823707102007839

def test_sign():
    assert int_helper.sign(-10) == -1
    assert int_helper.sign(10) == 1

def test_concat():
    assert int_helper.concat(100,101) == 100101

def test_bitlength():
    assert int_helper.bitlength(1024) == 11
    assert int_helper.bitlength(827364872364823) == 50

def test_binom():
    pass

def test_combinations():
    pass

def test_permutations():
    pass

# MODULAR ARITHMETIC

def test_mul_mod():
    res = int_helper.mul_mod(123456,123456,123)
    assert res == (123456*123456)%123

def test_mod_inverse():
    assert int_helper.mod_inverse(3,7) == 5

def test_modular_root():
    x0 = int_helper.modular_root(58, 101, 2)
    assert x0 in (19,82) 

def test_inverse_modulo():
    assert int_helper.inverse_modulo(3,11) == 4

def test_quad_solve_modulo():
    x0, x1 = int_helper.quad_solve_modulo(2,8,2,0,23)
    assert x0 in (5, 14)
    assert x1 in (5, 14)

def test_to_normal_modular_form():
    assert int_helper.to_normal_modular_form(16,12) == 4
    assert int_helper.to_normal_modular_form(-1,12) == 11

def test_count_inverses():
    pass

def test_generate_group():
    members, order = int_helper.generate_group(3,7)
    assert order == 6

def test_discrete_log():
    assert int_helper.discrete_log(17, 3, 101) == 70

# PRIMES

def test_primes_sieve():
    ps = int_helper.primes_sieve(1000000)
    assert len(ps) == 78498
    assert ps[-1]  == 999983

def test_is_prime():
    ps = int_helper.primes_sieve(1000)
    tests = map(int_helper.is_prime, ps)
    assert all(tests)

    not_ps = [x for x in range(1,1001) if x not in ps]
    tests = map(int_helper.is_prime, not_ps)
    assert not any(tests)

def test_is_prime2():
    assert int_helper.is_prime(p_10)
    assert int_helper.is_prime(p_30)
    assert int_helper.is_prime(p_100)
    assert int_helper.is_prime(p_200)

def test_aks():
    ps = int_helper.primes_sieve(100)
    tests = map(int_helper.is_prime, ps)
    assert all(tests)

    not_ps = [x for x in range(1,100) if x not in ps]
    tests = map(int_helper.is_prime, not_ps)
    assert not any(tests)

    assert int_helper.aks(p_10)

# FACTORS AND DIVISORS

def test_factors():
    prod = lambda xs: reduce(lambda x,y: x*y, xs)
    nums = [5,7,61,781]
    p1 = prod(nums)
    factors = int_helper.factors(p1)
    p2 = prod(factors)
    assert p1 == p2
    assert 5 in factors
    assert 7 in factors
    assert 11 in factors
    assert 61 in factors
    assert 71 in factors

def test_fermat_factor():
    p_10_b = 0
    for i in range(p_100+1, p_200):
        if int_helper.is_prime(i):
            p_10_b = i
            break
    s, t = int_helper.fermat_factor(p_100*p_10_b)
    assert s == p_100
    assert t == p_10_b

def test_pollard_rho():
    s,t = int_helper.pollard_rho(p_10*p_30)
    assert s == p_10
    assert t == p_30

def test_pollard_p_1():
    s,t = int_helper.pollard_p_1(p_10*p_30)
    assert s == p_10
    assert t == p_30

def test_factor():
    fs = int_helper.factor(p_10*p_30+2)
    assert 5 in fs
    assert 19 in fs
    assert 2687 in fs
    assert 132361 in fs
    assert 102816762607933019109385241527 in fs

# MISC

def test_phi():
    assert int_helper.phi(64) == 32

def test_phi_sieve():
    assert int_helper.phi_sieve(100)[64] == 32