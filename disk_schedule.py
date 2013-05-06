#-*- coding:utf-8 -*-
import random
import json

CYLINDER_START = 1 #cylinder NO. starts at 1
CYLINDER_END = 10240 # cylinderNO. ends at 1024 
#cylinder NO is also reference as track NO
ROUND= 100
DATA_LENGTH= 1000
ALGORITHMS=['SCAN','LOOK','CLOOK','CSCAN','SSF','FIFO','LIFO','RSS']
#ALGORITHMS=['CSCAN','LOOK','CLOOK']
#Names of algorithms ,used for dynamically call the corresponding functions

'''
          Input and output of each algorithms

The input data are a fix sized list of cylindes numbers, the parameter 'input' and
the current cylinder number which the head stays in- the parameter 'current'.
The output data are the total path cost of the seeking,the 'path_cost' and
the a list of the cylinders' number order by the visiting order, the 'visited_list'.
'''


def get_SCAN_direction(current,input):
    '''
    Decide the initial direction the SACN choose,up or down.
    Comparing the current track with the first should visited track of
    the input list,if two track numbers are the same, compared the current track
    with the next track.It is impossible that this function runs more than
    two times,because the input is a set of number, no repeated element.
    '''
    if current-input[0] > 0:
        return u'down'
    elif current-input[0] < 0:
        return  u'up'
    else:
        # just use 1 not a dynamic parameter 
        return get_SCAN_direction(current,input[1:])


def SCAN(current,input):
    '''
    SACN algorithm acts like a elevator, continue to travel in current direction
    until the end, then go the opposite direction till the other end.
    The start of the list will be describe as the ground/land floor,the end is 
    the toppest floor.
    '''
    #decide the scanning direction
    direction = get_SCAN_direction(current,input)
    #add current to the input, so the current will appear in the visited list,
    #a easy way to do it. 
    input.append(current)
    input.sort()
    if current == input[-1]:
        #current is the end of the list, so just going down all the way
        path_cost = current- CYLINDER_START
        visited_list = list(reversed(input))
    elif input[0] < current < input[-1]:    
        index = input.index(current)
        if direction == u'down':
            #first from current go down to the start of the input, 
            #then go up to the end
            visited_list=list(reversed(input[0:index+1]))+input[index+1:]
            path_cost = current + CYLINDER_END - CYLINDER_START*2
        else:
            #direction is up
            visited_list = input[index:] + list(reversed(input[:index]))
            path_cost = CYLINDER_END*2 - current - CYLINDER_START
    else:
        #current is the start of the list, so just go up all the way
        path_cost = CYLINDER_END - CYLINDER_START
        visited_list = input
    return path_cost,visited_list


def LOOK(current,input):
    '''
    LOOK is similar to SCAN,but LOOK will change directions when the head has
    reached the last request track in the current direction, acts exactly as a elevator.
    The difference of the implementations of two algorithms is path cost 
    '''
    direction = get_SCAN_direction(current,input)
    input.append(current)
    input.sort()
    if current == input[-1]:
        #current is the end of the list, so just go down all the way
        path_cost = current-input[0]
        visited_list = list(reversed(input))
    elif input[0] < current < input[-1]:    
        index = input.index(current)
        if direction == u'down':
            #first from current go down to the start of the input, 
            #then go up to the end
            visited_list=list(reversed(input[0:index+1]))+input[index+1:]
            path_cost=input[-1]+current-input[0]*2
        else:
            visited_list=input[index:]+list(reversed(input[:index]))
            path_cost=input[-1]*2-current-input[0]
    else:
        #current is the start of the list, so just go up all the way
        path_cost= input[-1] - current
        visited_list = input
    return path_cost,visited_list


def CSCAN(current,input):
    '''
    CSCAN make modification based on SCAN. CSCAN moves in one direction only.
    When the head reach the end of that direction, the head goes back and starts a 
    new seeking on the direction.
    '''
    direction = get_SCAN_direction(current,input)
    input.append(current)
    input.sort()
    index = input.index(current)
    flag=False
    if input.count(current) > 1:
    #this is the situation  there is a track NO which is the same as
    #the current track NO in the 'input'
        index += 1
        flag = True
    if direction == u'down':
        visited_list = list(reversed(input[:index+1])) + list(reversed(input[index+1:]))
        path_cost = current -CYLINDER_START
    else:
        if flag:
            visited_list = input[index-1:] + input[:index-1]
        else:    
            visited_list = input[index:] + input[:index]
        path_cost= CYLINDER_END - current

    path_cost += CYLINDER_END-CYLINDER_START
    return path_cost, visited_list    



def CLOOK(current,input):
    '''
    CLOOK is similar to CSCAN,but CLOOK will go back and restart at the same
    direction when the head has reached the last request in the current
    direction.
    '''
    direction = get_SCAN_direction(current,input)
    input.append(current)
    input.sort()
    if current == input[-1]:
        #current is the end of the list, so just go down all the way
        path_cost = current-input[0]
        visited_list = list(reversed(input))
    elif input[0] < current < input[-1]:    
        index = input.index(current)
        if direction == u'down':
            #first from current go down to the start of the input, 
            #then go up to the end
            visited_list=list(reversed(input[0:index+1]))+list(reversed(input[index+1:]))
            path_cost=input[-1]+current-input[0]*2
        else:
            visited_list=input[index:]+list(reversed(input[:index]))
            path_cost=input[-1]*2-current-input[0]
    else:
        #current is the start of the list, so just go up all the way
        path_cost= input[-1] - current
        visited_list = input
    return path_cost,visited_list
    


def SSF(current,input):
    '''
    Shortest seek first, keep comparing the two neighbours of current track.
    The closest one goes first.
    When raise a IndexError, the current must be the first(0) or last(-1) track
    of the sorted list. Then the rest problem is easynow, 
    travels in one direction, up or down depends on first or last. 
    '''
    visited_list=[]
    path_cost = 0
    input.append(current)
    input.sort()#add the current to the input list and sort the input
    try:
        while input:
            index=input.index(current)#current location
            if index == 0:
                raise IndexError
                #-1 is an legal index of a list in python,so raise this
                #error manually,becuase in next sentence, the index will
                # minus 1
            if current-input[index-1] >= input[index+1]-current:
                #comparing
                path_cost += (input[index+1]-current)
                visited_list.append(current)#add current to visited
                current = input[index+1]#set next current
                input.pop(index)#remove current from the input
            else:
                path_cost += (current-input[index-1])
                visited_list.append(current)
                current = input[index-1]
                input.pop(index)
    except IndexError,e:
        if index == 0:
            visited_list.extend(input[:])
        else:
            visited_list.extend(list(reversed(input[:])))
        path_cost += (input[-1]-input[0])
    return path_cost,visited_list

def FIFO(current,input):
    '''
    First in , first out. The head visit the tracks at the exact order of 
    the input list, first come in, first visited.
    '''
    path_cost = 0
    input.insert(0,current)
    visited_list = input
    for n in range(len(visited_list)-1):
    #considered to use xrange, but xrange will be remove in the future    
        path_cost += abs(visited_list[n]-visited_list[n+1])
    return path_cost, visited_list

def LIFO(current,input):
    '''
    Last in , first out. The head visit  the track at the opposite order of
    the input list, element last comes in ,first visited.
    '''
    path_cost = 0
    input.append(current)
    input.reverse()
    visited_list = input
    for n in range(len(visited_list)-1):
    #considered to use xrange, but xrange will be remove in the future    
        path_cost += abs(visited_list[n]-visited_list[n+1])
    return path_cost, visited_list



def RSS(current,input):
    '''
    Random scheduling,the head pick next shoude be visited track randomly.
    '''
    path_cost = 0
    visited_list=[current]
    while input:
        next = random.choice(input)
        input.remove(next)
        visited_list.append(next)
        path_cost += abs(current - next)
        current = next
    return path_cost, visited_list

def generate_data():
    '''
    Generate a set of number, each number in the input list
    stands for a request for the track of that number.Head is 
    in the current track at the beginning. 
    '''
    input=[]
    count=0
    while count < DATA_LENGTH:
        input.append(random.randint(CYLINDER_START,CYLINDER_END))
        count+=1
    input=list(set(input))    
    #the length of the list maybe less than DATA_LENGTH :)    
    current = random.randint(CYLINDER_START,CYLINDER_END)
    return current,input

def auto_test(local,n=None):

    current,input = generate_data()
    results=[]
    output = {'input':input,'current':current}
    for f in ALGORITHMS:
        funcs = local.get(f,None)
        if funcs:

            path_cost,visited_list = funcs(current,input[:])
            results.append({'name':funcs.__name__,'path_cost':path_cost,'visited_list':visited_list})
    output['results']=results
    return output    

if __name__ == '__main__':
    n=1
    results={}
    while n < ROUND+1:
        results[n]=auto_test(locals(),n)
        n+=1
    f=open('output.txt','w')
    f.write(json.dumps(results))
    f.close()

