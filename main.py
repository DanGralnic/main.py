import streamlit as st
import pandas as pd
import os
def Survay():
    per=""
    field=""
    st.sidebar.markdown("# Survay ")
    tab1, tab2, tab3 = st.tabs(["Survay", "Recommendation","next semester"])

    with tab1:
        per="None"
        field="None"
        list_course=[]
        df_prev=pd.DataFrame()
        str_name = "survay_file.parquet"
        d_by_ID = {}
        st.title(":green[Survay]")
        option=st.selectbox("Choose one course:",("None","Data Science","Linear 1","Probability"))
        ID=st.text_input("Enter ID", help="This input is used as an identifier",placeholder="XXXXXXXXX")
        if st.checkbox("open survay"):
            if option=="None" or len(ID)!=9:
                st.error(":red[The input is wrong]")
                st.stop()
            for i in range(len(ID)):
                if ID[i]<'0' or ID[i]>'9':
                    st.error("contain charater that not integer")
                    st.stop()
            if os.path.exists(str_name):
                df_prev = pd.read_parquet(str_name)
                if df_prev.empty == False:
                    df1 = df_prev[df_prev['ID'] == ID]
                    d_by_ID=df1.to_dict(df1)

            st.write("Hello ",ID,",")
            values=["None","I have children","I don't have children"]
            ind=0
            if d_by_ID!={}:
                ind=values.index(d_by_ID["Children"])
            child=st.selectbox("Your status:",values,index=ind)

            values1 = ["None","Yes","No"]
            ind1 = 0
            if d_by_ID != {}:
                ind1 = values1.index(d_by_ID["Work"])
            work=st.selectbox("Do you work?",values1,index=ind1)
            if work=="Yes":
                values2=["None","1-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100"]
                ind2=0
                if d_by_ID != {}:
                    ind2=values2.index(d_by_ID["job percentage"])
                per=st.selectbox("job percentage",values2,index=ind2)

                values3 = ["None", "hi-tech-development", "hi-tech-QA", "Cyber", "Other"]
                ind3 = 0
                if d_by_ID != {}:
                    ind3 = values3.index(d_by_ID["job field"])
                field=st.selectbox("job field",values3,index=ind3)

                ind10=0
                if d_by_ID!={}:
                    ind10=values1.index((d_by_ID[""]))
                important=  st.selectbox("Do you think the course contributes knowledge to your field of work? ",values1,index=ind10)

            values4=["None","0-3","3-6","6-9","9-12","12-15","15+"]
            ind4=0
            if d_by_ID != {}:
                ind4 = values4.index(d_by_ID["Number of weekly study hours"])
            studing=st.selectbox("Number of weekly study hours you spent during the semester",values4,index=ind4)

            values5=["None","1","2","3","4","5"]
            ind5=0
            if d_by_ID != {}:
                ind5 = values5.index(d_by_ID["Organized and relevant"])
            relevant=st.selectbox("Is the course organized and relevant?",values5,index=ind5)

            ind6 = 0
            if d_by_ID != {}:
                ind6 = values5.index(d_by_ID["Organized and relevant"])
            take=st.selectbox("Can this course be taken with other courses?",values1,index=ind6)
            #delete the select course from the list courses.
            if take=="Yes":
                list_choose =[option]
                if d_by_ID != {}:
                    list_choose =d_by_ID["list"]
                list_course=st.multiselect("mark all the courses that you think this course can be combined with",["Data Science","Linear 1","Probability"],list_choose)
                if option not in list_course:
                    st.error("You can't delete your course from the list")
                    st.stop()

            if st.button("send"):
                if child=="None" or work=="None" or per=="None" or  field=="None" or studing=="None" or relevant=="None" or  take=="None" or important=="None":
                    st.error("You need to fullfil all the questions")
                    st.stop()
                    new_data={
                        "ID": ID,
                        "Children": child,
                        "Work": work,
                        "job percentage": per,
                        "job field": field,
                        "important": important,
                        "Number of weekly study hours": studing,
                        "Organized and relevant": relevant,
                        "Taken with other courses": take,
                        "list": list_course
                    }
                    df_prev=df_prev._append(new_data,ignore_index=True)
                    df_prev.drop_duplicates(['ID'],keep="last")
                    df_prev.to_parquet(str_name)
                    st.write("Saved! Thank You!")



    with tab2:
        child=""
        work=""
        per=""
        field=""
        st.title(":green[Recommendation]")
        st.write("This page going to exhibit the data about the number of weekly study hours a student spent in the course")
        option = st.selectbox("Choose a course that you want to see the information about him on website:", ("None", "Data Science", "Linear 1", "Probability"))
        if st.checkbox("next"):
            if option == "None":
                st.error(":red[The input is wrong]")
                st.stop()
            if st.checkbox("Mark if you want to see information of a specific group regarding the course you have chosen "):
                child = st.selectbox("Your status:", ("None", "I have children", "I don't have children"))
                work = st.selectbox("Do you work?", ("None", "Yes", "No"))

                if st.checkbox("open graph of weekly study hours a student spent in the course according to your choises"):
                    if child != "None" and work == "None": #just parents
                        if st.checkbox("open graph that exhibit the number of weekly hours spent by students who testified that they are parents in this course"):
                            pass
                    elif child == "None" and work == "None":#mistake
                        st.error("You need to fullfil one filter at list")
                        st.stop()
                    else:#all other combinations
                        pass
            else:
                if st.checkbox("open graph of weekly study hours a student spent in the course"):
                    pass

    with tab3:
        st.title("Next semester")
        st.write(":green[Enter the course you want to take next semester. The page will display whether it is recommended to take the courses together]")
        list_courses=st.multiselect("Your courses", ["Data Science","Linear 1","Probability"])
        if st.checkbox("check"):
            if len(list_courses)==0:
                st.error("choose one course at least")
                st.stop()
            if len(list_courses)==1:
                st.write("You picked just one course so.. it's OK :) good luck!")
            if len(list_courses)>1:
                pass










page_names_to_funcs = {
    "Survay": Survay
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

