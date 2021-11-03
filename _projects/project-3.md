---
title: "<div style='clear: both;'> Chest X-Ray Medical Diagnosis and Brain Tumor Auto-Segmentation for MRI"
excerpt: "<img src='/images/AI-for_medicine/3d-Unet.png' width='100' height='100' style='float: left; margin-right: 1em; margin-bottom: 1em;'>Part of AI for Medicine Specialization Course provided by deeplearning.ai<br>"
collection: projects
---
April 2020 - May 2020 \
AI for Medicine Specialization Course, deeplearning.ai


In the first part of this project, I trained the top-layers of pre-trained [DenseNet121](https://www.kaggle.com/pytorch/densenet121) model to diagnose pathologies (Pneumonia, Edema, Cardiomegaly) in Chest X-rays of [ChestX-ray8 dataset](https://arxiv.org/abs/1705.02315). To address class imbalance, which is usually very high in medical diagnosis data, a weighted cross-entropy loss is used to train the model. To increase the interpretability of model, a [GradCAM's](https://arxiv.org/abs/1610.02391) technique is used to produce a heatmap highlighting the important regions in the image for predicting the pathological condition. \
In the second part of the project, a [3D U-Net](https://arxiv.org/abs/1606.06650) model is trained for Volumetric Segmentation of MRI Images ([DICOM format](https://en.wikipedia.org/wiki/DICOM)) with Multi-Class Soft Dice Loss as the loss function using the data from the [Decathlon 10 Challenge](https://decathlon-10.grand-challenge.org/).



[certificate](https://www.coursera.org/verify/specialization/M7WHUXH9APQC){:.btn}

<img src='/images/AI-for_medicine/3d-Unet.png' width='300' height='300' >