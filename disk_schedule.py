#-*- coding:utf-8 -*-
import random

def get_SCAN_direction(current,input):
    '''
    Decide the initial direction the SACN choose,up or down.
    Compare the current location with the first visited location,
    if they are the same, compared the current with the next of the list.
    It is impossible that this function runs more than two times.
    '''
    if current-input[0] > 0:
        direction = u'down'
    elif current-input[0] < 0:
        direction = u'up'
    else:
        get_SCAN_direction(current,input[1:])
    return direction    

def SCAN(current,input):
    '''
    SACN algorithm act as a elevator,continue to travel in current direction
    until the end, then go the opposite direction till the ohter end.
    '''
    direction = get_SCAN_direction(current,input)
    first = input[0]
    input.append(current)
    input.sort()
    if current == input[-1]:
        path_cost = current-input[0]
        visited_list = list(reversed(input))
    elif input[0] < current < input[-1]:    

        index = input.index(current)
        if direction == u'down':
            visited_list=list(reversed(input[0:index+1]))+input[index+1:]
            path_cost=input[-1]+current-input[0]*2
        else:
            visited_list=input[index:]+list(reversed(input[:index]))
            path_cost=input[-1]*2-current-input[0]
    else:
        path_cost= input[-1] - current
        visited_list = input
    return path_cost,visited_list


def SSF(current,input):
    '''
    Shortest seek first, keep comparing the two neighbours of current. The 
    closest one goes first. When raise a IndexError, the current must be the
    first(0) or last one(-1) of the sorted list. Then the problem is easy now,
    travels in one direction, up or down depends on first or last. 
    '''
    visited_list=[]
    path_cost = 0
    input.append(current)
    input.sort()#add the current to the input and sort the input
    try:
        while input:
            index=input.index(current)#current location
            if input[index-1]-current >= input[index+1]-current:
                path_cost += (input[index+1]-current)
                visited_list.append(current)
                current = input[index+1]#next current
                input.pop(index)#remove current
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

def generate_data():
    input=[]
    count=0
    while count < 20:
        input.append(random.randint(1,65536))
        count+=1
    input=list(set(input))    
    current = random.randint(1,65536)
    return input,current


if __name__ == '__main__':
    input,current = generate_data()
    input=[100, 50, 10, 20, 75]
    current=35
    print 'input:%s\ncurrent:%s'%(input,current)
    print 'SCAN\npathcost:%s\nvisited order:%s'%SCAN(current,input[:])
    print 'SSF\npathcost:%s\nvisited order:%s'%SSF(current,input[:])
    
