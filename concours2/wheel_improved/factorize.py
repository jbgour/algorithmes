import sys, os

#import time
from multiprocessing import Pool

def get_non_multiples(n, max_divisor):
    """
    return all  non multiples of base_list untill n.
    :param n: int
    :return: list of divisors
    """
    non_multiple = []
    is_multiple = [False] * (n + 1)
    for i in range(2, max_divisor + 1):
        is_multiple[::i] = [True] * ((n // i) + 1)
    for i in range(2, n + 1):
        if not is_multiple[i]:
            non_multiple.append(i)
    del is_multiple
    return non_multiple

def get_prime_and_product(n):
    """
    return all prime numbers between 2 and n
    :param n: int
    :return: list of prime numbers
    """
    prime = [2]
    product = 2
    is_prime = [True] * (n + 1)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if is_prime[i]:
            is_prime[i * i:: 2 * i] = [False] * ((n + 1 - i * i - 1) // (2 * i) + 1)
    for i in range(3, n + 1, 2):
        if is_prime[i]:
            prime.append(i)
            product *= i
    del is_prime
    return prime, product

def compute_wheel(max_given):
    inc = []
    initial = get_prime_and_product(max_given)
    initial_list = initial[0]
    initial_product = initial[1]
    lower_bound = initial_list[-1]
    first_shot = get_non_multiples(initial_product + 1, lower_bound)
    first_shot += [first_shot[0] + initial_product]

    s = len(first_shot)
    for i in range(s - 1):
        inc += [first_shot[i + 1] - first_shot[i]]
    return initial_list + [first_shot[0]], inc

def wheel(n, initial_list, inc):
    decomp = []
    for d in initial_list[:-1]:
        while n % d == 0:
            decomp.append(d)
            n = n // d
        if d*d > n:
            break
    end_turn = len(inc)
    i = -1
    d = initial_list[-1]
    while d * d <= n:
        if n % d == 0:
            decomp.append(d)
            n = n // d
        else :
            if i == end_turn:
                i = 0
            d += inc[i]
            i += 1
    if n != 1:
        decomp.append(n)
    return decomp

def parallel_ceci(initial_list, inc, numbers):
    dict= {}
    for n in numbers:
        #print('coucou')
        #t1 = time.time()
        dict[n] = wheel(n, initial_list, inc)
        #print(time.time()-t1)
    return dict

def factorize(numbers):
    """
        A Faire:         
        - Ecrire une fonction qui prend en paramètre une liste de nombres et qui retourne leurs decompositions en facteurs premiers
        - cette fonction doit retourner un dictionnaire Python où :
            -- la clé est un nombre n parmi la liste de nombres en entrée
            -- la valeur est la liste des facteurs premiers de n (clé). Leur produit correpond à n (clé).  
            
        - Attention : 
            -- 1 n'est pas un nombre premier
            -- un facteur premier doit être répété autant de fois que nécessaire. Chaque nombre est égale au produit de ses facteurs premiers. 
            -- une solution partielle est rejetée lors de la soumission. Tous les nombres en entrée doivent être traités. 
            -- Ne changez pas le nom de cette fonction, vous pouvez ajouter d'autres fonctions appelées depuis celle-ci.
            -- Ne laissez pas trainer du code hors fonctions car ce module sera importé et du coup un tel code sera exécuté et cela vous pénalisera en temps.
    """


    #t1 = time.time()

    generated_wheel = compute_wheel(13)

    initial_list = generated_wheel[0]
    inc = generated_wheel[1]

    n1 = numbers[0:len(numbers)//4]
    n2 = numbers[len(numbers)//4:len(numbers)//2]
    n3 = numbers[len(numbers)//2:3*len(numbers)//4]
    n4 = numbers[3*len(numbers)//4:]

    with Pool(processes=4) as pool:
        result = pool.starmap(parallel_ceci,[[initial_list, inc,n1],[initial_list, inc,n2],[initial_list, inc,n3],[initial_list, inc,n4]])

    #print(time.time()-t1)
    d = {}
    d.update(result[0])
    d.update(result[1])
    d.update(result[2])
    d.update(result[3])

    return d


#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des fichiers en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les résultats doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(input_dir, "doesn't exist")
        exit()
    #  Pour chacun des fichiers en entrée
    for data_filename in sorted(os.listdir(input_dir)):
        #  importer la liste des nombres
        data_file = open(os.path.join(input_dir, data_filename), "r")
        numbers = [int(line) for line in data_file.readlines()]

        # decomposition en facteurs premiers
        D = factorize(numbers)

        # fichier des reponses depose dans le output_dir
        output_filename = 'answer_{}'.format(data_filename)
        output_file = open(os.path.join(output_dir, output_filename), 'w')

        # ecriture des resultats
        for (n, primes) in D.items():
            output_file.write('{} {}\n'.format(n, primes))

        output_file.close()
