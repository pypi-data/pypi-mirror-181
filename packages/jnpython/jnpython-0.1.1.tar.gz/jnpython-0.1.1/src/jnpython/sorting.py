# MergeSort and InsertionSort are stable -> preserves the relative order of equal keys in the array
# QuickSort is unstable -> does not preserve the relative order of equal keys in the array
# InsertionSort is slowest (between N and N^2) but uses the least extra space (1)
# QuickSort sorts in NlogN and uses logN extra space, but 3-way quicksort is the fastest and sorts in between N and NlogN depending on input distribution
# MergeSort sorts in NlogN and uses N extra space 

__MERGE_CUTOFF = 7 # cutoff to insertion sort

def is_sorted(arr): return __is_sorted(arr, 0, len(arr) - 1)

def q_sort(arr): return __q_sort(arr ,0 , len(arr) -1)

def insertion_sort(arr): return __insertion_sort(arr, 0, len(arr)-1)

def merge_sort(arr): return __merge_sort(deepcopy(arr), arr, 0, len(arr) -1)

# ret[i] is the index of the ith smallest entry in arr, ret[0] = index of samllest entry
# or: if we sort the array, ret[i] gives the original position for sorted[i]
def merge_sort_get_indices(arr): 
    ix = list(range(0,len(arr)))
    aux = [0]*len(arr)
    __merge_sort_index(arr, ix, aux, 0, len(arr) - 1)
    return ix

################################################################################

def __merge_sort(src, dst, lo, hi):
    # insertion sort for small subarrays will improve the running time
    if hi <= lo + __MERGE_CUTOFF:
        __insertion_sort(dst, lo, hi)
        return
    mid = lo + (hi-lo) // 2
    __merge_sort(dst, src, lo, mid)
    __merge_sort(dst, src, mid+1, hi)

    # test whether array is already in order, thus reducing running time by skipping call to merge
    if not src[mid+1] < src[mid]:
        array_copy(src, lo, dst, lo, hi-lo + 1)
        return
    __merge(src, dst, lo, mid, hi)

# precondition: src[lo .. mid] and src[mid+1 .. hi] are sorted subarrays
def __merge(src, dst, lo, mid, hi):
    i, j  = lo, mid + 1
    for k  in range(lo, hi+1):
        if i > mid:
            dst[k] = src[j]
            j += 1
        elif j > hi:
            dst[k] = src[i]
            i +=1
        elif src[j] < src[i]:
            dst[k] = src[j];   # to ensure stability
            j += 1
        else:
            dst[k] = src[i]
            i +=1

def __merge_sort_index(arr, ix, aux, lo, hi):
    if hi <= lo:
        return
    mid = lo + (hi-lo)//2
    __merge_sort_index(arr, ix, aux, lo, mid)
    __merge_sort_index(arr, ix, aux, mid+1, hi)
    __merge_index(arr, ix, aux, lo, mid, hi)

def __merge_index(arr, ix, aux, lo, mid, hi):
    for k in range(lo,hi+1):
        aux[k] = ix[k]
    i,j = lo, mid+1
    for k in range(lo, hi+1):
        if i > mid:
            ix[k] = aux[j]
            j+=1
        elif j > hi:
            ix[k] = aux[i]
            i+=1
        elif arr[aux[j]] < arr[aux[i]]:
            ix[k] = aux[j]
            j+=1
        else:
            ix[k] = aux[i]
            i+=1

def __q_sort(arr, lo, hi):
    n = hi - lo +1
    if n <= __MERGE_CUTOFF:
        __insertion_sort(arr, lo, hi)
        return
    
    elif n<= 40: # use median-of-3 as partitioning element
        m = __median3(arr, lo, lo+n//2,hi)
        __exch(arr,m,lo)

    else: # use Tukey ninther as partitioning element
        eps = n//8
        mid = lo + n // 2
        m1 = __median3(arr, lo, lo+eps, lo+eps+eps)
        m2 = __median3(arr, mid-eps, mid, mid+eps)
        m3 = __median3(arr, hi-eps-eps, hi-eps, hi)
        ninther = __median3(arr, m1, m2 ,m3)
        __exch(arr, ninther, lo)

    # Bentley-McIlroy 3-way partitioning
    i,j = lo, hi+1
    p,q = lo, hi+1
    v = arr[lo]
    while True:
        i += 1
        while arr[i] < v:
            if i == hi:
                break
            i += 1
        j -=1
        while v < arr[j]:
            if j == lo:
                break
            j -=1
        
        # pointers cross
        if i == j and arr[i] == v:
            p +=1
            __exch(arr, p, i)
        if i >= j:
            break
        
        __exch(arr, i, j)
        
        if(arr[i] == v):
            p +=1
            __exch(arr, p, i)
        if arr[j] == v:
            q -=1
            __exch(arr, q, j)

    i = j+1
    for k in range(lo, p+1):
        __exch(arr, k, j)
        j-=1
    for k in range(hi, q-1, -1):
        __exch(arr, k, i)
        i+=1
    __q_sort(arr, lo, j)
    __q_sort(arr,i, hi)

# sort from a[lo] to a[hi] using insertion sort
def __insertion_sort(arr, lo, hi):
    for i in range(lo+1, hi+1):
        j = i
        while j > lo and arr[j] < arr[j-1]:
            __exch(arr, j, j-1)
            j -= 1

# slower than __is_sorted
def __is_sorted2(v, lo, hi): return all(v[i] <= v[i+1] for i in range(len(v) - 1))

def __is_sorted(v, lo, hi):
    for i in range(lo+1, hi+1):
        if v[i] < v[i-1]:
            return False
    return True


def __median3(a, i, j, k):
    if a[i] < a[j]:
        if a[j] < a[k]:
            return j
        else:
            return k if a[i] < a[k] else i
    else:
        if a[k] < a[j]:
            return j
        else:
            return k if a[k] < a[i] else i

def __exch(arr, i, j): arr[i], arr[j] = arr[j], arr[i]

################################################################################

def deepcopy(arr):
    if isinstance(arr, tuple):
        return tuple(arr)
    elif isinstance(arr, list):
        return [arr[i] for i in range(len(arr))]
    else:
        raise Exception("invalid type: ", type(arr))

def array_copy(src, src_start_ix, dst, dst_start_ix, length):
    for i in range(length):
        dst[i + dst_start_ix] = src[i + src_start_ix]

def main():
    pass

if __name__ == "__main__":
    #sys.exit(main())
    main()
    
