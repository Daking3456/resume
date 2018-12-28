# -*- coding: utf-8 -*-
"""
Created on Monday December 13 Dec 2018
@author: Rajendra Sapkota
"""
import re


def extract_education(education):
    technical_stream = set('computer engineering information technology it \
                           computer science csit software engineering'.split(' '))
    undergrad_degrees = set('bs be bsc bachelors associate bachelor'.split(' '))
    grad_degrees = set('ms me master masters graduate masters msc'.split(' '))
    try:
        degrees = {'grad_degree': '', 'undergrad_degree': ''}
        for items in education:
            items = re.sub(r'[^a-zA-Z0-9]', ' ', items.lower())
            for item in items.split(' '):
                if item in undergrad_degrees:
                    degrees['undergrad_degree'] = {item: ' '.join(technical_stream.intersection(set(items.split(' '))))}
                elif item in grad_degrees:
                    degrees['grad_degree'] = {item: ' '.join(technical_stream.intersection(set(items.split(' '))))}
                else:
                    pass
        return degrees

    except:
        print('Error: Educational degrees extraction failed...')