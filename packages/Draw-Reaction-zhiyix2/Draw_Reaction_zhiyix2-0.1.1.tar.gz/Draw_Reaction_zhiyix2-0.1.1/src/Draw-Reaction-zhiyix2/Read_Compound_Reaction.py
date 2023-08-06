

# Read TXT File into TextIOWrapper Object
# Input File Path
# Output TextIOWrapper f
def readFile(input):
    f = open(input, "r")
    return f

# Read TextIOWrapper Object into List of Reaction Strings
# Input TextIOWrapper
# Output filtered_reaction_list (list of String)
def get_reaction_list(f):
    reaction_list = list()
    is_reaction = False
    for line in f.readlines():
        if is_reaction and line == '\n':
            is_reaction = False
        if is_reaction:
            reaction_list.append(line)
        if "// Reactions:" in line:
            is_reaction = True

    filtered_reaction_list = list()
    for reaction in reaction_list:
        reaction = reaction.split(':')[1].split(';')[0].strip()
        filtered_reaction_list.append(reaction)
    return filtered_reaction_list

# Remove the Dollar Sign from the given List
# Input input_list (List of String)
# Output reaction_list (list of String with Dollar Sign Removed)
def replace_dollar_sign(input_list):
    for i in range(0, len(input_list)):
        input_list[i] = input_list[i].replace('$', '')
        #print(input_list[i])
    return input_list

# Split the Given List of Strings into List of Reaction Lists
# Input input_list (List of String)
# Output reaction_list (list of List)
def get_reaction_data(inputList):
    inputList = replace_dollar_sign(inputList)
    reaction_list = list()
    for reaction in inputList:
        reli = reaction.split()
        reaction_list.append(reli)
    return reaction_list

# Combine the Reaction Lists if the Product of Reaction One is the Reactant of the Reaction
# two
# Input reaction_list (List of List)
# Output result_list (list of List)
def get_compound_reaction(reaction_list):
    result_list = list()
    result_list.append(reaction_list[0])
    currentIndex = 0
    for i in range(1, len(reaction_list), 1):
        #print(reaction_list[i])
        #result = list()
        if reaction_list[i][0] == result_list[currentIndex][len(result_list[currentIndex]) - 1]:
            for j in range(1, len(reaction_list[i]), 1):
                result_list[currentIndex].append(reaction_list[i][j])
        else:
            result_list.append(reaction_list[i])
            currentIndex += 1
    return result_list


"""
reaction_list = get_reaction_list(readFile("Result2.txt"))
reaction_list = replace_dollar_sign(reaction_list)
#print(reaction_list)
reaction_list = get_reaction_data(reaction_list)
reaction_list = get_compound_reaction(reaction_list)
print(reaction_list)

print()
for li in reaction_list:
    print(li)
print()


"""
        


