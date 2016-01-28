
from abc import abstractmethod


class Agent(object):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Agent_" + self.name
    
    def will_buy(self, value, price, prob):
        """Given a value, price, and prob of Excellence,
        return True if you want to buy it; False otherwise.
        The rational agent. Do NOT change or override this."""
        return value*prob > price

    @abstractmethod
    def train(self, X, y):
        """Train the agent to learn a function that
        can predict, probabilistically, whether
        a product is Excellent or Trash.
        Override this method.

        Parameters:
        -----------
        X: A matrix (2D numpy array) where rows correspond to
           products and columns correspond to feature values of
           those products.
        y: A 1D numpy array where each entry corresponds to
           whether a product is Excellent or Trash. The ith
           entry in y corresponds to the ith row in X.
        """

    @abstractmethod
    def predict_prob_of_excellent(self, x):
        """Given a single product, predict and return
        the probability of the product being Excellent.
        Override this method.

        Parameters:
        -----------
        x: A 1D numpy array that corresponds to a single product.        
        """


class Agent_hawk_stan9(Agent):

    def __init__(self, name):
        self.name = name
        super(Agent_hawk_stan9, self).__init__(name)
        self.table = []


    #p(Excellent)
    def prior_Excellent(self, y):
        count = 0
        total = y.shape[0]
        for i in range(total):
            if y[i] == "Excellent":
                count += 1
        priorE = float(count)/total
        return priorE


    #p(True) for individual features
    def evidence(self, X, feature, val):
        count = 0
        total = X.shape[0]
        for i in range(total):
            if X[i][feature] == val:
                count += 1
        evi = float(count)/total
        return evi


    #p(True|Excellent)
    def likelihood(self, X, y, feature, val, cond):
        count = 0
        total = 0
        for i in range(X.shape[0]):
            if X[i][feature] == val and y[i] == cond:
                count += 1
            if y[i] == cond:
                total += 1
        cond_p = float(count)/total
        return cond_p


    def train(self, X, y):
        feature_dict_T = {"ft" + str(i + 1) : self.evidence(X, i, True)\
                for i in range(X.shape[1])}
        feature_dict_F = {"ft" + str(i + 1) : self.evidence(X, i, False)\
                for i in range(X.shape[1])}
        cond_TE = {"ft" + str(i + 1) : self.likelihood(X, y, i, True, "Excellent")\
                for i in range(X.shape[1])}
        cond_FE = {"ft" + str(i + 1) : self.likelihood(X, y, i, False, "Excellent")\
                for i in range(X.shape[1])}
     
        self.table.append(feature_dict_T)
        self.table.append(feature_dict_F)
        self.table.append(cond_TE)
        self.table.append(cond_FE)
        self.table.append(self.prior_Excellent(y))
        
        return self.table


    def predict_prob_of_excellent(self, x):
        p_ftrue = 1
        cp_true = 1
        p_ffalse = 1
        cp_false = 1
        for i in range(x.shape[0]):
            if x[i] == True:
                p_ftrue *= self.table[0]["ft"+str(i+1)]
                cp_true *= self.table[2]["ft"+str(i+1)]
            if x[i] == False:
                p_ffalse *= self.table[1]["ft"+str(i+1)]
                cp_false *= self.table[3]["ft"+str(i+1)]
        num = cp_true * cp_false * self.table[4]
        den = p_ftrue * p_ffalse
        predict = float(num)/den
        if predict > 1:
            predict = 1             #probability capped at 1
      
        return predict 

