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
