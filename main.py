import streamlit as st

def Survay():
    per=""
    field=""
    st.sidebar.markdown("# Survay ")
    tab1, tab2 = st.tabs(["Survay", "Recommendation"])
    with tab1:
        st.title(":green[Survay]")
        option=st.selectbox("Choose one course:",("None","Data Science","Linear 1","Probability"))
        ID=st.text_input("Enter ID",help="This input is used as an identifier",placeholder="XXXXXXXXX")
        if st.checkbox("open survay"):
            if option=="None" or len(ID)!=9:
                st.error(":red[The input is wrong]")
                st.stop()
            for i in range(len(ID)):
                if ID[i]>'9' or ID[i]<'0':
                    st.error("ID needs to be just a integers")
                    st.stop()
            st.write("Hello ",ID,",")
            child=st.selectbox("Your status:",("None","I have children","I don't have children"))
            work=st.selectbox("Do you work?",("None","Yes","No"))
            if work=="Yes":
                per=st.selectbox("job percentage",("None","1-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100"))
                field=st.selectbox("job field",("None","hi-tech-development","hi-tech-QA","Cyber","Other"))
            studing=st.selectbox("Number of weekly study hours you spent during the semester",("None","0-3","3-6","6-9","9-12","12-15","15+"))
            relevant=st.selectbox("Is the course organized and relevant?",("None","1","2","3","4","5"))
            take=st.selectbox("Can this course be taken with other courses?",("None","Yes","No"))
            if take=="Yes":
                list_course=st.multiselect("mark all the courses that you think this course can be combined with",["Data Science","Linear 1","Probability"],[option])
                if option not in list_course:
                    st.error("You can't delete your course from the list")
                    st.stop()
            if st.button("send"):
                if child=="None" or work=="None" or per=="None" or  field=="None" or studing=="None" or relevant=="None" or  take=="None":
                    st.error("You need to fullfil all the questions")
                    st.stop()
                else:
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
                per = st.selectbox("job percentage", ("None", "1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"))
                field = st.selectbox("job field", ("None", "hi-tech-development", "hi-tech-QA", "Cyber", "Other"))

                if st.checkbox("open graph of weekly study hours a student spent in the course according to your choises"):
                    if child != "None" and work == "None" and per == "None" and field == "None": #just parents
                        if st.checkbox("open graph that exhibit the number of weekly hours spent by students who testified that they are parents in this course"):
                            pass
                    elif child == "None" and work == "None" and per == "None" and field == "None":#mistake
                        st.error("You need to fullfil one filter at list")
                        st.stop()
                    else:#all other combinations
                        pass
            else:
                if st.checkbox("open graph of weekly study hours a student spent in the course"):
                    pass












page_names_to_funcs = {
    "Survay": Survay
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

