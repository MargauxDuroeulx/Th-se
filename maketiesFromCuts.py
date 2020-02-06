# Algorithm: compute minimal tie sets from cut sets of a CNF structure function.
# Python 3

import sys, time
from functions_lib import *
from maketiesDNF import *

# Function : get minimal tie sets from the CNF structure function.
def algorithm_Cut( MinCut ):
    Tie=[]
    MinTie=[]
    SeenTie=[]
    comp_nb=get_nb_comp()
    
    # What are the fathers of the minimal cut sets?
    for c in MinCut:
        for father in fathers(c, comp_nb):
            if not (father in Tie):
                Tie.append(father)
                SeenTie.append(father)
    #print ('Ties are:' ,Tie ,'\n' ,'SeenTies are:' ,SeenTie)

    # We consider each tie set of -Tie- one by one and its sons.
    while len(Tie) != 0:
        # We know that each element of -Tie- is a tie set.
        # Either it is a minimal tie set and we store it.
        # Either it is not and we consider its sons which are tie sets.
        for tieset in Tie :
            Tie.remove(tieset)
            # The binary variable -minimal- will turn to 0 if the tie set
            # is not minimal. Otherwise it will remain equal to 1.
            minimal = 1
            # We consider the sons of the -tieset- one by one.
            for son in sons(tieset, comp_nb):
                if is_a_tie_for_CNF(son, f, comp_nb):
                    minimal=0
                    #print (son, 'is a tie set')
                    if not (son in SeenTie):
                        Tie.append(son)
                        SeenTie.append(son)
            if minimal:
                #print ('Tie set considered :', tieset, ' is minimal')
                if not (tieset in MinTie):
                    MinTie.append(tieset)
    return MinTie

# Function : parse the input file, launch the algorithm and write the results
# in the output file.
def maketiesCut( inp, outp ) :
    # inp is the file where the structure function is given
    # outp is the file where we want to save the results
    
    # Time measure
    start=time.time()
    
    # Let's compute the minimal tie sets.
    MinTies = []
    with open (inp, "r") as modelFile :
        MinCut = modelFile.readlines()
    for t in algorithm_Cut(MinCut) :
        MinTies.append(transform_back(t))

    # Let's write the minimal tie sets into the output file.
    with open (outp, "w") as tieFile :
        for t in b :
            tieFile.write(' '.join( [str(q) for q in t] ))
            tieFile.write(' 0\n')

    #print ('The system contains', get_nComp_from_input(inp), 'components.')
    #print ('The structure funtion is:' , f)
    #print ('Minimal Tie Sets are :')
    for m in b :
        print (m)
    print ('->' , len(b) , 'minimal tie sets found')

    # Time measure
    end=time.time()
    timeNeeded = end - start
    print ('-> Time needed for the computation:', timeNeeded)
    return timeNeeded

def main() :
    if len(sys.argv) != 3 :
        print ("usage: maketiesFromCuts <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()











