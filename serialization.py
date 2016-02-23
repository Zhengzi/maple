import pickle
 
print "defining the class Puis"
class Puis:
    def __init__(self, x):
        self.data = "I'm Puis '%d'" % x
 
# code in case of standalone usage
if __name__ == '__main__':
    from pat import *
    my_pat  = Pat(1234)
    my_puis = Puis(5678)
    pickle.dump(my_pat, file('my_pat.pickle','w'))
    pickle.dump(my_puis, file('my_puis.pickle','w'))