import os
import json
import pymysql

def get_id(table, column, value):
    conn = pymysql.connect(
    host='localhost',
    port=int(3306),
    user="root",
    passwd="root",
    db="mydb",
    charset='utf8mb4')

    cur=conn.cursor()
    
    id_query = 'SELECT id from ' + table +  ' where ' + column +' = ' +value+';'
    cur.execute(id_query)
    ID = cur.fetchone()[0]
    
    conn.close()
    return ID

def insert_to_tables(result):
    
    conn = pymysql.connect(
    host='localhost',
    port=int(3306),
    user="root",
    passwd="root",
    db="mydb",
    charset='utf8mb4')

    cur=conn.cursor()
    
    
    def insert(table, cols, values):
        sql = 'INSERT INTO ' + table + '('+ ",".join(cols) +')' +  ' VALUES ' + '(' +",".join(values)+ ');'
        cur.execute(sql)
        conn.commit()
    

    def retrieve_id(table, column, value):
        id_query = 'SELECT id from ' + table +  ' where ' + column + ' = ' +value+';'
        cur.execute(id_query)
        ID = cur.fetchone()[0]
        return ID
    
    #Insert names
    namequery = 'insert into name_db (candidate_name) VALUES (%s)'
    insert('name_db', ['candidate_name'], [str( "'"+result["name"]+"'")])
    conn.commit()
    
    #retrieve Candidate ID
    candidate_id = retrieve_id('name_db', 'candidate_name', "'"+result["name"]+"'")
    
    #insert Email
    insert('candidate_email_db', ['candidate_id', 'email_id'], [str(candidate_id), str( "'"+result["email"]+"'")])
    
    #Insert Mobile Number
    insert('candidate_mobilenumber_db', ['candidate_id', 'mobilenumber'], [str(candidate_id), str(result["mobile"])])
    
    #Insert Work Experience
    insert('candidate_workexperience_db', ['candidate_id', 'workexperience'], [str(candidate_id), str( "'"+result["work_experience"]+"'")])
    
    #Insert Educational Experience
    insert('candidate_educationdetails_db', ['candidate_id', 'educational_qualification', 'graduation_years'], [str(candidate_id), str( "'"+result["education"]+"'"), str( "'"+result["years"]+"'")])
    
    #Insert College_id
   
    c = result['college']
    for i in range(len(c)):     
        college_id = retrieve_id('colleges_db', 'college_name', "'"+c[i]+"'")
        insert('candidate_college_db', ['candidate_id', 'college_id'], [str(candidate_id), str(college_id)])
    
    #city_id insert
    city_id = retrieve_id('cities_db', 'city_name', "'"+result["city"]+"'")
    insert('candidate_city_db', ['candidate_id', 'city_id'], [str(candidate_id), str(city_id)])
        
    #state_id insert
    state_id = retrieve_id('states_db', 'state_name', "'"+result["state"]+"'")
    insert('candidate_state_db', ['candidate_id', 'state_id'], [str(candidate_id), str(state_id)])
           
    #skills_id insert
    #s=extract_skills(t) 
    s = result["skills"]
    for i in range(len(s)):
        skill_id = retrieve_id('skills_db', 'skill_name', "'"+s[i]+"'")
        insert('candidate_skills_db', ['candidate_id', 'skills_id'], [str(candidate_id), str(skill_id)])
        
    conn.commit()
    conn.close()
    
def fetch_ids():
    cur.execute('SELECT id from name_db;')
    result = cur.fetchall()
    IDs = []
    for i in result:
        for j in i:
            IDs.append(j)
    return IDs

def record_to_json(record, filename = 'public/jobs.json'):
    json_filename = filename
    def write_json(json_file, filename=json_filename): 
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 
    
    
    with open(json_filename) as json_file: 
        data = json.load(json_file)
        data.append(record)
    write_json(data) 

def retrieve(ID):
    conn = pymysql.connect(
    host='localhost',
    port=int(3306),
    user="root",
    passwd="root",
    db="mydb",
    charset='utf8mb4')

    cur=conn.cursor()
     
    def select(column, table, ID, val):
    
        sql = 'SELECT ' +column+' FROM ' +table+' WHERE '+ID +' = ' + str(val) + ';'
        cur.execute(sql)
        col_val = cur.fetchone()[0]
        return col_val

    name = select('candidate_name', 'name_db', 'id', ID) 
    email_id = select('email_id', 'candidate_email_db', 'candidate_id', ID)  
    mobile_number = select('mobilenumber', 'candidate_mobilenumber_db', 'candidate_id', ID)
    work_experience = select('workexperience', 'candidate_workexperience_db', 'candidate_id', ID)
    education_qualification = select('educational_qualification', 'candidate_educationdetails_db', 'candidate_id', ID)
    graduation_years = select('graduation_years', 'candidate_educationdetails_db', 'candidate_id', ID)
    college_id = select('college_id', 'candidate_college_db', 'candidate_id', ID)
    college_name = select('college_name', 'colleges_db', 'id', college_id)
    city_id = select('city_id', 'candidate_city_db', 'candidate_id', ID)
    city = select('city_name', 'cities_db', 'id', city_id)
    state_id = select('state_id', 'candidate_state_db', 'candidate_id', ID)
    state = select('state_name', 'states_db', 'id', state_id)
    
    
    
    sql = 'SELECT skills_id from candidate_skills_db where candidate_id = '+str(ID)+' ;'
    cur.execute(sql)

    skills = cur.fetchall()

    skill_name = []
    for row in skills:
        for skill in row:
            skill_name.append(select('skill_name', 'skills_db', 'id', skill))
        
    
    result = {
        'name': name,
        'email': email_id,
        'mobile': mobile_number,
        'skills': skill_name,
        'education': education_qualification,
        'years': graduation_years,
        'city': city,
        'state': state,
        'work_experience': work_experience,
        'college': college_name
    }
    
    conn.commit()
    conn.close()
    
    return result

