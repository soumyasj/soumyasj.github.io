---
title: "<div style='clear: both;'> Classification of Emotions in Music"
excerpt: "<img src='/images/CS365-project/cs365_confusion_matrices.png' width='100' height='100' style='float: left; margin-right: 1em; margin-bottom: 1em;'>Comparative study of the different classifiers and their ability to predict different emotions in music.<br>"
collection: projects
---
January 2016 - April 2016 \
Advisor : Dr. Amitabha Mukerjee and Dr. Piyush Rai, Department of CSE, IIT Kanpur


In this project, we used the dataset made available by (Renato Panda et al., 2012) which consists of 903 audio clips of 30 seconds each prepared from All Music.com dataset. Emotional classification is attempted on the corpus using spectral features. The spectral features we used are Mel Frequency Cepstral Coefficients(MFCCs), RMS of amplitudes (for loudness), Spectrul Flux, Spectral Mean, Spectral Centroid, Zero Crossing rate among other spectral features. This dataset is trained on multiple classifiers, wherein with each classifier, hyperparameters were fine-tuned using grid-search to find the best set of classifiers. We also used PCA to analyse the effect of dimentionality reduction. The lists of accuracies, precisions, and f1-scores are compared.



[poster](/files/CS365A/AI_poster.pdf){:.btn}

<img src='/images/CS365-project/cs365_confusion_matrices.png' width='300' height='300' >