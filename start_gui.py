from __future__ import print_function
from packages_etma import *
from tree_build_and_process import *




current_directory = os.getcwd()


def path_partitioning(path_probabilities, paths, tree):
    print("")
    print(datetime.datetime.now(),"(path_partitioning) Initiating the path partitioning")
    preselect = None #[0, 2, 4]
    msg = "Pick the Event Tree Paths to calculate the probability"
    title = "ETMA: Event Tree Path Partitioning"
    concatenated_path_list = []
    for i in range(0, len(paths)):
        concatenated = paths[i]+' ('+str(path_probabilities[i])+')'
        concatenated_path_list.append(concatenated)
    selected_paths = multchoicebox(msg, title, concatenated_path_list, preselect)
    if selected_paths == None:
        closing()
    else:
        partitioned_probabilities = []
        for i in range(0, len(selected_paths)):
            partitioned_probabilities.append(path_probabilities[concatenated_path_list.index(selected_paths[i])])

    print(sum(partitioned_probabilities))
    prob_sum = sum(partitioned_probabilities)
    choices = ['OK']
    title = 'Selected Path Probabilities'
    msg = str(selected_paths)+'\n'
    msg = msg+str(prob_sum)
    prob_display = buttonbox(msg, title, choices)
    path_partitioning(path_probabilities, paths, tree)




def probability_calculator(cplist, paths, tree):
    print("")
    print(datetime.datetime.now(),"(probability_calculator) Calculating the path probabilities")
    path_probabilities = []
    path_set = []
    #comp = [ x.encode('ascii', errors='replace') for x in cplist[0] ]
    comp = [ x.replace(" ", "") for x in cplist[0] ]
    #prob = [ x.encode('ascii', errors='replace') for x in cplist[1] ]
    prob = cplist[1]
    for i in range(0, len(prob)):
        prob[i] = float(prob[i])
    IE = float(1)
    for i in range(0, len(paths)):
        current_path = paths[i].split('.')
        #current_path = [ x.encode('ascii', errors='replace') for x in current_path ]
        path_set.append(current_path)
        for j in range (0, len(current_path)):
            if "IE" == current_path[j]:
                current_path[j] = IE
            else:
                current_path[j] = prob[comp.index(current_path[j])]
        probability = np.prod(current_path)
        path_probabilities.append(probability)

    path_partitioning(path_probabilities, paths, tree)
    return path_probabilities, paths





def probability_specifier(inp_list):
    
    components = [j for sub in inp_list for j in sub]  # flatten the 2d input list
    component_list = [component + ' --> \n' for component in components]
    joined_list_text = "".join(component_list)
    

    title = 'Assign state probabilities'
    msg = "Enter the probability for each component state, ending with a semicolon ';' \n"
    msg = msg+"\n"
    msg = msg+"Example: COMPONENT-STATE --> 0.5;\n"

    comp_prob_text = textbox(msg, title, joined_list_text)
    print("")
    print(comp_prob_text)

    if comp_prob_text == None:
        print(datetime.datetime.now(), "(probability_specifier) No state entered")
        welcomepage()
    
    title = "Confirm the system state probabilities\n"
    msg = comp_prob_text
    msg = msg+'\n'
    choices = ["OK", "RE-ENTER"]
    prob_confirm = buttonbox(msg, title, choices)  # confirm the states
    
    if prob_confirm == "RE-ENTER":
        print(datetime.datetime.now(),"(probability_specifier) component states RE-ENTRY")
        comp_probs = probability_specifier(inp_list)  # re-entry call
    
    if prob_confirm == None:
        print(datetime.datetime.now(), "(probability_specifier) selected cancel")
        welcomepage()
    
    if prob_confirm == "OK":
        print(datetime.datetime.now(), "(probability_specifier) selected OK")    
    
    cplist = process_component_state_probs(comp_prob_text, inp_list)

    return cplist
    
    
    

def process_component_state_probs(probs, input_list):
    
    if debug:
        getLineInfo()

    arrow_count = 0
    semicolon_count = 0

    # split the input text between the lines
    split_sys_info = probs.split('\n')
    for i in range(0, len(split_sys_info)):
        if '-->' in split_sys_info[i]:
            arrow_count = arrow_count+1
            if ';' in split_sys_info[i]:
                semicolon_count = semicolon_count+1
            else:
                print("SYNTAX ERROR in line, ", i, split_sys_info[i])
                component_state_prob_recall = True

    if arrow_count == semicolon_count:
        component_state_prob_recall = False
        states = []
        probs = []
        for i in range(0, split_sys_info.__len__()):
            states.append(find_between(split_sys_info[i], "", "-->"))
            prob = find_between(split_sys_info[i], "-->", ";")
            prob_nospace = prob.replace(" ", "")
            probs.append(prob_nospace)

        states = list(filter(None, states))  # remove empty elements
        probs = list(filter(None, probs))  # remove empty elements
        
    # add sanity checks for probabilities 

    if component_state_prob_recall == True:
        [states, probs] = probability_specifier(input_list)
        return [states, probs]
    else:
        return [states, probs]




def tree_reduction(tree):

    node_list = node_sort_extract(tree)
    preselect = None #[0, 2, 4]
    msg = "Pick the Branch(s) you wish to delete"
    title = "ETMA: Event Tree Branch Deletion"
    selected_branches = multchoicebox(msg, title, node_list[1:], preselect)
    if selected_branches == None:
        temp_tree1 = tree
    else:
        temp_tree1 = branch_delete_loop(tree, selected_branches)
    
    # Pass temp_tree1 to node deletion program

    reduced_node_list = node_sort_extract(temp_tree1)
    preselect = None #[0, 2, 4]
    msg = "Pick the Node(s) you wish to delete"
    title = "ETMA: Event Tree Node Deletion"
    selected_nodes = multchoicebox(msg, title, reduced_node_list[1:], preselect)
    if selected_nodes == None:
        temp_tree = temp_tree1
    else:
        temp_tree = node_delete_loop(temp_tree1, selected_nodes)
    
    draw_reduced_tree(temp_tree)

    return temp_tree # after node and branch reduction





def component_state_list_processor(comp_list, state_list):
    # print(comp_list)
    # print(state_list)

    master_state_list = []

    for i in range(0, len(comp_list)):
        current_element = comp_list[i]
        current_element_nospace = current_element.split()
        # print(current_element_nospace[0])
        local_list = []
        for j in range(0, len(state_list[i])):
            current_state = state_list[i][j]
            current_state_nospace = current_state.split()
            target = current_state_nospace[0]
            local_list.append(target)
            # print(current_state_nospace[0])
        master_state_list.append(local_list)
        # print("----")
    tree = event_tree_builder(master_state_list)
    title = "ETMA"
    msg = "Complete Event Tree Saved to 'complete_tree.svg'"
    reply = buttonbox(msg=msg, title=title, choices=['Reduce Event Tree', 'Continue with the complete Event Tree'], default_choice='Continue with the complete Event Tree')
    if reply == 'Reduce Event Tree':
        print(datetime.datetime.now(), "Reducing the Event Tree")
        tree = tree_reduction(tree)
        print(datetime.datetime.now(), "Assigning Probabilities for each state")
        cplist = probability_specifier(master_state_list)
        print(datetime.datetime.now(), "Extracting the paths in the Event Tree")
        paths = end_node_extractor(tree)
        
    else:
        print(datetime.datetime.now(), "Assigning Probabilities for each state")
        cplist = probability_specifier(master_state_list)
        print(datetime.datetime.now(), "Extracting the paths in the Event Tree")
        paths = end_node_extractor(tree)
    
    calculated_probabilities_list, path_list = probability_calculator(cplist, paths, tree)
    
        



def process_component_states(comps, sys_name, sys_info):
    print("")
    print("-----------------------")
    print("System Name: ", sys_name)
    print("-----------------------")
    print("System Component --> States")
    print("")
    print(sys_info)

    if debug:
        getLineInfo()

    arrow_count = 0
    semicolon_count = 0

    # split the input text between the lines
    split_sys_info = sys_info.split('\n')
    for i in range(0, len(split_sys_info)):
        if '-->' in split_sys_info[i]:
            arrow_count = arrow_count+1
            if ';' in split_sys_info[i]:
                semicolon_count = semicolon_count+1
            else:
                print("SYNTAX ERROR in line, ", i, split_sys_info[i])
                component_state_recall = True

    if arrow_count == semicolon_count:
        component_state_recall = False
        components = []
        all_states = []
        for i in range(0, split_sys_info.__len__()):
            components.append(find_between(split_sys_info[i], "", "-->"))
            states = find_between(split_sys_info[i], "-->", ";")
            states_nospace = states.replace(" ", "")
            states_list = states.split(",")
            states_list = list(filter(None, states_list)
                               )  # remove empty elements
            all_states.append(states_list)

        components = list(filter(None, components))  # remove empty elements
        all_states = list(filter(None, all_states))  # remove empty elements
        component_state_list_processor(components, all_states)

    if component_state_recall == True:
        get_component_states(sys_info, "", False)


def get_component_states(components, system_name, first_run=True):
    if first_run == True:
        component_list = [component + ' --> \n' for component in components]
        joined_list_text = "".join(component_list)
    else:
        joined_list_text = components
    msg = "Enter the states for each component, ending with a semicolon ';' \n"
    msg = msg+"\n"
    msg = msg+"Example: COMPONENT --> STATE1, STATE2, STATE3;\n"
    title = "State entery for the components"
    system_info_text = textbox(msg, title, joined_list_text)
    if system_info_text == None:
        print(datetime.datetime.now(), "(get_component_states) No state entered")
        if debug:
            getLineInfo()
        welcomepage()
    title = "Confirm the system states\n"
    msg = system_info_text
    msg = msg+'\n'
    choices = ["OK", "RE-ENTER"]
    states_confirm = buttonbox(msg, title, choices)  # confirm the states
    if states_confirm == "RE-ENTER":
        print(datetime.datetime.now(),
              "(get_component_states) component states RE-ENTRY")
        if debug:
            getLineInfo()
        system_components = get_component_states(components, system_name)  # re-entry call
    if states_confirm == None:
        print(datetime.datetime.now(), "(get_component_states) selected cancel")
        if debug:
            getLineInfo()
        welcomepage()
    if states_confirm == "OK":
        print(datetime.datetime.now(), "(get_component_states) selected OK")
        if debug:
            getLineInfo()
    process_component_states(components, system_name, system_info_text)
    return system_info_text


def get_system_components(msg1, system_name):  # gets system components
    msg = "Please specify the components in the system.\n"
    msg = msg+"Avoid spaces in component names.\n"
    msg = msg+"\n"
    msg = msg+"eg: component1, component2, component3"
    msg = msg1 + "\n" + msg
    system_components = enterbox(msg)
    if system_components == "":  # dosent allow null system
        print(datetime.datetime.now(),
              "(get_system_components) Null component entry")
        msg = "System cannot have NULL components. \n"
        msg = msg+"\n"
        msg = msg+"Please enter your system components \n"
        system_components = get_system_components(msg, system_name)
    if system_components == None:  # selected cancel
        print(datetime.datetime.now(), "(get_system_components) selected cancel")
        if debug:
            getLineInfo()
        welcomepage()
    else:  # a valid system components are entered
        components = system_components.replace(
            " ", "").split(",")  # split between commas
        components = list(filter(None, components))  # removes empty components
        print(datetime.datetime.now(), "(get_system_components) system components:", components)
        if debug:
            getLineInfo()
        msg = "Entered system components:\n"
        msg = system_components+"\n"
        choices = ["OK", "RE-ENTER"]
        title = "Confirm System Components"
        components_confirm = buttonbox(
            components, title, choices)  # confirm the components
        print(datetime.datetime.now(),
              "(get_system_components) selected:", components_confirm)
        if debug:
            getLineInfo()
        if components_confirm == "RE-ENTER":
            system_components = get_system_components(
                "RE-ENTERY \n", system_name)  # re-entry call
            components = system_components.replace(
                " ", " ").split(",")  # split between commas
            # removes empty components
            components = list(filter(None, components))
        get_component_states(components, system_name, True)
        closing()
    return components




def start_etma_analysis(message):  # gets system name
    system_name_entered = enterbox(message)
    if system_name_entered == "":  # dosent allow empty system name
        print(datetime.datetime.now(),
              "(start_etma_analysis) Empty system name entry")
        if debug:
            getLineInfo()
        msg = "System name cannot be empty. \n"
        msg = msg+"\n"
        msg = msg+"Please enter your system name \n"
        system_name_entered = start_etma_analysis(msg)
        pass
    if system_name_entered == None:  # selected cancel
        print(datetime.datetime.now(), "(start_etma_analysis) selected cancel")
        if debug:
            getLineInfo()
        welcomepage()
    else:  # a valid system name is entered
        print(datetime.datetime.now(),
              "(start_etma_analysis) System Name:", system_name_entered)
        if debug:
            getLineInfo()
        get_system_components("", system_name_entered)  # get system components
    return system_name_entered


def start_fetma_analysis(message):  # gets system name
    system_name_entered = enterbox(message)
    if system_name_entered == "":  # dosent allow empty system name
        print(datetime.datetime.now(),
              "(start_fetma_analysis) Empty system name entry")
        if debug:
            getLineInfo()
        msg = "System name cannot be empty. \n"
        msg = msg+"\n"
        msg = msg+"Please enter your system name \n"
        system_name_entered = start_fetma_analysis(msg)
        pass
    if system_name_entered == None:  # selected cancel
        print(datetime.datetime.now(), "(start_fetma_analysis) selected cancel")
        if debug:
            getLineInfo()
        welcomepage()
    else:  # a valid system name is entered
        print(datetime.datetime.now(),
              "(start_fetma_analysis) System Name:", system_name_entered)
        if debug:
            getLineInfo()
        get_function_blocks("", system_name_entered)  # get system components
    return system_name_entered


def closing():
    msg = "Developed at HVG Lab, Concordia University.\n"
    msg = msg+"Montreal, QC, Canada.\n"
    msg = msg+"\n"
    msg = msg+"Developers: Sowmith Nethula, Mohamed Wagdy Abdelghany\n"
    msg = msg+"Supervisor: Prof. Dr. Sofiene Tahar\n"
    msgbox(msg, '')
    exit(0)


def welcomepage():
    msg = "-------------------------------------------------------------\n"
    msg = msg+"- Welcome to Functional Block Diagram and Event Tree Modelling and Analysis (FETMA) Software Tool. -\n"
    msg = msg+"-------------------------------------------------------------\n"
    msg = msg+"\n"
    msg = msg+"\n"
    msg = msg+"\n"
    msg = msg+"Click 'OK' and follow the steps as we guide you through the process. \n"
    msg = msg+"Click 'HELP' for documentation\n"
    msg = msg+"Click 'EXIT' to close. \n"
    msg = msg+"\n"
    msg = msg+"\n"
    #msg = msg+"* If you have generated a config file earlier, select 'Load Config'\n"
    msg = msg+"\n"
    msg = msg+"\n"
    title = "FBD-ETMA"
    choices = ["FBD", "ET", "EXIT", "HELP"]
    choice = buttonbox(msg, title, choices)
    if choice == 'ET':
        print(datetime.datetime.now(), "(welcome page) selected ET")
        start_etma_analysis("Please enter your system name")
    elif choice == 'FBD':
        print(datetime.datetime.now(), "(welcome page) selected FBD")
        start_fetma_analysis("Please enter your system name")
    elif choice == 'EXIT':
        print(datetime.datetime.now(), "(welcome page) Selected EXIT")
        print("Thank You")
        closing()
        exit(0)
    elif choice == 'HELP':
        print(datetime.datetime.now(), "(welcome page) Selected HELP")
        helppage()
    elif choice == '*Load Config':
        print(datetime.datetime.now(), "(welcome page) Selected *Load Config")
        f = loadconfig()
        if f == None:
            welcomepage()
        else:
            finalbox()





################ FETMA LAYER

def get_function_blocks(msg1, system_name):  # gets function blocks
    msg = "Please specify the Functional Blocks (FBs) in the system.\n"
    msg = msg+"Avoid spaces in FB names.\n"
    msg = msg+"\n"
    msg = msg+"eg: FB1, FB2, FB3"
    msg = msg1 + "\n" + msg
    function_blocks = enterbox(msg)
    if function_blocks == "":  # dosent allow null system
        print(datetime.datetime.now(),
              "(get_function_blocks) Null component entry")
        msg = "Function blocks cannot be Null. \n"
        msg = msg+"\n"
        msg = msg+"Please enter your function_blocks \n"
        function_blocks = get_function_blocks(msg, system_name)
    if function_blocks == None:  # selected cancel
        print(datetime.datetime.now(), "(get_function_blocks) selected cancel")
        if debug:
            getLineInfo()
        welcomepage()
    else:  # a valid function_blocks are entered
        blocks = function_blocks.replace(
            " ", "").split(",")  # split between commas
        blocks = list(filter(None, blocks))  # removes empty FBs
        print(datetime.datetime.now(), "(get_function_blocks) function_blocks:", blocks)
        if debug:
            getLineInfo()
        msg = "Entered function_blocks:\n"
        msg = function_blocks+"\n"
        choices = ["OK", "RE-ENTER"]
        title = "Confirm function_blocks"
        blocks_confirm = buttonbox(
            blocks, title, choices)  # confirm the FBs
        print(datetime.datetime.now(),
              "(get_function_blocks) selected:", blocks_confirm)
        if debug:
            getLineInfo()
        if blocks_confirm == "RE-ENTER":
            function_blocks = get_function_blocks(
                "RE-ENTERY \n", system_name)  # re-entry call
            blocks = function_blocks.replace(
                " ", " ").split(",")  # split between commas
            # removes empty FBs
            blocks = list(filter(None, blocks))
        #get_component_states(components, system_name, True) ///// get compinents for each block instead
        ## now get system components for each block
        recieve_function_blocks(blocks, system_name)
        closing()
    return blocks

enable_path_partitioning = 0 # Global variable

def recieve_function_blocks(block_list, system_name):
    print("Recieved blocks: ", block_list)
    end_node_list = []
    end_node_prob_list = []
    global enable_path_partitioning

    if debug:
        getLineInfo()

    for i in range(0, block_list.__len__()):

        if i == block_list.__len__()-1:
            enable_path_partitioning = 1

        print("================================================")
        print("Getting FB system components for ", block_list[i])
        if (i == 0):
            prob_end_nodes_for_fb, end_nodes_for_fb = get_FB_system_components(block_list[i], system_name)
            print("RECIEVE: End nodes for ", block_list[i], "-->", process_end_nodes(end_nodes_for_fb))
            print("RECIEVE: Probabilities for end nodes of", block_list[i], "-->", prob_end_nodes_for_fb)
        else:
            print("SEND: End nodes for ", block_list[i], "-->", process_end_nodes(end_nodes_for_fb))
            print("SEND: Probabilities for end nodes of", block_list[i], "-->", prob_end_nodes_for_fb)
            prob_end_nodes_for_fb, end_nodes_for_fb = get_FB_system_components(block_list[i], system_name, prob_end_nodes_for_fb, process_end_nodes(end_nodes_for_fb))
            print("RECIEVE: End nodes for ", block_list[i], "-->", process_end_nodes(end_nodes_for_fb))
            print("RECIEVE: Probabilities for end nodes of", block_list[i], "-->", prob_end_nodes_for_fb)


def process_end_nodes(inp_end_nodes_list):
    processed_end_nodes = []
    for i in range(0, inp_end_nodes_list.__len__()):
        temp_end_node1 = inp_end_nodes_list[i].replace("IE.","")
        temp_end_node2 = temp_end_node1.replace(".","-")
        #print(temp_end_node2)
        processed_end_nodes.append(temp_end_node2)
    return processed_end_nodes
        



def get_FB_system_components(msg1, system_name, end_nodes_probabilities=None, end_nodes_paths=None):  # gets system components
    function_block_name = msg1
    msg = "Please specify the components in the Functional Block (FB): "+msg1+".\n"
    msg = msg+"Avoid spaces in component names.\n"
    msg = msg+"\n"
    msg = msg+"eg: component1, component2, component3"
    system_components = enterbox(msg)
    if system_components == "":  # dosent allow null system
        print(datetime.datetime.now(),
              "(get_FB_system_components) Null component entry")
        msg = "System cannot have NULL components. \n"
        msg = msg+"\n"
        msg = msg+"Please enter your FB system components \n"
        system_components = get_FB_system_components(msg, system_name, end_nodes_probabilities, end_nodes_paths)
    if system_components == None:  # selected cancel
        print(datetime.datetime.now(), "(get_FB_system_components) selected cancel")
        if debug:
            getLineInfo()
        welcomepage()
    else:  # a valid system components are entered
        components = system_components.replace(
            " ", "").split(",")  # split between commas
        components = list(filter(None, components))  # removes empty components
        print(datetime.datetime.now(), "(get_FB_system_components) system components:", components)
        if debug:
            getLineInfo()
        msg = "Entered system components:\n"
        msg = system_components+"\n"
        choices = ["OK", "RE-ENTER"]
        title = "Confirm System Components"
        components_confirm = buttonbox(
            components, title, choices)  # confirm the components
        print(datetime.datetime.now(),
              "(get_FB_system_components) selected:", components_confirm)
        if debug:
            getLineInfo()
        if components_confirm == "RE-ENTER":
            system_components = get_FB_system_components(
                "RE-ENTERY \n", system_name, end_nodes_probabilities, end_nodes_paths)  # re-entry call
            components = system_components.replace(
                " ", " ").split(",")  # split between commas
            # removes empty components
            components = list(filter(None, components))
        calculated_probabilities_list, path_list = get_FB_component_states(components, system_name, function_block_name, end_nodes_probabilities, end_nodes_paths, True)
        #closing()
    return calculated_probabilities_list, path_list




def get_FB_component_states(components, system_name, function_block_name, end_nodes_probabilities=None, end_nodes_paths=None, first_run=True):
    # capture previous edge nodes and theit probabilities
    if first_run == True:
        component_list = [component + ' --> \n' for component in components]
        joined_list_text = "".join(component_list)
    else:
        joined_list_text = components
    
    if end_nodes_paths != None:
        line="previous_FBs_out --> "
        for i in range(0, end_nodes_paths.__len__()):
            if(i != end_nodes_paths.__len__()-1):
                line = line+str(end_nodes_paths[i])+str(",")
            else:
                line = line+str(end_nodes_paths[i])+str(";")
        #print(line) # add this to joined_list_text
        joined_list_text = line+"\n"+joined_list_text

    msg = "Enter the states for each component, ending with a semicolon ';' \n"
    msg = msg+"\n"
    msg = msg+"Example: COMPONENT --> STATE1, STATE2, STATE3;\n"
    title = "State entery for the components"
    system_info_text = textbox(msg, title, joined_list_text)
    if system_info_text == None:
        print(datetime.datetime.now(), "(get_FB_component_states) No state entered")
        if debug:
            getLineInfo()
        welcomepage()
    title = "Confirm the system states\n"
    msg = system_info_text
    msg = msg+'\n'
    choices = ["OK", "RE-ENTER"]
    states_confirm = buttonbox(msg, title, choices)  # confirm the states
    if states_confirm == "RE-ENTER":
        print(datetime.datetime.now(),
              "(get_FB_component_states) component states RE-ENTRY")
        if debug:
            getLineInfo()
        system_components = get_FB_component_states(components, system_name, function_block_name, end_nodes_probabilities, end_nodes_paths)  # re-entry call
    if states_confirm == None:
        print(datetime.datetime.now(), "(get_FB_component_states) selected cancel")
        if debug:
            getLineInfo()
        welcomepage()
    if states_confirm == "OK":
        print(datetime.datetime.now(), "(get_FB_component_states) selected OK")
        if debug:
            getLineInfo()
    calculated_probabilities_list, path_list = process_FB_component_states(components, system_name, system_info_text, end_nodes_probabilities, end_nodes_paths)
    return calculated_probabilities_list, path_list




def process_FB_component_states(comps, sys_name, sys_info, end_nodes_probabilities, end_nodes_paths):
    print("")
    print("-----------------------")
    print("System Name: ", sys_name)
    print("-----------------------")
    print("System Component --> States")
    print("")
    print(sys_info)

    if debug:
        getLineInfo()

    arrow_count = 0
    semicolon_count = 0

    # split the input text between the lines
    split_sys_info = sys_info.split('\n')
    for i in range(0, len(split_sys_info)):
        if '-->' in split_sys_info[i]:
            arrow_count = arrow_count+1
            if ';' in split_sys_info[i]:
                semicolon_count = semicolon_count+1
            else:
                print("SYNTAX ERROR in line, ", i, split_sys_info[i])
                component_state_recall = True

    if arrow_count == semicolon_count:
        component_state_recall = False
        components = []
        all_states = []
        for i in range(0, split_sys_info.__len__()):
            components.append(find_between(split_sys_info[i], "", "-->"))
            states = find_between(split_sys_info[i], "-->", ";")
            states_nospace = states.replace(" ", "")
            states_list = states.split(",")
            states_list = list(filter(None, states_list)
                               )  # remove empty elements
            all_states.append(states_list)

        components = list(filter(None, components))  # remove empty elements
        all_states = list(filter(None, all_states))  # remove empty elements
        calculated_probabilities_list, path_list = FB_component_state_list_processor(components, all_states, end_nodes_probabilities, end_nodes_paths)

    if component_state_recall == True:
        get_FB_component_states(sys_info, "", function_block_name, end_nodes_probabilities, end_nodes_paths, False)

    return calculated_probabilities_list, path_list


def FB_component_state_list_processor(comp_list, state_list, end_nodes_probabilities, end_nodes_paths):
    #print(comp_list)
    #print(state_list)

    master_state_list = []

    for i in range(0, len(comp_list)):
        current_element = comp_list[i]
        current_element_nospace = current_element.split()
        # print(current_element_nospace[0])
        local_list = []
        for j in range(0, len(state_list[i])):
            current_state = state_list[i][j]
            current_state_nospace = current_state.split()
            target = current_state_nospace[0]
            local_list.append(target)
            # print(current_state_nospace[0])
        master_state_list.append(local_list)
        # print("----")
    tree = event_tree_builder(master_state_list)
    title = "ETMA"
    msg = "Complete Event Tree Saved to 'complete_tree.svg'"
    reply = buttonbox(msg=msg, title=title, choices=['Reduce Event Tree', 'Continue with the complete Event Tree'], default_choice='Continue with the complete Event Tree')
    if reply == 'Reduce Event Tree':
        print(datetime.datetime.now(), "Reducing the Event Tree")
        tree = tree_reduction(tree)
        print(datetime.datetime.now(), "Assigning Probabilities for each state")
        cplist = FB_probability_specifier(master_state_list, end_nodes_probabilities, end_nodes_paths)
        print(datetime.datetime.now(), "Extracting the paths in the Event Tree")
        paths = end_node_extractor(tree)
        
    else:
        print(datetime.datetime.now(), "Assigning Probabilities for each state")
        cplist = FB_probability_specifier(master_state_list, end_nodes_probabilities, end_nodes_paths)
        print(datetime.datetime.now(), "Extracting the paths in the Event Tree")
        paths = end_node_extractor(tree)
    
    calculated_probabilities_list, path_list = FB_probability_calculator(cplist, paths, tree)
    #print("calculated_probabilities_list: ", calculated_probabilities_list)
    #print("path_list: ", path_list)
    return calculated_probabilities_list, path_list 




def FB_probability_specifier(inp_list, end_nodes_probabilities, end_nodes_paths):
    
    if end_nodes_probabilities != None:
        temp_prev_fb_out_list = []
        temp_prev_fb_out_list = inp_list[0]
        #print(temp_prev_fb_out_list)
        inp_list.pop(0) # remove 0th index because we will write them below anyway

    components = [j for sub in inp_list for j in sub]  # flatten the 2d input list
    component_list = [component + ' --> \n' for component in components]
    joined_list_text = "".join(component_list)

    if end_nodes_probabilities != None:
        line = ""
        for i in range(0, end_nodes_probabilities.__len__()):
            #print(temp_prev_fb_out_list[i], "-->", end_nodes_probabilities[i]) # 0th index has inp from previous FB
            line = line+str(temp_prev_fb_out_list[i])+" --> "+str(end_nodes_probabilities[i])+";"+"\n"
        joined_list_text = line+joined_list_text
    

    title = 'Assign state probabilities'
    msg = "Enter the probability for each component state, ending with a semicolon ';' \n"
    msg = msg+"\n"
    msg = msg+"Example: COMPONENT-STATE --> 0.5;\n"

    comp_prob_text = textbox(msg, title, joined_list_text)
    print("")
    print(comp_prob_text)

    if comp_prob_text == None:
        print(datetime.datetime.now(), "(probability_specifier) No state entered")
        welcomepage()
    
    title = "Confirm the system state probabilities\n"
    msg = comp_prob_text
    msg = msg+'\n'
    choices = ["OK", "RE-ENTER"]
    prob_confirm = buttonbox(msg, title, choices)  # confirm the states
    
    if prob_confirm == "RE-ENTER":
        print(datetime.datetime.now(),"(probability_specifier) component states RE-ENTRY")
        comp_probs = probability_specifier(inp_list)  # re-entry call
    
    if prob_confirm == None:
        print(datetime.datetime.now(), "(probability_specifier) selected cancel")
        welcomepage()
    
    if prob_confirm == "OK":
        print(datetime.datetime.now(), "(probability_specifier) selected OK")    
    
    cplist = process_component_state_probs(comp_prob_text, inp_list)

    return cplist
    
 


        
def FB_probability_calculator(cplist, paths, tree):
    print("")
    print(datetime.datetime.now(),"(FB_probability_calculator) Calculating the path probabilities")
    path_probabilities = []
    path_set = []
    #comp = [ x.encode('ascii', errors='replace') for x in cplist[0] ]
    comp = [ x.replace(" ", "") for x in cplist[0] ]
    #prob = [ x.encode('ascii', errors='replace') for x in cplist[1] ]
    prob = cplist[1]
    for i in range(0, len(prob)):
        prob[i] = float(prob[i])
    IE = float(1)
    for i in range(0, len(paths)):
        current_path = paths[i].split('.')
        #current_path = [ x.encode('ascii', errors='replace') for x in current_path ]
        path_set.append(current_path)
        for j in range (0, len(current_path)):
            if "IE" == current_path[j]:
                current_path[j] = IE
            else:
                current_path[j] = prob[comp.index(current_path[j])]
        probability = np.prod(current_path)
        path_probabilities.append(probability)

    print("enable_path_partitioning: ", enable_path_partitioning)
    if enable_path_partitioning == 1:
        path_partitioning(path_probabilities, paths, tree) # Move to the final part

    return path_probabilities, paths



def fetma_gui_entry():
    print(datetime.datetime.now(), "FBD-ETMA GUI START")
    welcomepage()


fetma_gui_entry()

