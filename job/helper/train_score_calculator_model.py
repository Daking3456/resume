# -*- coding: utf-8 -*-
"""
Created on Wednesday December 19 2018
@author: Rajendra Sapkota
"""
import pandas as pd
import pickle
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


def train_regression_model():
    try:
        #load excel data set for regression model
        score_calculation_df = pd.read_excel("/home/rajan/Desktop/project_wiork/"
                                             "project_wiork/static_local/resume_score_dataset.xlsx")

        # columns of score_calculation_df dataframe, i.e features to extract for resume score calculator
        # Index(['phd_present', 'grad_degree_present', 'under_grad_present',
        #        'grad_technical', 'under_grad_technical', 'basic_tech_skills_present',
        #        'advanced_tech_skills_present', 'intern_exp_months',
        #        'trainee_exp_months', 'junior_exp_months', 'developer_exp_months',
        #        'senior_exp_months', 'principal_engineer_exp_months',
        #        'teamlead_exp_months', 'project_manager_exp_months', 'score'],
        #       dtype='object')

        score_calculation_df = score_calculation_df.sample(frac=1)

        training_feature_matrix = score_calculation_df.drop(['score'], axis=1)
        # print(training_feature_matrix)
        training_label_score = score_calculation_df['score']
        X_train, X_test, y_train, y_test = train_test_split(training_feature_matrix,
                                                            training_label_score, random_state=0)
        # resume_score_calculator = SVR(kernel='poly', C=1e3, degree=2)
        # resume_score_calculator = resume_score_calculator.fit(training_feature_matrix,
        #                                                       training_label_score)
        knnreg = KNeighborsRegressor(n_neighbors=4).fit(X_train, y_train)

        # save resume score calculator regression model to calculater score for resumes
        with open("/home/rajan/Desktop/project_wiork/project_wiork/static_local/"
                  "resume_score_calculator.pickle", "wb") as output_file:
            pickle.dump(knnreg, output_file)


    except:
        print('Error: training the resume score model failed...')

train_regression_model()