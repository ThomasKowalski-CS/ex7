#############################
# Name: Thomas Kowalski
# ID: *********
# Assignment: ex7
#############################

import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" }, ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    while 1:
        user_input = input(prompt)
        if my_isdigit(user_input): 
            return int(user_input)
        print("Invalid input.")

def my_isdigit(str):
    """
    Checks if a string can be converted to int (including negative). returns True/False
    """
    for l in str:
        if (l < '0' or '9' < l) and l != '-':
            return False
    return True


def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found. 
    Enter the right ID dont worry about -1 :)
    """
    if 0 <= poke_id <= 135:
        return HOENN_DATA[poke_id-1]
    return None

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    for dict in HOENN_DATA:
        if dict['Name'] == name:
            return dict
    return None

########################
# 2) BST (By Owner Name)
########################

def create_new_owner():
    name = input("Owner name: ")

    # check if name exists
    global ownerRoot
    if check_name_dfs(ownerRoot, name.lower()) != None:
        print(f"Owner '{name}' already exists. No new Pokedex created.")
        return

    # starter
    STARTER1 = HOENN_DATA[0]['Name']
    STARTER2 = HOENN_DATA[3]['Name']
    STARTER3 = HOENN_DATA[6]['Name']
    print("Choose your starter Pokemon:")
    print(f"1) {STARTER1}\n2) {STARTER2}\n3) {STARTER3}")
    starter_id = read_int_safe("Your choice: ")
    if starter_id == 1:
        starter_id = 1
    elif starter_id == 2:
        starter_id = 4
    elif starter_id == 3:
        starter_id = 7
    else: # not a valid choice (an int but not a valid starter id)
        print("Invalid. No new Pokedex created.")
        return
    
    # create the node
    new_owner = create_owner_node(name, starter_id)
    #insert to tree (check if its empty)
    
    ownerRoot = insert_owner_bst(ownerRoot, new_owner) #idk if necessary

    print(f"New Pokedex created for {name} with starter {HOENN_DATA[starter_id-1]['Name']}.")

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    return {"Name": owner_name, "Pokedex": [get_poke_dict_by_id(first_pokemon)], "Left": None, "Right" : None}
        
def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    if root == None: # if empty add as root
        root = new_node
        return root
    
    cur = root
    while 1:
        if new_node['Name'].lower() < cur['Name'].lower():
            if cur['Left'] == None:
                cur['Left'] = new_node
                return root
            else:
                cur = cur['Left']
        else:
            if cur['Right'] == None:
                cur['Right'] = new_node
                return root
            else:
                cur = cur['Right']
        
def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if root == None:
        return None
    
    if root['Name'].lower() == owner_name.lower():
        return root
    
    if owner_name.lower() < root['Name'].lower():
        return find_owner_bst(root['Left'], owner_name)
    else:
        return find_owner_bst(root['Right'], owner_name) 

def find_parent(root, owner_name):
    # go in the tree by name (if bigger right if smaller left) check the children's name
    if root == None:
        return None, None

    if root['Left'] != None and root['Left']['Name'] == owner_name:
        return root, 'Left'
    elif root['Right'] != None and root['Right']['Name'] == owner_name:
        return root, 'Right'
    
    if root['Name'] < owner_name:
        root_value, side = find_parent(root['Right'], owner_name)
        if root_value != None:
            return root_value, side
    else:
        root_value, side = find_parent(root['Left'], owner_name)
        if root_value != None:
            return root_value, side

    return None, None # unnecessary? 

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    if node['Left'] == None:
        return node
    
    return min_node(node['Left'])

def delete_owner_bst(root):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    if root == None:
        print("No owners to delete.")
        return

    owner_name = input("Enter owner to delete: ")
    owner_name_low = owner_name.lower()

    # find node
    owner_node = find_owner_bst(root, owner_name_low)
    if owner_node == None:
        print(f"Owner '{owner_name}' not found.")
        return root
    
    print(f"Deleting {owner_name}'s entire Pokedex...")
    print("Pokedex deleted.")
    if owner_node['Left'] == None and owner_node['Right'] == None: # leaf
        return leaf_delete(root, owner_name_low)
    elif owner_node['Left'] != None and owner_node['Right'] != None: # two children
        return children_delete(root, owner_name_low)
    else: # one child
        return child_delete(root, owner_name_low)

def leaf_delete(root, owner_name):
    if root['Name'].lower() == owner_name:
        root = None
        return root
    
    # find parent
    parent_node, side = find_parent(root, owner_name)
    # point it to None
    parent_node[side] = None
    return root

def child_delete(root, owner_name):
    if root['Name'].lower() == owner_name: # if its the root
        if root['Left'] != None: # switch with the right child
            root = root['Left']
        else:
            root = root['Right']
        return root
    
    parent_node, side = find_parent(root, owner_name)
    if parent_node[side]['Left'] != None:
        parent_node[side] = parent_node[side]['Left']
    else:
        parent_node[side] = parent_node[side]['Right']
    return root

def children_delete(root, owner_name):
    if root['Name'].lower() == owner_name:
        owner_node = root
    else:
        # if not root find the owner
        owner_node = find_owner_bst(root, owner_name)
    # find min
    replacement = min_node(owner_node['Right'])
    # replace pokedex and owner name
    owner_node['Pokedex'] = replacement['Pokedex']
    owner_node['Name'] = replacement['Name']
    # delete old min

    if replacement['Left'] == None and replacement['Right'] == None:
        return leaf_delete(root, replacement['Name'])
    else:
        return child_delete(root, replacement['Name'])


########################
# 3) BST Traversals
########################

def check_name_dfs(root, name):
    if root == None:
        return None
    
    if root['Name'].lower() == name:
        return root
    
    left = check_name_dfs(root['Left'], name)
    if left != None:
        return left
    right = check_name_dfs(root['Right'], name)
    return right


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    # get id
    pokemon_id = read_int_safe("Enter Pokemon ID to add: ")
    
    #check if valid
    if pokemon_id < 1 or pokemon_id > 135: # HOENN range
        print(f"ID {pokemon_id} not found in Honen data.")
        return
    
    # check if exists
    for pokemon in owner_node['Pokedex']:
        if pokemon['ID'] == pokemon_id:
            print("Pokemon already in the list. No changes made.")
            return
    
    # append the new pokemon
    owner_node['Pokedex'].append(get_poke_dict_by_id(pokemon_id))
    print(f"Pokemon {owner_node['Pokedex'][-1]['Name']} (ID {pokemon_id}) added to {owner_node['Name']}'s Pokedex.")

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    i = 0
    pokemon_name = input("Enter Pokemon Name to release: ")

    #search for pokemon and pop if found
    for pokemon in owner_node['Pokedex']:
        if pokemon['Name'] == pokemon_name.capitalize():
            print(f"Releasing {owner_node['Pokedex'][i]['Name']} from {owner_node['Name']}.")
            owner_node['Pokedex'].pop(i)
            return
        i += 1
    
    print(f"No Pokemon named '{pokemon_name}' in {owner_node['Name']}'s Pokedex.")

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    old_name = input("Enter Pokemon Name to evolve: ")
    old_index = 0
    for pokemon in owner_node['Pokedex']:
        if pokemon['Name'] == old_name.capitalize():
            if pokemon['Can Evolve'] == "FALSE":
                print(f"{pokemon['Name']} cannot evolve.")
                return
            else: # found and can evolve
                new_id = pokemon['ID']+1
                print(f"Pokemon evolved from {pokemon['Name']} (ID {pokemon['ID']}) to {HOENN_DATA[new_id-1]['Name']} (ID {new_id}).")
                owner_node['Pokedex'].pop(old_index)

                # check if new pokemon present
                for new_pokemon in owner_node['Pokedex']:
                    if new_pokemon['ID'] == new_id:
                        print(f"{new_pokemon['Name']} was already present; releasing it immediately.")
                        return
                
                #if not present add it
                owner_node['Pokedex'].append(get_poke_dict_by_id(new_id))
                return
   
        old_index += 1

    print(f"No Pokemon named '{old_name}' in {owner_node['Name']}'s Pokedex.")


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    if root == None:
        return
    else:
        arr.append(root)

    gather_all_owners(root['Left'], arr)
    gather_all_owners(root['Right'], arr)
 

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    if ownerRoot == None:
        print("No owners at all.")
        return

    owner_list = []
    gather_all_owners(ownerRoot, owner_list)
    owner_list.sort(key=lambda x: (len(x['Pokedex']), x['Name'].lower()))

    print("=== The Owners we have, sorted by number of Pokemons ===")
    for owner in owner_list:
        print(f"Owner: {owner['Name']} (has {len(owner['Pokedex'])} Pokemon)")
        




########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    if ownerRoot == None:
        print("No owners in the BST.")
        return

    print("1) BFS\n2) Pre-Order\n3) In-Order\n4) Post-Order")
    choice = read_int_safe("Your choice: ")
    if choice == 1:
        bfs_print(ownerRoot)
    elif choice == 2:
        pre_order_print(ownerRoot)
    elif choice == 3:
        in_order_print(ownerRoot)
    elif choice == 4:
        post_order_print(ownerRoot)
    else:
        print("Invalid choice.")
        return


def bfs_print(root):
    queue = [root]
    while 1:
        if len(queue) == 0:
            break
            
        cur = queue[0]
        if cur['Left'] != None:
            queue.append(cur['Left'])
        if cur['Right'] != None:
            queue.append(cur['Right'])
        print(f"\nOwner: {cur['Name']}")
        print_all_pokedex(cur)
        queue.pop(0)


def pre_order_print(root):
    """
    Helper to print data in pre-order.
    """
    if root == None:
        return
    print(f"\nOwner: {root['Name']}")
    print_all_pokedex(root)
    pre_order_print(root['Left'])
    pre_order_print(root['Right'])


def in_order_print(root):
    """
    Helper to print data in in-order.
    """
    if root == None:
        return
    
    in_order_print(root['Left'])
    print(f"\nOwner: {root['Name']}")
    print_all_pokedex(root)
    in_order_print(root['Right'])


def post_order_print(root):
    """
    Helper to print data in post-order.
    """
    if root == None:
        return
    
    post_order_print(root['Left'])
    post_order_print(root['Right'])
    print(f"\nOwner: {root['Name']}")
    print_all_pokedex(root)
    

def print_all_pokedex(owner_node):
    print("\n".join(", ".join(f"{key}: {value}" for key, value in pokemon.items()) for pokemon in owner_node['Pokedex']) or "There are no Pokemons in this Pokedex that match the criteria.")
########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    while 1:
        print("\n-- Display Filter Menu --\n1. Only a certain Type\n2. Only Evolvable\n3. Only Attack above __\n"
                        "4. Only HP above __\n5. Only names starting with letter(s)\n6. All of them!\n7. Back")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            # Type
            type = input("Which Type? (e.g. GRASS, WATER): ").capitalize()
            print("\n".join(", ".join(f"{key}: {value}" for key, value in pokemon.items()) for pokemon in owner_node['Pokedex'] if pokemon['Type'] == type) or "There are no Pokemons in this Pokedex that match the criteria.")

            
        elif choice == 2:
            # Only Evolvable
            print("\n".join(", ".join(f"{key}: {value}" for key, value in pokemon.items()) for pokemon in owner_node['Pokedex'] if pokemon['Can Evolve'] == "TRUE") or "There are no Pokemons in this Pokedex that match the criteria.")

        elif choice == 3:
            # Attack
            min = read_int_safe("Enter Attack threshold: ")
            print("\n".join(", ".join(f"{key}: {value}" for key, value in pokemon.items()) for pokemon in owner_node['Pokedex'] if pokemon['Attack'] > min) or "There are no Pokemons in this Pokedex that match the criteria.")

        elif choice == 4:
            # HP
            min = read_int_safe("Enter HP threshold: ")
            print("\n".join(", ".join(f"{key}: {value}" for key, value in pokemon.items()) for pokemon in owner_node['Pokedex'] if pokemon['HP'] > min) or "There are no Pokemons in this Pokedex that match the criteria.")

        elif choice == 5:
            # starting letter
            letters = input("Starting letter(s): ").capitalize()
            print("\n".join(", ".join(f"{key}: {value}" for key, value in pokemon.items()) for pokemon in owner_node['Pokedex'] if pokemon['Name'].startswith(letters)) or "There are no Pokemons in this Pokedex that match the criteria.")

        elif choice == 6:
            # all
            print_all_pokedex(owner_node)

        elif choice == 7:
            # back
            print("Back to Pokedex Menu.")
            return
        else:
            print("Invalid choice.")
            continue


########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """

    # if tree is empty
    if ownerRoot == None:
        print("No owners at all.")
        return
    
    owner_name = input("Owner name: ")
    # search for owner
    owner_node = find_owner_bst(ownerRoot, owner_name)
    if owner_node == None:
        print(f"Owner '{owner_name}' not found.")
        return
    owner_name = owner_node['Name']

    while 1:
        print(f"\n-- {owner_name}'s Pokedex Menu --\n1. Add Pokemon\n2. Display Pokedex\n3. Release Pokemon\n"
                                                                        "4. Evolve Pokemon\n5. Back to Main")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            # Add Pokemon
            add_pokemon_to_owner(owner_node)
        elif choice == 2:
            # Display
            display_filter_sub_menu(owner_node)
        elif choice == 3:
            # Relese
            release_pokemon_by_name(owner_node)
        elif choice == 4:
            # Evolve
            evolve_pokemon_by_name(owner_node)
        elif choice == 5:
            # Back
            print("Back to Main Menu.")
            return
        else:
            print("Invalid choice.")
            continue


def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    global ownerRoot
    
    while 1:
        print("\n=== Main Menu ===\n1. New Pokedex\n2. Existing Pokedex\n3. Delete a Pokedex\n"
              "4. Display owners by number of Pokemon\n5. Print All\n6. Exit")
        choice = read_int_safe("Your choice: ")
        
        if choice == 1:
            # new pokedex
            create_new_owner()
        elif choice == 2:
            # enter a pokedex
            existing_pokedex()
        elif choice == 3:
            # delete pokedex
            ownerRoot = delete_owner_bst(ownerRoot)
        elif choice == 4:
            # sort owners
            sort_owners_by_num_pokemon()
        elif choice == 5:
            # print all
            print_all_owners()
        elif choice == 6:
            print("Goodbye!")
            exit(0) #??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        else:
            print("Invalid choice.")
            continue

    
    

def main():
    main_menu()
    """
    Entry point: calls main_menu().
    """
    

if __name__ == "__main__":
    main()
