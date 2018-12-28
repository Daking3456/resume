# -*- coding: utf-8 -*-
"""
Created on December 10 2018
@author: Rajendra Sapkota
"""
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume.settings')

import django
# Import settings
django.setup()
from django.conf import settings

import pickle


DICT_LABEL = {0: 'ANALYST', 1: 'SQL', 2: 'JAVA', 3: 'PYTHON'}

personal_info = set("personal information information: informations: introduction"
					" introduction:".split(' '))
objective = set("career objective objective: motivation motivation:".split(' '))
experiences = set("work job projects summary summary: jobs responsibilities "
				  "responsibilities: employment professional career experience"
				  " experience: experiences experiences: profile profile: "
				  "profiles profiles:".split(' '))
skills = set("technical key core professional skill skill: skills skills: "
			 "competencies competencies:".split(' '))
projects = set("training training: trainings trainings: college projects projects:"
			   " training trainings: attended attended:".split(' '))
academics = set("education education: educational acedemic qualification "
				"qualification: qualifications qualifications:".split(' '))
rewards = set("certification certification: certifications certifications "
			  "rewards rewards:License License honours awards Licenses"
			  " Licenses:".split(' '))
languages = set("language language: languages languages:".split(' '))
references = set("reference reference: references: references:".split(' '))

# listing all possible title words in the same set:
possible_title_keywords = personal_info | objective | experiences | skills | \
						  projects | academics | rewards | languages | references

# load trained model for heading prediction
with open(os.path.join(settings.STATIC_ROOT, "headings_finder_gaussian_model.pickle"), "rb")as input_file:
    headings_finder_gaussian_model = pickle.load(input_file)

def unique_index_headings(input_text):
    # Split text for heading extraction
    resume_text = input_text.splitlines()

    sent_lines = resume_text
    list_of_headings_with_repeated_index = []

    # get sentence and its sentence index in resume document.
    for index, sent in enumerate(sent_lines):
        # print(index, sent)

        sent = sent.split(" ")
        if len(sent) < 4:
            for word in sent:
                features = [word.istitle(), word.islower(), word.isupper(), word.endswith(":"),
                            len(word) <= 3, word.lower() in possible_title_keywords]

                # features until here are list of booleans which need to be converted to int values
                # features converted to int and made in a format of training input
                features = [[int(elem) for elem in features]]
                #                 predict if word with above features is heading
                if headings_finder_gaussian_model.predict(features) == 1:
                    list_of_headings_with_repeated_index.append({index: word})

    # from repeating index heading, join heading words with same sentence index
    uniquekeys = set()
    unique_indx_headings = dict()
    # titles_with_repeated_indices = predict_repeating_index_headings(input_text)

    for t in list_of_headings_with_repeated_index:
        for key, value in t.items():
            if key not in uniquekeys:
                unique_indx_headings[key] = value
                uniquekeys.add(key)
            else:
                unique_indx_headings[key] = unique_indx_headings[key] + ' ' + value


    return unique_indx_headings
