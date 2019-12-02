#/usr/bin/python3


# solve game from winning ways for your mathematical plays

#Win is a dict with the repr of the position as the index and the winning move as the value
win={}

# lose is a set of losing positions with teh repr of the position as the index (set member)
lose=set()

# kill is the number of pieces that can be taken from the selected heap
kill=[1,2]

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
    # print("Eval "+rp)

    # Position already known?
    if rp in win:
        print("Fast win "+rp)
        return "W"
    if rp in lose:
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
                    print("Slow win "+rp)
                    return "W"
    # no good moves -- I'm a loser
    lose.add(rp)
    print("Slow lose "+rp)
    return "L"


def main():
    # salt the problem
    lose.add(repr([]))
        
    TestHeapAray(SingleHeapArray(25))
    print("lose")
    print(sorted(list(lose)))
    
    for w in sorted(list(win)):
        print("{}\t->\t{}".format(w,win[w]))

if __name__ == "__main__":
    # execute only if run as a script
    main()
