# Algorithm: compute minimal tie sets from cut sets of a DNF structure function.
# Use Python 3

import sys, os, time
from functions_lib import *

# Function : get minimaln tie sets from the CNF structure function.
def algorithm_DNF( f, comp_nb ):
    # Inputs :
    # comp_nb : number of components of the system
    # f : structure function of the system
    
    # We want to get the minimal ties from the structure function.
    # Indeed, each conjunction of the DNF is a tie.
    Ties = []
    i=0
    while i < len(f) :
        element = f[i]
        if element not in Ties :
            Ties.append(element)
        i=i+1

    # We assume that the system is coherent.

    # We look for the minimal ties.
    MT=[]
    for i in range (0, len(Ties)) :
        #print("Variable i value:", i)
        list_size = len(MT)
        delete_list=[]
        x = Ties[i]
        for k in range (0, list_size) :
            if test_smaller ( MT[k], x ) :
                #print("test_smaller:", 1)
                x=[]
                break
            # The tie set is not minimal.
            elif test_smaller ( x, MT[k] ) :
                #print("test_smaller:", 0)
                #print("k", k)
                delete_list.append(k)
            # If not comparable:
            #elif test_smaller ( MT[k], x ) == test_smaller ( x, MT[k] ) :
                #print("tuples equals or not comparable:")
        if (len(delete_list)>0) :
            delete_list.reverse()
            print("delete_list:", delete_list, len(delete_list))
            for j in range(0, len(delete_list)) :
                #print("j:", j, delete_list)
                #print("delete_list", delete_list[j])
                p = delete_list[j]
                del(MT[p])
            delete_list=[]
        if (len(x)>0) :
            MT.append(x)

    # Is there residual cut sets ?
    #if is_system_coherent == 0 :
        #residualCut = get_residual_cut_sets(f, comp_nb)
        #print  ('Residual cut sets are:' , residualCut)
    
    # Now we need to find the residual cut sets.
    ### to do ###

    return MT

# Function : get minimal tie sets from a DNF structure function.
def run( inp, outp ):
    # inp is the file where the structure function is given
    # outp is the file where we want to save the results
    
    # Time measure
    start=time.time()
    
    # Properly write the structure function from the input file.
    st_function = clear_inp(inp)

    # How many component in the system?
    comp_nb = get_nb_comp(st_function)

    # What is the structure function of the system?
    f=[]
    for element in st_function:
        f.append(transform(element, comp_nb))
    
    # Let's compute the minimal tie sets.
    MinTies = []
    for t in algorithm_DNF(f, comp_nb) :
        MinTies.append(transform_back(t))

    # Let's write the minimal tie sets into the output file.
    with open (outp, "w") as tieFile :
        #tieFile.write("Minimal tie sets are : \n")
        for t in MinTies :
            tieFile.write(' '.join( [str(q) for q in t] ))
            tieFile.write(' 0\n')

    # Result display
    print ('System contains', comp_nb, 'components.')
    print ('Structure function is:\n', st_function)
    print ('Structure function is:\n', f)
    print ('Minimal Tie Sets are :')
    for m in MinTies :
        print (m)
    print ('->' , len(MinTies) , 'minimal tie sets found')

    # Time measure
    end=time.time()
    timeNeeded = end - start
    print ('-> Time needed for the computation:', timeNeeded)
    return timeNeeded

def main():
    if len(sys.argv) != 3 :
        # usage: maketies <input-file> <output-file>
        print ("usage: maketies <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()


