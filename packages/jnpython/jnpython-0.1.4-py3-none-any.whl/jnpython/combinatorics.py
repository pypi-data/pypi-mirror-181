from int_helper import permutations, binom

def pairs(arr): return [(a, b) for idx, a in enumerate(arr) for b in arr[idx + 1:]]

# permutaion = combination with order
def permute(arr, n = None) ->list:
    if n is not None and len(arr) != n:
        combs = combinations(arr,n)
        res = []
        for comb in combs:
            res = res + permute(comb)
        return res

    l = permutations(len(arr), len(arr), False)
    perms = [None] * l
    x = len(arr)- 1
    ix = [0]
    __go_permute(list(arr), 0, x, perms, ix)
    if isinstance(arr, str):
        return [''.join(elem) for elem in perms]
    else:
        return perms

def __go_permute(chars, k, m, strs, ix:list):
    if k == m:
        strs[ix[0]] = chars.copy()
        ix[0] +=1
    else:
        for i in range(k, m+1):
            (chars[i], chars[k]) = (chars[k], chars[i])
            __go_permute(chars, k+1, m, strs, ix)
            (chars[i], chars[k]) = (chars[k], chars[i])

# get combinations of length n from items (no repetition, order does not matter)
def combinations(arr, n) ->list:
    combs = []
    c = len(arr)
    for i in range(binom(c, n)):
        comb = [None] * n
        ans = [0]*n
        a=c
        b=n
        x = binom(a,b) - 1 - i

        for j in range(n):
            ans[j] = __largest_v_combinations(a,b,x)
            x -= binom(ans[j], b) # 0 if b > ans[j] else binom(ans[j], b)
            a = ans[j]
            b-=1
        
        for j in range(n):
            comb[j] = arr[c-1-ans[j]]
        
        combs.append(comb)
    if isinstance(arr, str):
        return [''.join(elem) for elem in combs]
    else:
        return combs

def __largest_v_combinations(a,b,x):
    v = a-1
    while binom(v,b)>x:
        v-=1
    return v