#!/usr/bin/env python
# coding: utf-8

# In[1]:


class style:
    BOLD = '\033[1m'
    END = '\033[0m' 


# In[2]:


import re
import io
import os
import pandas as pd
import nltk
import sys
import json
import spacy
import en_core_web_sm
from dateutil import relativedelta
from nltk.corpus import stopwords
from spacy.matcher import Matcher
from datetime import datetime
from io import StringIO
import datefinder
from datetime import date
from segmentation import *  
import csv
from fuzzywuzzy import fuzz, process
import unicodedata
from pdf2image import convert_from_path
from os import path
import subprocess

from db import *


# In[3]:



MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)
                   |(aug)|(sep)|(oct)|(nov)|(dec)'''
MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|
                   (august)|(september)|(october)|(november)|(december)'''
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'

STOPWORDS = set(stopwords.words('english'))


# In[4]:


nlp = en_core_web_sm.load()


# In[24]:


def pdf_img(file):
    c = 0
    
    
    pages = convert_from_path('resume/'+file+'.pdf',500, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
   
    for page in pages:
        c+=1
        if not os.path.isdir('imgs/'+file):
            os.mkdir('imgs/' + file)
        page.save(os.path.join('imgs', file, str(c)+'.jpg'), 'JPEG')
        
def extract_using_tesseract(file):

    #convert the PDF to image
    if file.endswith('.pdf'):
        filename = os.path.splitext(file)[0]
        pdf_img(filename)
    #convert the images to text
    for img in os.listdir(os.path.join('imgs', str(filename))):
        if(img.endswith('.jpg')):        
            os.system('tesseract --dpi 500 ' + os.path.join('imgs', str(filename), img) + ' ' + os.path.join('imgs', str(filename), os.path.splitext(img)[0]))
    #append text to python variable       
    text = ''
    img_text_files = os.listdir(os.path.join('imgs', filename))
    for text_file in sorted(img_text_files):
        if text_file.endswith('.txt'):
            text_file_obj = open(os.path.join('imgs', filename, text_file), encoding="utf8")
            text = text +' '+ text_file_obj.read()
    return text


# In[6]:


def extract_mobile_number(text, custom_regex=None):
    number = '0000'
    if not custom_regex:
        mob_num_regex = r'''(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'''
        phone = re.findall(re.compile(mob_num_regex), text)
    else:
        phone = re.findall(re.compile(custom_regex), text)
    if phone:
        number = ''.join(phone[0])
        #print("Phone Number:",number)
    return number

def extract_email(text):
       
        text = str(unicodedata.normalize('NFKD', text).encode('utf-8'))
        index = text.find("@")
        if index > 0:
            email = re.search(r'[\w\.-]+@[\w\.-]+', text)
            if email:
                return email.group(0)
        return 'no val'
    
def remove_spl_characters(text):
    text_alpha = ''
    for i in text:
        if not i.isalpha():
            if i == '+':
                text_alpha+=i
            else:
                text_alpha+=' '

        else:
            text_alpha+=i
    return text_alpha

def extract_skills(text):
    text = remove_spl_characters(text)
    doc=nlp(text)
    tokens = [token.text for token in doc if not token.is_stop]
    data = pd.read_csv("csvfiles/skills.csv")
    skills = list(data.columns.values)
    skillset = []
    
    for token in tokens:
        if token.lower().strip() in skills:
            skillset.append(token.lower())
            
    for token in doc.noun_chunks:
        token= token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    
    skillset = list(dict.fromkeys(skillset))
    if skillset == []:
        skillset = ['no val']
    #print("Skillset:",[i.upper() for i in set([i.lower() for i in skillset])]) 
    return skillset

def list_to_str(listt):
    if listt == []:

        strr = 'no val'
    else:
        strr = ""        
        for x in listt:
            if len(listt)>1:
                strr += str(x)+" "
            else:
                strr = str(x)
    return strr


def lists_to_str(lists):
    return list_to_str(lists[0]), list_to_str(lists[1])

def find_degree_dates(text):
    while(True):
        index = text.find("GPA")
        if index >= 0:
            temp = text[index:index+10]
            text = text.replace(temp,"")
        else:
            break
        
        index = text.find("CGPA")   
        if index >= 0:
            temp = text[index:index+10]
            text = text.replace(temp,"")
        else:
            break

    matches = list(datefinder.find_dates(text))
    edu_date = ""
    if not matches == []:
        currentYear = datetime.now().year
        for temp_date in matches:
            if not temp_date.year > currentYear + 4:
                edu_date += str(temp_date.month) + "/" + str(temp_date.year) + " - "
        year = edu_date[:(len(edu_date) - 2)]
        return year
    return 'no dates'
        

def extract_education(text):
    
    a=[]
    text = text.replace('\n', ' ')
    text = text.replace(' ', '')
    text = text.lower()
    
    def lower_list_elements(df_list):
        df_l = []
        for element in df_list:
            df_l.append("".join(element).replace(" ", "").lower())
        return df_l
   
    degree_df = pd.read_csv('csvfiles/qualification_degree_list.csv')
    degree_list_abbrev = lower_list_elements([ el.lower() for el in sorted(list(degree_df['Abbrev']))])
    degree_list_full = lower_list_elements([ el.lower() for el in sorted(list(degree_df['Full']))])
    
    major_df = pd.read_csv('csvfiles/educational_major.csv')
    major_list = lower_list_elements([ el.lower() for el in sorted(list(major_df['Major']))])
    
    pos1, names1 = search_list_element_in_text(text, degree_list_abbrev)
    pos2, names2 = search_list_element_in_text(text, degree_list_full)
    pos3, names3 = search_list_element_in_text(text, major_list)
    if not names1  == []:
        names1 = remove_repeated_names_from_list(names1)
        a.extend(names1)
    if not names2 == []:
        names2 = remove_repeated_names_from_list(names2)
        a.extend(names2)
    if not names3 == []:
        names3 = remove_repeated_names_from_list(names3)
        a.extend(names3)
        
#     doc= nlp(text)
#     for tokens in doc:
#         if tokens.text not in STOPWORDS:
#             if tokens.text.lower() in degree_list_abbrev:
#                 a.append(tokens.text.lower())
#             if tokens.text.lower() in degree_list_full:
#                  a.append(tokens.text.lower())
#             if tokens.text.lower() in major_list:
#                 a.append(tokens.text.lower())
            
#     if not a:
#         a = extract_degree(text)
    
    d = re.findall('(\d{4}-\d{4})', text)
    if not d:
        d = find_degree_dates(text)
    
    return [a, d]


def extract_degree(text):
    
    def get_education_word_list(dir_path):
        file_name = "education_segment.csv"
        reader = read_csv(dir_path+file_name)
        education_word_list = []
        for row in reader:
            education_word_list.append(row[0])
        return education_word_list 
    
    def get_keywords(file_name):
        dir_path = ''
        reader = read_csv(dir_path + file_name)
        keywords = []
        for row in reader:
            keywords.append(row[0])
        return keywords

    def read_csv(input_file):
        file = open(input_file, 'r')
        reader = csv.reader(file)
        return reader

    def get_major_word_list(dir_path):
        file_name = "csvfiles/educational_major.csv"
        reader = read_csv(dir_path + file_name)
        major_list = []
        for row in reader:
            major_list.append(row[0])
        return major_list

    def search_major(text, degree, edu_obj): 
        maxim = -1
        # Search for major
        for major in major_word_list:
            if major.lower() in (text.lower()) and len(major) > max:
                major = str(major).title()
                degree = degree.title()
                maxim = len(str(major))
        return degree_flag

    def get_qualification_word_list(dir_path):
        file_name = "csvfiles/qualification_degree_list.csv"
        reader = read_csv(dir_path+file_name)
        qualification_word_dict = {}
        qualification_word_dict_no_spaces = {}
        abbr_list = []
        degree_list = []
        for row in reader:
            abbr_list.append(row[0])
            abbr_list.append(row[0].replace(" ", ''))
            degree_list.append(row[1])
            degree_list.append(row[0].replace(" ", ''))
            qualification_word_dict[row[0]] = row[1]
            qualification_word_dict_no_spaces[row[0].replace(" ", '')] = row[1].replace(" ", '')
        return qualification_word_dict, qualification_word_dict_no_spaces, abbr_list, degree_list

    qualification_word_dict, qualification_word_dict_no_spaces, abbr_list, degree_list = get_qualification_word_list('')
    major_word_list = get_major_word_list('')
    education_degree_category = get_keywords("csvfiles/degree_category.csv")
    
    max_len = 0
    degree = 'no val'
    major = 'no val'
    for abbr, val in qualification_word_dict.items():
        score1 = fuzz.ratio(str(abbr).lower(), text.lower())
        score2 = fuzz.ratio(str(val).lower(), text.lower())
        if score1 > 90 or score2 > 90 and max_len < len(val):
            max_len = len(val)
            degree = val

        if str(abbr).lower() in text.lower():
            major = val
            

    for word in major_word_list:
        score3 = fuzz.partial_ratio(str(word).lower(), text.lower())
        if score3 > 90 and max_len < len(word):
            max_len = len(word)
            major = word
            
    for abbr, val in qualification_word_dict_no_spaces.items():
        score4 = fuzz.partial_ratio(str(abbr).lower(), text.lower())
        score5 = fuzz.partial_ratio(str(val).lower(), text.lower())
        if score4 > 90 or score5 > 90 and max_len < len(val):
            max_len = len(val)
            degree = val
    return degree, major

def extract_region(text):
    doc=nlp(text)
    tokens = [token.text for token in doc if not token.is_stop]
    region_df = pd.read_csv("csvfiles/region.csv")
    cities, states = list(region_df.loc[:, 'city']), list(region_df.loc[:, 'state'])
    cities, states = [x.lower() for x in cities], [x.lower() for x in states]
    city, state = 'no val', 'no val'

    for token in tokens:
        #for cities
        if token.lower().strip() in cities: 
            city = token.lower()
            i = cities.index(city)
            state = states[i]
        
    return city, state


def preprocess_collegename_files(file):
    df = pd.read_csv(file, encoding = "ISO-8859-1")
    df.drop(df.iloc[:,1:], inplace = True, axis = 1)
    if(file.find('college')!=-1):
        df.rename(columns={'Name of the College':'collegename'},inplace=True)
        df['collegename'] = df.collegename.str.split(",",expand=True) 
    else:
        df.rename(columns={'Name of the University':'univname'},inplace=True)
        df['univname'] = df.univname.str.split(",",expand=True)
        
    df_list = df.values
    df_l = []
    for element in df_list:
        df_l.append("".join(element).replace(" ", "").lower())
    return df_l


def search_list_element_in_text(text, l):
    pos = []
    names = []
    for val in l:
        x = text.find(val)
        if(x!=-1):
            pos.append(x)
            names.append(val)
    return pos, names


def extract_college_or_uni(text, college_l, uni_l):
    colleges = 'no val'
    pos, names = search_list_element_in_text(text, college_l)
    if(len(pos) == 0):
        pos, names = search_list_element_in_text(text, uni_l)
    pos = list(dict.fromkeys(pos))
    names = list(dict.fromkeys(names))
    colleges = remove_repeated_names_from_list(names)
    return colleges


def remove_repeated_names_from_list(names):
    multiple = []
    for i in range(len(names)):
        name = names[i]
        for j in range(len(names)):
            if names[j].find(name)!= -1:
                name = names[j]
        multiple.append(name)
    multiple = list(dict.fromkeys(multiple))
    return multiple


def extract_college(text):
    college_l = list(dict.fromkeys(preprocess_collegename_files('csvfiles/college.csv')))
    uni_l = list(dict.fromkeys(preprocess_collegename_files('csvfiles/unis.csv')))
    text = text.replace(" ","")
    text = text.lower()
    name = extract_college_or_uni(text, college_l, uni_l)
    if name == []:
        name = ['no val']
    return name


# In[7]:


def add_spaces_to_dates(date):
    match = re.match(r"([a-z]+)([0-9]+)", date, re.I)
    
    if match:
        items = match.groups()
        date = ''.join(items[0] + ' ' + items[1])
        return date
    else:
        return None

#no of months for each set of dates
def get_number_of_months_from_dates(date1, date2):
    date1 = add_spaces_to_dates(date1)
    date2 = add_spaces_to_dates(date2)

    if date1 and date2:
        if date2.lower() == 'present':
            date2 = datetime.now().strftime('%b %Y')
            
        try:
            if len(date1.split()[0]) > 3:
                date1 = date1.split()
                date1 = date1[0][:3] + ' ' + date1[1]

            if len(date2.split()[0]) > 3:
                date2 = date2.split()
                date2 = date2[0][:3] + ' ' + date2[1]
        except IndexError: 
            return 0
        try:
            date1 = datetime.strptime(str(date1), '%b %Y')
            date2 = datetime.strptime(str(date2), '%b %Y')
            months_of_experience = relativedelta.relativedelta(date2, date1)
            months_of_experience = (months_of_experience.years
                                    * 12 + months_of_experience.months)
        except ValueError:
            return 0
        return months_of_experience
    else:
        return 0

#extract all dates from resume
def find_dates(text):
    date_list = re.findall('(\w+.\d+)\s*(\D|to)\s*(\w+.\d+|present|Present)', text)
    str_list = []
    for tupl in date_list:
        name = tupl[0] + " "+ tupl[2]
        str_list.append("".join(name))
    return str_list

def get_work_exp_mmyyyy(text):
    while(True):
        index = text.find("GPA")
        if index >= 0:
            temp = text[index:index+10]
            text = text.replace(temp,"")
        else:
            break
        
        index = text.find("CGPA")   
        if index >= 0:
            temp = text[index:index+10]
            text = text.replace(temp,"")
        else:
            break

    matches = list(datefinder.find_dates(text))
    edu_date = ""
    
    def elapsed_months(date1, date2=datetime.today()):
        return abs(date1.year * 12 + date1.month) - (date2.year * 12 + date2.month)
    
    if not matches == []:
        currentYear = datetime.now().year
        for temp_date in matches:
            
            if not temp_date.year > currentYear + 4:
                edu_date += str(temp_date.month) + "/" + str(temp_date.year) + " - "
        year = edu_date[:(len(edu_date) - 2)]
        if 'present' in text.lower():
            year = year + date.today().strftime("%m/%y")
            matches.append(datetime.now())
        return elapsed_months(max(matches), min(matches))
    else: return 0

#from extracted dates, calculate sum of each work experience
def get_total_work_experience(text):
    resume_dates = find_dates(text)
    exp_ = []
    total_exp = 0
    for date in resume_dates:
        experience = re.search(MONTH, date.lower())
        if experience:
            for dates in date.split():
                
                is_date = re.search(MONTH, dates.lower())
                if 'present' in dates.lower():
                    is_date = 0
                
                if is_date:
                    exp_.append(date.split())
                
    total_exp = sum(
        [get_number_of_months_from_dates(i[0], i[1]) for i in exp_]
    )
    if total_exp == 0:
        total_exp = get_work_exp_mmyyyy(text)
    if total_exp < 12:
        total_experience = str(total_exp) + " months"
    else:
        year = str(int(total_exp/12)) + ' years'
        mon = str(int((total_exp/12 % 1)*12)) + ' months'
        total_experience = year + ' ' + mon
    return total_experience


# In[8]:


def print_rec(dic):
    keys = dic.keys()
    for key in keys:
        print(style.BOLD + key + ': '+ style.END)
        print(dic[key])
        print('\n')


# In[9]:


def parse(text):
    result = {
                'email': 'No val',
                'mobile': '0000',
                'skills': 'No val',
                'education': 'No val',
                'years': 'No val',
                'city': 'No val',
                'state': 'No val',
                'work_experience': 'No val',
                'college': 'No val'
            }
    email=str(extract_email(text)).lower()
    mobile_number=str(extract_mobile_number(text))
    skills=extract_skills(text)
    a, e = extract_education(text)
    if a and e:
        education, graduation_years=lists_to_str([a, e])
    else:
        education, graduation_years= 'no val', 'no val'
    city, state= extract_region(text)
    exp = get_total_work_experience(text)
    college_name = extract_college(text)

    result = {
                'email': email,
                'mobile': mobile_number,
                'skills': skills,
                'education': education,
                'years': graduation_years,
                'city': city,
                'state': state,
                'work_experience': exp,
                'college': college_name
            }
    return result


# In[10]:


def parser(text):
    record = {
                'email': 'no val',
                'mobile': '0000',
                'skills': 'No val',
                'education': 'No val',
                'years': 'No val',
                'city': 'No val',
                'state': 'No val',
                'work_experience': 'No val',
                'college': 'No val'
             }
    text2 = text.replace('\n', '\n ')
    text = text.replace(' ', '')
    
    text = text + "$$$"
    text2 = text2 + "$$$"
    segment_category, segment_text, segment_count = seg(text)
    segment_category2, segment_text2, segment_count2 = seg(text2)
    
    if segment_count <=1 or segment_count2 <=1:
        record = parse(text)
    else: 
        if 'education_segment' in segment_category2:
            record['education'], record['years'] = lists_to_str(extract_education(segment_text2[segment_category2.index('education_segment')]))
            record['college'] = extract_college(segment_text2[segment_category2.index('education_segment')])
        elif 'education_segment' in segment_category:
            record['education'], record['years'] = lists_to_str(extract_education(segment_text[segment_category.index('education_segment')]))
            record['college'] = extract_college(segment_text[segment_category.index('education_segment')])
        else:
            record['college'] = extract_college(text2)
            record['education'], record['years'] = lists_to_str(extract_education(text2))
            
        if 'personaldetails_segment' in segment_category:
        
            record['mobile'] = extract_mobile_number(segment_text2[segment_category2.index('personaldetails_segment')])
            record['email'] = extract_email(segment_text2[segment_category2.index('personaldetails_segment')])
            if record['mobile'] == None:
                record['mobile'] = extract_mobile_number(text2)
            if record['email'] == None: 
                record['email'] = extract_email(text2)
            record['city'], record['state'] = extract_region(segment_text2[segment_category2.index('personaldetails_segment')])
            if record['city'] == None or record['state'] == None:
                record['city'], record['state'] = extract_region(text2)         
        else:      
            
            record['mobile'] = extract_mobile_number(text2)
            record['email'] = extract_email(text2)
            record['city'], record['state'] = extract_region(text2)  
            
        
        if 'skill_segment' in segment_category:
            record['skills'] = extract_skills(segment_text2[segment_category2.index('skill_segment')])
        else:
            record['skills'] = extract_skills(text2)
        
        if 'work_experience_segment' in segment_category:
            record['work_experience'] = get_total_work_experience(segment_text2[segment_category2.index('work_experience_segment')])
        else:
            record['work_experience'] = get_total_work_experience(text)
       
    return record


# In[11]:


def print_segments(segment_category, segment_text, segment_count):
    for i in range(segment_count):
        print(style.BOLD + 'category: ' + segment_category[i] + style.END)
        print('segment: ' + segment_text[i])
        print('\n') 


# In[12]:


def segprnt(text):
    text = text + "$$$"
    segment_category, segment_text, segment_count = seg(text)
    print_segments(segment_category, segment_text, segment_count)
