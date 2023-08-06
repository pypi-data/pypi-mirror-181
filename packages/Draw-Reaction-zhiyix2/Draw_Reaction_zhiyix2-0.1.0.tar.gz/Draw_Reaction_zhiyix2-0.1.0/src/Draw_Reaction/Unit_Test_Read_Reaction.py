
import unittest
import sys
#sys.path[0] += '\\Draw_Reaction'
#sys.path.append('..\\')
#print(sys.path)
import Read_Compound_Reaction as read_reaction
#import Draw_Reaction.Read_Compound_Reaction as read_reaction



def test_get_reaction_list():
    reaction_list = read_reaction.get_reaction_list(read_reaction.readFile("Result2.txt"))
    target_list = ['MKKK => MKKK_P', 'MKKK_P => MKKK', 'MKK => MKK_P', 'MKK_P => MKK_PP', 'MKK_PP => MKK_P', 'MKK_P => MKK', 'MAPK => MAPK_P', 'MAPK_P => MAPK_PP', 'MAPK_PP => MAPK_P', 'MAPK_P => MAPK']
    assert len(reaction_list) == 10, "Should be 10"
    assert reaction_list == target_list, "The values should be ['MKKK => MKKK_P', 'MKKK_P => MKKK', 'MKK => MKK_P', 'MKK_P => MKK_PP', 'MKK_PP => MKK_P', 'MKK_P => MKK', 'MAPK => MAPK_P', 'MAPK_P => MAPK_PP', 'MAPK_PP => MAPK_P', 'MAPK_P => MAPK']"

def test_replace_dollar_sign():
    reaction_list = read_reaction.get_reaction_list(read_reaction.readFile("Result2.txt"))
    reaction_list = read_reaction.replace_dollar_sign(reaction_list)
    target_list = ['MKKK => MKKK_P', 'MKKK_P => MKKK', 'MKK => MKK_P', 'MKK_P => MKK_PP', 'MKK_PP => MKK_P', 'MKK_P => MKK', 'MAPK => MAPK_P', 'MAPK_P => MAPK_PP', 'MAPK_PP => MAPK_P', 'MAPK_P => MAPK']
    assert reaction_list == target_list, "The values should be ['MKKK => MKKK_P', 'MKKK_P => MKKK', 'MKK => MKK_P', 'MKK_P => MKK_PP', 'MKK_PP => MKK_P', 'MKK_P => MKK', 'MAPK => MAPK_P', 'MAPK_P => MAPK_PP', 'MAPK_PP => MAPK_P', 'MAPK_P => MAPK']"

    reaction_list2 = read_reaction.get_reaction_list(read_reaction.readFile("Result.txt"))
    reaction_list2 = read_reaction.replace_dollar_sign(reaction_list2)

    target_list2 = ['sul_ex => sul', 'eth_ex => eth', 'sul + A3c => aps + PPi', 'oxy_ex => oxy', 'oxy => oxy_ex', 'aps + A3c => pap + A2c', 'pap + 3 N2 => hyd + 3 N1', 'hyd + oah => cys', 'cys =>', 'eth + 2 N1 => aco + 2 N2', 'aco => oah', 'hyd =>', 'oah =>', 'S2 + aco => S1', 'S1 + 4 N1 => S2 + 4 N2', 'C1 + Hm + N2 => C2 + Ho + N1', 'C2 + oxy => C1 + H2O', 'A2c + A3m => A2m + A3c', 'Ho + A2m => Hm + A3m', 'Ho => Hm', 'A3c => A2c']
    assert reaction_list2 == target_list2, "The value should be ['sul_ex => sul', 'eth_ex => eth', 'sul + A3c => aps + PPi', 'oxy_ex => oxy', 'oxy => oxy_ex', 'aps + A3c => pap + A2c', 'pap + 3 N2 => hyd + 3 N1', 'hyd + oah => cys', 'cys =>', 'eth + 2 N1 => aco + 2 N2', 'aco => oah', 'hyd =>', 'oah =>', 'S2 + aco => S1', 'S1 + 4 N1 => S2 + 4 N2', 'C1 + Hm + N2 => C2 + Ho + N1', 'C2 + oxy => C1 + H2O', 'A2c + A3m => A2m + A3c', 'Ho + A2m => Hm + A3m', 'Ho => Hm', 'A3c => A2c']"

def test_get_reaction_data():
    reaction_list = read_reaction.get_reaction_list(read_reaction.readFile("Result2.txt"))
    reaction_list = read_reaction.get_reaction_data(reaction_list)
    target_list = [['MKKK', '=>', 'MKKK_P'], ['MKKK_P', '=>', 'MKKK'], ['MKK', '=>', 'MKK_P'], ['MKK_P', '=>', 'MKK_PP'], ['MKK_PP', '=>', 'MKK_P'], ['MKK_P', '=>', 'MKK'], ['MAPK', '=>', 'MAPK_P'], ['MAPK_P', '=>', 'MAPK_PP'], ['MAPK_PP', '=>', 'MAPK_P'], ['MAPK_P', '=>', 'MAPK']]
    assert reaction_list == target_list, "The value should be [['MKKK', '=>', 'MKKK_P'], ['MKKK_P', '=>', 'MKKK'], ['MKK', '=>', 'MKK_P'], ['MKK_P', '=>', 'MKK_PP'], ['MKK_PP', '=>', 'MKK_P'], ['MKK_P', '=>', 'MKK'], ['MAPK', '=>', 'MAPK_P'], ['MAPK_P', '=>', 'MAPK_PP'], ['MAPK_PP', '=>', 'MAPK_P'], ['MAPK_P', '=>', 'MAPK']]"

def test_get_compound_reaction():
    reaction_list = read_reaction.get_reaction_list(read_reaction.readFile("Result2.txt"))
    reaction_list = read_reaction.get_reaction_data(reaction_list)
    reaction_list = read_reaction.get_compound_reaction(reaction_list)
    target_list = [['MKKK', '=>', 'MKKK_P', '=>', 'MKKK'], ['MKK', '=>', 'MKK_P', '=>', 'MKK_PP', '=>', 'MKK_P', '=>', 'MKK'], ['MAPK', '=>', 'MAPK_P', '=>', 'MAPK_PP', '=>', 'MAPK_P', '=>', 'MAPK']]
    assert reaction_list == target_list, "The value should be [['MKKK', '=>', 'MKKK_P', '=>', 'MKKK'], ['MKK', '=>', 'MKK_P', '=>', 'MKK_PP', '=>', 'MKK_P', '=>', 'MKK'], ['MAPK', '=>', 'MAPK_P', '=>', 'MAPK_PP', '=>', 'MAPK_P', '=>', 'MAPK']]"




if __name__ == "__main__":

    test_get_reaction_list()
    test_replace_dollar_sign()
    test_get_reaction_data()
    test_get_compound_reaction()

    print("Everything passed")
