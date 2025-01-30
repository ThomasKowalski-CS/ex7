#############################
# Name: Thomas Kowalski
# ID: 
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
        choice = input(prompt)
        if choice.isdigit(): 
            return int(choice)
        print("Invalid Input")

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found. 
    Enter the right ID dont worry about -1 :)
    """
    if 0 <= poke_id < 135:
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

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    pass


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

    print(f"New Pokedex created for {name} with starter {HOENN_DATA[starter_id]['Name']}.")


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
        if new_node['Name'] < cur['Name']:
            if cur['Left'] == None:
                cur['Left'] = new_node
                return root
            else:
                cur = cur["Left"]
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
    
    if owner_name < root['Name'].lower():
        return find_owner_bst(root['Left'], owner_name)
    else:
        return find_owner_bst(root['Right'], owner_name) 

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    pass

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    pass


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    pass

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    pass

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    pass

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    pass

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
    if pokemon_id < 1 or pokemon_id > 134: # HOENN range
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
    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    pass

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    pass

def pre_order_print(node):
    """
    Helper to print data in pre-order.
    """
    pass

def in_order_print(node):
    """
    Helper to print data in in-order.
    """
    pass

def post_order_print(node):
    """
    Helper to print data in post-order.
    """
    pass


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
            print("\n".join(", ".join(f"{key}: {value}" for key, value in pokemon.items()) for pokemon in owner_node['Pokedex']) or "There are no Pokemons in this Pokedex that match the criteria.")

        elif choice == 7:
            # back
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
            continue
        elif choice == 5:
            # Back
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
    while 1:
        print("\n=== Main Menu ===\n1. New Pokedex\n2. Existing Pokedex\n3. Delete a Pokedex\n"
              "4. Display owners by number of Pokemon\n5. Print All\n6. Exit")
        choice = read_int_safe("Your choice: ")
        
        if choice == 1:
            # new pokedex
            create_new_owner()
            continue
        elif choice == 2:
            # enter a pokedex
            existing_pokedex()
            continue
        elif choice == 3:
            # delete pokedex
            continue
        elif choice == 4:
            # sort owners
            continue
        elif choice == 5:
            # print all
            continue
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
