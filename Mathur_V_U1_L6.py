# Name: Vihaan Mathur  
# Date: 9/29/21
import random, time, math

class HeapPriorityQueue():
   # copy your HeapPriorityQueue() from Lab3
   def __init__(self):
      self.queue = ["dummy"]  # we do not use index 0 for easy index calulation
      self.current = 1        # to make this object iterable

   def next(self):            # define what __next__ does
      if self.current >=len(self.queue):
         self.current = 1     # to restart iteration later
         raise StopIteration
    
      out = self.queue[self.current]
      self.current += 1
   
      return out

   def __iter__(self):
      return self

   __next__ = next

   def isEmpty(self):
      return len(self.queue) == 1    # b/c index 0 is dummy

   def swap(self, a, b):
      self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

   # Add a value to the heap_pq
   def push(self, value):
      self.queue.append(value)
      if len(self.queue) > 1:
        self.heapUp(len(self.queue) - 1)
      # write more code here to keep the min-heap property

   # helper method for push      
   def heapUp(self, k):
    parent = int(k/2)
    p = self.queue[parent]
    cur = self.queue[k]
    if(parent < 1):
         return
    else:
         if(cur < p):
            self.swap(parent, k)
            self.heapUp(parent) 
         else:
            return
               
   # helper method for reheap and pop
   def heapDown(self, k, size):
      right = (2*k) + 1
      left = (2*k)
      if(left > size or k > size):
            return
      elif(right > size):
            if(self.queue[k] > self.queue[left]):
               self.swap(k, left)
      else:
         if((self.queue[k] > self.queue[right] or self.queue[k] > self.queue[left])):
            if(self.queue[right] < self.queue[left]):
               self.swap(right, k)
               self.heapDown(right, size)
            else:
               self.swap(left, k)
               self.heapDown(left, size)
   # make the queue as a min-heap            
   def reheap(self):
      for i in range (int(len(self.queue)/2), 0 , -1):
         self.heapDown(i, len(self.queue)-1)   

   # remove the min value (root of the heap)
   # return the removed value            
   def pop(self):
     if(len(self.queue) > 2):
      removed = self.queue[1]
      self.queue[1] = self.queue[len(self.queue)-1]
      self.queue.pop()
      self.heapDown(1, len(self.queue)-1)
      return removed  # change this`
     else: 
        removed = self.queue[1]
        self.queue.pop()
        return removed
      
   # remove a value at the given index (assume index 0 is the root)
   # return the removed value   
   def remove(self, index):
      # Your code goes here
     removed = self.queue[index + 1]
     self.queue.remove(removed); 
     self.reheap()
     return removed

def inversion_count(new_state, width = 4, N = 4):
   ''' 
   Depends on the size(width, N) of the puzzle, 
   we can decide if the puzzle is solvable or not by counting inversions.
   If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
   If N is even, puzzle instance is solvable if
      the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) and number of inversions is even.
      the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) and number of inversions is odd.
   ''' 
   # Your code goes here
   invcount = 0
   j = [x for x in new_state if x != "_"]
   for x in range(len(j)): 
      for y in range(x + 1, len(j)):
         if ord(j[y]) < ord(j[x]):
            invcount += 1
   even = False
   if (((new_state.index("_") // N)%2) % 2) == 0 :
      even = True
   if N % 2 != 0 and invcount % 2 == 0:
      return True 
   if (N % 2 == 0 and invcount % 2 == 0 and even == True) or (N % 2 == 0 and invcount % 2 != 0 and even == False):
      return True
   return False

def check_inversion():
   t1 = inversion_count("_42135678", 3, 3)  # N=3
   f1 = inversion_count("21345678_", 3, 3)
   t2 = inversion_count("4123C98BDA765_EF", 4) # N is default, N=4
   f2 = inversion_count("4123C98BDA765_FE", 4)
   return t1 and t2 and not (f1 or f2)


def getInitialState(sample, size):
   sample_list = list(sample)
   random.shuffle(sample_list)
   new_state = ''.join(sample_list)
   while not inversion_count(new_state, size, size): 
      random.shuffle(sample_list)
      new_state = ''.join(sample_list)
   return new_state
   
def swap(n, i, j):
   # Your code goes here
   l = list(n)
   l[i], l[j] = l[j], l[i]
   return(''.join(l))
      
'''Generate a list which hold all children of the current state
   and return the list'''
def generate_children(state, size=4):
   children = []
   i = state.index('_')
   if (i%size>0): #left
      children.append(swap(state, i-1, i))
   if (i%size != size-1): #right
      children.append(swap(state, i, i+1))
   if (i-size >= 0): #up
      children.append(swap(state, i-size, i))
   if (i+size<len(state)): #down
      children.append(swap(state, i, i+size))
   return children 

def display_path_a(path_list, size):
   for n in range(size):
      for path in path_list:
         print (path[n*size:(n+1)*size], end = " "*size)
      print ()
   print ("\nThe number of steps :", len(path_list))
   return ""

def display_path(n, explored):
   l = []
   while n in explored and explored[n] != "": #"s" is initial's parent
      l.append(n)
      n = explored[n]
   l.append(n)
   l = l[::-1]
   return l

def listshow(l):
   for i in l:
      print (i[0:4], end = "   ")
   print ()
   for j in l:
      print (j[4:8], end = "   ")
   print()
   for k in l:
      print (k[8:12], end = "   ")
   print()
   for k in l:
      print (k[12:16], end = "   ")
   print()
   

''' You can make multiple heuristic functions '''
def dist_heuristic(state, goal = "_123456789ABCDEF", size=4):
   # Your code goes here
   sum = 0
   for x in state: 
      row = abs((goal.index(x) % size) - (state.index(x) % size))
      col= abs((goal.index(x) // size) - (state.index(x) // size))
      sum += (row + col)
   return sum

def check_heuristic():
   a = dist_heuristic("152349678_ABCDEF", "_123456789ABCDEF", 4)
   b = dist_heuristic("8936C_24A71FDB5E", "_123456789ABCDEF", 4)
   return (a < b) 

def a_star(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size = 4):
   frontier = HeapPriorityQueue()
   frontier.push(((dist_heuristic(start)), start, [start]))
   if start == goal: 
      return []
   while(not frontier.isEmpty()):
      s = frontier.pop()
      if (s[1] == goal):
         return (s[2])
      for a in generate_children(s[1]):
         if a not in s[2]:
            cost = len(s[2]) + dist_heuristic(a)
            frontier.push((cost, a, s[2] + [a]))
   return "No Solution"

def bi_bfs(start, goal = "_123456789ABCDEF"):
   '''The idea of bi-directional search is to run two simultaneous searches--
   one forward from the initial state and the other backward from the goal--
   hoping that the two searches meet in the middle. 
   '''
   if start == goal: 
      return []
   # TODO2: Bi-directional BFS Search
   Q1 = [start]
   Q2 = [goal]
   explored1 = {start:""}
   explored2 = {goal:""}#goal pop for loop goal (q1 q2 interctions) pop for loop 
   while(len(Q1) > 0 and len(Q2) > 0):
      s = Q1.pop(0)
      if (s in explored2):
         b = (display_path(s, explored1))
         h = (display_path(s, explored2))[::-1]
         h.pop(0)
         return (b + h)
      for a in generate_children(s):
         if a not in explored1:
            Q1.append(a)
            explored1[a] = s
      g = Q2.pop(0)
      if (g in explored1):
         b = (display_path(g, explored1))
         h = (display_path(g, explored2))[::-1]
         h.pop(0)
         return (b + h)
      for b in generate_children(g):
         if b not in explored2:
            Q2.append(b)
            explored2[b] = g
   return None

def solve(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size = 4):
   frontier1 = HeapPriorityQueue()
   frontier1.push((dist_heuristic(start), start, [start]))
   frontier2 = HeapPriorityQueue()
   frontier2.push((dist_heuristic(goal, start), goal, [goal]))
   if start == goal: 
      return []
   explored1 = {start: dist_heuristic(start, goal)}
   explored2 = {goal: dist_heuristic(goal, start)} #goal pop for loop goal (q1 q2 interctions) pop for loop 
   while(not (frontier1.isEmpty() and frontier2.isEmpty())):
      s = frontier1.pop()
      if (s[1] in explored2):
         h = []
         for m in frontier2: 
            if(m[1] == s[1] and m[0] == explored2[m[1]]): 
               h = m[2][::-1]
         h.remove(h[0])
         b = s[2]
         return (b + h)
      for a in generate_children(s[1]):
         cost = len(s[2]) + dist_heuristic(a, goal) 
         if a not in explored1 or explored1[a] > cost:
            explored1[a] = cost
            frontier1.push((cost, a, s[2] + [a]))
      g = frontier2.pop()
      if (g[1] in explored1):
         h = []
         for k in frontier1: 
            if(k[1] == g[1] and k[0] == explored1[k[1]]): 
               h = k[2]
         b = g[2][::-1]
         b.remove(b[0])
         return (h + b)
      for b in generate_children(g[1]):
         cost = len(g[2]) + dist_heuristic(b, start) 
         if b not in explored2 or explored2[b] > cost:
            explored2[b] = cost
            frontier2.push((cost, b, g[2] + [b]))
   return None

def main():
    # A star
   print ("Inversion works?:", check_inversion())
   print ("Heuristic works?:", check_heuristic())
   '''
   initial_state = getInitialState("_123456789ABCDEF", 4)
   initial_state = input("Type initial state: ")
   if inversion_count(initial_state):
      cur_time = time.time()
      path = (a_star(initial_state))
      if path != None: display_path_a(path, 4)
      else: print ("No Path Found.")
      print ("Duration: ", (time.time() - cur_time))
   else: print ("{} did not pass inversion test.".format(initial_state))
   '''
   #bi astar
   initial_state = getInitialState("_123456789ABCDEF", 4)
   initial_state = input("Type initial state: ")
   if inversion_count(initial_state):
      cur_time = time.time()
      path1 = (solve(initial_state))
      if path1 != None:
         display_path_a(path1, 4)
         #print ("The number of steps: ", len(path1))
         print ("Duration: ", time.time() - cur_time)
      else:
         print ("There's no path")
   else: print ("{} did not pass inversion test.".format(initial_state))


   
if __name__ == '__main__':
   main()


''' Sample output 1

Inversion works?: True
Heuristic works?: True
Type initial state: 152349678_ABCDEF
1523    1523    1_23    _123    
4967    4_67    4567    4567    
8_AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 4
Duration:  0.0


Sample output 2

Inversion works?: True
Heuristic works?: True
Type initial state: 2_63514B897ACDEF
2_63    _263    5263    5263    5263    5263    5263    5263    5263    52_3    5_23    _523    1523    1523    1_23    _123    
514B    514B    _14B    1_4B    14_B    147B    147B    147_    14_7    1467    1467    1467    _467    4_67    4567    4567    
897A    897A    897A    897A    897A    89_A    89A_    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 16
Duration:  0.005014657974243164


Sample output 3

Inversion works?: True
Heuristic works?: True
Type initial state: 8936C_24A71FDB5E
8936    8936    8936    893_    89_3    8943    8943    8_43    84_3    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
C_24    C2_4    C24_    C246    C246    C2_6    C_26    C926    C926    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 37
Duration:  0.27825474739074707


Sample output 4

Inversion works?: True
Heuristic works?: True
Type initial state: 8293AC4671FEDB5_
8293    8293    8293    8293    8293    8293    8293    8293    82_3    8_23    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
AC46    AC46    AC46    AC46    AC46    _C46    C_46    C4_6    C496    C496    C_96    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
71FE    71F_    71_F    7_1F    _71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5_    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 39
Duration:  0.7709157466888428

'''

