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

#HW2 Perceptron, POS tagging and NER

This repository is for howework 2.

##Overview of codes submitted
* preproc.py
* AvgPerceptron.py
* Util.py
* perceplearn.py
* percepclassify.py
* nerEval.py
* postagging/postrain.py
* postagging/postag.py
* ner/nelearn.py
* ner/netag.py

##Overview of data sets

**_POS tagging_**

|**_Dataset Type_**|**_#sentence_**|**_#token_**|**_#tag_**|
|------------------|---------------|----------  |----------|
|train.pos         |20000          |474568      |47        |
|dev.pos           |1700           |40117       |46        |
|pos.blind.test    |2416           |56684       |N/A       |

**_Name Entity Recognition_**

|**_Dataset Type_**|**_#sentence_**|**_#token_**|**_#tag_**|
|------------------|---------------|----------  |----------|
|ner.esp.train     |8323           |264715      |9         |
|ner.esp.dev       |1915           |52923       |9         |
|ner.esp.blind.test|1517           |51533       |N/A       |

##Features

**_POS tagging_**

* current word
* previous word
* next word

**_Name Entity Recognition_**

* current word
* previous word
* next word
* current POS tag
* previous POS tag
* next POS tag

##Questions

####What is the accuracy of your part-of-speech tagger?

|**_Megam_**|**_Averaged Perceptron_**|
|-----------|-------------------------|
|0.947      |N/A(too slow, debugging) |

**_*All the results below are generated using Megam_**

####What are the precision, recall and F-score for each of the named entity types for your named entity recognizer, and what is the overall F-score?

|**_NE Types_**|**_Precision_**|**_Recall_**|**_F-score_**|
|--------------|---------------|------------|-------------|
|LOC           |0.5744234800838|0.5569105691|0.56553147574|
|ORG           |0.7209720972097|0.4711764705|0.56990394877|
|PER           |0.7742382271468|0.4574468085|0.57510288065|
|MISC          |0.4705882352941|0.2696629213|0.34285714285|

_Overall F-score_: 0.548627079669958

####What happens if you use your Naive Bayes classifier instead of your perceptron classifier (report performance metrics)? Why do you think that is?

_POS tagging_

|**_POS Tag_**|**_Precision_**|**_Recall_**|**_F-score_**|
|-------------|---------------|------------|-------------|
|PRP$         |1.0            |0.59375     |0.74509803921|
|VBG          |0.9180327868852|0.2857142857|0.43579766536|
|FW           |0              |0           |N/A          |
|VBN          |0.8940397350993|0.4764705882|0.62164236377|
|,            |1.0            |0.8334111059|0.90913718503|
|''           |0.8927335640138|0.9020979020|0.89739130434|
|VBP          |0.9513513513513|0.5161290322|0.66920152091|
|WDT          |0.8102564102564|0.8729281767|0.84042553191|
|JJ           |0.9361413043478|0.2787216828|0.42955112219|
|WP           |1.0            |0.8170731707|0.89932885906|
|VBZ          |0.9850374064837|0.5602836879|0.71428571428|
|DT           |0.9977578475336|0.7604671033|0.86310004848|
|#            |0.0187667560321|1.0         |0.03684210526|
|RP  		  |0.5952380952380|0.5859375   |0.59055118110|
|$            |0.9941348973607|0.9630681818|0.97835497835|
|NN           |0.9753881105641|0.4499563318|0.61582596222|
|VBD          |0.9884020618556|0.4498533724|0.61829907295|
|POS          |0.9934853420195|0.7126168224|0.82993197278|
|.            |1.0            |0.9940511600|0.99701670644|
|TO           |1.0            |0.8052995391|0.89215060625|
|PRP          |0.9942307692307|0.8447712418|0.9134275618 |
|RB           |0.9161676646706|0.3509174311|0.50746268656|
|-LRB-        |1.0            |0.65        |0.78787878787|
|NNS          |0.9876404494382|0.3510383386|0.51797289334|
|NNP          |0.9892682926829|0.2508038585|0.40015785319|
|``           |1.0            |0.8767123287|0.93430656934|
|WRB          |0.9324324324324|0.7840909090|0.85185185185|
|CC           |0.9966887417218|0.602       |0.75062344139|
|LS           |0.0002826455624|0.6666666666|0.00056505156|
|PDT          |0.015625       |1.0         |0.03076923076|
|RBS          |0.0319829424307|0.7894736842|0.06147540983|
|RBR          |0.82           |0.3904761904|0.52903225806|
|CD           |0.9958018471872|0.6428184281|0.78129117259|
|EX           |0.2406015037593|1.0         |0.38787878787|
|IN           |0.9840860215053|0.5683060109|0.72051645410|
|WP$          |0.0245901639344|1.0         |0.048        |
|MD           |0.9922178988326|0.7412790697|0.84858569051|
|NNPS         |0              |0           |N/A          |
|-RRB-        |0.9642857142857|0.8709677419|0.91525423728|
|JJS          |0.5818181818181|0.7356321839|0.64974619289|
|JJR          |0.7247706422018|0.5984848484|0.65560165975|
|SYM          |0.0            |N/A         |N/A          |
|VB           |0.9499358151476|0.7527975584|0.83995459704|
|UH           |0.0028797696184|0.8         |0.00573888091|

The measures of a lot of tags are very low. I think the reason is that the frequencies of those tags are too low. The classifier did not capture enough information to predict accuartely. Conversely, those tags with high frequency are predicted successfully, such as PRP, $ and so forth.

_Name Entity Recognition_

|**_NE Types_**|**_Precision_**|**_Recall_**|**_F-score_**|
|--------------|---------------|------------|-------------|
|LOC           |0.2334315169366|0.6443089430|0.34270270270|
|ORG           |0.2439716312056|0.5058823529|0.32918660287|
|PER           |0.4173134328358|0.5720130932|0.48256817397|
|MISC          |0.0260366441658|0.2426966292|0.04702808621|

Overall F-score: 0.28035333536399637

The same things happen in the _NER_ task. Only O tags can predicted well, the others are not predicted so well. I obverserved that the only O occurs most frequently in the training set, the numbers of other tags are really small compared to that of the O tag. The number of each tag is listed below. The precision of each tag is positively related to the frequncy of each tag.
