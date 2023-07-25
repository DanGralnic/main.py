import streamlit as st
import pandas as pd
import os
def sum(get_dict, get_list):
    for i in get_list:
        if i in get_dict:
            get_dict[i]+=1
    return get_dict

def sum_hist(get_dict, get_list):
    for i in get_list:
        if i not in get_dict:
            get_list[i]=0
        get_dict[i]+=1
    return get_dict
def Survay():
    st.sidebar.markdown("# Survay ")
    tab1, tab2, tab3 = st.tabs(["Survay", "Recommendation","next semester"])

    with tab1:
        per="---"
        field="---"
        important="---"
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
                    if df1.empty==False:
                        df2=df1[df1['course']==option]
                        if df2.empty==False:
                            d_by_ID=dict(df2.iloc[0])
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
                important=st.selectbox("Do you think the course contributes knowledge to your field of work? ",values1,index=ind10)

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
                if len(list_course)==1:
                    st.error("You need to choose some courses")
                    st.stop()


            if st.button("send"):
                if child=="None" or work=="None" or per=="None" or  field=="None" or studing=="None" or relevant=="None" or  take=="None" or important=="None":
                    st.error("You need to fullfil all the questions")
                    st.stop()
                new_data={"ID": ID,"course": option,"Children": child,"Work": work,"job percentage": per,"job field": field,"important": important,"Number of weekly study hours": studing,"Organized and relevant": relevant,"Taken with other courses": take,"list": list_course}
                st.write(new_data)
                if os.path.exists(str_name)==False:
                    df_prev=pd.DataFrame.from_dict(new_data)
                    df_prev.to_parquet(str_name)
                else:
                    df_prev=df_prev._append(new_data,ignore_index=True)
                    st.write(df_prev,"here")
                    df_prev.drop_duplicates(['ID'],keep="last")
                    df_prev.to_parquet(str_name)
                st.write("Saved! Thank You!")



    with tab2:
        str_name = "survay_file.parquet"
        child="None"
        work="None"
        per=""
        field=""
        df3=pd.DataFrame.empty
        hist_hours={"0-3":0,"3-6":0,"6-9":0,"9-12":0,"12-15":0,"15+":0}
        hist_imp_and_rel={"1":0,"2":0,"3":0,"4":0,"5":0}
        data_hours = {"type": hist_hours.keys(), "sum": hist_hours.values()}
        data_imp_and_rel = {"type": hist_imp_and_rel.keys(), "sum": hist_imp_and_rel.values()}
        st.title(":green[Recommendation]")
        st.write("This page going to exhibit the data about the number of weekly study hours a student spent in the course")
        option = st.selectbox("Choose a course that you want to see the information about him on website:", ("None", "Data Science", "Linear 1", "Probability"))
        if st.checkbox("next"):
            if option == "None":
                st.error(":red[The input is wrong]")
                st.stop()
            else:
                child = st.selectbox("Your status:", ("None", "I have children", "I don't have children"))
                work = st.selectbox("Do you work?", ("None", "Yes", "No"))
                if st.button("check"):
                    if os.path.exists(str_name):
                        df_prev = pd.read_parquet(str_name)
                        if len(df_prev)>=1:
                            df1 = df_prev[df_prev['course'] == option]
                            if work!="None" and child!="None":
                                df3=df1[(df1["Work"]==work) & (df1['Children'] == child)]
                            elif work!="None":
                                df3 = df1[df1["Work"] == work]
                            elif child!="None":
                                df3 = df1[df1['Children'] == child]
                            else:
                                df3=df1
                            if len(df3)>=1:
                                lst_week=list(df3.loc[:, "Number of weekly study hours"])
                                hist_hours=sum(hist_hours,lst_week)
                                data_hours = {"hours": hist_hours.keys(), "sum": hist_hours.values()}
                                df_sum_hours = pd.DataFrame.from_dict(data_hours)

                                lst_important=list(df3.loc[:, "Organized and relevant"])
                                hist_imp_and_rel=sum(hist_imp_and_rel,lst_important)
                                data_imp_and_rel = {"Organized and relevant": hist_imp_and_rel.keys(), "sum": hist_imp_and_rel.values()}
                                df_sum_imp_and_rel = pd.DataFrame.from_dict(data_imp_and_rel)

                                tab1,tab2 = st.tabs(["Hours per week","Organized and relevant"])
                                with tab1:
                                    st.header("Hours per week")
                                    st.bar_chart(df_sum_hours, x="hours", y="sum")
                                with tab2:
                                    st.header("Organized and relevant")
                                    st.bar_chart(df_sum_imp_and_rel, x="Organized and relevant", y="sum")
                            else:
                                st.write("No data")
                    else:
                        st.write("No data")

    with tab3:
        list_course_to_take=[]
        dict_hist={}
        conter_No=0
        st.title("Next semester")
        st.write(":green[Enter the course you want to take next semester. The page will display whether it is recommended to take the courses together]")
        option= st.selectbox("Your courses", ["None","Data Science","Linear 1","Probability"], key="course")
        child = st.selectbox("Your status:", ["None", "I have children", "I don't have children"], key="status")
        work = st.selectbox("Do you work?", ["None", "Yes", "No"], key="work")
        if st.checkbox("check"):
            if option=="None":
                st.error("choose one course!")
                st.stop()
            if os.path.exists(str_name):
                df_prev = pd.read_parquet(str_name)
                if len(df_prev) >= 1:
                    df1 = df_prev[df_prev['course'] == option]
                    if work != "None" and child != "None":
                        df3 = df1[(df1["Work"] == work) & (df1['Children'] == child)]
                    elif work != "None":
                        df3 = df1[df1["Work"] == work]
                    elif child != "None":
                        df3 = df1[df1['Children'] == child]
                    else:
                        df3 = df1
                    if len(df3) >= 1:
                        lst_No = list(df3.loc[:, "Taken with other courses"])
                        for i in lst_No:
                            if i=="No":
                                conter_No+=1
                        list_course_to_take=list(df3.loc[:, "list"])
                        for i in list_course_to_take:
                            dict_hist=sum_hist(dict_hist,i)
                        dict_hist["No"]=conter_No
                        data_courses = {"courses": dict_hist.keys(), "sum": dict_hist.values()}
                        df_sum_courses = pd.DataFrame.from_dict(data_courses)
                        st.header("Recommendation courses")
                        st.bar_chart(df_sum_courses, x="courses", y="sum")
                    else:
                        st.write("No Data!")











page_names_to_funcs = {
    "Survay": Survay
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

