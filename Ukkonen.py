end_pointer = -1

class Node:
    
    def __init__(self, start_index_from_parent_edge = None, non_leaf_end_index_from_parent_edge = None, suffix_linked_towards = None, is_a_leaf_node = False):
        self.children = []
        self.start_index_from_parent_edge = start_index_from_parent_edge
        self.non_leaf_end_index_from_parent_edge = non_leaf_end_index_from_parent_edge #Will be instanteneously replaced by end_pointer if this is a leaf. See __getattr__
        self.suffix_linked_towards = suffix_linked_towards
        self.is_a_leaf_node = is_a_leaf_node #once a leaf, always a leaf
        self.termination_characters_following_this_node = set() #this will be used for the longest common substring

    def __getattr__(self, attribute): #python seems to read this as :if you ask me for an attribute I don't have, do this do this stuff instead
        if attribute == 'end_index_from_parent_edge':
            if self.is_a_leaf_node:
                return end_pointer #If I ask for the end_index_from_parent_edge of a leaf node, please give me end_pointer instead. Has the same effect as updating each leaf everytime we increment end_pointer, but this is O(1)
        return self.non_leaf_end_index_from_parent_edge # If it isn't a leaf, just give me its regular edge label!

    def create_child(self, start_index_from_parent_edge, end_index_from_parent_edge = None, suffix_linked_towards = None, is_a_leaf_node = False, return_child = False): #still return child in paces, even though its unnecessary
        child = Node(start_index_from_parent_edge, end_index_from_parent_edge, suffix_linked_towards, is_a_leaf_node)
        self.children.append(child)
        if return_child:
            return child

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def suffix_link_to(self, node_to_be_suffix_linked_to):
        self.suffix_linked_towards = node_to_be_suffix_linked_to

    def get_all_first_character_indices_of_edges_to_children(self):
        first_character_indices = []
        for child in self.children:
            first_character_indices.append(child.start_index_from_parent_edge)
        return first_character_indices
    
    def get_child_at_end_of_edge_with_given_first_character_index(self, string, first_character_index):
        first_character = string[first_character_index]
        for child in self.children:
            if string[child.start_index_from_parent_edge] == first_character:
                return child
        raise Exception("No child has that first letter on its edge")
    
    def get_edge_length(self, string, index_of_first_character_of_edge):
        child = self.get_child_at_end_of_edge_with_given_first_character_index(string, index_of_first_character_of_edge)
        return child.end_index_from_parent_edge + 1 - child.start_index_from_parent_edge
    
    def debug_this_node(self):
        for child in self.children:
            print(child.start_index_from_parent_edge, child.end_index_from_parent_edge, 'is a leaf =', child.is_a_leaf_node)

def ukkonen(string, debug = False, i_want_to_test_if_this_results_in_the_same_tree_as_something_else = False, return_root = False):

    def perform_extension():
        if active_point['Active Length'] == 0:
            execute_active_point_change_for_active_length_is_zero()
        if active_node_has_active_edge_coming_out_of_it():
            walk_down_if_necessary()
            if active_point_is_followed_by_current_character():
                excecute_extension_rule_3()
            else:
                execute_extension_rule_2()
        else:
            execute_extension_rule_2()

    def walk_down_if_necessary():
        #the first part of this 'and' statement makes sure I don't check for the length of an edge that doesn't exist. Not the prettiest, but can't think of a pretty solution
        while active_point['Active Length'] != 0 and active_point['Active Length'] >= active_point["Active Node"].get_edge_length(string, active_point['Active Edge Index']):
            execute_active_point_change_for_walk_down()
        stuff_to_keep_track_of['total length walked down so far'] = 0 #reset memory of how far down we have walked

    def active_node_has_active_edge_coming_out_of_it():
        indices = active_point['Active Node'].get_all_first_character_indices_of_edges_to_children()
        characters = turn_list_of_indices_into_list_of_characters(indices) # I think it's necessary to turn things into characters first, because the indices could be different with the letters the same
        return string[active_point['Active Edge Index']] in characters
    
    def active_point_is_followed_by_current_character():
        current_character = string[end_pointer]
        first_character_indices = active_point['Active Node'].get_all_first_character_indices_of_edges_to_children()
        for index in first_character_indices:
            if string[index] == string[active_point['Active Edge Index']]:
                return string[index + active_point['Active Length']] == current_character
        #If we get here, I think we may as well return false. I think this happens due to the confusuion of what active edge should be after we walk down. Not pretty, but it ain't broke, so I won't fix it
        return False
    
    def execute_extension_rule_2():
        if active_point['Active Length'] == 0:
            execute_extension_rule_2_new_leaf_only()
        else:
            execute_extension_rule_2_with_new_internal_node()

    def execute_extension_rule_2_new_leaf_only():
        active_point['Active Node'].create_child(end_pointer, is_a_leaf_node = True)
        execute_active_point_change_for_extension_rule_2()

    def execute_extension_rule_2_with_new_internal_node():
        node_whose_parent_edge_we_are_splitting = active_point['Active Node'].get_child_at_end_of_edge_with_given_first_character_index(string, active_point['Active Edge Index'])
        new_internal_node = create_and_return_new_internal_node(node_whose_parent_edge_we_are_splitting)
        stuff_to_keep_track_of['recently created internal nodes'].append(new_internal_node)
        reorganise_parent_child_edges_for_extension_rule_2(node_whose_parent_edge_we_are_splitting, new_internal_node) #this also creates the last child, which isn't really indicated by the name
        execute_active_point_change_for_extension_rule_2()

    def excecute_extension_rule_3():
        execute_active_point_change_for_extension_rule_3()
        stuff_to_keep_track_of['rule 3 was just executed'] = True

    def execute_active_point_change_for_active_length_is_zero():
        active_point['Active Edge Index'] = end_pointer

    def execute_active_point_change_for_extension_rule_2():
        if active_point['Active Node'] == root:
            if active_point['Active Length'] == 0:
                execute_active_point_change_for_active_length_is_zero()
            else:
                execute_active_point_change_for_extension_rule_2_when_active_node_is_root()
        else:
            execute_active_point_change_for_extension_rule_2_when_active_node_is_not_root()

    def execute_active_point_change_for_extension_rule_2_when_active_node_is_root():
        active_point['Active Length'] -= 1
        active_point['Active Edge Index'] = end_pointer - remaining_suffix_count + 2

    def execute_active_point_change_for_extension_rule_2_when_active_node_is_not_root():
        #if successful, split this into two functions?
        #maybe sometimes we need to walk down several times
        if active_point['Active Node'].suffix_linked_towards != root: 
            follow_suffix_link()
        else:
            adjust_active_point_via_root()

    def follow_suffix_link():
        active_point["Active Node"] = active_point['Active Node'].suffix_linked_towards

    def adjust_active_point_via_root(): #When 'suffix linked' to root, we don't have the same nice relationships as we do with 2 internal nodes suffix linked. Have to be more careful about how to update active point
            index_of_first_character_we_were_inserting = end_pointer - remaining_suffix_count + 1
            index_of_first_character_we_now_want_to_insert = index_of_first_character_we_were_inserting + 1 #because we've done the last one
            length_of_string_we_were_inserting = end_pointer - index_of_first_character_we_were_inserting
            active_point['Active Length'] = length_of_string_we_were_inserting - 1
            active_point["Active Node"] = active_point['Active Node'].suffix_linked_towards
            active_point['Active Edge Index'] = index_of_first_character_we_now_want_to_insert

    def execute_active_point_change_for_extension_rule_3():
        active_point['Active Length'] += 1

    def execute_active_point_change_for_walk_down():
        length_of_edge_to_walk_down = active_point["Active Node"].get_edge_length(string, active_point["Active Edge Index"]) #maybe calculate this at the start of the function
        active_point['Active Node'] = active_point['Active Node'].get_child_at_end_of_edge_with_given_first_character_index(string, active_point['Active Edge Index'])
        active_point['Active Edge Index'] += length_of_edge_to_walk_down
        active_point['Active Length'] -= length_of_edge_to_walk_down
        # keep track of how far down we have walked so we know what we should change active edge to as we walk down several nodes
        stuff_to_keep_track_of['total length walked down so far'] += length_of_edge_to_walk_down

    def reorganise_parent_child_edges_for_extension_rule_2(node_whose_parent_edge_we_are_splitting, new_internal_node):
        active_point['Active Node'].remove_child(node_whose_parent_edge_we_are_splitting)
        new_internal_node.add_child(node_whose_parent_edge_we_are_splitting)
        node_whose_parent_edge_we_are_splitting.start_index_from_parent_edge += active_point['Active Length']
        new_internal_node.create_child(end_pointer, is_a_leaf_node = True)

    def turn_list_of_indices_into_list_of_characters(list_of_indices):
        list_of_characters = []
        for index in list_of_indices:
            list_of_characters.append(string[index])
        return list_of_characters

    def create_and_return_new_internal_node(node_whose_parent_edge_we_are_splitting):
        new_internal_node_start_index = node_whose_parent_edge_we_are_splitting.start_index_from_parent_edge
        new_internal_node_end_index = new_internal_node_start_index + active_point['Active Length'] - 1
        return active_point['Active Node'].create_child(new_internal_node_start_index, new_internal_node_end_index, return_child = True)


    def create_suffix_links_between_internal_nodes():
        for i in range(len(stuff_to_keep_track_of["recently created internal nodes"]) - 1):
            stuff_to_keep_track_of['recently created internal nodes'][i].suffix_link_to(stuff_to_keep_track_of['recently created internal nodes'][i + 1])
        stuff_to_keep_track_of['recently created internal nodes'][-1].suffix_link_to(root)

    def debug_tree():
        print(' ')
        print('phase index', phase_index, 'remaining_suffix_count', remaining_suffix_count)
        print('root:')
        root.debug_this_node()
        print('children:')
        for child in root.children:
            child.debug_this_node()
        print('grandchildren:')
        for child in root.children:
            for grandchild in child.children:
                grandchild.debug_this_node()
        print("active node:", active_point['Active Node'].start_index_from_parent_edge, active_point['Active Node'].end_index_from_parent_edge, "   active edge:", string[active_point['Active Edge Index']], "   active length:", active_point['Active Length'])

    def assign_root_a_number_to_test_if_it_is_the_same_as_something_else():
        #just get some number to identify the tree. Collisions are ok. Really arbitrary
        number = 0
        for child in root.children:
            number += child.start_index_from_parent_edge + child.end_index_from_parent_edge
            for grandchild in child.children:
                number += grandchild.start_index_from_parent_edge + grandchild.end_index_from_parent_edge
        return number

    #actual execution of algorithm starts here
    global end_pointer
    root = Node(is_a_leaf_node = False)
    active_point = {
        'Active Node' : root,
        'Active Edge Index' : 0,
        'Active Length' : 0
    }
    remaining_suffix_count = 0
    stuff_to_keep_track_of = {"rule 3 was just executed" : False,
             "recently created internal nodes" : [],
             "total length walked down so far" : 0}

    for phase_index in range(len(string)):
        end_pointer += 1
        remaining_suffix_count += 1
        if len(stuff_to_keep_track_of["recently created internal nodes"]) != 0:
            create_suffix_links_between_internal_nodes()
            stuff_to_keep_track_of["recently created internal nodes"] = []
        while remaining_suffix_count != 0:
            perform_extension()
            if debug:
                debug_tree()
            if stuff_to_keep_track_of["rule 3 was just executed"]:
                stuff_to_keep_track_of['rule 3 was just executed'] = False
                break
            remaining_suffix_count -= 1

    if i_want_to_test_if_this_results_in_the_same_tree_as_something_else:
        return assign_root_a_number_to_test_if_it_is_the_same_as_something_else()
    
    if return_root:
        return root
               
def find_longest_common_substring(strings, termination_characters):

    def create_mega_string(strings, termination_characters):
        if len(strings) > len(termination_characters):
            raise Exception("You haven't provided enough terminating characters for this many strings")
        else:
            mega_string = ''
            for i in range(len(strings)):
                mega_string += strings[i]
                mega_string += termination_characters[i]
        return mega_string

    def get_all_terminating_characters_following_node(node, termination_characters):
        if node.is_a_leaf_node:
            return find_first_terminating_character_on_parent_edge(node, termination_characters)
        else:
            termination_characters_following_this_node = set()
            for child in node.children:
                termination_characters_following_this_node.update(get_all_terminating_characters_following_node(child, termination_characters))
            node.termination_characters_following_this_node = termination_characters_following_this_node
            return termination_characters_following_this_node

    def find_first_terminating_character_on_parent_edge(node, termination_characters):
        for i in range(node.start_index_from_parent_edge, node.end_index_from_parent_edge + 1):
            if mega_string[i] in termination_characters:
                return set(mega_string[i]) #return as a 1 element set so it can be smoothly added to the set of following termination characters of its parent node
        raise Exception("this edge doesn't appear to have a terminating character on it")
    
    def find_longest_common_string_from_node(node): #doesn't consider terminating characters yet
        longest = ''
        for child in node.children:
            if len(child.termination_characters_following_this_node) == number_of_termination_characters_used:
                edge_string = mega_string[child.start_index_from_parent_edge : child.end_index_from_parent_edge + 1]
                longest_from_grandchildren = find_longest_common_string_from_node(child)
                longest_from_child = edge_string + longest_from_grandchildren
                if len(longest_from_child) > len(longest):
                    longest = longest_from_child
        return longest

    #algorithm starts here
    mega_string = create_mega_string(strings, termination_characters)
    root = ukkonen(mega_string, return_root = True)
    get_all_terminating_characters_following_node(root, termination_characters)
    number_of_termination_characters_used = len(strings)
    return find_longest_common_string_from_node(root)

#a few test cases to make sure any changes don't break the algorithm
tests = {
"abdabaaaacdf$" : 178,
"abcdab$" : 72,
"abxxa$" : 53,
"abxxc$" : 51,
"abcabxabcd$" : 131, #double checked
"abcabaa$" : 75,
"abcdabaacdefg$" : 268,
"atgcatcgtagct$" : 234,
"cagacgagac$" : 112, #double checked
"cgcacgacgc$" : 120, #double checked except for great grandkids
"ccacagccac$" : 88, #double checked except for great grandkids
"actttatttaa$" : 126 #double checked except for great grandkids
}

def i_have_not_broken_ukkonen(tests):
    for test_string in tests:
        reset_end_pointer()
        if ukkonen(test_string, i_want_to_test_if_this_results_in_the_same_tree_as_something_else = True) != tests[test_string]:
            print(test_string)
            return False
    return True

def reset_end_pointer():
    global end_pointer
    end_pointer = -1

def get_list_of_terminating_characters():
    list_of_terminating_characters = []
    for i in range(500):
        if i not in range(65, 65 + 26) and i not in range(97, 97 + 26): #exclude upper and lower case latin alphabet
            list_of_terminating_characters.append(chr(i))
    return list_of_terminating_characters

