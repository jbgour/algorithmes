import sys, os, time
import networkx as nx


def dominant(g):
    """
        A Faire:
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """

    ##################################
    ### useful functions, not all used
    ##################################

    def sort_nodes(g):
        """
        used to sort the nodes by their descending number of neigbors
        :param g: graph
        :return: list of nodes, sorted
        """
        nodes = set(g)
        nodes_sorted = dict()
        for node in nodes:
            nodes_sorted[node] = len(g[node])
        nodes_sorted = {node: neigbors for node, neigbors in
                        sorted(nodes_sorted.items(), key=lambda item: item[1], reverse=True)}
        return list(nodes_sorted.keys())

    def sort_nodes_2(g, remaining_nodes):
        """
        used to sort the nodes by their descending number of neigbors
        :param g: graph
        :return: list of nodes, sorted
        """
        nodes = set(g)
        nodes_sorted = dict()
        for node in nodes:
            nodes_sorted[node] = max(remaining_neighbors_neighbors_number(node, g, remaining_nodes),len(g[node]))
        nodes_sorted = {node: neigbors for node, neigbors in
                        sorted(nodes_sorted.items(), key=lambda item: item[1], reverse=True)}
        return list(nodes_sorted.keys())

    def remaining_neighbors_number(node, g, remaining_nodes):
        """
        compute the number of neighbors of v
        :param g: graph
        :param node: node of the graph
        :return: number of neigbors
        """
        return len(remaining_nodes.intersection(set(g[node])))+1

    def remaining_neighbors_neighbors_number(node, g, remaining_nodes):
        """
        compute the max number of neighbors of neighgbors of v
        :param g: graph
        :param node: node of the graph
        :return: number of neigbors
        """
        number = 0
        for node in remaining_nodes.intersection(set(g[node])):
            number = max(number, remaining_neighbors_number(node, g, remaining_nodes))
        return number

    def has_remaining_neighbors(node, g, remaining_nodes):
        """
        return True if node has neighbors, 0 else
        :param node: node
        :param g: graph
        :return: Bool
        """
        return remaining_nodes.intersection(set(g[node])) !={}

    def neighbors(node, g):
        """
        returns the neigbors of node
        :param node: node
        :param g: grah
        :return: set of nodes
        """
        return g[node]


    def evaluate_solution(n, d):
        """
        used to compute the score of the solution, same methodology as codalab
        :param n: int, nodes
        :param d: int, dominant nodes
        :return: int, score
        """
        return 1 - (d / n)


    #######################################
    ### 2 approaches, first one is the best
    #######################################

    def dominant_oneshot(g):
        """
        one instance of the greedy algorithm
        :param g: graph
        :return: tuple, (dominant nodes, score)
        """
        g = g.copy()
        inital_nodes = set(g)
        remaining_nodes = set(g)
        nodes_sorted_list = sort_nodes(g)
        selected_node = nodes_sorted_list.pop(0)
        dominant_nodes = set([selected_node])
        dominated_nodes = set(g[selected_node])
        remaining_nodes = set(nodes_sorted_list) - dominant_nodes - dominated_nodes
        g.remove_node(selected_node)
        while remaining_nodes:
            nodes_sorted_list = sort_nodes(g)
            selected_node = nodes_sorted_list.pop(0)
            dominant_nodes.add(selected_node)
            dominated_nodes.update([node for node in g[selected_node] if node not in dominated_nodes])
            remaining_nodes = inital_nodes - dominant_nodes - dominated_nodes
            g.remove_node(selected_node)

        e = evaluate_solution(len(inital_nodes), len(dominant_nodes))
        return dict({'dominant_nodes': dominant_nodes, 'score': e})



    def dominant_oneshot_2(g):
        """
        one instance of a personal try
        :param g: graph
        :return: tuple, (dominant nodes, score)
        """
        g = g.copy()
        inital_nodes = set(g)
        dominant_nodes = set({})
        dominated_nodes = set({})
        remaining_nodes = set(inital_nodes) - dominant_nodes - dominated_nodes
        while remaining_nodes:
            for selected_node in remaining_nodes:
                if has_remaining_neighbors(selected_node,g, remaining_nodes):
                    weight = remaining_neighbors_number(selected_node, g, remaining_nodes)
                    if (weight >= max([remaining_neighbors_number(node, g, remaining_nodes) for node in remaining_nodes]) and
                            weight >= max([remaining_neighbors_neighbors_number(node, g, remaining_nodes) for node in remaining_nodes])) :
                        dominant_nodes.add(selected_node)
                        dominated_nodes.update([node for node in g[selected_node] if node not in dominated_nodes])
                        remaining_nodes = inital_nodes - dominant_nodes - dominated_nodes
                        g.remove_node(selected_node)
                else:
                    dominant_nodes.add(selected_node)
                    remaining_nodes = inital_nodes - dominant_nodes - dominated_nodes
                    g.remove_node(selected_node)
                if not remaining_nodes:
                    break
        e = evaluate_solution(len(inital_nodes), len(dominant_nodes))
        return dict({'dominant_nodes': dominant_nodes, 'score': e})


    ###################################
    ### actual script, ran at execution
    ###################################

    #input, choose your strategy here
    dominant_approach = dominant_oneshot

    #initialisation
    score = 0  # score set at 0
    dominant_nodes = set(g)  # initial bad dominating set

    #loop
    for i in range(50):  # we compute the greedy 50 times and take the best one
        res = dominant_approach(g)
        if res['score'] > score:
            dominant_nodes = res['dominant_nodes']
            score = res['score']

    #result
    return (dominant_nodes, score)


#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__ == "__main__":
    t1 = time.time()
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(input_dir, "doesn't exist")
        exit()

        # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')
    e = 0
    for graph_filename in sorted(os.listdir(input_dir)):
        # importer le graphe
        g = nx.read_adjlist(os.path.join(input_dir, graph_filename))

        # calcul du dominant
        res = dominant(g)
        D = sorted(res[0], key=lambda x: int(x))
        e += res[1]
        # ajout au rapport
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
        output_file.write('\n')
    print(e)
    t2 = time.time()
    print("durée: " + str(t2 - t1))
    output_file.close()
