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
App last updated 25 September 2018  
Readme last updated 9 October 2018

# Operation

- Place the required, updated data files into the same directory as the app file
- Run the Student_Database_Preparer.py file from within Spyder or from the command
line
- Select the desired function from the menu
- Provide the names for any required files or press enter to open the Open file 
dialog.

# Functions

## Prepare ADV Course Assessment Table Data

Prepares the upload file for updating the ResultsADV table in the Student 
Database.

### Required Files

- Course Assessment Data File
- Assessments File
- Enrolment IDs File

### Notes

Function needs rewriting.

## Prepare Course Attendance Table Data

Prepares the upload file for updating the Course Attendance table in the Student Database.

### Required Files

- Course Attendance Data File
- Course IDs File
- Student_Course File
- Dates File

## Prepare Course Tutors Table Data

Prepares the upload file for updating the Course Tutors table in the Student Database.

### Required Files

- Course Tutors Data File
- Course IDs File
- Course Tutors File
- Tutor IDs File

## Prepare Courses Table Data

Prepares the upload file for updating the Courses table in the Student Database.

### Required Files

- Course IDs File
- Courses Data File

## Prepare Enrolments Table Data

Prepares the upload file for updating the Enrolments table in the Student Database.

### Required Files

- Course IDs File
- Enrolment Data Sheet
- Student IDs File
- Tutor IDs File

## Prepare Extensions Table Data

Prepares the upload file for updating the Extensions table in the Student 
Database.

### Required Files

- Enrolment Codes File
- Extension Codes File
- Extensions Data

## Prepare Graduates Table Data

Prepares the upload file for updating the Graduates table in the Student 
Database.

### Required Files

- Enrolment Codes File
- Graduate Data
- Graduates Current File

## Prepare Students Table Data

Prepares the upload file for updating the Students table in the Student Database.

### Required Files

- Combined Data File
- Course IDs File
- Enrolment Data Sheet
- Student IDs File

## Prepare Tutors Table

Prepares the upload file for updating the Tutors table in the Student Database.

### Required Files

- Tutor Data File
- Tutor IDs File

## Prepare Workshop Attendance Table Data

Prepares the upload file for updating the Workshop Attendance table in the Student 
Database.

### Required Files

- Students_Workshop File
- Workshop Attendance Data File
- Workshop IDs File

## Prepare Workshop Tutors Table Data

Prepares the upload file for updating the Workshop Tutors table in the Student Database.

### Required Files

- Tutor IDs File
- Workshop IDs File
- Workshop Tutors Data File
- Workshop Tutors File

## Prepare Workshops Table Data

Prepares the upload file for updating the Workshops table in the Student Database.

### Required Files

- Workshops Data File
- Workshop IDs File

# Files used

## Assessments File

### File Name

\<Course_Code>_assessments.csv where <Course_Code> is the base course code
e.g. ADV.

### Contents

Assessment name for each assessment in the base course.

### Structure

CSV file with the full name of each assessment on the ADV course.

### Source

Base Course setup.

## Combined Data File

### File Name

cdf.csv

### Contents

Raw enrolment form data downloaded from the website with the Student ID added
in the first column. Contains students that need to be added to the Student
Database.

### Structure

CSV file with Student ID column followed by each column of data from the Enrolment
form.

### Source

Exported from the forms section of the Fit College website Admin area (Enrolment
Form).

## Course Assessment Data File

### File Name

\<TBC>

### Contents

\<TBC>

### Structure

\<TBC>

### Source

\<TBC>

## Course Attendance Data File

### File Name

<course_code>.csv where <course_code> is the full course code, e.g. ADV-PT-003.

### Contents

Course attendance data to be added to the Student Database.

### Structure

CSV file with Course Attendance data. Student ID, First Name, Last Name, Each day
of the course. Each day should be the date of the session.

### Source

Course Attendance tab of the Enrolments Google sheet.

## Course Tutors Data File

### File Name

ct.csv

### Contents

Course tutor details for course tutors to be added to the Student Database.

### Structure

CSV file with Course Tutors data. Columns are the same as the Course Tutors table
in the Student Database.

### Source

Course Tutors tab of the Enrolments Google sheet.

## Course IDs File

### File Name

Course_IDs.csv

### Contents

Course code and Course Date for courses currently in the Courses table of the 
Student Database. 

### Structure

CSV file with Course Code and the Course Date information.

### Source

Courses tab of the Enrolments Google sheet - Course Code and Form Text columns.

## Course Tutors File

### File Name

Course_Tutors.csv

### Contents

Course tutor details for course tutors currently in the Course Tutors table in
the Student Database.

### Structure

Course Tutors data. Columns are the same as the Course Tutors table
in the Student Database.

### Source

Course Tutors table in the Student Database.

## Courses Data File

### File Name

coursedata.csv

### Contents

Course details for courses to be added to the Student Database.

### Structure

CSV file with Course data. Columns are the same as the Courses table in the
Student Database.

### Source

Courses tab of the Enrolments Google sheet.

## Dates File

### File Name

dates.csv

### Contents

Dates that the course was held on.

### Structure

CSV file with the dates that the course was hekd on (one date for each day of the
course).

### Source

Course Attendance Data File.

## Enrolment Codes File

### File Name

Enrolment_Codes.csv

### Contents

Enrolment ID and Student ID combinations for students that have been enrolled in a
course.

### Structure

CSV file with the Enrolment ID and Student ID combinations for students that have
been enrolled in a course.

### Source

Enrolments table of the Student Database.

## Enrolment IDs File

### File Name

enrolment_ids.csv

### Contents

Enrolment details of each student in the Enrolments table of the Student Database.

### Structure

CSV file with the Enrolment ID, Student ID, NameGIven, NameSurname, CoursePK,
Status and Tutor.

### Source

qryEnrolmentDetailsAll query in the Student Database.

## Enrolment Data Sheet

### File Name

es.csv

### Contents

Enrolment sheet data from the Enrolments tab of the Enrolments Google sheet. 
Contains students that need to be added to the Student Database.

### Structure

CSV file with the enrolment data for the student from the Enrolments tab of the
Enrolments Google sheet.

### Source

Enrolments tab of the Enrolments Google sheet.

## Extensions Data File

### File Name

extensions.csv

### Contents

Extensions data for students to be added to the Extensions table in the Student
Database.

### Structure

CSV file with the Extensions data. Columns are Student ID, Name, Enrolment Code,
Extension Length, Acceptance Date, New Expiry Date.

### Source

Extensions sheet of the Enrolments Google sheet.

## Extension Codes File

### File Name

Extension_Codes.csv

### Contents

Enrolment ID and Acceptance Date combinations for students that are currently in
the Extensions table of the Student Database.

### Structure

CSV file with the Enrolment ID and Acceptance Date combinations for students that
have been granted an extension.

### Source

Extensions table of the Student Database.

## Graduate Data File

### File Name

grads.csv

### Contents

Graduate data for students to be added to the Graduates table in the Student
Database.

### Structure

CSV file with the Graduate data. Columns are Student ID, Name, Enrolment Code,
Graudation Date, Certificate Number.

### Source

Graduates sheet of the Enrolments Google sheet.

## Graduates Current File

### File Name

Graduates_Current.csv

### Contents

Graduate data for students currently in the Graduates table in the Student
Database.

### Structure

CSV file with the GraduatePK and EnrolmentFK combinations for students in the
Graduates table of the Student Database.

### Source

Graduates table of the Student Database.

## Student_Course File

### File Name

scc.csv

### Contents

Student ID and Course ID combinations for all students in the Enrolments table of
the Student Database.

### Structure

CSV file with the Student ID and Course ID for all students enrolled in a course.

### Source

Enrolments table of the Student Database.

## Students_Workshop File

### File Name

swc.csv

### Contents

Student ID and Workshop ID combinations for all students in the Workshop Attendance
table of the Student Database.

### Structure

CSV file with the Student ID and Workshop ID for all students that have attended 
a workshop.

### Source

Workshop Attendance table of the Student Database.

## Student IDs File

### File Name

Student_IDs.csv

### Contents

Student ID, First Name and Last Name of each student in the Student Database.

### Structure

CSV file with the Student ID, NameGIven and NameSurname for each student in the
Student Database.

### Source

Students table of the Student Database.

## Tutor Data File

### File Name

tutors.csv

### Contents

Tutor details for tutors to be added to the Student Database.

### Structure

CSV file with the Tutor ID, First Name, Last Name, Email, Phone Number.

### Source

Tutors sheet of the Enrolments Google sheet.

## Tutor IDs File

### File Name

Tutor_IDs.csv

### Contents

Tutor details for tutors currently in the Student Database (Tutors table).

### Structure

CSV file with the Tutor ID, First Name, Last Name.

### Source

Tutors table of the Student Database.

## Workshop Attendance Data File

### File Name

workshopatt.csv

### Contents

Workshop attendance data to be added to the Student Database.

### Structure

CSV file with Workshop Attendance data. Workshop ID, Student ID, First Name, 
Last Name.

### Source

Workshop Attendance tab of the Enrolments Google sheet.

## Workshop Tutors Data File

### File Name

Workshop_Tutors.csv

### Contents

Workshop tutor details for workshop tutors to be added to the Student Database.

### Structure

CSV file with Workshop Tutors data. Columns are the same as the Workshop Tutors
table in the Student Database.

### Source

Workshop Tutors tab of the Enrolments Google sheet.

## Workshop IDs File

### File Name

Workshop_IDs.csv

### Contents

Workshop details for workshops currently in the Student Database (Workshops table).

### Structure

CSV file with Workshop Code and the Workshop Name information.

### Source

Workshops table in the Student Database.

## Workshop_Tutors File

### File Name

Workshop_Tutors.csv

### Contents

Workshop tutor details for workshop tutors currently in the Student Database.

### Structure

CSV file with Workshop Tutors data. Columns are the same as the Workshop Tutors
table in the Student Database.

### Source

Workshop Tutors table in the Student Database.

## Workshops Data File

### File Name

workshops.csv

### Contents

Workshop details for workshops to be added to the Student Database.

### Structure

CSV file with Workshops data. Columns are the same as the Workshops table in the
Student Database.

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

- ADV Results processing

## Required development steps

- Add loading and loaded statements to Extensions and Graduates processing

## Future additions

- Add function: Filter students by course (e.g. for withdrawn students in Results
functions)
- Add function: Extract students not already in Results table (e.g. for Results
functions)
- Add function: Compare Results_update students with Master_Results file
- Group warnings by warning type e.g. Mobile number
- Add progress status to processes that take a while to run
- Graduates certificate - strip and remove any spaces
- Course attendance - take course code and use in save file name rather than time
- Remove warning for Course date missing for ADV-ON-001
- Update file names (e.g. replace Tutor_IDs.csv with Tutor IDs) in print statements
