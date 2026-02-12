import heapq
import itertools
import time

#goal puzzle
goal = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

#below are example puzzles
easy = [
    [1,2,3],
    [4,5,6],
    [7,0,8]
]

normal = [
    [0,1,2],
    [4,5,3],
    [7,8,6]
]

hard = [
    [8,7,1],
    [6,0,2],
    [5,4,3]
]

class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.cost = cost  # This is g(n)


def generalSearch(problem, searchType):
    startNode = Node(problem)  #root node
    nodes = []  #This is queue
    counter = itertools.count()

    heapq.heappush(nodes, (0,next(counter), startNode))  #root node is pushed into priority queue
    numNodesExpanded = 1
   

    visitedNode = set(); #This is going to have all the nodes that was visited to prevent checking again

    while nodes:
        _, _, node = heapq.heappop(nodes)  #pop the node which has the lowest cost

        g = node.cost
        h = 0

        if searchType == "misplaced":
            h = misplacedTile(node.state)
        elif searchType == "manhattan":
            h = manhattan(node.state)

        print(f"The best state to expand with a g(n) = {g} and h(n) = {h} is...")  #printing the best expanded state
        for row in node.state:
            print(row)


        nodeState = tuple(map(tuple, node.state))
        numNodesExpanded += 1

        if(nodeState in visitedNode):   #if the node is in visted list, do nothing
            continue
    
        visitedNode.add(nodeState)

        if (node.state == goal):  #Found solution
            print("Success!")
            print("depth: ", node.cost)
            print("Number of nodes expanded: ", numNodesExpanded)
            return node
        
        for child in expand(node):    #generates all the valid movements from the current node
            childState = tuple(map(tuple, child.state))

            if(childState in visitedNode):  #if the node is in visted list, do nothing
                continue

            else:
                priority = search(child,searchType)
                heapq.heappush(nodes, (priority, next(counter), child))    #add to the priority queue


    print("Failure. No solution exsist in this problem")
    return None





def expand(node):
    children = []
    childNode = node.state
    row, col = 0,0

    #generates all possible movements
    for i in range(3):    
        for j in range(3):
            if node.state[i][j] == 0: 
                row, col = i, j
                break

    move = [(-1,0),(1,0),(0,-1),(0,1)]

    #generates child nodes
    for moveRow, moveCol in move:
        newRow = row+moveRow
        newCol = col + moveCol

        if((0 <= newRow <= 2) and (0 <= newCol <= 2)): #checking if the node exist
            newState = [r.copy() for r in childNode]
            newState[row][col], newState[newRow][newCol] = newState[newRow][newCol],newState[row][col]

            newChildNode = Node(newState, parent = node, cost = node.cost+1)
            children.append(newChildNode)

    return children





def search(node,algorithm):     #returns the cost of node depending on the algorithms
    if(algorithm == "UCS"):
        return node.cost
    
    elif(algorithm == "misplaced"):
        return node.cost + misplacedTile(node.state)
    
    else:
        return node.cost + manhattan(node.state)
    





def misplacedTile(state): #counts the tiles that are not in the correct position
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count += 1
    return count





def manhattan(state):  #calculate the total distance of all tiles from the goal positions but ignoring 0.
    goal_pos = {1:(0,0), 2:(0,1), 3:(0,2),
                4:(1,0), 5:(1,1), 6:(1,2),
                7:(2,0), 8:(2,1)}
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                goal_i, goal_j = goal_pos[tile]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

    



    
def main():
    puzzleMode = input("Welcome to the 8-puzzle problem solver! Type '1' to solve for the example puzzle and type '2' to solve the problem you create. \n")
    
    while (puzzleMode != '1' or puzzleMode != '2'):    #check for invalid inputs
        if(puzzleMode != '1' and puzzleMode !='2'):
            puzzleMode = input("Invalid input. Type '1' to solve for example puzzle and type '2' to solve the problem you create. \n")

        elif(puzzleMode == '1' or puzzleMode == '2'):
            puzzleMode = int(puzzleMode)
            break



    searchType = input("Choose a search type. Type '1' for Uniform Cost Search, '2' for A* with the Misplaced Tile heuristic, '3' for A* with the Manhattan Distance heuristic. \n")
    
    while (searchType != '1' or searchType != '2' or searchType != '3'):   #check for invalid inputs
            if(searchType != '1' and searchType !='2' and searchType != '3'):
                searchType = input("Invalid input. Type '1' for Uniform Cost Search, '2' for A* with the Misplaced Tile heuristic, '3' for A* with the Manhattan Distance heuristic. \n")

            elif(searchType == '1' or searchType == '2' or searchType == '3'):
                searchType = int(searchType)
                if(searchType == 1):
                    searchType = "UCS"

                elif(searchType == 2):
                    searchType = "misplaced"

                else:
                    searchType = "manhattan"

                break

            
    if(puzzleMode == 1):
        exampleTest = input("Choose a test example. Type '1' for a easy test, '2' for a normal test, and '3' for a hard test. \n" )

        while (exampleTest != '1' or exampleTest != '2' or exampleTest != '3'):   #check for invalid inputs
            if(exampleTest != '1' and exampleTest !='2' and exampleTest != '3'):
                exampleTest = input("Invalid input. Type '1' for a easy test, '2' for a normal test, and '3' for a hard test. \n")

            elif(exampleTest == '1' or exampleTest == '2' or exampleTest == '3'):
                exampleTest = int(exampleTest)
                if(exampleTest == 1):
                    exampleTest = easy

                elif(exampleTest == 2):
                    exampleTest = normal

                else:
                    exampleTest = hard
                break
    
        

    
    else:
        firstRow = input("Enter the first row (Ex. '1 2 3'): ")
        secondRow = input("Enter the second row: ")
        thirdRow = input("Enter the third row: ")

        firstRow = firstRow.split()
        secondRow = secondRow.split()
        thirdRow = thirdRow.split()

        for i in range(3):       #convert the puzzle from string to integer
            firstRow[i] = int(firstRow[i])
            secondRow[i] = int(secondRow[i])
            thirdRow[i] = int(thirdRow[i])

        exampleTest = [firstRow, secondRow, thirdRow]

    start_time = time.time()    #start timing

    generalSearch(exampleTest, searchType)  #do search based on inputs

    end_time = time.time()     #end timing

    print("Time taken: ", end_time - start_time, "seconds")

    return

if __name__ == "__main__":
    main()


