from random import randint
from typing import Tuple, Set
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


def prime_test_ferma(prime_number:int, base_number=2) -> bool:
    assert prime_number%2 != 0, "First argument should be odd number"
    return base_number ** (prime_number -1 ) % prime_number == 1


def prime_test_miller_rabin(prime_number:int, num_rounds:int, base_number=2) -> bool:
    def find_decomposition_components(prime_number:int) -> Tuple[int, int]:
        prime_number -= 1
        s = 0
        while prime_number%2==0:
            s += 1
            prime_number /= 2
        t = prime_number
        return int(s), int(t)

    assert prime_number%2 != 0, "First argument should be odd number"
    s, t = find_decomposition_components(prime_number)
    for _ in range(num_rounds):
        prime_condition = (base_number ** t) % prime_number
        if prime_condition == 1 or prime_condition == prime_number - 1:
            continue
        for i in range(1, s):
            prime_condition = prime_condition ** 2 % prime_number
            if prime_condition == prime_number - 1:
                break
        else:
            return False
    return True
        

def estimate_convergence(upper_boundary:int) -> Tuple[float, float]:
    prime_numbers = prime_test_eratosthenes(upper_boundary)
    accuracy_ferma = 0
    accuracy_miller_rabin = 0
    num_iters = 0
    for i in tqdm(range(3, upper_boundary, 2)):
        if prime_test_ferma(i) == (i in prime_numbers): accuracy_ferma += 1
        if prime_test_miller_rabin(i, 1) == (i in prime_numbers): accuracy_miller_rabin += 1
        num_iters += 1
    return num_iters - accuracy_ferma, num_iters - accuracy_miller_rabin


if __name__=='__main__':
    accuracy_ferma, accuracy_miller_rabin = estimate_convergence(1000000)
    print(f"Точность теста Ферма: {accuracy_ferma}")
    print(f"Точность теста Миллера-Рабина: {accuracy_miller_rabin}")