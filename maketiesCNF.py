# Algorithm: compute minimal tie sets from cut sets of a CNF structure function.
# Use Python 3

import sys, os, time, subprocess
from functions_lib import *
from maketiesDNF import *

# The program expects two arguments, namely the input and output file names.
# The input file might be in DIMACS format; it is modified by the program.
# The output file will be created (resp., overwritten if it already exists).

def algorithm_CNF( inp, outp ):
    # Run MiniSAT a first time on the input
    subprocess.getoutput('minisat ' + inp + ' minisat.out')
    with open ("minisat.out", "r") as modelFile :
        modelLines = modelFile.readlines()
    
    # We want to know if the system is coherent (=1).
    is_coherent = 1

    # We want to store the minimal tie sets we find..
    minimalties = []

    # We want to count how many times we use miniSAT.
    i = 0

    ### SAT
    while modelLines[0] =='SAT\n' :
        i = i+1
        # Since the problem is SAT, the second line contains the model,
        # represented as a spaces-separated sequence of integers.
        model = modelLines[1].split()
        if is_coherent :
            tie = newtie_c(model)
        #if not is_coherent :
            #tie = newtie_nc(model)
        print (tie)

        # We compare this tie (actually its negation) to the previous ties found
        if not contains_smaller(minimalties, tie) :
            minties = [t for t in minimalties if not tie.issubset(t)]
            minimalties.append(tie)
        # We add the negations of these literals to the clauses given to miniSAT
        # Observe in particular that -0 is 0, so we get a valid clause in DIMACS
        negLits = [-l for l in tie]
        negLits.append(0)
        # open CNF file for appending clause
        with open(inp, "a") as cnfFile :
            cnfFile.write(' '.join(map(str, negLits)))
            cnfFile.write('\n')

        # run MiniSAT again on the input and the additional clause
        # NB: we rely on the fact that MiniSAT ignores the number of clauses
        # given in the first line of the DIMACS input
        subprocess.getoutput('minisat ' + inp + ' minisat.out')
        with open ("minisat.out", "r") as modelFile :
            modelLines = modelFile.readlines()
    
    ### UNSAT
    if modelLines[0] =='UNSAT\n' or modelLines[0] =='UNSAT' :
        with open (outp, "w") as tieFile :
        # tieFile : file where we are going to solve system tie sets
            tieFile.write("Minimal ties are : \n")
            for t in minimalties :
                tieFile.write(' '.join( [str(l) for l in t] ))
                tieFile.write(' 0\n')
    ### TROUBLE
    else :
        print ("There is an error with MiniSAT output.\n") # should never happen

    return minimalties

def run( inp, outp ):
    # Time measurement
    start=time.time()

    # We call the algorithm to compute the minimal tie sets.
    minimalties = algorithm_CNF(inp, outp)
    #for m in minimalties :
        #print (m)
        
    # Properly write the structure function from the input file.
    st_function = clear_inp(inp)
    
    # How many component in the system?
    comp_nb = get_nb_comp(st_function)

    #for m in minimalties :
        # Rewrite the set as a list for the DNF algorithm
        ### to do ###
    
    # From the tie sets, we compute the minimal tie sets :
    #MinTie = algorithm_DNF(comp_nb, minimalties)
    #print ('->', MinTie)

    print ('->', len(minimalties) , 'minimal tie sets found')

    # Time measure
    end=time.time()
    timeNeeded = end - start
    print ('-> Time needed for the computation:', timeNeeded)
    return timeNeeded

def main():
    if len(sys.argv) != 3 :
        print ("usage: maketies <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()


