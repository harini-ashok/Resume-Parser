
import pandas as pd
import utils, os, operator
import re


segments = utils.get_category_list()

def string_match(text):
    category_list = list(segments.keys())
    category_flag = {}
    for i in category_list:
        category_flag[i] = 0
    segs = {}
    
    for i in range(len(category_list)):
        for cat_options in segments[category_list[i]]:
            match = text.find(cat_options)
            if match != -1 and text[match+len(cat_options) : match+len(cat_options)+10].find('\n') != -1:
                start = match 
#                 print(match)
#                 print("matched text: " + text[match: match+len(cat_options)])
                segs[category_list[i]] = match
    sorted_segs = dict(sorted(segs.items(), key=operator.itemgetter(1)))
    return sorted_segs

def seg(text):
    category_list = list(segments.keys())
    category_flag = {}
    for i in category_list:
        category_flag[i] = 0
    seg = ''
    
    segment_category = []
    segment_text = []
    c = 0 
    found_flag = 0
    
    for i in range(len(category_list)):
        for cat_options in segments[category_list[i]]:
            if re.search(r'\b'+cat_options+r'\b', text) and category_flag[category_list[i]] != 1:
                ind=[]
                end_options = []
                end_segment_options = []
                start_segment = category_list[i]
                start = text.index(cat_options)
#                 print('verificattion')
#                 print(start_segment)
#                 print(cat_options)
#                 print(start)
                
                next_to_start = start + len(cat_options) + 1
#                 print(next_to_start)
                #checking if the new line character is present to verify match is actually a title 
                if text[next_to_start:next_to_start+10].find('\n') != -1:
#                     print('here ')
                    for j in range(len(category_list)):
                        if start_segment != category_list[j]:
                            indin = []
                            end_options_for_category = []
                            for cat_options2 in segments[category_list[j]]:
                                start= text.index(cat_options)
                                sub = text[start:]
                                if re.search(r'\b'+cat_options2+r'\b', sub):
                                    e = text.index(cat_options2)
                                    next_to_end = e + len(cat_options2) + 1
                                    if e > start and text[next_to_end:next_to_end+5].find('\n') != -1:
                                        indin.append(e)
                                        end_options_for_category.append(cat_options2)
                                        end_segment_options.append(category_list[j])
#                                         print(style.BOLD + 'i\'m here nowwwwww'+style.END)
#                                         print(end_options_for_category)
#                                         print(end_segment_options)

                            if indin:
                                longest_match = max(end_options_for_category, key = len)
                                longest_index = indin[end_options_for_category.index(longest_match)]
                                ind.append(longest_index)
                                end_options.append(longest_match)
                                end_segment_options.append(category_list[j])

                    if ind:
#                         print("start segement: " + start_segment)
#                         print(style.BOLD + "start is: " + cat_options + style.END)
                        end=min(ind)
                        ending = end_options[ind.index(end)]
#                         print("end segment: " + end_segment_options[ind.index(end)])
#                         print("end is: " +ending)
#                         print("endings: " + str(end_options))
#                         print("indices: " + str(ind))
                        segtext=text[start:end]
                        segment_category.append(start_segment)
                        segment_text.append(segtext)
                        c+=1
                        category_flag[start_segment] = 1
                        found_flag = 1
                    
#                         print("\n")
#                         print("seg text: " + segtext)
#                         print("\n")
    if not seg and not found_flag :
        #print('regex didn\'t catch')
        segment_index_dict = string_match(text)
        seg, indices =  list(segment_index_dict.keys()), list(segment_index_dict.values())
        c = len(indices)
        for i in range(c):
            segment_category.append(seg[i])
            
            if i+1 < c:
                segment_text.append(text[indices[i]:indices[i+1]])
                
            elif i+1 >= c:
                amp = text.find('$$$')
                segment_text.append(text[indices[i]:amp])
               
    else:    
        headings = []
        heading_segment = []
        for i in range(len(category_list)):
            for cat_options in segments[category_list[i]]:
                if re.search(r'\b'+cat_options+r'\b', text):
                    start= text.index(cat_options)
                    headings.append(start)
                    heading_segment.append(category_list[i])
        last_headings = max(headings)
        last_heading_segment = heading_segment[headings.index(last_headings)]
        ending = text.index('$$$')

        segment_category.append(last_heading_segment)
        segment_text.append(text[last_headings:ending])
        c+=1


    return [segment_category, segment_text, c]