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
        tab1, tab2 = st.tabs(["Recommendation", "I'm a teacher"])
        histoPath = r"C:\Users\user\OneDrive\שולחן העבודה\main.py\privateTeachers.csv"
        histoDate = pd.read_csv(histoPath)

        with tab1:
            st.title("Recommendation :")
            selected = st.selectbox("Course", ("Algorithms","Linear 1","Intro to Java", "Data Science"))
            teachers = histoDate.loc[histoDate.Courses.str.contains(selected),
            ["Name", "Phone", "When", "Where", "Student", "OP Student"]]
            st.write(teachers)

        with tab2:
            studentOP = "No"
            d_by_ID = {}
            st.title("Please enter your details :")
            ID = st.text_input("Enter your ID number :", help="This input is used as an identifier",
                               placeholder="XXXXXXXXX")
            if st.checkbox("open details"):
                if not check_input(ID, 9):
                    st.warning("You must insert a valid ID number")
                    st.stop()
                teacherName = st.text_input("Enter your name : ")
                phone = st.text_input("Enter your phone number :", placeholder="XXXXXXXXXX")
                option = st.multiselect("Choose the relevant courses :", ("None", "Data Science", "Linear 1", "Probability"))
                time = st.multiselect("When do you prefer to teach ?", ("Morning", "Afternoon", "Evening"))

                value = ["Jerusalem District", "Northern District", "Haifa District", "Central District",
                         "Tel Aviv District", "Southern District"]
                area = st.selectbox("Cost per hour : ",value)

                place = st.multiselect("Choose where you perfer to teach :", ("Zoom", "My home", "Student's home"))
                value1 = ["0-100", "100-200", "200-300"]
                cost = st.selectbox("Cost per hour : ",value1)
                if st.button("send"):
                    if not check_input(phone, 10):
                        st.error("You must enter a valid phone number")
                        st.stop()
                    if teacherName == "" or len(option) == 0 or len(place) == 0 or\
                            len(time) == 0 or len(area) == 0 or len(cost) == 0:
                        st.error("Some information is missing")
                        st.stop()

                    st.write("Saved! Thank You!")


def main():
    registerTeacher()


if __name__ == '__main__':
    main()
