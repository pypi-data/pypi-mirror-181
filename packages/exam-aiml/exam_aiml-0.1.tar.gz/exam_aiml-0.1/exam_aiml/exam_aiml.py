class exam_aiml:
    def pgm1(self):
        print('''def aStarAlgo(start_node, stop_node):
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

    def heuristic(n):
        H_dist = {
            'S': 5,
            'A': 4,
            'B': 5,
            'E': 0,
        }
        return H_dist[n]
    Graph_nodes = {
        'S': [('A', 1), ('B', 2)],
        'A': [('E', 13),],
        'B': [('E', 5)] 
    }
    aStarAlgo('S', 'E')''')


    def pgm3(self):
        print('''
    import numpy as np 
    import pandas as pd
    data = pd.read_csv("ws.csv",header=None)
    concepts = np.array(data.iloc[:,0:-1])
    print("\nInstances are:\n",concepts)
    target = np.array(data.iloc[:,-1])
    print("\nTarget Values are: ",target)

    def learn(concepts,target): 
        specific_h = concepts[0].copy()
        print("\nInitialization of specific_h and genearal_h")
        print("\nSpecific Boundary: ", specific_h)
        general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
        print("\nGeneric Boundary: ",general_h)  

        for i,h  in enumerate(concepts):
            print("\nInstance", i+1 , "is ", h)
            if target[i] == "Yes":
                print("Instance is Positive ")
                for x in range(len(specific_h)): 
                    if h[x]!= specific_h[x]:                    
                        specific_h[x] ='?'                     
                        general_h[x][x] ='?'
                    
            if target[i] == "No":            
                print("Instance is Negative ")
                for x in range(len(specific_h)): 
                    if h[x]!= specific_h[x]:                    
                        general_h[x][x] = specific_h[x]                
                    else:                    
                        general_h[x][x] = '?'        
            
            print("Specific Boundary after ", i+1, "Instance is ", specific_h)         
            print("Generic Boundary after ", i+1, "Instance is ", general_h)
            print("\n")
        indices = [ i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]   
        for i in indices:   
            general_h.remove(['?', '?', '?', '?', '?', '?']) 
        return specific_h, general_h 
    s_final, g_final = learn(concepts,target)
    print("Final Specific_h: ", s_final, sep="\n")
    print("Final General_h: ", g_final, sep="\n")
    ''')

    def pgm5(self):
        print('''import numpy as np
    X=np.array(([2,9],[1,5],[3,6]),dtype=float)  #Features(Hrs Slept,Hrs Studied)
    y=np.array(([92],[86],[89]),dtype=float) #Labels(Marks Obtained)
    X=X/np.amax(X,axis=0)  #Normalize
    y=y/100
    def sigmoid(x):
        return 1/(1+np.exp(-x))
    def sigmoid_grad(x):
        return x*(1-x)
    #variable initialization
    epoch=1000  #Setting training iterations
    eta=0.2     # Setting learning rate(eta)
    input_neurons=2   # number of features in data set
    hidden_neurons=3  # number of hidden layers neurons
    output_neurons=1  
    # weight and bias random initialization
    wh=np.random.uniform(size=(input_neurons,hidden_neurons))
    bh=np.random.uniform(size=(1,hidden_neurons))
    wout=np.random.uniform(size=(hidden_neurons,output_neurons))
    bout=np.random.uniform(size=(1,output_neurons))
    for i in range(epoch):
    #forward propogation
        h_ip=np.dot(X,wh)+bh
        h_act=sigmoid(h_ip)
        o_ip=np.dot(h_act,wout)+bout
        output=sigmoid(o_ip)
    #Back propogation
    #Error at output layer
        Eo=y-output
        outgrad=sigmoid_grad(output)
        d_output=Eo*outgrad
    #Error at hidden layer
        Eh=d_output.dot(wout.T)
        hiddengrad=sigmoid_grad(h_act)
        d_hidden=Eh*hiddengrad
        wout+=h_act.T.dot(d_output)*eta
        wh+=X.T.dot(d_hidden)*eta
    print("Normalized Input:\n"+str(X))
    print("Actual Output:\n"+str(y))
    print("Predicted output:\n",output)
    ''')

    def pgm7(self):
        print('''
        import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np

    #import some data
    iris=datasets.load_iris()
    X=pd.DataFrame(iris.data)
    X.columns=['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
    y=pd.DataFrame(iris.target)
    y.columns=['Targets']


    #Build the K Means model
    model=KMeans(n_clusters=3)
    model.fit(X)    # model.labels_ : Gives cluster no for which samples belongs to

    #Visualize the clustering results
    plt.figure(figsize=(14,14))
    colormap=np.array(['red','lime','black'])

    #Plot the original classifications using Petal features 
    plt.subplot(2,2,1)
    plt.scatter(X.Petal_Length, X.Petal_Width,c=colormap[y.Targets],s=40)
    plt.title('Real Clusters')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')

    #Plot the models classification
    plt.subplot(2,2,2)
    plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[model.labels_],s=40)
    plt.title('K-means Clustering')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')

    #General EM for GMM
    from sklearn import preprocessing
    # transform your data such that its distribution will have a
    # mean value 0 and standard deviation of 1.
    scaler=preprocessing.StandardScaler()
    scaler.fit(X)
    xsa=scaler.transform(X)
    xs=pd.DataFrame(xsa,columns=X.columns)

    from sklearn.mixture import GaussianMixture
    gmm=GaussianMixture(n_components=3)
    gmm.fit(xs)
    gmm_y=gmm.predict(xs)

    plt.subplot(2,2,3)
    plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[gmm_y],s=40)
    plt.title('GMM Clustering')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')
    print("Observation:The GMM using EM algorithm based clustering matched the true labels more closely than Kmeans")
    plt.show()
    ''')

    def pgm8(self):
        print('''
        from sklearn.datasets import load_iris
    from sklearn.neighbors import KNeighborsClassifier
    import numpy as np
    from sklearn.model_selection import train_test_split
    iris_dataset=load_iris()

    print("\n IRIS FEATURES \ TARGET NAMES: \n ", iris_dataset.target_names)
    for i in range(len(iris_dataset.target_names)):
        print("\n[{0}]:[{1}]".format(i,iris_dataset.target_names[i]))

    print("\n IRIS DATA :\n",iris_dataset["data"])
    X_train, X_test, y_train, y_test = train_test_split(iris_dataset["data"], iris_dataset["target"], random_state=0)
    print("\n Target :\n",iris_dataset["target"])
    print("\n X TRAIN \n", X_train)
    print("\n X TEST \n", X_test)
    print("\n Y TRAIN \n", y_train)
    print("\n Y TEST \n", y_test)
    kn = KNeighborsClassifier(n_neighbors=1)
    kn.fit(X_train,y_train )

    x_new = np.array([[5, 2.9, 1, 0.2]])
    print("\n XNEW \n",x_new)
    prediction = kn.predict(x_new)
    print("\n Predicted target value: {}\n".format(prediction))
    print("\n Predicted feature name: {}\n".format(iris_dataset["target_names"][prediction]))
    i=1
    x= X_test[i]
    x_new = np.array([x])
    print("\n XNEW \n",x_new)

    for i in range(len(X_test)):
        x = X_test[i]
        x_new = np.array([x])
        prediction = kn.predict(x_new)
        print("\n Actual : {0} {1}, Predicted :{2}{3}".format(y_test[i],iris_dataset["target_names"][y_test[i]],prediction,iris_dataset["target_names"][prediction]))
    print("\n TEST SCORE[ACCURACY]: {:.2f}\n".format(kn.score(X_test, y_test)))

    ''')

    def pgm9(self):
        print('''
        import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    def kernel(point,xmat,k):
        m,n = np.shape(xmat)
        weights = np.mat(np.eye((m)))
        for j in range(m):
            diff=point - X[j]
            weights[j,j] = np.exp(diff*diff.T/(-2.0*k**2))
        return weights

    def localWeight(point,xmat,ymat,k):
        wei=kernel(point,xmat,k)
        W=(X.T*(wei*X)).I*(X.T*(wei*ymat.T))
        return W

    def localweightregression(xmat,ymat,k):
        m,n=np.shape(xmat)
        ypred=np.zeros(m)
        for i in range(m):
            ypred[i]=xmat[i]*localWeight(xmat[i],xmat,ymat,k)
        return ypred

    def graphplot(X,ypred):
        sortindex=X[:,1].argsort(0)
        xsort=X[sortindex][:,0]
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)
        ax.scatter(bill,tip,color='green')
        ax.plot(xsort[:,1],ypred[sortindex],color='red',linewidth=4)
        plt.xlabel('Total Bill')
        plt.ylabel('Tip')
        plt.show();

    data=pd.read_csv('data10_tips.csv')
    bill=np.array(data.total_bill)
    tip=np.array(data.tip)
    mbill=np.mat(bill)
    mtip=np.mat(tip)
    m=np.shape(mbill)[1]
    one=np.mat(np.ones(m))
    X=np.hstack((one.T,mbill.T))
    ypred=localweightregression(X,mtip,0.5)
    graphplot(X,ypred)

    ''')



#1,3,5,7.8,9