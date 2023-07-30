import streamlit as st
import pandas as pd
import os

def Convert(string):
    li = list(string.split(", "))
    return li

def check_input(number, digitNumber):
        if number == "":
            return False
        if len(number) != digitNumber:
            return False
        for i in range(len(number)):
            if number[i] < '0' or number[i] > '9':
                st.error("contain charater that not integer")
                return False
        return True

def phone_check(phone):
    if not check_input(phone, 10):
        return False
    if phone[0:2] != "05":
        return False
    return True


def registerTeacher():
        tab1, tab2 = st.tabs(["Recommendation", "I'm a teacher"])
        str_name = "teachers_file.parquet"

        with tab1:
            st.title("Recommendation :")
            selected = st.selectbox("Course", ("Introduction to Computer Science in Java", "OOP", "Data Science", "Linear 1", "Linear 2", "Probability"))
            if os.path.exists(str_name):
                df_prev = pd.read_parquet(str_name)
                if not df_prev.empty:
                    df1 = df_prev.loc[df_prev['Courses'].str.contains(selected), ["Name", "Phone", "Area", "Where", "When", "Cost per Hour"]]
                    st.table(df1)
            else:
                st.info("We couldn't find a private teacher for this course")

        with tab2:
            d_by_ID = {}
            st.title("Please enter your details :")
            ID = st.text_input("Enter your ID number :", help="This input is used as an identifier",
                               placeholder="XXXXXXXXX")

            if st.checkbox("open details"):
                if not check_input(ID, 9):
                    st.error("You must insert a valid ID number")
                    st.stop()
                if os.path.exists(str_name):
                    df_prev = pd.read_parquet(str_name)
                    if not df_prev.empty:
                        df1 = df_prev[(df_prev['ID'] == ID)]
                        if not df1.empty:
                            d_by_ID = dict(df1.iloc[0])

                teacher_name = st.text_input("Enter your name : ", d_by_ID.get("Name", ""))
                phone = st.text_input("Enter your phone number :", d_by_ID.get("Phone", ""))
                list_course = st.multiselect("Choose the relevant courses :", ("Introduction to Computer Science in Java", "OOP", "Data Science", "Linear 1", "Linear 2", "Probability"),
                                            Convert(d_by_ID.get("Courses", "Data Science")))
                string_course = ', '.join(list_course)

                list_time = st.multiselect("When do you prefer to teach ?", ("Morning", "Afternoon", "Evening"),
                                            Convert(d_by_ID.get("When", "Morning")))
                string_time = ', '.join(list_time)


                value = ["Jerusalem District", "Northern District", "Haifa District", "Central District",
                         "Tel Aviv District", "Southern District"]
                area = st.selectbox("Cost per hour : ", value, index=value.index(d_by_ID.get("Area", "Central District")))
                list_place = st.multiselect("Choose where you perfer to teach :", ("Zoom", "My home", "Student's home"),
                                            Convert(d_by_ID.get("Where", "Student's home")))
                string_place = ', '.join(list_place)

                value1 = ["0-100", "100-200", "200-300"]
                cost = st.selectbox("Cost per hour : ", value1, index=value1.index(d_by_ID.get("Cost per Hour", "100-200")))

                if st.button("send"):
                    if not phone_check(phone):
                        st.error("You must enter a valid phone number")
                        st.stop()
                    if teacher_name == "" or len(list_course) == 0 or len(list_place) == 0 or\
                            len(list_time) == 0 or len(area) == 0 or len(cost) == 0:
                        st.error("Some information is missing")
                        st.stop()
                    new_row = {
                        "ID": ID,
                        "Name": teacher_name,
                        "Phone": phone,
                        "Courses": string_course,
                        "Area": area,
                        "Where": string_place,
                        "When": string_time,
                        "Cost per Hour": cost
                    }

                    if not os.path.exists(str_name):
                        df = pd.DataFrame([new_row])
                        df.to_parquet(str_name)
                    else:
                        df1 = pd.DataFrame([new_row])
                        df = pd.concat([df_prev, df1], ignore_index=True)
                        df = df.drop_duplicates(subset=['ID'], keep='last')
                        df.to_parquet(str_name)
                    st.write("Saved! Thank You!")


def main():
    registerTeacher()


if __name__ == '__main__':
    main()
