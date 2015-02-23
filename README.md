##Homework of csci544 applied natural language processing at USC

##HW1 Text Classification
Implement Naive Bayes Classifier to do spam filtering and sentiment analysis

##Overview of files submitted
* preproc.py
* postproc.py
* nblearn.py
* nbclassify.py
* NBClassifier.py
* Utility.py

##Overview of datasets
**_Spam dataset_**

**_Preprocessing_**

* All the tokens are converted into lower case
* All pure numbers are replaced by '/digit'. If the numiber is within the range [1000, 2100], it is replaced by '/year'.
* Stop words are removed. No more than 25 words are considered, the stop words are selected from [this paper](http://www.cs.uccs.edu/~jkalita/work/cs586/2010/Kalita2002NaiveBayes.pdf)[1]
* All the punctuations are removed
* 'Subject:' is removed. Because it appears in every example in the spam detection data sets, it does not make any sense in distinguishing betweent spams and hams

|**_Data_**     |**_# of examples_**|
|---------------|-------------------|
|Training set   |18441              |
|Development set|1361               |
|Test set       |2723               |

**_Sentiment analysis dataset_**

**_Preprocessing_**

* All pure numbers are replaced by '/digit'. If the numiber is within the range [1000, 2100], it is replaced by '/year'.
* All invalid tokens (string of size 0) are removed
* All punctuaion and blank characters in each token are removed
* Stop words are removed.
* A 10% random sample is extracted from the original data set as the development set

|**_Data_**     |**_# of examples_**|
|---------------|-------------------|
|Training set   |22594              |
|Development set|2406               |
|Test set       |25000              |

##Reference
[1] J. K. Kalita. Naive bayes classifier for spam detection, 2002

##Questions

####What are the precision, recall and F-score on the development data for your classifier in part I for each of the two datasets. Report precision, recall and F-score for each label.

#####Spam Detecion

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|
|-----------|---------------|------------|-------------|
|_SPAM_     |0.992          |0.984       |0.988        |
|_HAM_      |0.957          |0.978       |0.967        |

#####Sentiment Analysis

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|
|-----------|---------------|------------|-------------|
|_POS_      |0.836          |0.885       |0.860        |
|_NEG_      |0.874          |0.821       |0.847        |

####What are the precision, recall and F-score for your classifier in part II for each of the two datasets. Report precision, recall and F-score for each label.

#####_SVM_

######Spam Detection

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|
|-----------|---------------|------------|-------------|
|_SPAM_     |0.941          |0.477       |0.633        |
|_HAM_      |0.388          |0.917       |0.545        |

######Sentiment analysis

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|
|-----------|---------------|------------|-------------|
|_POS_      |0.509          |0.923       |0.657        |
|_NEG_      |0.510          |0.083       |0.142        |

#####_MegaM_

######Spam Detection

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|
|-----------|---------------|------------|-------------|
|_SPAM_     |0.840          |0.961       |0.897        |
|_HAM_      |0.821          |0.496       |0.618        |

######Sentiment analysis

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|
|-----------|---------------|------------|-------------|
|_POS_      |0.867          |0.852       |0.858        |
|_NEG_      |0.848          |0.868       |0.857        |

####What happens exactly to precision, recall and F-score in each of the two tasks (on the development data) when only 10% of the training data is used to train the classifiers in part I and part II? Why do you think that is?

Almost all the measures decreased evidently except the results of spam detection by naive bayes classifier. The reason of deceasing is that information is not enough. I think the reason why the results of naive bayes classifier are not so undermined is that the data given is well selected and within the same topics. Therefore the naive bayes classifer can capture enough information when fed a small portion of training data.

#####_Naive Bayes Classifier_

#####Spam Detecion

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|**_Precision(0.1)_**|**_Recall(0.1)_**|**_F-score(0.1)_**|
|-----------|---------------|------------|-------------|--------------------|-----------------|------------------|
|_SPAM_     |0.992          |0.984       |0.988        |0.991               |0.979            |0.985             |
|_HAM_      |0.957          |0.978       |0.967        |0.945               |0.975            |0.959             |

#####Sentiment Analysis

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|**_Precision(0.1)_**|**_Recall(0.1)_**|**_F-score(0.1)_**|
|-----------|---------------|------------|-------------|--------------------|-----------------|------------------|
|_POS_      |0.839          |0.881       |0.860        |0.802               |0.850            |0.825             |
|_NEG_      |0.873          |0.830       |0.851        |0.835               |0.783            |0.808             |

#####_SVM_

#####Spam Detecion

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|**_Precision(0.1)_**|**_Recall(0.1)_**|**_F-score(0.1)_**|
|-----------|---------------|------------|-------------|--------------------|-----------------|------------------|
|_SPAM_     |0.941          |0.477       |0.633        |0.735               |1.00             |0.847             |
|_HAM_      |0.388          |0.917       |0.545        |1.00                |0.003            |0.006             |

#####Sentiment Analysis

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|**_Precision(0.1)_**|**_Recall(0.1)_**|**_F-score(0.1)_**|
|-----------|---------------|------------|-------------|--------------------|-----------------|------------------|
|_POS_      |0.840          |0.961       |0.897        |0.520               |0.704            |0.599             |
|_NEG_      |0.510          |0.083       |0.142        |0.519               |0.329            |0.403             |

#####_MegaM_

#####Spam Detecion

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|**_Precision(0.1)_**|**_Recall(0.1)_**|**_F-score(0.1)_**|
|-----------|---------------|------------|-------------|--------------------|-----------------|------------------|
|_SPAM_     |0.840          |0.961       |0.897        |0.784               |0.996            |0.877             |
|_HAM_      |0.821          |0.496       |0.618        |0.956               |0.238            |0.381             |

#####Sentiment Analysis

|**_Label_**|**_Precision_**|**_Recall_**|**_F-score_**|**_Precision(0.1)_**|**_Recall(0.1)_**|**_F-score(0.1)_**|
|-----------|---------------|------------|-------------|--------------------|-----------------|------------------|
|_POS_      |0.839          |0.881       |0.860        |0.802               |0.646            |0.715             |
|_NEG_      |0.873          |0.830       |0.851        |0.695               |0.835            |0.759             |

