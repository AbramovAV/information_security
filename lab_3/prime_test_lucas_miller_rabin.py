from typing import List, Tuple, Set
from tqdm import tqdm


def prime_test_eratosthenes(upper_boundary:int) -> Set[int]:
    prime_numbers = []
    least_primes = [0 for _ in range(upper_boundary+1)]
    for i in range(2, upper_boundary+1):
        if least_primes[i] == 0:
            least_primes[i] = i
            prime_numbers.append(i)
        for prime_number in prime_numbers:
            if prime_number>least_primes[i] or prime_number * i > upper_boundary:
                break
            else:
                least_primes[prime_number * i] = prime_number
    return set(prime_numbers)


def compute_Legendre_symbol(n:int) -> int:
    a = n % 5
    if a in (1, 4): 
        return 1
    else: 
        return -1


def compute_fibonacci_table(upper_boundary:int, modulo=None) -> List[Tuple[int, int]]:
    fibonacci_table = [(1,1)]
    for r in range(upper_boundary):
        fk,fk1 = fibonacci_table[-1]
        fk, fk1 = (
                        (fk * (2 * fk1 - fk)),
                        (fk1 ** 2 + fk ** 2)
                  )
        if modulo:
            fk %= modulo
            fk1 %= modulo
        fibonacci_table.append((fk, fk1))
    return fibonacci_table


def compute_fibonacci_number_by_sum(fibonacci_index:int, fibonacci_table:List[Tuple[int, int]], modulo=None) -> Tuple[int, int]:
    fibonacci_index_bin = bin(fibonacci_index)[2:][::-1]
    fn, fn1 = 0, 1
    for idx, digit in enumerate(fibonacci_index_bin):
        if digit == '1':
            fm, fm1 = fibonacci_table[idx]
            fn, fn1 = (
                (fm * fn1 + fm1 * fn - fn * fm),
                (fm1 * fn1 + fm * fn)
            )
            if modulo:
                fn %= modulo
                fn1 %= modulo
    return fn, fn1


def prime_test_lucas_miller_rabin(prime_number:int) -> bool:
    def find_decomposition_components(prime_number:int) -> Tuple[int, int]:
        s = 0
        while prime_number%2==0:
            s += 1
            prime_number /= 2
        t = prime_number
        return int(s), int(t)
    assert prime_number%2, "Argument should be odd number"
    
    Legendre_symbol = compute_Legendre_symbol(prime_number)
    s,t = find_decomposition_components(prime_number - Legendre_symbol)
    fibonacci_index = prime_number - Legendre_symbol
    fibonacci_table = compute_fibonacci_table(len(bin(fibonacci_index))-2, prime_number)
    fn, _ = compute_fibonacci_number_by_sum(t, fibonacci_table, prime_number)

    if fn == 0:
        return True
    
    for i in range(s):
        m = t * (2**i)
        fm_left, _ = compute_fibonacci_number_by_sum(m-1, fibonacci_table)
        fm_right, _ = compute_fibonacci_number_by_sum(m+1, fibonacci_table)
        if (fm_left+fm_right)%prime_number == 0:
            return True

    return False


if __name__=='__main__':
    #Получаем набор простых чисел до 1e6
    prime_numbers_eratosthenes = prime_test_eratosthenes(1000000)

    for prime_number in range(5,1000000,2):
        if prime_test_lucas_miller_rabin(prime_number) and \
            prime_number not in prime_numbers_eratosthenes:
            if prime_number%3 and prime_number%5:
                print(prime_number)#prime_number - псевдопростое число