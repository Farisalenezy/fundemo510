import streamlit as st

st.image('https://cdn1.iconfinder.com/data/icons/grocery-3/128/mayonnaise-512.png', width=200)

st.header("Team Mayo project")
#st.subheader("project demo")







import pandas as pd
from sqlalchemy import create_engine
from io import BytesIO, StringIO
#engine = create_engine("sqlite:///TestDB.db")

@st.cache(allow_output_mutation=True)
def get_connection():
    
    return create_engine("sqlite:///TestDB.db")


#https://github.com/streamlit/streamlit/issues/352
def multiselect(label, options, default, format_func=str):
    """multiselect extension that enables default to be a subset list of the list of objects
     - not a list of strings

     Assumes that options have unique format_func representations

     cf. https://github.com/streamlit/streamlit/issues/352
     """
    options_ = {format_func(option): option for option in options}
    default_ = [format_func(option) for option in default]
    selections = st.multiselect(
        label, options=list(options_.keys()), default=default_, format_func=format_func
    )
    return [options_[format_func(selection)] for selection in selections]



engine =get_connection()
#@st.cache( suppress_st_warning=True)
def main_df():
    query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname
            FROM FACULTY'''
    df = pd.read_sql_query(query,engine)
    return df

dataviz_choice = st.selectbox("Choose a Lookup",
                                          ["Instructor Classes Lookup",
                                           "Do my Own SQL Query"])






#instructor_lname_unique_m = st.text_input("Enter the instructor's last name").capitalize()
#    instructor_last_list = df_main.query('instructor_lname.str.contains("{}")'.format(instructor_lname_unique_m), engine='python')


if dataviz_choice =='Instructor Classes Lookup' :
    df_main = main_df()
    instructor_lname_unique = df_main['instructor_lname'].unique()
    #instructor_lname_unique_2 = year_unique
        
    instructor_lname_unique_m = st.multiselect("Enter the instructor's last name:",instructor_lname_unique)
    instructor_last_list = df_main[df_main['instructor_lname'].isin(instructor_lname_unique_m)]
    
    
    instructor_fname_unique = instructor_last_list['instructor_fname'].unique()
    
        
    instructor_fname_unique_m = st.multiselect("Enter the instructor's first name:",instructor_fname_unique)
    instructor_fisrt_list = instructor_last_list[instructor_last_list['instructor_lname'].isin(instructor_fname_unique_m)]
    
    
    #input_instructor = st.text_input("Enter the instructor's last name")
    ##input_instructor_f = str(instructor_fname_unique_m)[1:-1]


    if instructor_fname_unique_m  :
        
    
        query = '''SELECT FACULTY.instructor_fname,FACULTY.instructor_lname,Title,Catalog_id,Section,Semester,Year
            FROM FACULTY
            JOIN COURSE_OFFERING USING(FID)
            WHERE FACULTY.instructor_lname like '%{0}' and FACULTY.instructor_fname like '%{1}'
        ORDER BY Year, Semester'''.format(instructor_lname_unique_m[0] ,instructor_fname_unique_m[0])
        df = pd.read_sql_query(query,engine)
        #st.dataframe(df[1:])
        year_unique = df['YEAR'].unique()
        year_unique_2 = year_unique
        
        year = multiselect("Select the year you wish to see:", options=year_unique, default= year_unique)
        if year :
            year_df = df[df['YEAR'].isin(year)]
            sem = year_df['SEMESTER'].unique()
            sem_2 = sem
            
            Semester =  multiselect("Select the semester you wish to see:", options=sem, default= sem)
            if Semester:
            

                new_df =df[df['SEMESTER'].isin(Semester)].reset_index()
                new_df.pop("index")
                st.success("**Showing {} records:**".format(new_df.shape[0]))
                st.write(new_df)
            


            
elif  dataviz_choice == 'Do my Own SQL Query' :
    query = st.text_area("Run a SQL Query")
   
    if  st.button("Run it") :
        try:
                        
            tables = pd.read_sql_query(query,engine)
            st.write(tables)
        except:
            st.write("you entered a wrong Query")
            st.button("Re Run")

                
    
        
        
        
        
        

