import pandas
import streamlit
import altair


def histoDatePage():
    with streamlit.container():
        histoPath = "https://raw.githubusercontent.com/DanGralnic/main.py/master/histoData.csv"
        histoDate = pandas.read_csv(histoPath)
        # Open Data file

        selected = streamlit.selectbox("Course", sorted(set(histoDate["Course"])))
        # Create selectbox, include only courses that exists in histoData.csv (histoDate["Course"])
        # Display each course once (set), Show courses in a sorted manner (sorted)

        streamlit.info("If a wanted course or semester doesn't appear, it means we don't have any data for it")
        streamlit.write("")
        # User info

        chart_data = histoDate.loc[histoDate["Course"] == selected, ["Semester", "Final Grade"]] \
            .sort_values(["Semester", "Final Grade"], ascending=False)
        # Filter selected course, keep only "Semester" and "Final Grade" columns
        # Sort values by semester (primary) and final grade (secondary) in descending order
        # I.e. most recent semester first, then highest grade first

        selected_semester = chart_data.iloc[0, 0]
        # Get the most recent semester, it will be in the sorted DateFrame at the first line, and first column

        selected_semester = streamlit.select_slider("Show semesters:", options=sorted(set(chart_data["Semester"])))
        # Get user desired semester

        streamlit.write(f"Showing histogram from {selected_semester} semester")

        streamlit.bar_chart(chart_data.loc[chart_data["Semester"] == selected_semester, "Final Grade"].value_counts(),
                            y="count")
        # Create a bar chart containing for the most recent semester, keep only "Final Grade" Column
        # Count each Grade occurrences
        # Y axis is the count

        streamlit.write(f"Showing average grade since {chart_data.iloc[len(chart_data)-1, 0]} up to {chart_data.iloc[0, 0]}")

        streamlit.line_chart(
            chart_data.sort_values(["Semester", "Final Grade"]).groupby("Semester")["Final Grade"].mean(),
            y="Final Grade")
        # Create a line chart, group the DataFrame by semesters, for each semester find its mean grade
        # Y axis is the final grade


def predictedAVG():
    with streamlit.container():
        histoPath = r"C:\Users\gabiy\PycharmProjects\main.py\histoData.csv"
        histoDate = pandas.read_csv(histoPath)
        # Open Data file

        selectedCourses = streamlit.multiselect("Course", sorted(set(histoDate["Course"])))
        # Create multiselect, include only courses that exists in histoData.csv (histoDate["Course"])
        # Display each course once (set), Show courses in a sorted manner (sorted)

        selectedSemesters = streamlit.multiselect("Semester", sorted(set(histoDate.loc[histoDate[
            "Course"].isin(selectedCourses)]["Semester"]), reverse=True))
        # Create multiselect, include only semesters that exists in histoData.csv (histoDate["Semester"])
        # Filter only semesters that exists in the selected courses
        # Display each semester once (set), Show semester in a sorted manner (sorted)

        chart_data = histoDate.loc[histoDate["Course"].isin(selectedCourses) & histoDate["Semester"].isin(
            selectedSemesters), ["Course", "Semester", "Final Grade"]]
        # Filter only the selected cources and semesters

        data = chart_data.groupby(["Course", "Semester"]).mean().reset_index()
        # Group the rows first by course then by semester, find the mean grade and re-index the table

        chart = altair.Chart(data, title="Predicted Average Grade").mark_bar().encode(
            x=altair.X("Semester:O", title=None, ),
            y="Final Grade:Q",
            color="Course:N",
            xOffset="Course:N"
        )
        # Build the Altair Table

        streamlit.altair_chart(chart, use_container_width=True)
        # Display the chart


def loadPage():
    histoTab, predictedAVGTab = streamlit.tabs(["Histograms", "Predicted average"])
    with histoTab:
        histoDatePage()
    with predictedAVGTab:
        predictedAVG()


def main():
    loadPage()


if __name__ == '__main__':
    main()
