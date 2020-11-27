import sys, os, time
from statistics import mean
import random as rd

# calcul de distance de manhattan entre 2 points, un point est un tuple (x, y)
def manhatan_distance (p_1, p_2):
    return abs(p_1[0] - p_2[0]) + abs(p_1[1] - p_2[1])

def online_k_serveurs(pos_sites, pos_serveurs, demande):
    """
        A Faire:         
        - Ecrire une fonction qui retourne la liste des serveurs répondant aux demandes 

        :param pos_sites: un dictionnaire Python représentant la position de chaque site où:
            -- la clé (int) est le numéro du site entre 0 et n-1 (on a n sites)
            -- la valeur est un tuple (x, y) de coordonnées cartésiennes
        
        :param pos_serveurs: un dictionnaire Python représentant la position de chaque serveur où:
            -- la clé (int) est le numéro du serveur entre 0 et k-1 (on a k sites)
            -- la valeur est un tuple (x, y) de coordonnées cartésiennes
                
        :param demande: un numéro de site entre 0 et n-1 qui correpond à la demande courante 

        :return un numéro de serveur entre 0 et k-1 qui se déplacera à la demande courante         
    """
    def glouton():
        p_2 = pos_sites[demande]
        l = [manhatan_distance(pos_serveurs[serveur_i],p_2) for serveur_i in range(k)]
        index_min = min(range(len(l)), key=l.__getitem__)
        value_min = int(l[index_min])
        return index_min, value_min

    def random_glouton(seuil):
        serveur_glouton, dist_glouton = glouton()
        if dist_glouton == 0:
            return serveur_glouton
        seuil2 = 0
        initial = []
        r2 = 0
        for i in pos_serveurs:
            if pos_serveurs[i] == (0,0):
                initial += [i]
                seuil2 += 1/k
        if len(initial)>0:
            initial_random = rd.choice(initial)
            r2 = int(rd.random()+seuil2)

        l = [i for i in range(k)]
        serveur_random = rd.choice(l)
        r = int(rd.random()+seuil)

        if r2 == 1:
            return initial_random
        elif r == 1:
            return serveur_random
        else:
            return serveur_glouton

    k = len(pos_serveurs)
    seuil=0.1

    return random_glouton(seuil) # ceci n'est pas une solution optimale

##############################################################
#### LISEZ LE MANIFEST et NE PAS MODIFIER LE CODE SUIVANT ####
##############################################################
if __name__=="__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
	    print(input_dir, "doesn't exist")
	    exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
	    print(output_dir, "doesn't exist")
	    exit()

    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    ratios = []

    for instance_filename in sorted(os.listdir(input_dir)):
        # importer l'instance depuis le fichier (attention code non robuste)
        instance_file = open(os.path.join(input_dir, instance_filename), "r")
        lines = instance_file.readlines()

        cout_opt = int(lines[1])
        k = int(lines[4])

        idx_demande = lines.index('# demandes\n')
        sites = {}
        for i in range(7,idx_demande-1):
            coords = lines[i].split()
            sites[i-7] = (int(coords[0]), int(coords[1]))

        demandes = [int(d) for d in lines[idx_demande+1].split()]

        # lancement de l'algo online 10 fois et calcul du meilleur cout
        nb_runs = 10
        meilleur_cout = float('inf')
        for _ in range(nb_runs):
            cout_online = 0
            serveurs = {i:(0,0) for i in range(k)} #tous les serveurs à la position 0,0 au départ
            for d in demandes:
                r = online_k_serveurs(sites.copy(), serveurs.copy(), d)
                cout_online += manhatan_distance(serveurs[r], sites[d])
                serveurs[r] = sites[d]

            meilleur_cout = min(meilleur_cout, cout_online)

        ratios.append(meilleur_cout/cout_opt)

        # ajout au rapport
        output_file.write(instance_filename + ': optimal: {}, online: {}, ratio: {}\n'.format(cout_opt, meilleur_cout, ratios[-1]))

    output_file.write('score (moyenne des ratios) :' + str(mean(ratios)))

    output_file.close()

