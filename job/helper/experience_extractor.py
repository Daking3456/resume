# -*- coding: utf-8 -*-
"""
Created on Monday December 02 2018
@author: Rajendra Sapkota
"""
import re
from dateutil.parser import parse
from datetime import date

"""
  @desc: takes sliced_text dictionary, identify dates in the text and calculate the difference
  """
# total_experience_in_months [(months, designation), (m,d) , ..]


designations = set('intern trainne internship trainee trainning junior associate software'
                   ' developer engineer mid level senior sr. principal team lead'
                   ' lead cloud frontend backend django python java javascript .net'
                   ' c# c visual basic scala julia hadoop big data data scientist sql '
                   ' database administrator network analyst ai machine learning data '
                   'engineer aws azure web data analyst scientist project manager'
                   ' technical officer adviser consultant'.split(' '))

date_reg = r'(?:[\s]?\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|' \
           r'Oct|Nov|Dec)?[a-z\s,./]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)?(?:\d{2,4})|' \
           r'(?:[Pp]resent|[Cc]urrent|[Tt]oday|[Tt]ill\s[Nn]ow)'


def extract_total_experience(experience):


    try:
        total_experience_in_months = []
        for index, items in enumerate(experience):
            date_entity = re.findall(date_reg, items.lower())
            items = re.split("[, \-!?:\/]+", items.lower())
            designation = designations.intersection(set(items))
            for item in date_entity:
                date_entity = [date.today().strftime('%Y, %m')
                               if item == ('present' or 'now' or 'till' or 'current'
                                           or 'today') else parse(item).strftime('%Y, %m') for item in date_entity]
            if len(date_entity) == 2:
                experience = (parse(date_entity[1]) - parse(date_entity[0])).days // 30
                total_experience_in_months.append((experience, ' '.join(designation)))

        # # use total_experience (which is in months to calculate resume scores)
        # total_experience = sum(x[0] for x in total_experience_in_months)
        # print('total experience in months:', total_experience)
        #
        # #just for readability
        # # for clear readability for experience, use year and months format
        # if total_experience>12:
        #     exp_yr = total_experience//12
        #     exp_mont = total_experience%12
        #     readable_experience = str(exp_yr) + ' years ' + str(exp_mont) + ' months'
        #     print('experience:', readable_experience)
        #     # print('total experience:', exp_yr, 'year', exp_mont, 'months')
        # print(total_experience_in_months,'\n')
        return total_experience_in_months

    except KeyError:
        print('No Experience Found...')
        total_experience = 0
        return total_experience
