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
import re
import pickle
from .education_extractor import extract_education
from .slice_resume_text import *
from .experience_extractor import extract_total_experience

def resume_score(text):
    try:
        # features columns to extract for resume score calculation
        # Index(['phd_present', 'grad_degree_present', 'under_grad_present', 'grad_technical',
        #        'under_grad_technical', 'advanced_tech_skills_present', 'intern_exp_months',
        #        'junior_exp_months', 'developer_exp_months', 'senior_exp_months',
        #        'principal_engineer_exp_months', 'teamlead_exp_months', 'project_manager_exp_months']
        #        >>> not included--->'score' (this has to be predicted by regression model)],
        #       dtype='object')

        with open(os.path.join(settings.STATIC_ROOT, "resume_score_calculator.pickle"), "rb") as input_file:
            resume_score_model = pickle.load(input_file)

        technical_stream = set('computer engineering information technology it \
                               computer science csit software engineering'.split(' '))
        phd_degree = set('Doctor Philosophy PhD Ph.D. DPhil D.Phil)'.split(' '))
        undergrad_degrees = set('bs be bsc bachelors associate bachelor'.split(' '))
        grad_degrees = set('ms me master masters graduate masters msc'.split(' '))

        skills_collection = set('python c c++ java javascript js angular angular js node'
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

        # with open("/home/rajan/Desktop/project_wiork/new_resume_dataset/ashwin.txt", "r") as file:
        #     text = file.read()
        cleaned_resume = (re.sub(r'\W+', ' ', re.sub(r'\.', '', text.lower()))).split(' ')
        extracted_info = formated_parsed_information(text)
        # returns a dictionary with resume information extracted
        # extracted_info = {'profile': Profile,
        #                   'objectives': Objectives,
        #                   'experiences': Experiences,
        #                   'skills': Skills,
        #                   'projects': Projects,
        #                   'academics': Educations,
        #                   'rewards': Rewards,
        #                   'languages': Languages,
        #                   'references': References}

        # sliced list of degrees
        degrees_list = extracted_info['academics']

        # extracted as graduate and under graduate degree
        degrees = extract_education(degrees_list)

        # join degrees, remove special punctuations and split words to clearly identify phd
        edu_text = (re.sub(r'\W+', ' ', re.sub(r'\.', '', ' '.join(degrees_list).lower()))).split()
        # text = (re.sub(r'\W+', ' ', re.sub(r'\.', '', text.lower()))).split()

        # look for phd/ doctor/ philosophy dphil in education section
        phd_points = 5 if 'phd' in edu_text else 0

        sliced_experience = extracted_info['experiences']
        months_with_designation = extract_total_experience(sliced_experience)

        if len(degrees['grad_degree']) != 0:
            grad_degree_points = 5
            # check if the grad_degree present is technical, only considered the first degree name
            grad_technical_points = 5 if len(set(' '.join(list(degrees['grad_degree'].values())).split(' ')). \
                                             intersection(technical_stream)) != 0 else 0

        else:
            grad_degree_points = 0
            grad_technical_points = 0

        if len(degrees['undergrad_degree']) != 0:
            under_grad_points = 2
            # check if the undergrad_degree present is technical, only considered the first degree name
            under_grad_technical_points = 2 if len(set(' '.join(list(degrees['undergrad_degree'].values())).split(' ')). \
                                                   intersection(technical_stream)) != 0 else 0
        else:
            under_grad_points = 0
            under_grad_technical_points = 0
        # set(list(set(degrees['grad_degree'].values()))[0].split())
        # The code above gives the set of tokens in the frist degree name present in grad_degree
        # check if tokens intersect with technical_stream tokens to know if the degree is technical

        # can be compared with two skill pools having 'basic skills' and 'advance skills'
        # basic_tech_skills_present = 1 if len(set(cleaned_resume).
        #                                      intersection(skills_collection)) < 13 else 0
        advanced_tech_skills_points = 3 if len(set(cleaned_resume).
                                               intersection(skills_collection)) > 13 else 0

        intern_exp_months = 0
        junior_exp_months = 0
        developer_exp_months = 0
        midlevel_dev_exp_months = 0
        senior_exp_months = 0
        principal_engineer_exp_months = 0
        teamlead_exp_months = 0
        project_manager_exp_months = 0

        # months_with_designation = extract_total_experience(sliced_experience)
        for months, designation in months_with_designation:
            designation = set(designation.split(' '))
            if len(designation.intersection(set('intern internship trainee training'.split()))) >= 1:
                intern_exp_months += months

            elif len(designation.intersection(set('jr junior associate entry'.split()))) >= 1:
                junior_exp_months += months

            elif len(designation.intersection(set('principal consultant adviser specialist'.split()))) >= 1:
                principal_engineer_exp_months += months

            elif len(designation.intersection(set('project engineer manager lead'.split()))) >= 2:
                project_manager_exp_months += months

            elif len(designation.intersection(set('team lead'.split()))) >= 2:
                teamlead_exp_months += months

            elif len(designation.intersection(set('senior sr lead'.split()))) >= 1:
                senior_exp_months += months

            elif len(designation.intersection(set('mid developer'.split()))) == 2:
                midlevel_dev_exp_months += months

            elif designation.intersection(set('developer'.split())) is not None:
                developer_exp_months += months
            else:
                pass

        # intern_points
        if intern_exp_months != 0 & intern_exp_months < 5:
            intern_points = 3
        elif intern_exp_months > 5:
            intern_points = 5
        else:
            intern_points = 0

        # junior_dev_points
        if junior_exp_months == 0:
            junior_dev_points = 0
        elif junior_exp_months < 12:
            junior_dev_points = 5
        elif junior_exp_months > 12:
            junior_dev_points = 7
        else:
            junior_dev_points = junior_exp_months * 0.3

        # developer_points
        if developer_exp_months == 0:
            developer_points = 0
        elif developer_exp_months < 12:
            developer_points = 5
        elif junior_exp_months > 12:
            developer_points = 7
        else:
            developer_points = developer_exp_months * 0.3

        # mid_dev_points
        if midlevel_dev_exp_months == 0:
            mid_dev_points = 0
        elif midlevel_dev_exp_months < 12:
            mid_dev_points = 5
        elif midlevel_dev_exp_months > 12:
            mid_dev_points = 7
        else:
            mid_dev_points = midlevel_dev_exp_months * 0.3

        # sr_dev_points
        if senior_exp_months == 0:
            sr_dev_points = 0
        elif senior_exp_months < 12:
            sr_dev_points = 5
        elif senior_exp_months > 12:
            sr_dev_points = 7
        else:
            sr_dev_points = senior_exp_months * 0.2

        # principal_dev_points
        if principal_engineer_exp_months == 0:
            principal_engineer_points = 0
        elif principal_engineer_exp_months < 12:
            principal_engineer_points = 5
        elif principal_engineer_exp_months > 12:
            principal_engineer_points = 7
        else:
            principal_engineer_points = principal_engineer_exp_months * 0.25

        # team_lead_points
        if teamlead_exp_months == 0:
            team_lead_points = 0
        elif teamlead_exp_months < 12:
            team_lead_points = 5
        elif teamlead_exp_months > 12:
            team_lead_points = 7
        else:
            team_lead_points = teamlead_exp_months * 0.25

        # project_manager_points
        if project_manager_exp_months == 0:
            project_manager_points = 0
        elif project_manager_exp_months < 12:
            project_manager_points = 5
        elif project_manager_exp_months > 12:
            project_manager_points = 7
        else:
            project_manager_points = project_manager_exp_months * 0.25

        # phd_points = 0
        # grad_degree_points = 0
        # under_grad_points = 0
        # grad_technical_points = 0
        # under_grad_technical_points = 0
        # advanced_tech_skills_present = 0
        # intern_exp_months = 0
        # junior_exp_months = 0
        # developer_exp_months = 0
        # midlevel_dev_exp_months = 0
        # senior_exp_months = 0
        # principal_engineer_exp_months = 0
        # teamlead_exp_months = 0
        # project_manager_exp_months = 0

        score_features = [phd_points, grad_degree_points, under_grad_points, grad_technical_points,
                          under_grad_technical_points, advanced_tech_skills_points,
                          intern_points, junior_dev_points, developer_points,
                          mid_dev_points, sr_dev_points, principal_engineer_points,
                          team_lead_points, project_manager_points]

        print(score_features)
        print(int(resume_score_model.predict([score_features])))

        return int(resume_score_model.predict([score_features]))

    except:
        return 'Error: Resume score calculation error...'

