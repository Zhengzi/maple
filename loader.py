import pickle
from serialization import Puis  ### look here ###
 
my_pat = pickle.load(file('my_pat.pickle'))
print my_pat.data
 
my_puis = pickle.load(file('my_puis.pickle'))
print my_puis.data