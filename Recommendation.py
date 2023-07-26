import streamlit as st
import pandas as pd
import os


def check_input(phone, digitNumber):
        if phone == "":
            return False
        if len(phone) != digitNumber:
            return False
        for i in range(len(phone)):
            if phone[i] < '0' or phone[i] > '9':
                st.error("contain charater that not integer")
                return False
        return True

def registerTeacher():
        tab1, tab2 = st.tabs(["Add me to teachers list", "Recommendation"])
        str_name = "privateTeachers.parquet"
        with tab1:
            studentOP = "---"
            list_course = []
            df_prev = pd.DataFrame()
            d_by_ID = {}
            st.title("Please enter your details :")
            teacherName = st.text_input("Enter your name : ")
            ID = st.text_input("Enter your ID number :",help="This input is used as an identifier", placeholder="XXXXXXXXX")
            phone = st.text_input("Enter your phone number :", placeholder="XXXXXXXXXX")
            option = st.multiselect("Choose the relevant courses :", ("None", "Data Science", "Linear 1", "Probability"))
            place = st.multiselect("Choose where you perfer to teach :", ("Zoom", "My home", "Student's home"))
            time = st.multiselect("Choose when you perfer to teach :", ("Morning", "Afternoon", "Evening"))
            value = ["No", "Yes"]
            student = st.selectbox("Are you a student?",value,index = value.index(d_by_ID.get("student", "No")))
            if student == "Yes":
                value2 = ["No", "Yes"]
                studentOP = st.selectbox("Are you an Open University student?", value2,
                                        index = value2.index(d_by_ID.get("student", "No")))
            if st.button("send"):
                if not check_input(phone, 10):
                    st.error("You must enter a valid phone number")
                    st.stop()
                if not check_input(ID, 9):
                    st.error("You must enter a valid ID number")
                    st.stop()
                if teacherName == "" or len(option) == 0 or len(place) == 0 or len(time) == 0:
                    st.error("Some information is missing")
                    st.stop()
                st.write("Saved! Thank You!")


def main():
    registerTeacher()


if __name__ == '__main__':
    main()
