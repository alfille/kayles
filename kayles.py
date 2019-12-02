#/usr/bin/python3


# solve game from winning ways for your mathematical plays

#Win is a dict with the repr of the position as the index and the winning move as the value
win={}

# lose is a set of losing positions with teh repr of the position as the index (set member)
lose=set()

# kill is the number of pieces that can be taken from the selected heap
kill=[1,2]

# Debug flag for showing internal process
dbg = False


# heap array is a list of the number of heaps of different sizes
# big-endian
# i.e. [2,0,1] is 2 heaps of 3 and 1 heap of one
#   legal moves: (heap,killsize,subheap size)
#   (1,1,0) -> [2,0,0]
#   (3,1,1) -> [1,0,2]
#   (3,2,0) -> [1] (actually [0,0,1] but we take off leading zeroes)

def SingleHeapArray(size):
    # Single heap, rest are empty
    return [1] + [0]*(size-1)
    
def StartWithNonempty(heapArray):
    while heapArray:
        if heapArray[0] != 0 :
            return
        del(heapArray[0])

def TestHeapAray(heapArray):
    StartWithNonempty(heapArray)
    rp=repr(heapArray)
    if dbg:
        print("Eval "+rp)

    # Position already known?
    if rp in win:
        if dbg:
            print("Fast win "+rp)
        return "W"
    if rp in lose:
        if dbg:
            print("Fast lose "+rp)
        return "L"

    # Try all legal moves
    heaparrayLength = len(heapArray)
    for i,h in enumerate(heapArray): # loop through heaps
        
        if h==0:
            # no heaps of this size
            continue
            
        heapSize = heaparrayLength-i
        for k in kill: 
            #loop through kill sizes
            
            if k > heapSize:
                # heap size too small for this kill size
                continue
                
            for subheap1 in range(heapSize-k+1): 
                #loop through splits
                subheap2=heapSize-k-subheap1
                
                if subheap2 > subheap1: 
                    #redundant by symmetry
                    continue
                    
                # apply the move to a copy of heapArray
                modHeapArray = heapArray.copy()
                modHeapArray[i] -= 1
                if subheap1 > 0:
                    modHeapArray[heaparrayLength-subheap1] += 1
                if subheap2 > 0:
                    modHeapArray[heaparrayLength-subheap2] += 1

                # Test the modified position
                if TestHeapAray(modHeapArray) == "L":
                    # made other guy a loser
                    win[rp] = (heapSize,k,subheap1)
                    if dbg:
                        print("Slow win "+rp)
                    return "W"
    # no good moves -- I'm a loser
    lose.add(rp)
    if dbg:
        print("Slow lose "+rp)
    return "L"

def CommandLine():
    cl = argparse.ArgumentParser(description="Solve Kayles game from Winning Ways for Your Mathematical Plays\n{c} Paul H Alfille 2019")
    cl.add_argument("H",help="Size of initial large heap (default = 25)",type=int,nargs="?",default=25)
    cl.add_argument("-L","--lose",help="Show losing positions found",action="store_true")
    cl.add_argument("-W","--win",help="Show winning positions with correct move triplet (heapsize,killsize,split_heapsize)",action="store_true")
    cl.add_argument("-D","--debug",help="Debug -- show progress through analysis",action="store_true")
    cl.add_argument("-R","--reverse",help="Reverse rule -- no moves is a WIN",action="store_true")
    return cl.parse_args()


def main(args):

    args = CommandLine()
    dbg = args.debug
    
    # salt the problem
    if args.reverse:
        win[repr([])]="Finished"
    else:
        lose.add(repr([]))
        
    if args.H < 1:
        print("Starting haeap size must be a positive number, of course")
        return
        
    value = TestHeapAray(SingleHeapArray(args.H))

    if args.lose:
        print("lose")
        print(sorted(list(lose)))
    
    if args.win:
        for w in sorted(list(win)):
            print("{}\t->\t{}".format(w,win[w]))

    print("Kayles with initial heap size of {} is a {}".format(args.H,value))

if __name__ == "__main__":
    import sys
    import argparse
    # execute only if run as a script
    sys.exit(main(sys.argv))
