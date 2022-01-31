# Allowed Python packages: pyhtml, jinja2, matplotlib or any standard Python3 package.
import sys
import pyhtml as h
import matplotlib.pyplot as plt

# first and second parameters
fparam, sparam = sys.argv[1], int(sys.argv[2])

# Try and except block just to run on my machine as well
data = open("data.csv", "r")

# Reading the first line of headings
a = data.readline()

# Creating empty lists to store data
student_id = []
course_id = []
marks = []

# While loop to add data to respective lists
while a != "":
    a = data.readline()
    if a != "":
        l = a.split(",")
        student_id.append(int(l[0]))
        course_id.append(int(l[1]))
        marks.append(int(l[2]))


# Function error to generate Something went wrong output file
def error():
    t = h.html(
        h.head(
            h.title("Something Went Wrong")
        ),
        h.body(
            h.h1("Wrong Inputs"),
            h.div("Something went wrong")
        )
    )
    html_out = t.render()
    output = open("output.html", "w")
    output.write(html_out)
    output.close()
    return


# Function Student_detail to generate the student's data output file
def Student_detail(stu_id):
    # Empty list for storing the items to be inserted in the table
    rows = []
    tot_marks = 0

    # for loop to add tuples of data to the rows list and find total marks
    for i in range(len(student_id)):
        if student_id[i] == stu_id:
            rows.append((student_id[i], course_id[i], marks[i]))
            tot_marks += marks[i]

    # If the list is empty, that means parameters are wrong. Terminate with error output file
    if len(rows) == 0:
        return error()

    t = h.html(
        h.head(
            h.title("Student Data")
        ),
        h.body(
            h.h1("Student Details"),
            h.table(border="2px")(
                h.tr(
                    h.th("Student id"),
                    h.th("Course id"),
                    h.th("Marks")
                ),
                (h.tr(
                    h.td(cell) for cell in row
                ) for row in rows),
                h.tr(
                    h.td(colspan="2", style="text-align:center")("Total Marks"),
                    h.td(tot_marks)
                )
            )
        )
    )

    html_out = t.render()
    output = open("output.html", "w")
    output.write(html_out)
    output.close()
    return


# Function Course_detail to generate the course's data output file
def Course_detail(crs_id):
    # Empty list for storing the marks scored by student in the course
    rows = []
    tot_marks = 0

    # for loop to insert marks in the "rows" list ((helps with max &avg marks and the plot))
    for i in range(len(course_id)):
        if course_id[i] == crs_id:
            rows.append(marks[i])
            tot_marks += marks[i]

    # If the list is empty, that means parameters are wrong. Terminate with error output file
    if len(rows) == 0:
        return error()

    # Calculating the max and avg marks
    max_marks = max(rows)
    avg_marks = tot_marks / (len(rows))

    # Generating the figure using matplotlib and saving it with "histogram.png" name
    plt.hist(rows)
    plt.savefig("histogram.png")

    t = h.html(
        h.head(
            h.title("Course Data")
        ),
        h.body(
            h.h1("Course Details"),
            h.table(border="2px")(
                h.tr(
                    h.th("Average Marks"),
                    h.th("Maximum Marks")
                ),
                h.tr(
                    h.td(str(avg_marks)),
                    h.td(str(max_marks))
                )
            ),
            h.img(src="histogram.png")

        )
    )

    html_out = t.render()
    output = open("output.html", "w")
    output.write(html_out)
    output.close()
    return


# fparam, sparam = sys.argv[1], sys.argv[2]
# Calling functions according to the parameters
if fparam == "-s":
    Student_detail(sparam)
elif fparam == "-c":
    Course_detail(sparam)
else:
    error()
