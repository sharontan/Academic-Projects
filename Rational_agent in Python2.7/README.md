An electronic product that has a $value and a $price can be in an Excellent condition, which works flawlessly, or in a Trash condition, where, hmm, it is trash. A purchase of a product in Excellent condition will increase the Agent's wealth by $value-$price. If, however, the product turns out to be Trash, the Agent's wealth decreases by $price. The condition of the product is not known until after the purchase. The objective is to increase the Agent's wealth as much as possible.

The Agent is not provided with the probability of the product being Excellent. Rather, the Agent needs to learn the features of Excellent and Trash products by going through an existing list of products whose conditions and features are known. Once it learns about Excellent and Trash products, given a product’s features, it should be able to predict the probability of it being Excellent.
1. train(self, X, y)
Given:
X: A matrix (2D numpy array) where rows correspond to products and columns correspond to feature values of those products. Each feature is a binary feature.
y: A 1D numpy array where each entry corresponds to whether a product is Excellent or Trash. The ith entry in y corresponds to the ith row in X.
Task:
Train the Agent to learn features of Excellent and Trash products.
2. predict_prob_of_excellent(self, x)
Given:
x: A 1D numpy array that corresponds to a single product.
Task:
Predict the probability of x being Excellent.

