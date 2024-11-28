from flight import Flight
def comparator_fare(a,b):
    return a[0]< b[0]
def comparator_innovate(a,b):
    if(a[1] == b[1]):
        return a[0]<b[0]

    return a[1]< b[1] 

def comparator_innovate2(a,b):
    return a[0]< b[0] 
class Heap:
    def __init__(self, comparison_function, init_array=[]):
        self.heap: list = init_array[:]
        self.comp = comparison_function
        if init_array:
            self.heapify()   
    def insert(self, value):
        # Write your code here
        self.heap.append(value)
        self.heapify_up(len(self.heap)-1)
    def extract(self):
        root = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heapify_down(0)
        return root
    def top(self):
        return self.heap[0]
    def parent(self,i):
        return (i-1)//2
    def left_child(self,i:int):
        return 2*i+1
    def right_child(self,i:int):
        return 2*i+2
    def heapify_up(self,index):
        while index>0:
            parent_idx = self.parent(index)
            if(self.comp(self.heap[index],self.heap[parent_idx])):
                self.heap[index],self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
                index = parent_idx
            else:
                break  
    def heapify_down(self,index):

        while(self.left_child(index) < len(self.heap)):
            
            left = self.left_child(index)
            right = self.right_child(index)
            # print('done',left,right)

            if(right < len(self.heap) and self.comp(self.heap[right],self.heap[left])):
                smaller = right
            else:
                smaller = left

            if(self.comp(self.heap[smaller],self.heap[index])):
                self.heap[index],self.heap[smaller] = self.heap[smaller], self.heap[index]
                index = smaller
            else:
                break
    def heapify(self):
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self.heapify_down(i)


















class Node:
    def __init__(self,value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def isEmpty(self):
        if(self.size == 0):
            return True
        return False
    
    def enqueue(self,value):
        if(self.rear == None):
            self.rear = Node(value)
            self.front = self.rear
            self.size +=1
        else:    
            self.rear.next = Node(value)
            self.rear = self.rear.next
            self.size +=1


    def dequeue(self):
        if(self.isEmpty()):
            raise Exception("Empty")
        store = self.front
        value = store.value
        self.front = store.next 
        if(self.front == None):
            self.rear = None
        del(store)
        self.size -=1
        return value
    def peek(self):
        if(self.front  == None):
            raise Exception("Empty")
        return self.front.value
























class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.no = len(flights)
        self.check_list = [0]*(self.no+1)
        self.lis  = flights
        self.check_list2 = [False]*(self.no+1)
        for i in flights:
            self.check_list[i.start_city] += 1
        lis = [[] for _ in range(self.no)] 
        k  =-1
        # for i in self.check_list:
        #     k +=1
        #     if(i != 0):
        #         lis.append([k,[]])
        #         self.check_list[k] = len(lis)-1

        for i in flights:
            lis[i.start_city].append(i)
   
        self.adjacency_list =lis      
    def bfs_all_shortest_paths3(self,graph, source:Flight, destination:Flight,t1,t2):
        if source.start_city == destination.start_city:
            return [source]
        queue = Heap(comparator_innovate)
        queue.insert([0,0,[source]])
        source.visited = True
        all_shortest_paths = []
        shortest_length = float('inf')
        min_arrival  = float('inf')
        while  queue.heap:
            
            fare,length,current_path = queue.extract()
            current_node = current_path[-1]
            if length > shortest_length:
                continue
            for neighbor in graph[current_node.end_city] :
                if neighbor.visited == False and (((neighbor.departure_time -current_path[-1].arrival_time)>=20) or length <= 0) and neighbor.arrival_time<=t2 and neighbor.departure_time>=t1:  # Avoid cycles
                    current_path.append(neighbor)
                    neighbor.visited = True
                    new_path = current_path[:]
                    new_length = length +1
                    new_fare = fare + neighbor.fare
                    if neighbor.end_city == destination.start_city:
                        if new_length+1 < shortest_length:
                            shortest_length = new_length+1
                            all_shortest_paths = new_path
                            min_arrival = new_fare
                        elif new_length+1 == shortest_length and new_fare<min_arrival:
                            min_arrival = new_fare
                            all_shortest_paths = new_path
  
                    else:
                        queue.insert([new_fare,new_length,new_path])
                        
                    # current_path[-1].visited = False
                    current_path.pop()  
        for i in self.lis:
            i.visited = False
        

            
        return all_shortest_paths
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        dummy1 = Flight(-1,start_city,0,start_city,-20,0)
        dummy2 = Flight(-2,end_city,0,end_city,-20,0)

        req = self.bfs_all_shortest_paths2_use(self.adjacency_list,dummy1,dummy2,t1,t2)
        final = req
        final2 = []
        for i in final:
            if(i.end_city != start_city):
                final2.append(i)     
          
        return final2

    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        dummy1 = Flight(-1,start_city,0,start_city,-20,0)
        dummy2 = Flight(-2,end_city,0,end_city,-20,0)
        req =  self.bfs_to_be_Dj(self.adjacency_list,dummy1,dummy2,t1,t2)
        final = req
        final2 = []
        for i in final:
            if(i.start_city != i.end_city):
                final2.append(i)  
        if(req == None):
            return []
        return final2
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        dummy1 = Flight(-1,start_city,0,start_city,0,0)
        dummy2 = Flight(-2,end_city,0,end_city,0,0)

        req = self.bfs_all_shortest_paths3(self.adjacency_list,dummy1,dummy2,t1,t2)
        # maxp =float('inf') 
        final = req
        # for i in req:
        #     price = 0
        #     for k in i:
        #         price += k.fare
        #     if(price<maxp):
        #         final = i    

        final2 = []
        if(final == None):
            return final2
        for i in final:
            if(i.start_city != i.end_city):
                final2.append(i)        
        return final2
    def dijkstra(self, source:Flight, dest,t1,t2):
        adj = self.adjacency_list
        n =len(adj)
        dist = [float('inf')] * (self.no+1)
        parent = [-1] * (self.no+1)
        visited = [False] * (self.no+1)
        dist[source.end_city] = 0
        pq = Heap(comparator_fare)
        pq.insert((0, source))

        while pq.heap:
            d, u = pq.extract()
            # print(d,u.start_city,u.end_city,u.arrival_time,u.departure_time,u.fare)

            # If the node has already been visited, skip it
            if visited[u.end_city] or u.arrival_time>t2:
                continue
            
            visited[u.end_city] = True
            # print(adj[self.check_list[u.end_city]][1])
            # Process each neighbor of u
            for v in adj[u.end_city]:
                # # Relaxation step
                # print(d,u.start_city,u.end_city,u.arrival_time,u.departure_time,u.fare,"lol")
                # print(d,v.start_city,v.end_city,v.arrival_time,v.departure_time,v.fare,"sol")
                if ( v.departure_time-u.arrival_time)<20 or (v.arrival_time >t2 or  v.departure_time< t1):
                    continue
                
                if not visited[v.end_city] and dist[u.end_city] + v.fare < dist[v.end_city]:
                    dist[v.end_city] = dist[u.end_city] + v.fare
                    if ( v.departure_time-u.arrival_time)>=20:
                        parent[v.end_city] = v 
                    parent[v.end_city] = v 
                    pq.insert((dist[v.end_city], v))

        if dist[dest.end_city] == float('inf'):
            return
        path = []
        v = dest
        while v != -1:
            path.append(v)
            v = parent[v.start_city]
        path.reverse()
        path.pop()
        return path
    
    def bfs_all_shortest_paths2_use(self,graph, source:Flight, destination:Flight,t1,t2):
        if source.start_city == destination.start_city:
            return [source]
        
        # Queue to store paths during BFS traversal
        queue = Queue()
        queue.enqueue([0,source])
        source.visited = True
        shortest_length = float('inf')
        min_arrival  = float('inf')
        parent = [-1] * (self.no+1)
        
        while  not queue.isEmpty():
            length,current_path = queue.dequeue()
            current_node = current_path
            # print(current_path)
            # Stop exploring longer paths
            
            if length > shortest_length-1:
                continue
            # print(graph[current_node.end_city][1],current_node.end_city)
            for neighbor in graph[current_node.end_city] :
                if neighbor.visited == False and (((neighbor.departure_time -current_node.arrival_time)>=20) or length <= 0) and neighbor.arrival_time<=t2 and neighbor.departure_time>=t1:  # Avoid cycles
                    # print(neighbor,neighbor.arrival_time)
                    current_path = neighbor
                    neighbor.visited = True
                    new_path = current_path
                    new_length = length+1
                    
                    # Check if we've reached the destination
                    if neighbor.end_city == destination.start_city:
                        if new_length+1 < shortest_length:
                            # Found a new shortest length path
                            shortest_length = new_length+1
                            # all_shortest_paths = new_path
                            parent[neighbor.end_city] = neighbor
                            min_arrival = new_path.arrival_time
                        elif new_length+1 == shortest_length and new_path.arrival_time<min_arrival:
                            # Found another path of the same shortest length
                            parent[neighbor.end_city] = neighbor
                            min_arrival = new_path.arrival_time
                            # all_shortest_paths = new_path
                    else:
                        # Add the path for further exploration
                        # new_path = current_path
                        if(parent[neighbor.end_city] == -1 or (parent[neighbor.end_city].arrival_time>neighbor.arrival_time and new_length<shortest_length)):
                            parent[neighbor.end_city] = neighbor
                        queue.enqueue([new_length,new_path])
                    # current_path.visited = False
                    # current_path.pop()
            
        v = parent[destination.end_city] 
        p = []        
        check = [-1] * (self.no+1) 
        while(v!= -1   and v.end_city != source.start_city and check[v.end_city] == -1):
            check[v.end_city] = 0
            p.append(v)
            v = parent[v.start_city]
        p.reverse()
        for i in self.lis:
            i.visited = False
        return p
    def bfs_to_be_Dj(self,graph, source:Flight, destination:Flight,t1,t2):
        if source.start_city == destination.start_city:
            return [source]
        
        # Queue to store paths during BFS traversal
        queue = Heap(comparator_innovate2)
        queue.insert([0,[source]])
        source.visited = True
        all_shortest_paths = []
        min_arrival  = float('inf')
        while  queue.heap:         
            fare,current_path = queue.extract()
            current_node = current_path[-1]

            if(fare > min_arrival):
                continue

            for neighbor in graph[current_node.end_city] :
                if neighbor.visited == False and (((neighbor.departure_time -current_path[-1].arrival_time)>=20)) and neighbor.arrival_time<=t2 and neighbor.departure_time>=t1:  # Avoid cycles
                    current_path.append(neighbor)
                    neighbor.visited = True
                    new_path = current_path[:]
                    new_fare = fare + neighbor.fare
                    if neighbor.end_city == destination.start_city:
                        if  new_fare<min_arrival:
                            all_shortest_paths = new_path[:]
                            min_arrival = new_fare
                        elif new_fare == min_arrival:
                            min_arrival = new_fare
                            all_shortest_paths = new_path[:]
                    else:
                        queue.insert([new_fare,new_path])
                    # current_path[-1].visited = False
                    current_path.pop() 
        for i in self.lis:
            i.visited = False             
            
        return all_shortest_paths





