import streamlit as st
import pandas as pd
import numpy as np
import os

def check_df_if_empty(df):
    df = df.fillna(np.nan)
    null_df = df[df.isna().any(axis=1)]
    if not null_df.empty:
        st.error("ERROR! THERE ARE MISSING VALUES! FILL THEM ALL")
        return False
    return True

def save_df(df_prev,str_course,df_data,key_sort=["ID"]):
    if not os.path.exists(str_course):
        df_prev = pd.DataFrame.from_dict(df_data)
        df_prev.to_parquet(str_course)
    else:
        df_prev=pd.concat([pd.DataFrame.from_dict(df_data),df_prev],ignore_index=True,axis=0)
        # df_prev = df_prev.append(pd.DataFrame.from_dict(df_data), ignore_index=True)
        df_prev.drop_duplicates(key_sort, keep="last")
        df_prev.to_parquet(str_course)

def check_lists(lst):
    if lst==[]:
        return False
    for i in range(len(lst)):
        if lst[i].isdigit()==False:
            return False
    return True

def check_data_and_list(lst_grades,lst_weight,test_grade):
    if lst_grades==[] or lst_weight==[] or len(lst_grades)!=len(lst_weight) or int(test_grade)<0 or int(test_grade)>100:
        return -1

def final_grade(lst_grades,lst_weight,test_grade):
    count_weigh=0
    avg=0
    if check_data_and_list(lst_grades,lst_weight,test_grade)==-1:
        st.error("The input is wrong")
        return -1
    for i in range(len(lst_weight)):
        count_weigh+=lst_weight[i]
    part_of_final_grade=100-count_weigh
    if part_of_final_grade<=0:
        st.error("The sum of weight is not 100")
        return -1
    for i in range(len(lst_weight)):
        avg+=lst_grades[i]*((lst_weight[i])/100)
    avg+=test_grade*(part_of_final_grade/100)
    return avg

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
        if not df_prev.empty:####################(df_prev) >= 1:
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
    if option == "None" or len(ID) != 9 or ID.isdigit()==False:
        st.error(":red[The input is wrong]")
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
                save_df(df_prev, str_name, new_data, ["ID"])
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
                if not df3.empty:
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
            if not df3.empty:
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

def calculator():
    col_config={"The weight of the grade from the final grade": st.column_config.NumberColumn("The weight of the grade from the final grade",
                                                                                                          help="How much the weigth of the grade(1-100)?",
                                                                                                          min_value=1, max_value=100, step=1, format="%d"),"grade": st.column_config.NumberColumn("grade",
                                                                                                          help="grade(1-100)?",
                                                                                                          min_value=1, max_value=100, step=1)}
    d_by_ID={}
    str_course="grades_at_course.parquet"
    st.sidebar.markdown("# Calculator ")
    st.header(":green[Grade for Course]")
    st.write(":green[Enter your grades in course and your grade in the test and get your grade in the course]")
    ID=st.text_input("Enter ID:",placeholder="XXXXXXXXX")
    course=st.selectbox("Choose one course:",["None","Data Science","Linear 1","Probability"])
    cols = ["Name", "The weight of the grade from the final grade", "grade"]
    table = pd.DataFrame([[""] * len(cols)], columns=cols)
    if st.checkbox("check"):
        if not check_input(ID,course):
            st.stop()

        if os.path.exists(str_course):
            df_prev = pd.read_parquet(str_course)
            df1=df_prev[(df_prev["ID"]==ID)&(df_prev["course"]==course)]
            if not df1.empty:
                d_by_ID=dict(df1.iloc[0])
                df=st.data_editor(df1,column_order=["The weight of the grade from the final grade","grade"],num_rows="dynamic",hide_index=True)
            else:
                df= st.data_editor(table,column_config=col_config, num_rows="dynamic",hide_index=True)
        else:
            df = st.data_editor(table, column_config=col_config, num_rows="dynamic",hide_index=True)
        test_grade = st.text_input("Enter your grade in the exam:", d_by_ID.get("final_grade", "0-100"))
        col1,col2=st.columns(2)

        with col1:
            if st.button("Check the final grade"):
                if not check_df_if_empty(df):
                    st.stop()
                lst_grades = df["grade"].values.tolist()
                lst_weight = df["The weight of the grade from the final grade"].values.tolist()
                if not check_lists(lst_weight) or not check_lists(lst_grades):
                    st.error("Wrong input")
                    st.stop()
                df[["grade","The weight of the grade from the final grade"]]=df[["grade","The weight of the grade from the final grade"]].astype(int)
                lst_grades = df["grade"].values.tolist()
                lst_weight = df["The weight of the grade from the final grade"].values.tolist()
                avg=final_grade(lst_grades,lst_weight,int(test_grade))
                if avg==-1:
                    # st.error("Input is wrong")
                    st.stop()
                st.write("The final grade in this course is:",avg)

        with col2:
            if st.button("save data"):
                df_data={"ID":ID,"course":course,"The weight of the grade from the final grade":df["The weight of the grade from the final grade"].values.tolist(),
                                     "grade":df["grade"].values.tolist(),"final_grade":test_grade}
                if not test_grade.isdigit():
                    st.error("Wrong input")
                    st.stop()
                if not check_input(df_data["ID"],df_data["course"]) or check_data_and_list(df_data["The weight of the grade from the final grade"],df_data["grade"],int(test_grade))==-1:
                    st.stop()
                save_df(df_prev,str_course,df_data,["ID"])
                st.write("saved!")


page_names_to_funcs = {
    "Survay": Survay,
    "Calculator": calculator
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

