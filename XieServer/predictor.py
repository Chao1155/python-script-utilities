#!/usr/bin/python

import csv

def read_csv(fileName):
    csvfile = open(fileName, 'rb')
    reader = csv.reader(csvfile)    # a list of list.
    return list(reader)

#Data = read_csv ('policies_100us.csv')
Data = read_csv ('policies_1us.csv')
Length = len(Data) - 1

def get_history(row, col, n):
    """ get n entries of history started from the (row, col)
    """
    code = 0
    for k in range (1, n+1, 1):
        if row - k < 2:
            info = 0
        else:
            info = int(Data[row - k][col]) # -1, 0, 1
            # take 0 as 1
            if info == -1:
                info = 0
            elif info == 0:
                info = 1
        code += info * (2**(k-1))
    return code

class Predictor(object):
    """ A naive (1,n) predictor
    """
    B_vec = 0
    Max_p = 1
    Mid_p = 1
    Mid_judge = 1
    B_vec = {}
    def __init__ (self, m =1, n = 1):
        self.Max_p = 2 ** n - 1
        self.Mid_p = self.Max_p /2 + 1
        for key in range(0,2 **m, 1):
            self.B_vec[key] = 0
        self.Mid_judge = (2 ** m) /2
    def predict(self, history):
    # make sure the input is a number, not a string!
        cur_try = 0
        if self.B_vec[history] >= self.Mid_p:
            cur_try = 1
        else:   # B_vec <= 0
            cur_try = -1
        if history >= self.Mid_judge and self.B_vec[history] < self.Max_p:
            self.B_vec[history] += 1
        if history < self.Mid_judge and self.B_vec[history] >0:
            self.B_vec[history] -= 1
#        print self.B_vec
        return cur_try
def test_error(a,b):
    if abs (int (a) - int (b)) > 1:
        return 1
    else:
        return 0
def find_the_best():
    M = 10
    N = 10
    smallest = 100000
    # The best one is (2, 2)
    for m in range (1, M, 1):
        for n in range (1,N,1):
        # search the space.
            total = 0;
            for j in range (0, len(Data[0]), 1):
                p1 = Predictor(m,n)
                errors = 0
                for i in range(0, Length + 1, 1):
                    if i <2:
                        #print Data[i][j]
                        pass
                    else:
                        choice1 = p1.predict(get_history(i,j, m))
                        errors += test_error(choice1, Data[i][j])
                total += errors
            print m, n, total
            if total < smallest:
                best = (m,n, total)
                smallest = total
    print "Best is ", best

            
def show_prediction(m=1, n=1):
    """ the above funtion show the best is 2.3 for 100us, 1,1 for 1us
    """
    total = 0;
    for j in range (0, len(Data[0]), 1):
        p1 = Predictor(m,n)
        errors = 0
        for i in range(0, Length + 1, 1):
            if i <2:
                #print Data[i][j]
                pass
            else:
                choice1 = p1.predict(get_history(i,j, m))
                errors += test_error(choice1, Data[i][j])
        print "%s\t%.4f" %(Data[0][j], float(errors)/Length)
        total += errors
    print "Total error rate is %.4f." % (float(total)/(Length * len(Data[0])))
#find_the_best()
show_prediction()
