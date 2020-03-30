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
from io import BytesIO, StringIO
#engine = create_engine("sqlite:///TestDB.db")

#@st.cache(hash_funcs={_io.BytesIO: my_hash_func})
def get_connection():
    
    return create_engine("sqlite:///TestDB.db")
engine =get_connection()
dataviz_choice = st.selectbox("Choose Data Visualization",
                                          ["Instructor Classes Lookup",
                                           "Do my Own SQL Query"])

clubs = st.sidebar.multiselect('Show Player for clubs?', df['Club'].unique())
nationalities = st.sidebar.multiselect('Show Player from Nationalities?', df['Nationality'].unique())

new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]
st.write(new_df)


values = st.slider('Select a range of values',2014, 2019 )
st.write('Values:', values)


if dataviz_choice =='Instructor Classes Lookup' :
    input_instructor = st.text_input("Enter the instructor's last name")
    input_instructor_f = st.text_input("Enter the instructor's first name")


    if input_instructor_f :
        input_year =st.text_input("Enter the year you wish to see or type in No to see all the years:").lower()
      
        if input_year == "no" or  input_year == "n" or  input_year == "nah" or  input_year == ""or  input_year == " ":
    
            query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname,Title,Catalog_id,Section,Semester,Year
            FROM FACULTY
            JOIN COURSE_OFFERING USING(FID)
            WHERE FACULTY.instructor_lname like '%{0}' and FACULTY.instructor_fname like '%{1}'
        ORDER BY Year, Semester'''.format(input_instructor ,input_instructor_f)
            tables = pd.read_sql_query(query,engine)
            st.dataframe(tables[1:])
    
        elif input_year != "no" or  input_year != "n" or  input_year != "nah" :
            if input_year:
                
                input_semester = st.text_input("Enter the semester you wish to see or type in No to see all the courses that the instructor is teaching :")
           #.format(input_year)).lower()
                if input_semester:
                    if input_semester == "no" or input_semester== "n" or  input_semester == "nah":
                        query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname,Title,Catalog_id,Section,Semester,Year
            FROM FACULTY
            JOIN COURSE_OFFERING USING(FID)
            WHERE FACULTY.instructor_lname like '%{0}' and FACULTY.instructor_fname like '%{1}' and year = {2}
            ORDER BY Year, Semester'''.format(input_instructor ,input_instructor_f, input_year )
                        tables = pd.read_sql_query(query,engine)
                        st.write (tables)
                    elif input_semester != "no" or  input_semester != "n" or  input_semester != "nah":
                        query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname,Title,Catalog_id,Section,Semester,Year
        FROM FACULTY
        JOIN COURSE_OFFERING USING(FID)
        WHERE FACULTY.instructor_lname like '%{0}'  AND FACULTY.instructor_fname like '%{1}'
        AND year = {2}
        AND SEMESTER == '{3}'
        ORDER BY Year, Semester'''.format(input_instructor ,
                           input_instructor_f,
                           input_year , 
                           input_semester.capitalize() )
                        tables = pd.read_sql_query(query,engine)
                        st.write (tables)


            
elif  dataviz_choice == 'Do my Own SQL Query' :
    query = st.text_area("Run a SQL Query")
   
    if  st.button("Run it") :
        try:
                        
            tables = pd.read_sql_query(query,engine)
            st.write(tables)
        except:
            st.write("you entered a wrong Query")
            st.button("Re Run")

                
    
        
        
        
        
        

