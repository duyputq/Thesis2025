import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score

df_ddos = pd.read_csv('datasets/dataset_ddos.csv')
df_normal = pd.read_csv('datasets/dataset_normal.csv')

features_ddos = df_ddos[['SDFB', 'SDFP', 'RPF']]
features_normal = df_normal[['SDFB', 'SDFP', 'RPF']]

# Gộp 2 lớp lại thành ma trận đặc trưng X
X = pd.concat([features_ddos, features_normal], ignore_index=True).to_numpy()

# Tạo nhãn: DDoS là 1, Normal là 0
y_ddos = np.ones(len(features_ddos))    # Nhãn cho DDoS
y_normal = np.zeros(len(features_normal))  # Nhãn cho Normal
y = np.concatenate([y_ddos, y_normal])  # Gộp lại thành một mảng

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
svm=SVC(kernel='linear')
svm.fit(X_train, y_train)
y_predict = svm.predict(X_test)

print('Do chinh xac', accuracy_score(y_test, y_predict))
print('Precision', precision_score(y_test,y_predict))
print('Confusion Matrix', confusion_matrix(y_test, y_predict))

print("(weights):", svm.coef_)    
print("Bias (intercept):", svm.intercept_)

#45.645507957456395,0.46577048936179993,45,1.0,0
#8956384.161472624,51473.430898223814,212,0.18009478672985782,1

x_new = np.array([9000000, 50000, 0.2])

# w = svm.coef_
w = np.array([[ 3.84717557e-07,  2.21100421e-09, -7.26798815e-14]])
b = svm.intercept_
z = np.dot(w, x_new) + b
label = 1 if z >= 0 else 0

print(label)
print(w)
