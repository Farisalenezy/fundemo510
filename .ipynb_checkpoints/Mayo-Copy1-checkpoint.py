import streamlit as st

st.image('https://cdn1.iconfinder.com/data/icons/grocery-3/128/mayonnaise-512.png', width=200)

st.header("Team Mayo project")
#st.subheader("project demo")





#@st.cache( suppress_st_warning=True)








#import flask
##################################################################################################
#from flask_sqlalchemy import SQLAlchemy

import pandas as pd
from sqlalchemy import create_engine
#engine = create_engine("sqlite:///TestDB.db")

@st.cache(allow_output_mutation=True)
def get_connection():
    return create_engine("sqlite:///TestDB.db")

engine =get_connection()
dataviz_choice = st.selectbox("Choose Data Visualization",
                                          ["instructor lookup",
                                           "Do my Own SQL Query"])

if dataviz_choice =='instructor lookup' :
    input_instructor = st.text_input("Enter the instructor's last name")


    input_year =st.text_input("Enter the year you wish to see or type in No to see all the years:").lower()
    input_semester = st.text_input("Enter the semester you wish to see or type in No to see all the courses that the instructor is teaching :"
    
    if input_year == "no" or  input_year == "n" or  input_year == "nah" :
    
        query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname,Title,Catalog_id,Section,Semester,Year
        FROM FACULTY
            JOIN COURSE_OFFERING USING(FID)
        WHERE FACULTY.instructor_lname like '%{}'
        ORDER BY Year, Semester
        LIMIT 20'''.format(input_instructor)
            tables = pd.read_sql_query(query,engine)
            st.write(tables)
    
    elif input_year != "no" or  input_year != "n" or  input_year != "nah" :
           #.format(input_year)).lower()
           
        if input_semester == "no" or input_semester== "n" or  input_semester == "nah":

            query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname,Title,Catalog_id,Section,Semester,Year
            FROM FACULTY
            JOIN COURSE_OFFERING USING(FID)
            WHERE FACULTY.instructor_lname like '%{0}' and year = {1}
            ORDER BY Year, Semester
            LIMIT 20'''.format(input_instructor , input_year )
                tables = pd.read_sql_query(query,engine)
                st.write (tables)
    elif input_semester != "no" or  input_semester != "n" or  input_semester != "nah":
        query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname,Title,Catalog_id,Section,Semester,Year
        FROM FACULTY
        JOIN COURSE_OFFERING USING(FID)
        WHERE FACULTY.instructor_lname like '%{0}' 
        AND year = {1}
        AND SEMESTER == '{2}'
        ORDER BY Year, Semester
        LIMIT 20'''.format(input_instructor ,
                           input_year , 
                           input_semester.capitalize() )
        tables = pd.read_sql_query(query,engine)
        st.write (tables)


            
elif  dataviz_choice == 'Do my Own SQL Query' :
    query = st.text_input("Run a SQL Query")
    if query :
        try:
                        
            tables = pd.read_sql_query(query,engine)
            st.write(tables)
        except:
            st.write("you entered a wrong Query")
            st.button("Re Run")

                
    
        
        
        
        
        

