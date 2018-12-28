# -*- coding: utf-8 -*-
"""
Created on 10 Dec 2018
@author: Rajendra Sapkota

"""
import os
# Configure settings for project
# Need to run this before calling models from application!
import django
# Import settings
from django.conf import settings
from sklearn.externals import joblib
import dill


django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume.settings')

DICT_LABEL = {0: 'ANALYST', 1: 'SQL', 2: 'JAVA', 3: 'PYTHON'}


def resume_verifier(text_file):

    with open(os.path.join(settings.STATIC_ROOT,'doc_classifier_nb_model.sav'), 'rb') as input_file:
        resume_verifier_modl = joblib.load(input_file)

    # document Prediction [ 0 - Not Resume, 1 - Resume]
    doc_prediction = resume_verifier_modl.predict(text_file.split(' '))
    # print("Prediction:", doc_prediction[0])

    if doc_prediction[0] == 1:
        return True
    else:
        return False


def resume_domain_identifier(input_text):
    with open(os.path.join(settings.STATIC_ROOT, 'savedresumemodel.dill'), 'rb') as input_file:
        mnb = dill.load(input_file)

    with open(os.path.join(settings.STATIC_ROOT, 'savedvectorizer.dill'), 'rb') as vectorizer:
        vect = dill.load(vectorizer)

    # Vectorize
    X_test_dtm = vect.transform([input_text])

    # Predict
    y_pred = mnb.predict(X_test_dtm)

    # Prediction
    resume_domain = DICT_LABEL[y_pred[0]]

    return resume_domain
