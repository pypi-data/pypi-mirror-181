import pyperclip
class data:
    
    def __init__(self):
        pass
    
    def cpy(self,pgn):
        p1 = '''
def aStarAlgo(start_node, stop_node):
    
    open_set = set(start_node)
    closed_set = set()
    g = {}
    parents = {}
    g[start_node] = 0
    parents[start_node] = start_node

    while len(open_set) > 0 :
        n = None

        for v in open_set:
            if n == None or g[v] + heuristic(v) < g[n] + heuristic(n):
                n = v

        if n == stop_node or Graph_nodes[n] == None:
            pass
        else:
            for (m, weight) in get_neighbors(n):
                if m not in open_set and m not in closed_set:
                    open_set.add(m)      
                    parents[m] = n       
                    g[m] = g[n] + weight 

                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)

        if n == None:
            print('Path does not exist!')
            return None

        if n == stop_node:
            path = []

            while parents[n] != n:
                path.append(n)
                n = parents[n]

            path.append(start_node)

            path.reverse()

            print('Path found: {}'.format(path))
            return path

        open_set.remove(n)
        closed_set.add(n)

    print('Path does not exist!')
    return None

def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        return None
#
 
def heuristic(n):
    H_dist = {
        'A': 10,
        'B': 8,
        'C': 5,
        'D': 7,
        'E': 3,
        'F': 6,
        'G': 5,
        'H': 3,
        'I': 1,
        'J': 0
    }

    return H_dist[n]

Graph_nodes = {
    
    'A': [('B', 6), ('F', 3)],
    'B': [('C', 3), ('D', 2)],
    'C': [('D', 1), ('E', 5)],
    'D': [('C', 1), ('E', 8)],
    'E': [('I', 5), ('J', 5)],
    'F': [('G', 1),('H', 7)] ,
    'G': [('I', 3)],
    'H': [('I', 2)],
    'I': [('E', 5), ('J', 3)],

}
aStarAlgo('A', 'J')
'''
        p2 = '''
class Graph:
    def __init__(self, graph, heuristicNodeList, startNode):

        self.graph = graph
        self.H=heuristicNodeList
        self.start=startNode
        self.parent={}
        self.status={}
        self.solutionGraph={}

    def applyAOStar(self):
        self.aoStar(self.start, False)

    def getNeighbors(self, v):
        return self.graph.get(v,'')

    def getStatus(self,v):
        return self.status.get(v,0)

    def setStatus(self,v, val):
        self.status[v]=val

    def getHeuristicNodeValue(self, n):
        return self.H.get(n,0)

    def setHeuristicNodeValue(self, n, value):
        self.H[n]=value


    def printSolution(self):
        print("FOR GRAPH SOLUTION, TRAVERSE THE GRAPH FROM THE STARTNODE:",self.start)
        print("------------------------------------------------------------")
        print(self.solutionGraph)
        print("------------------------------------------------------------")

    def computeMinimumCostChildNodes(self, v):
        minimumCost=0
        costToChildNodeListDict={}
        costToChildNodeListDict[minimumCost]=[]
        flag=True
        for nodeInfoTupleList in self.getNeighbors(v):
            cost=0
            nodeList=[]
            for c, weight in nodeInfoTupleList:
                cost=cost+self.getHeuristicNodeValue(c)+weight
                nodeList.append(c)
        
            if flag==True:
                minimumCost=cost
                costToChildNodeListDict[minimumCost]=nodeList
                flag=False
            else:
                if minimumCost>cost:
                    minimumCost=cost
                    costToChildNodeListDict[minimumCost]=nodeList


        return minimumCost, costToChildNodeListDict[minimumCost]


    def aoStar(self, v, backTracking):

        print("HEURISTIC VALUES :", self.H)
        print("SOLUTION GRAPH :", self.solutionGraph)
        print("PROCESSING NODE :", v)

        print("-----------------------------------------------------------------------------------------")
    
        if self.getStatus(v) >= 0:
            minimumCost, childNodeList = self.computeMinimumCostChildNodes(v)
            self.setHeuristicNodeValue(v, minimumCost)
            self.setStatus(v,len(childNodeList))

            solved=True
        
            for childNode in childNodeList:
                self.parent[childNode]=v
                if self.getStatus(childNode)!=-1:
                    solved=solved & False

            if solved==True:
                self.setStatus(v,-1)
                self.solutionGraph[v]=childNodeList


            if v!=self.start:
                self.aoStar(self.parent[v], True)

            if backTracking==False:
                for childNode in childNodeList:
                    self.setStatus(childNode,0)
                    self.aoStar(childNode, False)

h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 7, 'J':1, 'T': 3}
graph1 = {
    'A': [[('B', 1), ('C', 1)], [('D', 1)]],
    'B': [[('G', 1)], [('H', 1)]],
    'C': [[('J', 1)]],
    'D': [[('E', 1), ('F', 1)]],
    'G': [[('I', 1)]]
}
G1= Graph(graph1, h1, 'A')
G1.applyAOStar()
G1.printSolution()

h2 = {'A': 1, 'B': 6, 'C': 12, 'D': 10, 'E': 4, 'F': 4, 'G': 5, 'H': 7}
graph2 = {
    'A': [[('B', 1), ('C', 1)], [('D', 1)]],
    'B': [[('G', 1)], [('H', 1)]],
    'D': [[('E', 1), ('F', 1)]]
}

G2 = Graph(graph2, h2, 'A')
G2.applyAOStar()
G2.printSolution()
'''
        p3 = '''
import numpy as np
import pandas as pd
data=pd.DataFrame(data=pd.read_csv('trainingexamples.csv'))
concepts=np.array(data.iloc[:,0:-1])
target=np.array(data.iloc[:,-1])

def learn(concepts,target):
    specific_h=concepts[0].copy()
    general_h=[["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    
    for i,h in enumerate(concepts):
        if target[i]=="Yes":
            
            for x in range(len(specific_h)):
                if h[x]!=specific_h[x]:
                    specific_h[x]='?'
                    general_h[x][x]='?'
        if target[i]=="No":
            
            for x in range(len(specific_h)):
                if h[x]!=specific_h[x]:
                    general_h[x][x]=specific_h[x]
                else:
                    general_h[x][x]='?'
                    
    indices=[i for i, val in enumerate(general_h) if val==['?','?','?','?','?','?']]
    for i in indices:
        general_h.remove(['?','?','?','?','?','?'])
    return specific_h,general_h

s_final,g_final=learn(concepts,target)
print("Final S: ",s_final)
print("")
print("Final G: ",g_final)
'''
        p4 = '''
import pandas as pd
import math
import numpy as np
data=pd.read_csv("tennis.csv")
features=[feat for feat in data]
features.remove("answer")
class Node:
    
    def __init__(self):
        self.children=[]
        self.value=""
        self.isLeaf=False
        self.pred=""
        
def entropy(examples):
        pos=0.0
        neg=0.0
        for _, row in examples.iterrows():
            if row["answer"]=="yes":
                pos+=1
            else:
                neg+=1
        if pos==0.0 or neg==0.0:
            return 0.0
        else:
            p=pos/(pos+neg)
            n=neg/(pos+neg)
            return -(p*math.log(p,2)+ n*math.log(n,2))
        
def info_gain(examples,attr):
        uniq=np.unique(examples[attr])
        gain=entropy(examples)
        for u in uniq:
            subdata=examples[examples[attr]==u]
            sub_e=entropy(subdata)
            gain-=(float(len(subdata))/float(len(examples)))*sub_e
        return gain
    
def ID3(examples,attrs):
        root= Node()
        max_gain=0
        max_feat=""
        for feature in attrs:
            gain=info_gain(examples, feature)
            if gain>max_gain:
                max_gain=gain
                max_feat=feature
            root.value=max_feat
            uniq=np.unique(examples[max_feat])
        for u in uniq:
            subdata=examples[examples[max_feat]==u]
            if entropy(subdata)==0.0:
                newNode=Node()
                newNode.isLeaf=True
                newNode.value=u
                newNode.pred=np.unique(subdata["answer"])
                root.children.append(newNode)
            else:
                dummyNode=Node()
                dummyNode.value=u
                new_attrs=attrs.copy()
                new_attrs.remove(max_feat)
                child=ID3(subdata, new_attrs)
                dummyNode.children.append(child)
                root.children.append(dummyNode)
        return root
    
def printTree(root: Node, depth=0):
        for i in range(depth):
             print("\t",end="")
        print(root.value,end="")
        if root.isLeaf:
            print("->",root.pred)
        print()
        for child in root.children:
            printTree(child, depth+1)
                    
def classify(root: Node, new):
        for child in root.children:
            if child.value==new[root.value]:
                if child.isLeaf:
                    print("Predicted Label foer new example", new, "is", child.pred)
                    exit
                else:
                    classify(child.children[0], new)
root=ID3(data,features)
print("Decsion tree is")
printTree(root)
print("---------------")
    
new={"outlook":"sunny","temparature":"hot","humidity":"normal","wind":"strong"}
classify(root,new)
'''
        p5 = '''
import numpy as np
X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([92], [86], [89]), dtype=float)
X = X/np.amax(X,axis=0)
y = y/100

def sigmoid (x):
    return 1/(1 + np.exp(-x))

def derivatives_sigmoid(x):
    return x * (1 - x)

epoch=5000                
lr=0.1                    
inputlayer_neurons = 2   
hiddenlayer_neurons = 3   
output_neurons = 1       

wh=np.random.uniform(size=(inputlayer_neurons,hiddenlayer_neurons))
bh=np.random.uniform(size=(1,hiddenlayer_neurons))
wout=np.random.uniform(size=(hiddenlayer_neurons,output_neurons))
bout=np.random.uniform(size=(1,output_neurons))

for i in range(epoch):
    
    hinp1=np.dot(X,wh)
    hinp=hinp1 + bh
    hlayer_act = sigmoid(hinp)
    outinp1=np.dot(hlayer_act,wout)
    outinp= outinp1+ bout
    output = sigmoid(outinp)
    
    EO = y-output
    outgrad = derivatives_sigmoid(output)
    d_output = EO* outgrad
    EH = d_output.dot(wout.T)

    hiddengrad = derivatives_sigmoid(hlayer_act)
    d_hiddenlayer = EH * hiddengrad
    
    wout += hlayer_act.T.dot(d_output) *lr
    wh += X.T.dot(d_hiddenlayer) *lr
    
print("Input : " + str(X))
print("Actual Output : " + str(y))
print("Predicted Output : " ,output)
'''
        p6 = '''
import numpy as np
import pandas as pd 
mush = pd.read_csv("mushroom.csv")
mush.replace('?',np.nan,inplace=True)
print(len(mush.columns),"columns,after dropping NA,",len(mush.dropna(axis=1).columns))
 
mush.dropna(axis=1,inplace=True)    
    
target = 'class'
features = mush.columns[mush.columns != target]
classes = mush[target].unique()
test = mush.sample(frac=0.3)
mush = mush.drop(test.index)
probs = {}
probcl = {}
for x in classes:
    mushcl = mush[mush[target]==x][features]
    clsp = {}
    tot = len(mushcl)
    for col in mushcl.columns:
        colp = {}
        for val,cnt in mushcl[col].value_counts().iteritems():
            pr = cnt/tot
            colp[val] = pr
            clsp[col] = colp
     
    probs[x] = clsp
    probcl[x] = len(mushcl)/len(mush)
def probabs(x):
    if not isinstance(x,pd.Series):
        raise IOError("Arg must of type Series")
    probab = {}
    
    for cl in classes:
        pr = probcl[cl]
        for col,val in x.iteritems():
            try:
                pr *= probs[cl][col][val]
            except KeyError:
                pr=0
        probab[cl] = pr
    return probab

def classify(x):
        probab = probabs(x)
        mx = 0
        mxcl=''
        for cl,pr in probab.items():
            if pr>mx:
                mx=pr
                mxcl=cl
        return mxcl
b = []
for i in mush.index:
    b.append(classify(mush.loc[i,features])==mush.loc[i,target])
        
print(sum(b),"correct of",len(mush))
print("Accuracy:",sum(b)/len(mush))
    
b=[]
for i in test.index:
    b.append(classify(test.loc[i,features])==test.loc[i,target])
print(sum(b),"correct of ",len(test))
print("Accuracy:",sum(b)/len(test))
'''
        p7 = '''
from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
# Importing the dataset
data = pd.read_csv('ex.csv')
print("Input Data and Shape")
print(data.shape)
data.head()
print(data.head())
# Getting the values and plotting it
f1 = data['V1'].values
print("f1")
print(f1)
f2 = data['V2'].values
X = np.array(list(zip(f1, f2)))
print("x")
print(X)
print('Graph for whole dataset')
plt.scatter(f1, f2, c='black', s=600)
plt.show()
##########################################
kmeans = KMeans(2, random_state=0)
labels = kmeans.fit(X).predict(X)
print("labels")
print(labels)
centroids = kmeans.cluster_centers_
print("centroids")
print(centroids)
plt.scatter(X[:, 0], X[:, 1], c=labels, s=40);
print('Graph using Kmeans Algorithm')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=200, c='#050505')
plt.show()
#gmm demo
gmm = GaussianMixture(n_components=2).fit(X)
labels = gmm.predict(X)
print("lLABELS GMM")
print(labels)
probs = gmm.predict_proba(X)
size = 10 * probs.max(1) ** 3
print('Graph using EM Algorithm')
#print(probs[:300].round(4))
plt.scatter(X[:, 0], X[:, 1], c=labels, s=size, cmap='viridis');
plt.show()
'''
        p8 = '''
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.model_selection import train_test_split
iris_dataset=load_iris()
print("")
print(" IRIS FEATURES \ TARGET NAMES: ", iris_dataset.target_names)
print("")
for i in range(len(iris_dataset.target_names)):
    print("")
    print("[{0}]:[{1}]".format(i,iris_dataset.target_names[i]))

print("")    
print(" IRIS DATA :",iris_dataset["data"])
print("")

X_train, X_test, y_train, y_test=train_test_split(iris_dataset["data"],iris_dataset["target"],random_state=0)

print("")
print("Target :", iris_dataset["target"])
print("")
print("X TRAIN ",X_train)
print("")
print("X TEST ",X_test)
print("")
print("Y TRAIN ",y_train)
print("")
print("Y TEST ",y_test)
print("")
kn=KNeighborsClassifier(n_neighbors=1)
kn.fit(X_train, y_train)

for i in range(len(X_test)):
    x=X_test[i]
    x_new=np.array([x])
    prediction=kn.predict(x_new)
    print("")
    print(" Actual : {0}{1}, Predicted : {2}{3}".format(y_test[i],iris_dataset["target_names"][y_test[i]],prediction,iris_dataset["target_names"][prediction]))
    print("")
    print(" TEST SCORE[ACCURACY]: {:.2f}".format(kn.score(X_test, y_test)))
    print("")
'''
        p9 = '''
from numpy import *
import operator
from os import listdir
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from numpy.linalg import *
def kernel(point,xmat,k):
     m,n=shape(xmat)
     weights=mat(eye((m)))
     for j in range(m):
            diff= point -X[j]
            weights[j,j]=exp(diff*diff.T/(-2.0*k**2))
            return weights
def localWeight(point,xmat,ymat,k):
    wei=kernel(point,xmat,k)
    W=(X.T*(wei*X)).I*(X.T*(wei*ymat.T))
    return W

def localWeightRegression(xmat,ymat,k):
    m,n=shape(xmat)
    ypred=zeros(m)
    for i in range(m):
        ypred[i]=xmat[i]*localWeight(xmat[i],xmat,ymat,k)
    return ypred

data=pd.read_csv('tips.csv')
bill=array(data.total_bill)
tip=array(data.tip)
mbill=mat(bill)
mtip=mat(tip)
m=shape(mbill)[1]
one=mat(ones(m))
X=hstack((one.T,mbill.T))
ypred=localWeightRegression(X,mtip,10)
SortIndex=X[:,1].argsort(0)
xsort=X[SortIndex][:,0]
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.scatter(bill,tip,color='green')
ax.plot(xsort[:,1],ypred[SortIndex],color='red',linewidth=5)
plt.xlabel('Total bill')
plt.ylabel('Tip')
plt.show();
'''
        if pgn==1:
            pyperclip.copy(p1)
        if pgn==2:
            pyperclip.copy(p2)
        if pgn==3:
            pyperclip.copy(p3)
        if pgn==4:
            pyperclip.copy(p4)
        if pgn==5:
            pyperclip.copy(p5)
        if pgn==6:
            pyperclip.copy(p6)
        if pgn==7:
            pyperclip.copy(p7)
        if pgn==8:
            pyperclip.copy(p8)
        if pgn==9:
            pyperclip.copy(p9)
        print("Done")