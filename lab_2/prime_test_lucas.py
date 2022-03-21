from typing import List, Tuple


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


def compute_Legendre_symbol(n:int) -> int:
    a = n % 5
    if a in (1, 4): 
        return 1
    else: 
        return -1


def Lucas_primality_test(prime_number:int) -> bool:
    if prime_number in (2, 3, 5): return True
    assert prime_number%2, "Argument should be odd number"
    Legendre_symbol = compute_Legendre_symbol(prime_number)
    fibonacci_index = prime_number - Legendre_symbol
    fibonacci_table = compute_fibonacci_table(len(bin(fibonacci_index))-2, prime_number)
    fn, _ = compute_fibonacci_number_by_sum(fibonacci_index, fibonacci_table, prime_number)
    if fn: return False
    return True


if __name__=='__main__':
    #Пример расчёта таблицы с числами Фибоначчи и расчета 249 и 250 чисел Фибоначчи
    fibonacci_table = compute_fibonacci_table(10)
    fn, fn1 = compute_fibonacci_number_by_sum(249, fibonacci_table)
    print(f"249 число Фибоначчи: {fn}")
    print(f"250 число Фибоначчи: {fn1}")
    
    #Пример определения простоты числа с помощью теста Лукаса
    print(f"Число 877 простое: {Lucas_primality_test(877)}")
    print(f"Число 879 простое: {Lucas_primality_test(879)}")