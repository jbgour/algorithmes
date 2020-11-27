import sys, os
import time


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
    #import time

    def trial_division(n):
        decomp = []
        while n%2==0:
            decomp.append(2)
            n/=2
        f = 3
        while f*f <= n:
            if n%f==0:
                decomp.append(f)
                n = n/f
            else:
                f += 2
        if n != 1:
            decomp.append(int(n))
        return decomp


    def wheel(n):
        decomp = []
        for d in [2,3,5]:
            while n%d == 0:
                decomp.append(d)
                n = n//d
        increments = [4, 2, 4, 2, 4, 6, 2, 6]
        i = 0
        d = 7
        while d*d <= n :
            if n%d == 0:
                decomp.append(d)
                n = n // d
            else:
                if i==8:
                    i = 0
                d += increments[i]
                i += 1

        if n != 1:
            decomp.append(n)
        return decomp

    dict ={}

    approach = wheel
    #t1 = time.time()
    for n in numbers:
        dict[n] = approach(n)
    #print(dict)
    #print(time.time()-t1)

    return dict

#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__=="__main__":
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
     # Pour chacun des fichiers en entrée
    for data_filename in sorted(os.listdir(input_dir)):
        # importer la liste des nombres
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

    
