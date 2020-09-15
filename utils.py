class style:
   BOLD = '\033[1m'
   END = '\033[0m'
    
def print_rec(dic):
    keys = dic.keys()
    for key in keys:
        print(style.BOLD + key + ': '+ style.END)
        print(dic[key])
        print('\n')
        
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

def list_to_str(listt):
    strr = ""        
    for x in listt:
        if len(listt)>1:
            strr += str(x)+" "
        else:
            strr = str(x)
    return strr

def lists_to_str(lists):
    return list_to_str(lists[0]), list_to_str(lists[1])

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


def search_college_from_text(text, l):
    pos = []
    names = []
    for val in l:
        x = text.find(val)
        if(x!=-1):
            pos.append(x)
            names.append(val)
    return pos, names


def extract_college_or_uni(text, college_l, uni_l):
    pos, names = search_college_from_text(text, college_l)
    if(len(pos) == 0):
        pos, names = search_college_from_text(text, uni_l)
    pos = list(dict.fromkeys(pos))
    names = list(dict.fromkeys(names))
    colleges = remove_repeated_collegenames(names)
    return colleges


def remove_repeated_collegenames(names):
    multiple = []
    for i in range(len(names)):
        name = names[i]
        for j in range(len(names)):
            if names[j].find(name)!= -1:
                name = names[j]
        multiple.append(name)
    multiple = list(dict.fromkeys(multiple))
    return multiple

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

import os

def csv_to_list(file):
    import csv
    data = []
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(''.join(row))

    return data

def get_category_list():
    path = 'list/'
    filenames = os.listdir(path)
    segment = {}
    for file in filenames:
        if '.csv' in file:
            segment[str(os.path.splitext(file)[0])] = csv_to_list(os.path.join(path, file))
    segments = {}

    for key in segment.keys():
        l = []
        for i in range(len(segment[key])):
            l.append((segment[key][i]).upper())
            l.append((segment[key][i]).title())
            l.append((segment[key][i]).upper().replace(' ', ''))
            l.append((segment[key][i]).title().replace(' ', ''))
        segments[key] = l
    return segments


def print_segments(segment_category, segment_text, segment_count):
    for i in range(segment_count):
        print(style.BOLD + 'category: ' + segment_category[i] + style.END)
        print('segment: ' + segment_text[i])
        print('\n') 