---
title: "<div style='clear: both;'>Explorations in handwritten digit classification using the MNIST data"
excerpt: " <img src='/images/MNIST-project/mnist.png' width='100' height='100' style='float: left; margin-right: 1em; margin-bottom: 1em;' > Implemented and analysed different machine learning tools and algorithms to classify the handwritten digits in the MNIST dataset.<br>" 
collection: projects
---
July 2016 - November 2016 \
Advisor : Dr. Piyush Rai, Department of CSE, IIT Kanpur


In this project, we tried out different learning algorithms and/or combinations thereof, to see what’s the best classification accuracy you can achieve on the test data of Handwritten Digit Recognisation problem using the MNIST dataset. We used PCA to reduce the dimention of each image feature vector to 50 (from 784=28x28) as eigen decomposition of covariance matrix showed that 82.8% of variance is covered by top 50 eigen vectors. We did a comparative analysis of SVM, K-NN, Random Forest, and Log-regression algorithms in classifying the handwritten digits. We also implemented and analysed neural network based methods LeNet and Disturbed LeNet in which a subset of training data is randomly selected and its labels are corrupted to reduce overfitting and to better generalize the model.

[presentation](/files/CS771A/cs771_presentation.pdf){:.btn}

<!-- <img src='/images/MNIST-project/mnist.png' width='300' height='300' > -->