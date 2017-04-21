#CS331 programming assignment 1
#Group work by Xiaoyi Yang and Jiaxu Li
#Some idea from Stack Overflow
import sys
import time


#function which read file
def readfromfile(file):
    fs=open(file,'r')
    data=[]
    for line in fs:
        if line is not None:
            data.append(map(int,line.split(',')))
    fs.close()
    #return value state in one, this makes things easier.
    return state(data[0], data[1])

#find the path of parents for an specific node
#(To partner: )Find path used in many places.
def find_path(current):
    path=[]
    while current is not None:
        path.insert(0,(current.left, current.right)) #This is the way append thing into first place!
        current = current.parent
    return path #list that from start to current nodes with order!



#check if reach the over state(Working-done) check if the current right hand side is = goal. dont need to check left, but same thing
def goal_test(current, goal):
    if current.right[0] == goal.right[0] and current.right[1] == goal.right[1] and current.right[2] == goal.right[2]:
        return True
    return False

#dont need a new goal test for DFS
#def goal_test2(current, goal):
 #   if current.right[0] == goal.right[0] and current.right[1] == goal.right[1] and current.right[2] == goal.right[2]:
 #       return True
#    return False

#check if the move is vaild/if not here, It may cause steps problem. Check if miss >=0 and make sure there is no empty in any side(if so, may have a dinner).
#(To partner: )Dont do this in child, Im sure it cause problem!
def action(next):
    if next.left[0]>=next.left[1] or next.left[0]==0:
        if next.right[0]>=next.right[1] or next.right[0]==0:
            return True
    return False

#state class is important!!!
#cost parament using in Astar. To make sort easy.
class state():
    def __init__(this, tleft=None, tright=None, tparent=None, tcost=None):
        this.left=tleft
        this.right=tright
        this.parent=tparent
        this.cost=tcost

#Use for append child node
#(To partner:) Again! dont move action in this one!
def child(current):
    
    child_node = []
    #current in left hand side
    if current.left[2] == 1:
        #send 1 miss
        if current.left[0]>=0 and current.left[1] >=0:
            temp=state([current.left[0]-1,current.left[1],current.left[2]-1],[current.right[0]+1,current.right[1],current.right[2]+1], current)
            if action(temp):
                child_node.append(temp)
        #send 2 miss
        if current.left[0]>=0 and current.left[1] >=0:
            temp=state([current.left[0]-2,current.left[1],current.left[2]-1],[current.right[0]+2,current.right[1],current.right[2]+1], current)
            if action(temp):
                child_node.append(temp)
        #send 1 can
        if current.left[0]>=0 and current.left[1] >=0:
            temp=state([current.left[0],current.left[1]-1,current.left[2]-1],[current.right[0],current.right[1]+1,current.right[2]+1], current)
            if action(temp):
                child_node.append(temp)
        #send 2 can
        if current.left[0]>=0 and current.left[1] >=0:
            temp=state([current.left[0],current.left[1]-2,current.left[2]-1],[current.right[0],current.right[1]+2,current.right[2]+1], current)
            if action(temp):
                child_node.append(temp)
        #send 1&1, good friends!
        if current.left[0]>=0 and current.left[1] >=0:
            temp=state([current.left[0]-1,current.left[1]-1,current.left[2]-1],[current.right[0]+1,current.right[1]+1,current.right[2]+1], current)
            if action(temp):
                child_node.append(temp)
    #current in right hand side, just repeat!
    else:
        #send 1 miss
        if current.right[0]>=0 and current.right[1]>=0:
            temp=state([current.left[0]+1,current.left[1],current.left[2]+1],[current.right[0]-1,current.right[1],current.right[2]-1], current)
            if action(temp):
                child_node.append(temp)
        #send 2 miss
        if current.right[0]>=0 and current.right[1]>=0:
            temp=state([current.left[0]+2,current.left[1],current.left[2]+1],[current.right[0]-2,current.right[1],current.right[2]-1], current)
            if action(temp):
                child_node.append(temp)
        #send 1 can
        if current.right[0]>=0 and current.right[1]>=0:
            temp=state([current.left[0],current.left[1]+1,current.left[2]+1],[current.right[0],current.right[1]-1,current.right[2]-1], current)
            if action(temp):
                child_node.append(temp)
        #send 2 can
        if current.right[0]>=0 and current.right[1]>=0:
            temp=state([current.left[0],current.left[1]+2,current.left[2]+1],[current.right[0],current.right[1]-2,current.right[2]-1], current)
            if action(temp):
                child_node.append(temp)
        #send 1&1, good friends!
        if current.right[0]>=0 and current.right[1]>=0:
            temp=state([current.left[0]+1,current.left[1]+1,current.left[2]+1],[current.right[0]-1,current.right[1]-1,current.right[2]-1], current)
            if action(temp):
                child_node.append(temp)

    #done append, now return the child_node
    return child_node


#Main function. 
def main():
    if len(sys.argv) != 5:
        print 'Usage: project1.py < initial state file > < goal state file > < mode > < output file > \n'
        exit(0)

    #four argvs.
    start_file=str(sys.argv[1])
    goal_file=str(sys.argv[2])
    search_type=str(sys.argv[3])
    output=str(sys.argv[4])

    first_state=readfromfile(start_file)
    goal=readfromfile(goal_file)

    #type switch
    if search_type.lower() == 'bfs':
        result, expand=BFS(first_state, goal)
    elif search_type.lower() == 'dfs':
        result, expand=DFS(first_state, goal)
    elif search_type.lower() == 'iddfs':
        result, expand=IDDFS(first_state, goal)
        if result == 'fail':
            result = False
    elif search_type.lower() == 'astar':
        result, expand=Astar(first_state, goal)
    else:
        print 'Not a vaild type.'
        exit(0)
    outfile=open(output,'w+')
    
    #places that output information and output to file are same.
    if result and len(find_path(result)) != 0:
        outfile.write('Path of solution: ')
        print 'Path: '
        for state in find_path(result):
            print 'Left Bank: ' + str(state[0][0])+' missionaries, '+ str(state[0][1])+' cannibal, '+str(state[0][2])+ ' boal | Right: ' + str(state[1][0]) + ' missionaries, '+str(state[1][1])+' cannibal, '+ str(state[1][2]) + ' boal'
            outfile.write('Left Bank: ' + str(state[0][0])+' missionaries, '+ str(state[0][1])+' cannibal, '+str(state[0][2])+ ' boal | Right: ' + str(state[1][0]) + ' missionaries, '+str(state[1][1])+' cannibal, '+ str(state[1][2]) + ' boal\n')
        print 'It spend '+str(len(find_path(result)))+ ' steps(nodes)'
        outfile.write('It spend '+str(len(find_path(result)))+ ' steps(nodes)\n')
        print 'expand nodes: ' + str(expand)
        outfile.write('expand nodes: ' + str(expand)+'\n')
        outfile.close()
    else:
        print 'No solution found!'

    

#My partner is a genius! tuple is so fucking good!
def First_search(current):
    return (str(current.left[0])+str(current.left[1])+str(current.left[2])+str(current.right[0])+str(current.right[1])+str(current.right[2]), current)

#contains function checks the number of a current. (The number should be "XXXX" which "leftmiss_leftcan_rightmiss_rightcan")
def contains(lists, element):
    for elem in lists:
        if element[0]==elem[0]:
            return True
    return False

#function which checks the goal is in the list.
def check_goal(lists, element):
    for elem in lists:
        if goal_test(element, elem):
            return False
    return True


#(To partner: )I dont think this simple one has any logic need to know.
def BFS(start, goal):
    queue=[start]
    state_check=[]
    k = 0
    while len(queue) != 0:
        current=queue.pop(0)
        #print current
        if goal_test(current, goal):  #if reach the goal
            return current, k
        state_check.append(First_search(current))
        k=k+1
        children = child(current) #make a new list for child nodes
        for nodes in children:
            if check_goal(queue, nodes) and (not contains(state_check, First_search(nodes))):
                queue.append(nodes)
    #Thanks the idea from StackOverflow!
    return False, k

#(To Partner: )The logic of this one is insert. insert nodes by its level into places, can be pop by order.
def DFS(start, goal):
    queue=[start]
    state_check=[]
    k = 0
    while len(queue) != 0:
        current=queue.pop(0)  #the main idea of our four searching!
        if goal_test(current, goal):
            return current, k
        state_check.append(First_search(current))
        k = k+1;
        children = child(current) #not a lot difference with BFS. Just append and insert places.
        s = 0
        for nodes in children:
            if check_goal(queue, nodes) and (not contains(state_check, First_search(nodes))):
                queue.insert(s, nodes) #make sure insert place correct. means pop is correct.
                s = s + 1
    #Thanks the idea from StackOverflow!*2
    return False, k

#logic of this one is complex. It's like select nodes in different level. and calculate every child it has. Textbook P89 have a specific graph.
def IDDFS(start, goal):
    limit = 0
    k = 0
    while(1):  #because I dont know how to make inifinite loop in for.
        queue=[start]
        state_check=[]
        final_state, k = IDDFS2(start, goal, queue, state_check, limit, k)  #loop start
        if final_state!='cut':
            return final_state, k
        limit = limit + 1

#this one is the Depth limit search. Just name it IDDFS2, dont need think too much. All idea from textbook
def IDDFS2(current, goal, queue, state_check, limit, k):
    temp = []
    state_check.append(First_search(current)) #append the first node for queue. The node has a tuple with it like all other search
    if len(queue) != 0:
        queue.pop(0)
    if goal_test(current, goal):
        return current, k
    elif limit == 0:
        return 'cut', k
    else:
        children = child(current)
        i = 0
        k = k + 1
        check = False
        #recu here, leave argl for IDDFS. two loops
        for nodes in children:
            if check_goal(queue, nodes) and (not contains(state_check, First_search(nodes))):
                queue.insert(i, nodes)
                temp.insert(i, nodes)
                i = i + 1
        for nodes in temp:
            temps, k = IDDFS2(nodes, goal, queue, state_check, limit-1, k)
            if temps == 'cut':
                check=True
            elif temps != 'fail':
                return temps, k

        if check:
            return 'cut', k
        else:
            return 'fail', k
    


#function Astar
#(To partner: )The logic of this one is listed the cost of a node. After put nodes into Queue, sorted queue by cost. In this case the smaller node can be pop earlier.
def Astar(start, goal):
    queue=[]
    state_check=[]
    start_cost = 0 + (goal.left[0]-start.left[0]) + (goal.left[1]-start.left[1]) #heuristic
    start.cost=start_cost #because we made a cost to state(node)
    queue.append(start)
    k = 0
    while len(queue) != 0:
        current=queue.pop(0)
        #print current
        #print queue
        if goal_test(current, goal):
            return current, k
        state_check.append(First_search(current))
        k=k+1
        children = child(current)
        for nodes in children:
            if check_goal(queue, nodes) and (not contains(state_check, First_search(nodes))):
                nodes_cost=len(find_path(nodes)) + (goal.left[0]-nodes.left[0]) + (goal.left[1]-nodes.left[1])#heuristic
                nodes.cost=nodes_cost
                queue.append(nodes)
                templist = queue
                queue=sorted(templist, key=lambda nodes: nodes.cost) #heuristic 
    #Thanks the idea from StackOverflow!
    return False, k

#function start running
main()