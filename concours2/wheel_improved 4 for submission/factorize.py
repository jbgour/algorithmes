import sys, os


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
    from math import sqrt

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
        initial = get_prime_and_product(max_given)
        initial_list = initial[0]
        initial_product = initial[1]
        lower_bound = initial_list[-1]
        first_shot = get_non_multiples(initial_product + 1, lower_bound)
        return initial_list + first_shot, first_shot

    def compute_all_wheel(initial_list, first_shot, end_wheel, size):
        l = first_shot
        i = 0
        while l[-1] < end_wheel:
            i += 1
            l += [n + i * size for n in initial_list]
        return initial_list + l

    def wheel(n, initial_list):
        decomp = []
        encountered = False
        for d in initial_list:
            while n % d == 0:
                decomp.append(d)
                n = n // d
                encountered = True
            if encountered:
                if d > sqrt(n):
                    break
        if n != 1:
            decomp.append(n)
        return decomp

    dict = {}
    m = max(numbers)
    end_wheel = int(sqrt(m))
    last_prime = 13
    size = get_prime_and_product(last_prime)[1]
    generated_wheel = compute_wheel(last_prime)
    initial_list = generated_wheel[0]
    first_shot = generated_wheel[1]
    generated_complete_wheel = compute_all_wheel(initial_list, first_shot, end_wheel, size)

    for n in numbers:
        ll = filter(lambda x: n % x, generated_complete_wheel)
        dict[n] = wheel(n, generated_complete_wheel)
    return dict


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
