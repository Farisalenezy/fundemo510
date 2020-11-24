import streamlit as st
import markdown
st.set_option('deprecation.showImageFormat', False)
st.beta_set_page_config(
 page_title="Mayo SQL Project",
page_icon="ms-icon-310x310.png",
initial_sidebar_state="expanded",)
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 750px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

md = markdown.Markdown()
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        #page-content {
  flex: 0 0 auto;
}

#sticky-footer {
  flex-shrink: none;
}

/* Other Classes for Page Styling */

body {
  background: #007bff;
  background: linear-gradient(to right, #e66465, #9198e5);
}
            
   </style>          """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#st.image('cover123.png', width=700)

rep_img = '''<img src="https://i.imgur.com/NuKYeTy.png" class="img-fluid" alt="Responsive image">'''
st.markdown(rep_img, unsafe_allow_html=True)

st.markdown("#### Choose a Lookup:")
#st.subheader("project demo")







import pandas as pd
from sqlalchemy import create_engine

#engine = create_engine("sqlite:///TestDB.db")

@st.cache(allow_output_mutation=True)
def get_connection():
    
    return create_engine("sqlite:///CourseData.db")


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

def get_year ():
        query = '''SELECT YEAR , SEMESTER From CATALOG_YEAR '''
        year_df = pd.read_sql_query(query,engine)
        
        return year_df
    
def classes_df():
        query = '''SELECT CRN, COURSE_OFFERING.Semester,COURSE_OFFERING.Year,COURSE_OFFERING.Title,COURSE_OFFERING.Catalog_ID, COURSE_OFFERING.CatalogYear,COURSE_OFFERING.Meetings,COURSE_OFFERING.Timecodes,COURSE_OFFERING.Section,COURSE_OFFERING.Cap,COURSE_OFFERING.Act,COURSE_OFFERING.Rem,COURSE_OFFERING.instructor_lname, COURSE_OFFERING.instructor_fname ,PROGRAMS.program_name  From COURSE_OFFERING  join COURSE using (CID) join PROGRAMS using (PID) '''

        classes_df = pd.read_sql_query(query,engine)
        
        return classes_df
def tables_info():
    
    query = 'SELECT name from sqlite_master where type= "table"'
    tables = pd.read_sql_query(query,engine)
    tables = tables.rename(columns={"name": "DatabaseTables"})
    return tables

dataviz_choice = st.selectbox(" ",
                                          ['Course Lookup' ,"Instructor Classes Lookup", "Database Tables Information" ,
                                           "Do my Own SQL Query"])






#instructor_lname_unique_m = st.text_input("Enter the instructor's last name").capitalize()
#    instructor_last_list = df_main.query('instructor_lname.str.contains("{}")'.format(instructor_lname_unique_m), engine='python')
if dataviz_choice =='Database Tables Information':
    tables =tables_info()
    t_info = tables.copy()
    st.header("Database Tables Overview :")
    st.markdown(f'''<div class="list-group">
  <button type="button" class="list-group-item list-group-item-action active"> Database Tables</button>
  <button type="button" class="list-group-item list-group-item-action">{str(t_info.DatabaseTables[0])}</button>
  <button type="button" class="list-group-item list-group-item-action">{str(t_info.DatabaseTables[1])}</button>
  <button type="button" class="list-group-item list-group-item-action">{str(t_info.DatabaseTables[2])}</button>
  <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[3])}</button>
   <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[4])}</button>
   <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[5])}</button>
   <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[6])}</button>
</div>''', unsafe_allow_html=True)
    #st.table(t_info)
     
    if st.checkbox("Click Here to See The ERD"):
        st.image("Mayo.png" , use_column_width=True ,format =  'PNG' )# ,width = 900)
    st.header("Database Tables Information :")
    for i in tables.DatabaseTables.values : 
    
        query = "PRAGMA TABLE_INFO ({}) ".format (i)

        table_info = pd.read_sql_query(query,engine)
        table_info =table_info.rename(columns={"name": "ColumnName" ,"type": "DataType" , 'dflt_value':'default_value',"pk": 'primary_key'})
        table_info.primary_key = table_info.primary_key.map({1:"Yes" , 0: ""})
        
        st.write("** Table : **", i)
        st.write(table_info)
        st.markdown("---")

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
                
            
    
                new_df =year_df[year_df['SEMESTER'].isin(Semester)].reset_index()
                new_df.pop("index")
                st.success("**Showing {} records:**".format(new_df.shape[0]))
                st.write(new_df)

            

if dataviz_choice =='Course Lookup' :
    #year_df = get_year ()
    classes_df = classes_df()
    year_pick = (2018,2019)
    #instructor_lname_unique_2 = year_unique
        
    year_pick_m = st.multiselect("Pick a term year:",year_pick)
    classes_df_year = classes_df[classes_df['YEAR'].isin(year_pick_m)]
    
    
    semester_pick = classes_df_year['SEMESTER'].unique()
    
    if year_pick_m : 
        semester_pick_m = multiselect("Select the semester you wish to see:", options=semester_pick, default= semester_pick)
        classes_df_year_semseter = classes_df_year[classes_df_year['SEMESTER'].isin(semester_pick_m)]
    #st.write(classes_df_year)
    #st.write(classes_df_year_semseter)
    
    #######################
        if semester_pick_m :
    
            program_name = classes_df_year_semseter['program_name'].unique()
    #instructor_lname_unique_2 = year_unique
    
        
            program_name_m = st.multiselect("Pick a program:",program_name)
            classes_df_year_semseter_pro_name = classes_df_year_semseter[classes_df_year_semseter['program_name'].isin(program_name_m)]
    
    
            catalog_id_pick = classes_df_year_semseter_pro_name['CATALOG_ID'].unique()
    
        
            catalog_id_pick_m = multiselect("Pick a course:", options=catalog_id_pick, default= catalog_id_pick)
            classes_df_year_semseter_pro_name = classes_df_year_semseter_pro_name[classes_df_year_semseter_pro_name['CATALOG_ID'].isin(catalog_id_pick_m)].reset_index()
            if catalog_id_pick_m :
                
                classes_df_year_semseter_pro_name.pop("index")
                st.success("**Showing {} records:**".format(classes_df_year_semseter_pro_name.shape[0]))
                st.write(classes_df_year_semseter_pro_name)
    #input_instructor = st.text_input("Enter the instructor's last name")
    ##input_instructor_f = str(instructor_fname_unique_m)[1:-1]


    
            


            
elif  dataviz_choice == 'Do my Own SQL Query' :
    if st.checkbox("Click Here to See The ERD"):
        st.image("Mayo.png" , use_column_width=True ,format =  'PNG' )# ,width = 900)
    query = st.text_area("Run a SQL Query")
    tables =tables_info()
    t_info = tables.copy()
   
   
    if  st.button("Run it") :
        try:
                        
            tables = pd.read_sql_query(query,engine)
            st.write(tables)
        except:
            st.write("you entered a wrong Query")
            st.button("Re Run")
    st.markdown(f'''<div class="list-group">
  <button type="button" class="list-group-item list-group-item-action active"> Database Tables</button>
  <button type="button" class="list-group-item list-group-item-action">{str(t_info.DatabaseTables[0])}</button>
  <button type="button" class="list-group-item list-group-item-action">{str(t_info.DatabaseTables[1])}</button>
  <button type="button" class="list-group-item list-group-item-action">{str(t_info.DatabaseTables[2])}</button>
  <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[3])}</button>
   <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[4])}</button>
   <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[5])}</button>
   <button type="button" class="list-group-item list-group-item-action"> {str(t_info.DatabaseTables[6])}</button>
</div>''', unsafe_allow_html=True)

md2= f'''</div>
<div class="card bg-light mb-3" style="max-width: 18rem;">
  <div class="card-header">About</div>
  <div class="card-body">
    <p class="card-text">This App was built to show how SQLite and pandas work together to produce fast lookups and customized outputs.</p>
<a href="https://github.com/Farisalenezy/fundemo510" class="btn btn-primary btn-sm active" role="button" aria-pressed="false">The App Repository Link</a>
  </div>
</div>'''

md3= f'''<div class="card bg-light mb-3" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">Made by:</h5>
    <p class="card-text">Faris Alenezy</p>
     <p class="card-text"><a href="https://alenezy.com/">Website</a></p>
  </div>
</div>'''
t0= f'''</div>
<div class="card bg-light mb-3" style="max-width: 45rem;">
  <div class="card-header">info</div>
  <div class="card-body">
    <p class="card-text">Read more about how was the database was built by clicking the report button below</p>
<a href="https://github.com/fairfield-ba510-spring2020/term-project-mayo" class="btn btn-primary btn-sm active" role="button" aria-pressed="false">The Report Github Link</a>
  </div>
</div>'''
t1= st.sidebar.markdown(md3, unsafe_allow_html=True)
t2= st.sidebar.markdown(md2, unsafe_allow_html=True)


#if button:
footer= f'''<body class="d-flex flex-column">
  <div id="page-content">
    <div class="container text-center">
      <div class="row justify-content-center">
        <div class="col-md-7">
          <h1 class="font-weight-light mt-4 text-white">Read more about how  the database was built by clicking the report button below   &nbsp; &nbsp; <a href="https://github.com/fairfield-ba510-spring2020/term-project-mayo" class="btn btn-primary btn-sm active" role="button" aria-pressed="false">The Report Github Link</a></h1>
          


      
   
  <footer id="sticky-footer" class="py-4 bg-dark text-white-50">
    <div class="container text-center">
      <small>Copyright &copy; Your Website</small>
    </div>
  </footer>
</body>'''
 

st.markdown(footer, unsafe_allow_html=True)


