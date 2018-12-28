# -*- coding: utf-8 -*-
"""
Created on December 12 2018
@author: Rajendra Sapkota
"""
from nltk.corpus import stopwords
from nltk import FreqDist, pos_tag, word_tokenize
from nltk.util import ngrams

skills_collection =set('python c c++ java javascript js angular angular js node'
                       'node js html css jquery bootstrap soap rest hibernate '
                       'spring restful jersey tomcat apache weblogic oracle mssql' 
                       'server mysql jenkins intellij eclipse netbeans webct elastic' 
                        'search git grunt bower buzilla rally agile devops database' 
                        'xhtml dhtml xml oop ajax scrum mvc notepad sublime' 
                        'komodo ui ux ria aem strurs spring framework sailpoint' 
                        'identityiq flask bottle sdlc jsp jsp gui swings plsql' 
                        'ddl dml dao pandas jupyter machine learning ai  elasticsearch' 
                        'linux  unix windows amazon kanban android ios django jira sql' 
                        'access excel teradata blazemeter loader.io jmeter bash shell'.
                       split(' '))

soft_skills = set(['problem solving', 'communication', 'creative', \
                   'problem solving', 'team player', 'adaptive', \
                   'ability to multitask', 'switch between different technologies' ,\
                   'work under pressure', 'citical thinking', 'take risk', \
                   'analytical behavior','decision making','problem solving',\
                   'adaptive behavior','adaptive','strategic',\
                   'create innovative solutions','solve complex problem',\
                   'quick learner','communication skills','effectively communicate',\
                   'leader','positive thinker','problem solving skills','leadership skills',\
                   'responsible and dependable','team player','work in team',\
                   'attentive','hard working','set realistic goal','manage time effectively'])

stop_words = set(stopwords.words('english'))

def resume_skills(input_skills):
    # Bigrams and trigrams identifier
    ''.join(input_skills)
    bigrams_present = []
    trigrams_present = []
    s1 = []
    s1.append(input_skills)
    for phrase in s1:
        bigrams_present.extend([" ".join(bi) for bi in ngrams(phrase.lower().split(), 2)])
        trigrams_present.extend([" ".join(tri) for tri in ngrams(phrase.lower().split(), 3)])

    all_grams = set(bigrams_present).union(set(trigrams_present))
    soft_skills_present = soft_skills.intersection(all_grams)
    # print(soft_skills_present)


    tokenized_data = word_tokenize(input_skills)

    tokenized_data = [word for word in tokenized_data if word not in stop_words]
    tagged = pos_tag(tokenized_data)
    nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == 'JJ' or pos == 'VBP')]
    nouns.extend(list(soft_skills_present))
    test_data_freq = FreqDist(nouns)
#     print(' '.join(test_data_freq.keys()))
    skills_present = test_data_freq.keys()

    return skills_present

def job_des_skills(job_skills):
    """
    :Author: Anmol Shrestha
    :desc: takes job description and matches with skills_collection
    :param: job_skills:
    :return: required_skills
    """
    # Bigrams and trigrams identifier
    bigrams_present = []
    trigrams_present = []
    s1 = []
    s1.append(job_skills)
    for phrase in s1:
        bigrams_present.extend([" ".join(bi) for bi in ngrams(phrase.lower().split(), 2)])
        trigrams_present.extend([" ".join(tri) for tri in ngrams(phrase.lower().split(), 3)])

    all_grams = set(bigrams_present).union(set(trigrams_present))
    soft_skills_present = soft_skills.intersection(all_grams)
    # print(soft_skills_present)

    tokenized_data = word_tokenize(job_skills)
    tokenized_data = [word for word in tokenized_data if word not in stop_words]
    tagged = pos_tag(tokenized_data)
    nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == 'JJ')]
    nouns.extend(list(soft_skills_present))
    required_skills = [items for items in nouns if items in skills_collection or items in soft_skills]
    return required_skills

