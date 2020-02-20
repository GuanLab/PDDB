import glob
import sklearn
import numpy as np
from sklearn import ensemble
 


the_train='feature_train.txt'
data=np.loadtxt(the_train)
X=data[:,1:]
Y=data[:,0]
est = sklearn.ensemble.RandomForestRegressor(n_estimators=100, max_depth=5, random_state=0).fit(X,Y)
    
test=np.loadtxt('feature_test.txt')
test_X=test[:,1:]
value=est.predict(test_X)
np.savetxt('prediction.dat',value)
    
    
    
