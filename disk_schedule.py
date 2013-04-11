#-*- coding:utf-8 -*-
import random
CYLINDER_START = 1
CYLINDER_END = 1024

def get_SCAN_direction(current,input):
    '''
    Decide the initial direction the SACN choose,up or down.
    Comparing the current track with the first should visited track of
    the input list,if two track numbers are the same, compared the current track
    with the next track.It is impossible that this function runs more than
    two times,because the input is a set of number.
    '''
    if current-input[0] > 0:
        return u'down'
    elif current-input[0] < 0:
        return  u'up'
    else:
        # current == input[0]
        return get_SCAN_direction(current,input[1:])

def SCAN(current,input):
    '''
    SACN algorithm acts like a elevator, continue to travel in current direction
    until the end, then go the opposite direction till the other end.
    '''
    direction = get_SCAN_direction(current,input)
    input.append(current)
    input.sort()
    if current == input[-1]:
        #current is the end of the list, so just go down all the way
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
    reached the last request in the current direction, acts as a elevator.
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
    direction = get_SCAN_direction(current,input)
    input.append(current)
    input.sort()
    index = input.index(current)
    if input.count(current) > 1:
        index += 1
    if direction == u'down':
        visited_list = list(reversed(input[:index+1])) + list(reversed(input[index+1:]))
    else:
        visited_list = input[index+1:] + input[:index+1]
    path_cost = (input[-1] - input[0]) * 2    
    return path_cost, visited_list    

def SSF(current,input):
    '''
    Shortest seek first, keep comparing the two neighbours of current track.
    The closest one goes first. When raise a IndexError, the current must be the
    first(0) or last(-1) track of the sorted list. Then the rest problem is easy
    now, travels in one direction, up or down depends on first or last. 
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
    First in , first out
    '''
    path_cost = 0
    input.insert(0,current)
    visited_list = input
    for n in range(len(visited_list)-1):
    #considered to use xrange, but xrange will be remove in the future    
        path_cost += abs(visited_list[n]-visited_list[n+1])
    return path_cost, visited_list

def RSS(current,input):
    '''
    Random scheduling
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
    while count < 20:
        input.append(random.randint(CYLINDER_START,CYLINDER_END))
        count+=1
    input=list(set(input))    
    current = random.randint(CYLINDER_START,CYLINDER_END)
    return input,current


if __name__ == '__main__':
    input,current = generate_data()
    input=[1,2,334,454,676,3,434,78,899,232,343,454,782,45,13,1024]
    print 'input:%s\ncurrent track:%s'%(input,current)
    print 'Using SCAN\npath cost:%s\nvisited order:%s'%SCAN(current,input[:])
    print 'Using LOOK\npath cost:%s\nvisited order:%s'%LOOK(current,input[:])
    print 'Using CSCAN\npath cost:%s\nvisited order:%s'%CSCAN(current,input[:])
    print 'Using SSF\npath cost:%s\nvisited order:%s'%SSF(current,input[:])
    print 'Using FIFO\npath cost:%s\nvisited order:%s'%FIFO(current,input[:])
    print 'Using RSS\npath cost:%s\nvisited order:%s'%RSS(current,input[:])
    
