# -*- coding: ISO-8859-1 -*-

# Algorithm: compute minimal tie sets from cut sets of a DNF structure function.
# Use Python 3

import sys, os, time
from functions_lib import *
from varsupprSMT_Z3 import *

# Function : get minimal cut sets from the cut sets.
def mincuts_SMT( inp, outp ):

    CutSets = var_suppr_SMT(inp,"CutSetsWAV.txt") # liste de liste, contient les cut sets avec uniquement le events
    
    #On commence par transformer les liste d'elements en set pour pouvoir utiliser la methode .issubset()
    for i in range(len(CutSets)):
        CutSets[i]=set(CutSets[i])
    
    MinCuts = [CutSets[0]]  #on met le premier element pour pouvoir commencer les comparaisons ensuite
    
    taille = len(CutSets)
    
    for j in range(1,len(CutSets)):
    
        #for j in range(len(CutSets)):
            #if (CutSets[j].issubset(CutSets[i])) and (CutSets[j] != CutSets[i]) and (CutSets[j] not in MinCuts):
        drapeau=0
        for c in MinCuts:
            if c.issubset(CutSets[j]):  #si dans mincuts, un plus grand, alors on brea 
                drapeau=1
            if CutSets[j].issubset(c):  #on supprime le MC pour lequel [j] est subset si il s'avère que [j] sera un MC
                MinCuts.remove(c)
        if drapeau==0:      
            MinCuts.append(CutSets[j]) #si aucun mincut est subset de celui là, on le rajoute  
            
        print("Nombre d'iteration dans calcul MinCuts : ",j+1, "/",taille," => ", round(((j+1)*100)/taille,2), "%")
    
    return MinCuts

# Function : get minimal cut sets from a DNF structure function.
def run( inp, outp ):
    # Time measure
    start=time.time()
    
    # Let's compute the minimal cut sets.
    MinCuts = mincuts_SMT( inp, outp )

    with open (outp, "w") as cutFile :
        cutFile.write("Minimal cut sets are : \n")
        for t in MinCuts :
            cutFile.write("\n"+str(t))
            
    print ('->' , len(MinCuts) , 'minimal cut sets found')

    # Time measure
    end=time.time()
    timeNeeded = end - start
    print ('-> Time needed for the computation:', timeNeeded)
    return timeNeeded

def main():
    if len(sys.argv) != 3 :
        print ("usage: mincuts <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()


