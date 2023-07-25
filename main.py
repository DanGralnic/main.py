import streamlit as st
import pandas as pd
import os
def sum(get_dict, get_list,dict_keys):
    if get_dict!={} and get_list!=[] and dict_keys!=[]:
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

def build_df(str_name,option,work,child):
    df3 = pd.DataFrame.empty
    if str=="":
        return df3
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
    return df3

def build_df_sum_x(get_dict,get_list,str_name,dict_keys):
    ret_dict={}
    data_dict={}
    df_sum=pd.DataFrame.empty
    if str_name=="":
        return df_sum
    ret_dict = sum(get_dict, get_list,dict_keys)
    data_dict = {str_name: ret_dict.keys(), "sum": ret_dict.values()}
    df_sum= pd.DataFrame.from_dict(data_dict)
    return df_sum


def No_count(get_lst):
    if get_lst==[]:
        return 0
    count=0
    for i in get_lst:
        if i=="No":
            count+=1
    return count

def check_input(ID,option):
    if ID=="" or option=="":
        return False
    if option == "None" or len(ID) != 9:
        st.error(":red[The input is wrong]")
        return False
    for i in range(len(ID)):
        if ID[i] < '0' or ID[i] > '9':
            st.error("contain charater that not integer")
            return False
    return True


def Survay():
    st.sidebar.markdown("# Survay ")
    tab1, tab2, tab3 = st.tabs(["Survay", "Recommendation","next semester"])
    str_name = "survay_file.parquet"
    with tab1:
        per="---"
        field="---"
        important="---"
        list_course=[]
        df_prev=pd.DataFrame()
        d_by_ID = {}
        st.title(":green[Survay]")
        option=st.selectbox("Choose one course:",("None","Data Science","Linear 1","Probability"))
        ID=st.text_input("Enter ID", help="This input is used as an identifier",placeholder="XXXXXXXXX")
        if st.checkbox("open survay"):
            if not check_input(ID,option):
                st.stop()
            if os.path.exists(str_name):
                df_prev = pd.read_parquet(str_name)
                if not df_prev.empty:
                    df1 = df_prev[(df_prev['ID'] == ID)&(df_prev['course']==option)]
                    if not df1.empty:
                        d_by_ID=dict(df1.iloc[0])
            st.write("Hello ",ID,",")
            values=["None","I have children","I don't have children"]
            child=st.selectbox("Your status:",values,index=values.index(d_by_ID.get("Children", "None")))

            values1 = ["None","Yes","No"]
            work=st.selectbox("Do you work?",values1,index=values1.index(d_by_ID.get("Work", "None")))

            if work=="Yes":
                values2=["None","1-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100"]
                per=st.selectbox("job percentage",values2,index=values2.index(d_by_ID.get("job percentage", "None")))

                values3 = ["None", "hi-tech-development", "hi-tech-QA", "Cyber", "Other"]
                field=st.selectbox("job field",values3,index=values3.index(d_by_ID.get("job field", "None")))

                important=st.selectbox("Do you think the course contributes knowledge to your field of work? ",values1,index=values1.index(d_by_ID.get("important", "None")))

            values4=["None","0-3","3-6","6-9","9-12","12-15","15+"]
            studing=st.selectbox("Number of weekly study hours you spent during the semester",values4,
                                 index=values4.index(d_by_ID.get("Number of weekly study hours", "None")))

            values5=["None","1","2","3","4","5"]
            relevant=st.selectbox("In your opinion, how much this course organized and relevant?",values5,index=values5.index(d_by_ID.get("Organized and relevant", "None")))


            take=st.selectbox("Can this course be taken with other courses?",values1,
                              index=values1.index(d_by_ID.get("Taken with other courses", "None")))

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
                if "None" in (child,work,per, field, studing,relevant,take,important):
                    st.error("You need to fill all the questions")
                    st.stop()
                new_data={"ID": ID,
                          "course": option,
                          "Children": child,
                          "Work": work,
                          "job percentage": per,
                          "job field": field,
                          "important": important,
                          "Number of weekly study hours": studing,
                          "Organized and relevant": relevant,
                          "Taken with other courses": take,
                          "list": list_course}

                if not os.path.exists(str_name):
                    df_prev=pd.DataFrame.from_dict(new_data)
                    df_prev.to_parquet(str_name)
                else:
                    df_prev = df_prev.append(new_data,ignore_index=True)
                    df_prev.drop_duplicates(['ID'],keep="last")
                    df_prev.to_parquet(str_name)
                st.write("Saved! Thank You!")


    with tab2:
        hist_hours={"0-3":0,"3-6":0,"6-9":0,"9-12":0,"12-15":0,"15+":0}
        hist_imp_and_rel={"1":0,"2":0,"3":0,"4":0,"5":0}
        st.title(":green[Recommendation]")
        st.write("This page going to exhibit the data about the number of weekly study hours a student spent in the course")
        option = st.selectbox("Choose a course that you want to see the information about him on website:", ("None", "Data Science", "Linear 1", "Probability"))
        if st.checkbox("next"):
            if option == "None":
                st.error(":red[The input is wrong]")
                st.stop()

            child = st.selectbox("Your status:", ("None", "I have children", "I don't have children"),key="status1")
            work = st.selectbox("Do you work?", ("None", "Yes", "No"),key="work1")
            if st.button("check"):
                df3 = build_df(str_name,option,work,child)
                if not df3.empty:#############################len(df3)>=1
                    lst_week=df3["Number of weekly study hours"].values.tolist()
                    df_sum_hours = build_df_sum_x(hist_hours,lst_week,"hours", hist_hours.keys())
                    lst_important=df3["Organized and relevant"].values.tolist()
                    df_sum_imp_and_rel = build_df_sum_x(hist_imp_and_rel,lst_important,"Organized and relevant",hist_imp_and_rel.keys())
                    tab1, tab2 = st.tabs(["Hours per week","Organized and relevant"])
                    with tab1:
                        st.header("Hours per week")
                        st.bar_chart(df_sum_hours, x="hours", y="sum")
                    with tab2:
                        st.header("Organized and relevant")
                        st.bar_chart(df_sum_imp_and_rel, x="Organized and relevant", y="sum")
                else:
                    st.write("No data")

    with tab3:
        dict_hist={}
        st.title("Next semester")
        st.write(":green[Enter the course you want to take next semester. The page will display whether it is recommended to take the courses together]")
        option= st.selectbox("Your courses", ["None","Data Science","Linear 1","Probability"], key="course")
        child = st.selectbox("Your status:", ["None", "I have children", "I don't have children"], key="status")
        work = st.selectbox("Do you work?", ["None", "Yes", "No"], key="work")
        if st.checkbox("check"):
            if option=="None":
                st.error("choose one course!")
                st.stop()
            df3=build_df(str_name,option,work,child)
            if not df3.empty:#############################len(df3)>=1
                list_course_to_take = df3["list"].values.tolist()
                for i in list_course_to_take:
                    dict_hist=sum_hist(dict_hist,i)
                lst_No = df3["Taken with other courses"].values.tolist()
                dict_hist["No"]=No_count(lst_No)
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

