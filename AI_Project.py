"""
Team: Yi-Ling(100958447), Eshant(100943729)
"""
import numpy as np
import math
import time
start_time = time.time() 
class Peg(object):

    def __init__(self, disks=[], max_disks=0):
        if len(disks) > 0:
            self.disks = disks
        else:
            self.disks = [i for i in range(max_disks, 0, -1)]

    def __iter__(self):
        return iter(self.disks)

    def check_empty(self):
        return len(self.disks) == 0

    def remove_top_disk(self):
        if self.check_empty():
            return math.inf
        return self.disks[-1:].pop()

    def add_disk(self, disk):
        if not self.check_empty():
            if disk < self.disks[-1:].pop():
                self.disks.append(disk)
        else:
            self.disks.append(disk)

    def pop_disk(self):
        return self.disks.pop()

    def move_to(self, Peg_dest):
        if not self.check_empty():
            if self.remove_top_disk() < Peg_dest.remove_top_disk():
                Peg_dest.add_disk(self.pop_disk())

    def current_state(self):
        return tuple(self.disks)


class PuzzleState(object):
    def __init__(self, A, B , C, D ,predecessor, goal_state=False):
        self.state = ([e for e in A],
                      [e for e in B],  
                      [e for e in C],
                      [e for e in D])
        self.goal_state = goal_state
        self.value = None
        self.predecessor = predecessor

    def __eq__(self, other):
        if isinstance(other, PuzzleState):
            try:
                for p in range(0, len(self.state)):
                    for d in range(0, len(self.state[p])):
                        if self.state[p][d] != other.state[p][d]:
                            return False
                for p in range(0, len(other.state)):
                    for d in range(0, len(other.state[p])):
                        if other.state[p][d] != self.state[p][d]:
                            return False
            except IndexError:
                return False
            return True

    def TotalCost(self, cost, goal_state):
        if ip ==1:
            self.value = self.RealCost(cost) + self.H_inadmissible(goal_state)
        elif ip==2:
            self.value = self.RealCost(cost) + self.H_admissible(goal_state)
        elif ip ==3:
            #This corresponds to breadth-first/blind-search as the heuristic value is zero
            self.value = self.RealCost(cost) 

        return self.value

    def RealCost(self, cost):
        """
        This calculates actions cost which is 1 for each action
        """
        return cost + 1

    def H_inadmissible(self, goal_state):
        """
        This is our inadmissible heuristic function, It's working is explained in the report. In summary, It's is calculating out of order
        disks and adding them. We are using a smart way of checking the number of disk before each equality check and usinf pass for Index         error which makes the code a bit short.
        """
        current_Peg_1 = self.state[0]
        current_Peg_2 = self.state[1]
        current_Peg_3 = self.state[2]
        current_Peg_4 = self.state[3] 
        final_Peg_1 = goal_state.state[0]
        final_Peg_2 = goal_state.state[1]
        final_Peg_3 = goal_state.state[2]
        final_Peg_4 = goal_state.state[3]
        
        h= 0
        try:
            for d in range(0, len(current_Peg_1)):
                if current_Peg_1[d] != final_Peg_1[d]:
                    h+=1
        except IndexError:
            pass

        try:
        
            for d in range(0, len(current_Peg_2)):
                if current_Peg_2[d] != final_Peg_2[d]:
                    h+= 1       
                    
        except IndexError:
            pass

        try:
            for d in range(0, len(current_Peg_3)):
                if current_Peg_3[d] != final_Peg_3[d]:
                     h+= 1
        except IndexError:
            pass
        
        try:
            for d in range(0, len(current_Peg_4)):
                if current_Peg_4[d] != final_Peg_4[d]:
                    h+= 1
        except IndexError:
            pass

        return h
    
      
    def H_admissible(self, goal_state):
        """
        This is an admissible heuristic function, it assigns the values based on the difference between the desired number of disk in the 
        tower 4(defind as final peg 4 disk count) and the number of disks in order in the tower 4 at present.
        """
        current_Peg_4 = np.array(self.state[3])
        final_Peg_4 = np.array(goal_state.state[3])
        #i have cast the python list into a numpy array to calculate number of disk in order i current tower 4 in one step
        h =len(final_Peg_4) -sum(current_Peg_4 ==final_Peg_4[0:len(current_Peg_4)])
        
        return h

class TheHanoiTower(object):
    #The class for the Hanoi Tower
    def __init__(self, initial_state, goal_state):
        self.goal_state = goal_state
        self.initial_state = initial_state
        self.unsolved_list = []
        self.solved_list = []


    def select_next_node(self, cost):
        child_totalcost = math.inf
        index = 0
        child_index = math.inf
        for node in self.unsolved_list:
            node_totalcost = node.TotalCost(cost=cost, goal_state=self.goal_state)
            if node_totalcost < child_totalcost:
                child_totalcost = node_totalcost
                child_index = index
            index += 1

        selected = self.unsolved_list[child_index]
        del self.unsolved_list[child_index]
        return selected

    def generate_next_states(self, node):
        """
        This function generates next states based on our constraint of moving one disk at a time. every block of 4 lines is generating
        a state and then adding it to the list of states
        """
        P1 = Peg(node.state[0])
        P2 = Peg(node.state[1])
        P3 = Peg(node.state[2])
        P4 = Peg(node.state[3])
        next_states = []
        
        P_1 = Peg(disks=P1.disks[:])
        P_2 = Peg(disks=P2.disks[:])
        P_1.move_to(P_2)
        next_states.append(PuzzleState(P_1, P_2, P3,P4, predecessor=node))

        P_1 = Peg(disks=P1.disks[:])
        P_3 = Peg(disks=P3.disks[:])
        P_1.move_to(P_3)
        next_states.append(PuzzleState(P_1, P2, P_3,P4, predecessor=node))
        
        P_1 = Peg(disks=P1.disks[:])
        P_4 = Peg(disks=P4.disks[:])
        P_1.move_to(P_4)
        next_states.append(PuzzleState(P_1, P2, P3, P_4,predecessor=node))
        
        P_1 = Peg(disks=P1.disks[:])
        P_2 = Peg(disks=P2.disks[:])
        P_2.move_to(P_1)
        next_states.append(PuzzleState(P_1, P_2, P3, P4,predecessor=node))

        P_2 = Peg(disks=P2.disks[:])
        P_3 = Peg(disks=P3.disks[:])
        P_2.move_to(P_3)
        next_states.append(PuzzleState(P1, P_2, P_3,P4 ,predecessor=node))
        
        P_2 = Peg(disks=P2.disks[:])
        P_4 = Peg(disks=P4.disks[:]) 
        P_2.move_to(P_4)
        next_states.append(PuzzleState(P1, P_2, P3,P_4, predecessor=node))

        P_1 = Peg(disks=P1.disks[:])
        P_3 = Peg(disks=P3.disks[:])
        P_3.move_to(P_1)
        next_states.append(PuzzleState(P_1, P2, P_3,P4, predecessor=node))
        
        P_2 = Peg(disks=P2.disks[:])
        P_3 = Peg(disks=P3.disks[:])
        P_3.move_to(P_2)
        next_states.append(PuzzleState(P1, P_2, P_3,P4, predecessor=node))


        P_3 = Peg(disks=P3.disks[:])
        P_4 = Peg(disks=P4.disks[:])
        P_3.move_to(P_4)
        next_states.append(PuzzleState(P1, P2, P_3,P_4, predecessor=node))
        
        P_1 = Peg(disks=P1.disks[:])
        P_4 = Peg(disks=P4.disks[:])
        P_4.move_to(P_1)
        next_states.append(PuzzleState(P_1, P2, P3,P_4, predecessor=node))
        
        P_2 = Peg(disks=P2.disks[:])
        P_4 = Peg(disks=P4.disks[:])
        P_4.move_to(P_2)
        next_states.append(PuzzleState(P1, P_2, P3,P_4, predecessor=node))
        
        
        P_3 = Peg(disks=P3.disks[:])
        P_4 = Peg(disks=P4.disks[:])
        P_4.move_to(P_3)
        next_states.append(PuzzleState(P1, P2, P_3,P_4, predecessor=node))

        return next_states

    def retrieve_path(self, node):
        #Here, we are retrieving the path we have travelled
        path = []
        while node.predecessor != None:
            path.append(node)
            node = node.predecessor
        path.append(self.initial_state)
        return path

    def Search(self):
        #This is the function for our main search algorithm.
        cost = 0
        self.unsolved_list.append(self.initial_state)
        while len(self.unsolved_list) > 0:
            node = self.select_next_node(cost)
            cost += 1
            self.solved_list.append(node)
            if node == self.goal_state:
                # if we have reached the solution, we will trace back
                print (" States Expanded: " ,len(self.solved_list))
                print('Number of moves taken: ',len(self.retrieve_path(node))-1)
                print ("Path To Solution:")
                for r in reversed(self.retrieve_path(node)):
                    print (r.state)
                break
            else:
                next_states = self.generate_next_states(node)
                for ns in next_states:
                    new_state = True
                    for sl in self.solved_list:
                        if sl == ns:
                            new_state = False
                    if new_state:
                        for ul in self.unsolved_list:
                            if ul == ns:
                                new_state = False
                                if ns.value != None:
                                    if ul.value > ns.value:
                                        self.unsolved_list.remove(ul)
                                        self.unsolved_list.append(ns)
                                        break
                        if new_state:
                            self.unsolved_list.append(ns)
                        

# main body from here 
ip = 0 #this variable defines the heuristic/algorithm to choose
n = int(input('Enter the number of disks in the first peg,(greater than zero):'))
while ip not in [1,2,3]:
    ip = int(input('Enter the number corresponding to each method of solving the puzzle\n 1- A* with Inadmissible heuristic\n 2- A* with Admissible Heuristic\n 3- Breath-First Search '))

Ipeg1 = Peg(max_disks=n)
Ipeg2 = Peg()
Ipeg3 = Peg()
Ipeg4 = Peg()
initial_state = PuzzleState(Ipeg1, Ipeg2, Ipeg3,Ipeg4 ,predecessor=None)

Gpeg1 = Peg()
Gpeg2 = Peg()
Gpeg3 = Peg()
Gpeg4 = Peg(max_disks=n)
goal_state = PuzzleState(Gpeg1, Gpeg2, Gpeg3,Gpeg4 ,predecessor=None, goal_state=True)
print("Initial State:" , initial_state.state)
print("Goal State:" ,goal_state.state)

TheHanoiTower(initial_state, goal_state).Search()

print('---%s seconds---'%(time.time()-start_time))
