# Overview

The Student Database Preparer App takes in raw student data and prepares
it for uploading to the Student Database. It cleans the data and ensures that
it is compatible with the database.

## Inputs

The app takes in csv files containing raw data to be uploaded to the Student
Database.

## Outputs

The app outputs txt files that can be uploaded into the Student Database to
update the required tables.

## Version

Version Number 1.0  
Last updated 25 September 2018

# Operation

- Place the required, updated data files into the same directory as the app file
- Run the Student_Database_Preparer.py file from within Spyder or from the command
line
- Select the desired function from the menu
- Provide the names for any required files or press enter to open the Open file 
dialog.

# Functions

## Prepare Students Table Data

Prepares the upload file for updating the Students table in the Student Database.

### Required Files

- Combined Data File
- Course_IDs.csv
- Enrolment Data Sheet
- Student_IDs.csv

## Prepare Tutors Table

Prepares the upload file for updating the Tutors table in the Student Database.

### Required Files

- Tutor Data File
- Tutor_IDs.csv

## Prepare Courses Table Data

Prepares the upload file for updating the Courses table in the Student Database.

### Required Files

- Course_IDs.csv
- Courses Data File

## Prepare Workshops Table Data

Prepares the upload file for updating the Workshops table in the Student Database.

### Required Files

- Workshops Data File
- Workshops_IDs.csv

## Prepare Course Tutors Table Data

Prepares the upload file for updating the Course Tutors table in the Student Database.

### Required Files

- Course Tutors Data File
- Course_IDs.csv
- Course_Tutors.csv
- Tutor_IDs.csv

## Prepare Workshop Tutors Table Data

Prepares the upload file for updating the Workshop Tutors table in the Student Database.

### Required Files

- Tutor_IDs.csv
- Workshop_IDs.csv
- Workshop Tutors Data File
- Workshop_Tutors.csv

## Prepare Enrolments Table Data

Prepares the upload file for updating the Enrolments table in the Student Database.

### Required Files

- Course_Ids.csv
- Enrolment Data Sheet
- Student_IDs.csv
- Tutor_IDs.csv

## Prepare Course Attendance Table Data

Prepares the upload file for updating the Course Attendance table in the Student Database.

### Required Files

- Course Attendance Data File
- Course_IDs.csv
- Student_Course File
- dates.csv

## Prepare Workshop Attendance Table Data

Prepares the upload file for updating the Workshop Attendance table in the Student 
Database.

### Required Files

- Student-Workshop File
- Workshop Attendance Data File
- Workshop_IDs.csv

## Prepare Graduates Table Data

Prepares the upload file for updating the Graduates table in the Student 
Database.

### Required Files

- Enrolment_Codes.csv
- Graduate Data
- Graduates_Current.csv

## Prepare Extensions Table Data

Prepares the upload file for updating the Extensions table in the Student 
Database.

### Required Files

- Enrolment_Codes.csv
- Extension_Codes.csv
- Extensions Data

## Prepare ADV Course Assessment Table Data

Prepares the upload file for updating the ResultsADV table in the Student 
Database.

### Required Files

- Course Assessment Data File
- adv_assessments
- enrolment_ids.csv

# Files used

## adv_assessments.csv

### Structure

CSV file with the full name of each assessment on the ADV course.

### Contents

Assessment name for each assessment in the ADV course.

### Source

ADV Course.
## Combined Data File

### Structure

CSV file with Student ID column followed by each column of data from the Enrolment
form.

### Contents

Raw enrolment form data downloaded from the website with the Student ID added
in the first column. Contains students that need to be added to the Student
Database.

### Source

Exported from the forms section of the Fit College website Admin area (Enrolment
Form).

## Course Assessment Data File

### Structure

\<TBC>

### Contents

\<TBC>

### Source

\<TBC>

## Course Attendance Data File

### Structure

CSV file with Course Attendance data. Student ID, First Name, Last Name, Each day
of the course. Each day should be the date of the session.

### Contents

Course attendance data to be added to the Student Database.

### Source

Course Attendance tab of the Enrolments Google sheet.

## Course Tutors Data File

### Structure

CSV file with Course Tutors data. Columns are the same as the Course Tutors table
in the Student Database.

### Contents

Course tutor details for course tutors to be added to the Student Database.

### Source

Course Tutors tab of the Enrolments Google sheet.

## Course_IDs.csv

### Structure

CSV file with Course Code and the Course Date information.

### Contents

Course code and Course Date for courses currently in the Courses table of the 
Student Database. 

### Source

Courses tab of the Enrolments Google sheet - Course Code and Form Text columns.

## Course_Tutors.csv

### Structure

Course Tutors data. Columns are the same as the Course Tutors table
in the Student Database.

### Contents

Course tutor details for course tutors currently in the Course Tutors table in
the Student Database.

### Source

Course Tutors table in the Student Database.

## Courses Data File

### Structure

CSV file with Course data. Columns are the same as the Courses table in the
Student Database.

### Contents

Course details for courses to be added to the Student Database.

### Source

Courses tab of the Enrolments Google sheet.

## Dates File

### Structure

CSV file with the dates that the course was hekd on (one date for each day of the
course).

### Contents

Dates that the course was held on.

### Source

Course Attendance Data File.

## Enrolment_Codes.csv

### Structure

CSV file with the Enrolment ID and Student ID combinations for students that have
been enrolled in a course.

### Contents

Enrolment ID and Student ID combinations for students that have been enrolled in a
course.

### Source

Enrolments table of the Student Database.

## enrolment_ids.csv

### Structure

CSV file with the Enrolment ID, Student ID, NameGIven, NameSurname, CoursePK,
Status and Tutor.

### Contents

Enrolment details of each student in the Enrolments table of the Student Database.

### Source

qryEnrolmentDetailsAll query in the Student Database.

## Enrolment Data Sheet

### Structure

CSV file with the enrolment data for the student from the Enrolments tab of the
Enrolments Google sheet.

### Contents

Enrolment sheet data from the Enrolments tab of the Enrolments Google sheet. 
Contains students that need to be added to the Student Database.

### Source

Enrolments tab of the Enrolments Google sheet.

## Extensions Data File

### Structure

CSV file with the Extensions data. Columns are Student ID, Name, Enrolment Code,
Extension Length, Acceptance Date, New Expiry Date.

### Contents

Extensions data for students to be added to the Extensions table in the Student
Database.

### Source

Extensions sheet of the Enrolments Google sheet.

## Extension_Codes.csv

### Structure

CSV file with the Enrolment ID and Acceptance Date combinations for students that
have been granted an extension.

### Contents

Enrolment ID and Acceptance Date combinations for students that are currently in
the Extensions table of the Student Databse.

### Source

Extensions table of the Student Database.

## Graduate Data File

### Structure

CSV file with the Graduate data. Columns are Student ID, Name, Enrolment Code,
Graudation Date, Certificate Number.

### Contents

Graduate data for students to be added to the Graduates table in the Student
Database.

### Source

Graduates sheet of the Enrolments Google sheet.

## Graduates_Current.csv

### Structure

CSV file with the GraduatePK and EnrolmentFK combinations for students in the
Graduates table of the Student Database.

### Contents

Graduate data for students currently in the Graduates table in the Student
Database.

### Source

Graduates table of the Student Database.

## Student-Course File

### Structure

CSV file with the Student ID and Course ID for all students enrolled in a course.

### Contents

Student ID and Course ID combinations for all students in the Enrolments table of
the Student Database.

### Source

Enrolments table of the Student Database.

## Student-Workshop File

### Structure

CSV file with the Student ID and Workshop ID for all students that have attended 
a workshop.

### Contents

Student ID and Workshop ID combinations for all students in the Workshop Attendance
table of the Student Database.

### Source

Workshop Attendance table of the Student Database.

## Student_IDs.csv

### Structure

CSV file with the Student ID, NameGIven and NameSurname for each student in the
Student Database.

### Contents

Student ID, First Name and Last Name of each student in the Student Databse.

### Source

Students table of the Student Database.

## Tutor Data File

### Structure

CSV file with the Tutor ID, First Name, Last Name, Email, Phone Number.

### Contents

Tutor details for tutors to be added to the Student Database.

### Source

Tutors sheet of the Enrolments Google sheet.

## Tutor_IDs.csv

### Structure

CSV file with the Tutor ID, First Name, Last Name.

### Contents

Tutor details for tutors currently in the Student Database (Tutors table).

### Source

Tutors table of the Student Database.

## Workshop Attendance Data File

### Structure

CSV file with Workshop Attendance data. Workshop ID, Student ID, First Name, 
Last Name.

### Contents

Workshop attendance data to be added to the Student Database.

### Source

Workshop Attendance tab of the Enrolments Google sheet.

## Workshop Tutors Data File

### Structure

CSV file with Workshop Tutors data. Columns are the same as the Workshop Tutors
table in the Student Database.

### Contents

Workshop tutor details for workshop tutors to be added to the Student Database.

### Source

Workshop Tutors tab of the Enrolments Google sheet.

## Workshop_IDs.csv

### Structure

CSV file with Workshop Code and the Workshop Name information.

### Contents

Workshop details for workshops currently in the Student Database (Workshops table).

### Source

Workshops table in the Student Database.

## Workshop_Tutors.csv

### Structure

CSV file with Workshop Tutors data. Columns are the same as the Workshop Tutors
table in the Student Database.

### Contents

Workshop tutor details for workshop tutors currently in the Student Database.

### Source

Workshop Tutors table in the Student Database.

## Workshops Data File

### Structure

CSV file with Workshops data. Columns are the same as the Workshops table in the
Student Database.

### Contents

Workshop details for workshops to be added to the Student Database.

### Source

Workshops tab of the Enrolments Google sheet.

# Dependencies

The following third-party libraries are imported and therefore are required for
the app to run:

- admintools from custtools
- databasetools from custtools
- datetools from custtools
- filetools from custtools

# Development

## Known bugs

- Process results - if file name is changed the original file name is saved.
- ADV Processing - additional comma added at end of output

## Items to fix

- Get updated file name when processing results
- Remove final comma from output of ADV processing

## Current development step

- ADVResults processing

## Required development steps

- Add loading and loaded statements to Extensions and Graduates processing

## Future additions

- Group warnings by warning type e.g. Mobile number
- Add progress status to processes that take a while to run
- Graduates certificate - strip and remove any spaces
- Course attendance - take course code and use in save file name rather than time
- Remove warning for Course date missing for ADV-ON-001
