
# coding: utf-8
"""
Created on Monday December 10 2018
@author: Rajendra Sapkota
"""

import os
import re
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

personal_info = set("personal informaion information: informations: "
                    "introduction introduction:".split(' '))
objective = set("career objective objective: motivation motivation:".split(' '))
experiences = set("work job projects summary jobs practical responsibilities "
                  "responsibilities: employment professional career experience"
                  " experience: experiences experiences: profile profile:"
                  " profiles profiles:".split(' '))
skills = set("technical skills key core professional practical skill skill: "
             "skills skills: experience experience: experiences experiences: "
             "competencies competencies:".split(' '))
projects = set("training training: trainings trainings: college projects projects:"
               " training trainings: attended attended:".split(' '))
academics = set("education education: educational acedemic qualification "
                "qualification: qualifications qualifications:".split(' '))
rewards = set("certification certification: certifications certifications "
              "rewards rewards:License License honours awards "
              "Licenses Licenses:".split(' '))
languages = set("language language: languages languages:".split(' '))
references = set("reference reference: references: references:".split(' '))

# listing all possible title words in the same set:
possible_title_keywords = personal_info | objective | experiences | \
                          skills | projects | academics | rewards | \
                          languages | references


# function to extract possible heading titles, classical approach by comparing the keywords in the possible headings
# also to make a dataframe of words in the resume -> 'text' as a features for machine learning model
def heading_features_extractor(text):
    mycolumns = ['word', 'word.istitle()', 'word.islower()', 
             'word.isupper()', 'word.endswith(":")', 'len(word)<=3',
             'possible_title_keywords', 'title_label', 'sent_index'
            ]

    df = pd.DataFrame(columns=mycolumns)
    sent_lines = text.splitlines()
    possible_titles= []
    #get sentence and its sentence index in resume document.
    for index,sent in enumerate(sent_lines):
        #print(index, sent)
        sent = sent.split(" ")
        if len(sent) < 4:
            for word in sent:
                df = df.append({'word': word,
                              'word.istitle()': word.istitle(),
                              'word.islower()': word.islower(), 
                              'word.isupper()': word.isupper(), 
                              'word.endswith(":")': word.endswith(":"), 
                              'len(word)<=3':len(word) <= 3,
                              'possible_title_keywords': word.lower() in possible_title_keywords,
                              'title_label': word.lower() in possible_title_keywords, 
                              'sent_index': index}, ignore_index=True) 
    
    df.replace(False, 0,  inplace=True) 
    df.replace(True, 1, inplace=True)   
    
# # returns possible titles with their sentence index in resume, and dataframe of features    
#     return possible_titles, df
# return features data-frame only
    return df

# folder 'new_resume_dataset' contains many resumes in .txt format
# first we find complete path for each of the resume


filenames_resume = []
path_resume = os.path.abspath("/home/rajan/Desktop/project_wiork/new_resume_dataset")
resumefiles = os.listdir("/home/rajan/Desktop/project_wiork/new_resume_dataset")
for i in range(1, len(resumefiles)):
    filenames_resume.append(os.path.join(path_resume, resumefiles[i]))

print(filenames_resume)
    
# make a complete dataframe of features of headings for training of machine
# learning model, which can be used for extraction of resume headings later


def training_features():
    mycolumns = ['word', 'word.istitle()', 'word.islower()', 'word.isupper()',
                 'word.endswith(":")', 'len(word)<=3', 'possible_title_keywords',
                 'title_label', 'sent_index']

    training_features_set = pd.DataFrame(columns=mycolumns)
#     print(trainig_features_set)
    for file in filenames_resume:
        with open(file, "r") as file:
            text=file.read()
#         features_set of single resume    
        single_resume_features = heading_features_extractor(text)
        training_features_set = pd.concat([training_features_set,
                                           single_resume_features], ignore_index=True)
        
    training_set = np.array(training_features_set[['word.istitle()', 'word.islower()',
                                                   'word.isupper()', 'word.endswith(":")',
                                                   'len(word)<=3', 'possible_title_keywords']])
    labels_set = training_features_set['title_label'].astype(int)

    # returns training_features_set, training_label_set
    return training_set, labels_set   
            

features_and_labels = training_features()
training_features_set = features_and_labels[0]
training_labels_set = features_and_labels[1]    

X_train, X_test, y_train, y_test = train_test_split(training_features_set,
                                                    training_labels_set,
                                                    test_size=0.33, random_state=42)

# will be using GaussioanNB machine learning model
headings_finder_gaussian_model = GaussianNB()
headings_finder_gaussian_model.fit(X_train, y_train)

def save_pickle(possible_titles, model_headings_finder):
    # save the set of possible title words for production label use
    with open("/home/rajan/Desktop/project_wiork/project_wiork/static_local/"
              "possible_title_keywords.pickle", "wb") as output_file:
        pickle.dump(possible_titles, output_file)
        
    # save trained heading extraction model for production label use
    with open("/home/rajan/Desktop/project_wiork/project_wiork/static_local/"
              "headings_finder_gaussian_model.pickle", "wb") as output_file:
        pickle.dump(model_headings_finder, output_file)      


save_pickle(possible_title_keywords, headings_finder_gaussian_model)

