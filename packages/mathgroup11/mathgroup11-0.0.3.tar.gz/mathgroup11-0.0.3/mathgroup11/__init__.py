def connectArray(list1, list2): 
    return list1 + list2

def calculate_mean(n):
    s = sum(n)
    N = len(n)
    
    mean = s / N
    
    return mean

def sum_List(n, lst):
    answer = 0
    for v in lst:
        answer += v
    return answer

def myMax(list1):
    max = list1[0]

    for x in list1:
        if x > max:
            max = x
 
    return max

