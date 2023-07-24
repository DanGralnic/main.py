import pandas
import streamlit


def histoDatePage():
    histoPath = r"C:\Users\gabiy\PycharmProjects\main.py\histoData.csv"
    histoDate = pandas.read_csv(histoPath)
    # Open Data file

    selected = streamlit.selectbox("Course", sorted(set(histoDate["Course"])))
    # Create selectbox, include only courses that exists in histoData.csv (histoDate["Course"])
    # Display each course once (set)
    # Show courses in a sorted manner (sorted)

    streamlit.info("If a wanted course doesn't appear, it means we don't have any data for it")
    streamlit.write("")
    # User info

    chart_data = histoDate.loc[histoDate["Course"] == selected, ["Semester", "Final Grade"]] \
        .sort_values(["Semester", "Final Grade"], ascending=False)
    # Filter selected course, keep only "Semester" and "Final Grade" columns
    # Sort values by semester (primary) and final grade (secondary) in descending order
    # I.e. most recent semester first, then highest grade first

    max_semester = chart_data.iloc[0, 0]
    # Get the most recent semester, it will be in the sorted DateFrame at the first line, and first column

    streamlit.bar_chart(chart_data.loc[chart_data["Semester"] == max_semester, "Final Grade"].value_counts(), y="count")
    # Create a bar chart containing for the most recent semester, keep only "Final Grade" Column
    # Count each Grade occurrences
    # Y axis is the count

    streamlit.line_chart(chart_data.sort_values(["Semester", "Final Grade"]).groupby("Semester")["Final Grade"].mean(),
                         y="Final Grade")
    # Create a line chart, group the DataFrame by semesters, for each semester find its mean grade
    # Y axis is the final grade


def main():
    histoDatePage()


if __name__ == '__main__':
    main()
