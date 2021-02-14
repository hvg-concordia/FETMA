from __future__ import print_function
from packages_etma import *



def event_tree_builder(ml):
    tree_graph.clear()
    tempnodeslist = []
    start_node = 'IE'
    for i in range(0, ml.__len__()):
        if debug: print(i, ">>>", tempnodeslist, "-----------------------")
        tempnodeslist_processed = []
        for r in range (0, tempnodeslist.__len__()):
            current_list_element = tempnodeslist[r]
            c = current_list_element.count('.')
            # print(r, '->', current_list_element, c)
            if c == i: tempnodeslist_processed.append(current_list_element)
        tempnodeslist = tempnodeslist_processed

        if i == 0:
            source_node = 'IE'
            current_list = ml[i]
            for i in range(0,current_list.__len__()):
                sink_node = source_node+'.'+current_list[i]
                if debug: print(i,source_node, '->',sink_node)
                tree_graph.add_edge(source_node, sink_node)
                tempnodeslist.append(sink_node)
        else:
            current_list = ml[i]
            previous_list = tempnodeslist
            for x in range(0,previous_list.__len__()):
                source_node = previous_list[x]
                for z in range(0, current_list.__len__()):
                    sink_node = source_node+'.'+current_list[z]
                    if debug: print(z,source_node, '->',sink_node)
                    tree_graph.add_edge(source_node, sink_node)
                    tempnodeslist.append(sink_node)
    
    tempnodeslist_processed = []
    for r in range (0, tempnodeslist.__len__()):
        current_list_element = tempnodeslist[r]
        c = current_list_element.count('.') # count number of dots while adding the paths
        if c == i+1: tempnodeslist_processed.append(current_list_element)
    tempnodeslist = tempnodeslist_processed # End nodes of complete tree

    draw_complete_tree()
    temp_tree_graph = tree_graph
    return temp_tree_graph  # return a tree instance


def draw_complete_tree():
    tree_graph.graph['graph']={'rankdir':'LR', 'splines':'ortho'}
    A = nx.nx_agraph.to_agraph(tree_graph)
    pos = A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
    A.draw('complete_tree.svg')
    print("")
    print(datetime.datetime.now(), "Complete Event Tree written to 'complete_tree.svg'")
    print("")


def draw_reduced_tree(tree_instance):
    tree_instance.graph['graph']={'rankdir':'LR', 'splines':'ortho'}
    A = nx.nx_agraph.to_agraph(tree_graph)
    pos = A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
    A.draw('reduced_tree.svg')
    print("")
    print(datetime.datetime.now(), "Reduced Event Tree written to 'reduced_tree.svg'")
    print("")


def node_deletion(node_origin, tree_instance):

    if tree_instance.has_node(node_origin):
    
        print("Deleting the Event Tree Node: ", node_origin)
        
        preceding_node = list(tree_instance.predecessors(node_origin))
        succeding_nodes = list(tree_instance.successors(node_origin))

        if debug==True: print("P: ", preceding_node)
        if debug==True: print("S: ", succeding_nodes)

        tree_instance.remove_node(node_origin)

        if debug:
            B = nx.nx_agraph.to_agraph(tree_instance)
            B.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
            B.draw('temp_tree.svg')

        
        undirected_graph = tree_instance.to_undirected()
        sub_graphs = nx.connected_component_subgraphs(undirected_graph)
        edges = []
        nodes = []
        for i, sg in enumerate(sub_graphs):
            if debug==True: print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
            if debug==True: print("\tNodes:", sg.nodes())
            if debug==True: print("\tEdges:", sg.edges())
            edges.append(sg.edges())
            nodes.append(sg.nodes())

        delete_handle = False
        for i in range(0, len(edges)):
            temp_list = list(edges[i])
            if debug: print(temp_list)
            for j in range(0, len(temp_list)):
                if debug: print(temp_list[j])
                if "IE" in temp_list[j]:
                    if debug: print("origin graph is: ", i)
                    origin_graph_index = i
                    delete_handle = True

        if delete_handle: del edges[origin_graph_index]

        #print(edges)

        name_part_to_be_removed = node_origin.split('.')[-1]
        name_part_to_be_removed = '.'+name_part_to_be_removed
        
        if debug: print("name_part_to_be_removed", name_part_to_be_removed)

        for i in range(0, len(succeding_nodes)):
            temp_node = succeding_nodes[i]
            temp_node = temp_node.replace(name_part_to_be_removed,'')
            if debug: print(preceding_node[0], "-->", temp_node)
            tree_instance.add_edge(preceding_node[0], temp_node)

        for i in range(0, len(edges)):
            if debug: print("For each in edge list --------------------------")
            temp_list = list(edges[i])
            if debug: print(temp_list)
            for j in range(0, len(temp_list)):
                temp_tuple = temp_list[j]
                if debug: print("temp_tuple", temp_tuple)
                if temp_tuple[0].count('.') < temp_tuple[1].count('.'):
                    temp_source_node = temp_tuple[0]
                    #print("if block:", temp_source_node)
                    temp_sink_node = temp_tuple[1]
                    #print("if block:", temp_sink_node)
                elif temp_tuple[0].count('.') > temp_tuple[1].count('.'):
                    temp_source_node = temp_tuple[1]
                    #print("else block:", temp_source_node)
                    temp_sink_node = temp_tuple[0]
                    #print("else block:", temp_sink_node)
                temp_source_node = temp_source_node.replace(name_part_to_be_removed,'')
                temp_sink_node = temp_sink_node.replace(name_part_to_be_removed,'')
                tree_instance.add_edge(temp_source_node, temp_sink_node)

        for i in range(0, len(nodes)):
            temp_list = list(nodes[i])
            parent_node_of_subgraph = temp_list[len(temp_list)-1]
            if 'IE' in temp_list:
                if debug: print('subgraph', i, 'is the main graph')
            else:
                if debug: print('subgraph', i, 'is the removed from the tree')
                for k in range (0, len(temp_list)):
                    tree_instance.remove_node(temp_list[k])


    else: pass

    return tree_instance


def branch_deletion(branch_origin, tree_instance):   
    
    if tree_instance.has_node(branch_origin):

        print("Deleting the Event Tree branches originating form the Node: ", branch_origin)
    
        tree_instance.remove_node(branch_origin)

        if debug:
            B = nx.nx_agraph.to_agraph(tree_instance)
            B.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
            B.draw('temp_tree.svg')

        undirected_graph = tree_instance.to_undirected()
        sub_graphs = nx.connected_component_subgraphs(undirected_graph)
        nodes = []
        for i, sg in enumerate(sub_graphs):
            if debug: print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
            if debug: print("\tNodes:", sg.nodes())
            if debug: print("\tEdges:", sg.edges())
            nodes.append(sg.nodes())


        for i in range(0, len(nodes)):
            temp_list = list(nodes[i])
            if 'IE' in temp_list:
                if debug: print('subgraph', i, 'is the main graph')
            else:
                if debug: print('subgraph', i, 'is the removed from the tree')
                for k in range (0, len(temp_list)):
                    tree_instance.remove_node(temp_list[k])


    else: pass

    return tree_instance


def node_sort_extract(tree_instance):
    sorted_graph = nx.topological_sort(tree_instance)
    sorted_node_list = list(sorted_graph)
    return sorted_node_list


def branch_delete_loop(tree_instance, branch_origin_list):
    for i in range(0, len(branch_origin_list)):
        tree_instance = branch_deletion(branch_origin_list[i], tree_instance)
        #print("->", tree_instance)
    #print(tree_instance)
    return tree_instance


def node_delete_loop(tree_instance, node_list):
    for i in range(0, len(node_list)):
        tree_instance = node_deletion(node_list[i], tree_instance)
    return tree_instance



def end_node_extractor(tree_instance):
    return [x for x in tree_instance.nodes() if tree_instance.out_degree(x)==0 and tree_instance.in_degree(x)==1]


