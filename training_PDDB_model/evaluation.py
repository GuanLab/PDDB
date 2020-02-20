from sklearn.metrics import auc
import numpy as np
from sklearn.metrics import precision_recall_curve
import sklearn.metrics as metrics

y=np.loadtxt('feature_test.txt')
pred=np.loadtxt('prediction.dat')

print(y.shape)
fpr, tpr, thresholds = metrics.roc_curve(y[:,0], pred, pos_label=1)
the_auc=metrics.auc(fpr, tpr)
F=open('auc.txt','w')
F.write('%.4f\n' % the_auc)
F.close()

precision, recall, thresholds = precision_recall_curve(y[:,0], pred)
the_auprc = auc(recall, precision,reorder=False)
F=open('auprc.txt','w')
F.write('%.4f\n' % the_auprc)
F.close()
