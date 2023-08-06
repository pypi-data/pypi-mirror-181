#!/usr/bin/env python
import sys, getopt

from tkinter import Tk, Canvas, Frame, BOTH
import Draw_Reaction
import Read_Compound_Reaction

# Determine the Maximum Column Number
# Input: Reaction_List
# Output: Max as Int
def getMaxColumn(reaction_list):
    max = 0
    for reaction in reaction_list:
        if len(reaction) > max:
            max = len(reaction)
    return max
    
# Main Method
def main(values):
    #values = sys.argv[1:]

    try:
        root = Tk()
        
        ex = Draw_Reaction.Draw_Reaction(values)
        margin = 10
        height = 40
        width = 100
        reaction_list = Read_Compound_Reaction.get_reaction_list(Read_Compound_Reaction.readFile(values[0]))

        inputList = Read_Compound_Reaction.get_reaction_data(reaction_list)
        inputList = Read_Compound_Reaction.get_compound_reaction(inputList)

        
        rows = len(inputList)
        column = getMaxColumn(inputList)
        windowHeight = (rows * margin + 2) + (height * rows + 2)
        windowWidth = (column * margin + 2) + (column * width + 2)
            
        height_width = "{}x{}+300+300".format(windowWidth, windowHeight)
        #print(height_width)
        root.geometry(height_width)
        root.mainloop()
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        print("Incorrect File Names given <input file>")



if __name__ == '__main__':
    main(sys.argv[1:])