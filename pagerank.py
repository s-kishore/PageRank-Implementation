import sys
from math import log
import operator

#P is the set of all pages
#S is the set of sink nodes, i.e., pages that have no out links
#M(p) is the set (without duplicates) of pages that link to page p
#L(q) is the number of out-links (without duplicates) from page q
#d is the PageRank damping/teleportation factor; use d = 0.85 as is typical

P = []
S = []
M = {}
L = {}
PR = {}
newPR = {}
d = 0.85
perplexity = []
PRSorted = []
IL = {}
ILSorted = []

#Main function
def main():
    filename = sys.argv[1]
    inlinks_file = open(filename , 'r')
    create_graph(inlinks_file)
    compute_pagerank()

    PRSorted = sorted(PR.iteritems(), key=operator.itemgetter(1), reverse=True)
    ILSorted = sorted(IL.iteritems(), key=operator.itemgetter(1), reverse=True)
    print "\n Top 50 Pages Sorted by PageRank Values:\n"
    for i in range(50):
        print PRSorted[i]
    print "\n Top 50 Pages Sorted by Inlink Count:\n"
    for i in range(50):
        print ILSorted[i]


#This function creates the required data structures for the program
def create_graph(inlinks_file):

#Foreach line l in the inlinks_file, split the letters into nodes
    for l in inlinks_file:
        l = l.strip()
        nodes = l.split(" ")

#Taking first element of the line as the key of dictionary M and appending the
# rest of the line as values with duplicates removed.
        p = nodes[0]
        M[p] = []
        for i in nodes[1:]:
            if i not in M[p]:
                M[p].append(i)
        P.append(p)

#Creating all pages in P as keys for inlinks dictionary
# Initializing values of inlinks count of pages as 0
    for p in P:
        IL[p] = 0

#For each occurrence of the page in dictionary M, adding length of the inlink count.
    for keys in M.keys():
        IL[keys] = len(M.get(keys))

#Creating all pages in P as keys for dictionary L and assigning 0 as value
    for p in P:
        L[p] = 0

#Foreach occurrence of the page in values of dictionary M,
# updates its outlink count by 1.
    for values in M.values():
        for value in values:
                L[value] += 1

#Pages which are in dictionary L and have value as 0, add them to list S.
    for key in L.keys():
        if L.get(key) == 0:
            S.append(key)

    return P, M, L, S, IL

#This function calculates the perplexity
# Perplexity is defined as simply 2 raised to the (Shannon) entropy of the PageRank distribution
def calculate_perplexity(i):
    H = 0
    perplexity = 0
    for page in PR.keys():
        H += PR[page] * log(1/PR[page], 2)
    perplexity = 2**H
    print i+1, perplexity
    return perplexity

#This function computes the pagerank
def compute_pagerank():
    N = len(P)
    for p in P:
        PR[p] = 1.0/N                     #initial value

    i = 0
    print "Perplexity Values:"
    while not converged(i):
    #"PageRank Algorithm starts.."
        sinkPR = 0
        for p in S:                       #calculate total sink PR
            sinkPR += PR[p]
        for p in P:
            newPR[p] = (1.0-d)/N          #teleportation
            newPR[p] += d*sinkPR/N        #spread remaining sink PR evenly
            for q in M[p]:                #pages pointing to p
                newPR[p] += d*PR[q]/L[q]  #add share of PageRank from in-links
        for p in P:
            PR[p] = newPR[p]
        i += 1

    return PR

#This function calculates whether perplexity values have converged or not.
# Convergence here is defined as when the change in perplexity is less than 1 for at least four iterations.
def converged(i):
    change = 0
    count = 0
    perplexity.append(calculate_perplexity(i))
    if i > 0:
        change = abs(perplexity[i] - perplexity[i-1])
        if change < 1 and count <= 4:
            count += 1
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    main()


