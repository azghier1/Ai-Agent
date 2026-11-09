# 5 Analysis Models

## 5.1 Domain model

![Figure 5.1 Domain model](../diagrams/P2%205.1%20-%20Domain.drawio.png)

*Figure 5.1 Domain model (conceptual classes, attributes, associations). Diagram by Omor Igiehon; source `docs/p2/diagrams/CE 3354 P2 5.1 - Omor Igiehon.drawio`. The classes marked "added in 5.3" below were found missing by cross-check K1 and are recorded here; the figure will be redrawn to include them in P3.*

| Class | What it represents (one line) | Key attributes | Associations (with multiplicity) |
|---|---|---|---|
| Student | A person enrolled in one or more courses who uses the assistant | name, student ID, email | Student 0..* to 1..* Course (is enrolled in); Student 1 to 0..* Submission (makes); Student 1 to 0..* Question (asks) |
| Instructor | A person who teaches a course and posts its material | name, instructor ID, email | Instructor 1..* to 0..* Course (teaches) |
| Course | A course offering the student can see | course ID, title, description, schedule, syllabus, status | Course 1 to 0..* Assignment (has); Course 1 to 0..* Announcement (has); Course 1 to 0..* CourseMaterial (has) |
| Assignment | A piece of graded work set in a course | title, description (instructions), maximum points, due date (may be empty) | Assignment 1 to 0..* Submission (receives) |
| Submission | One student's attempt at one assignment | title, file type, time submitted, status | Submission 0..1 to 0..1 Grade (is given) |
| Grade | The mark given to a submission | score, maximum, date graded | Grade 0..1 to 1 Submission |
| Announcement | A notice an instructor posts to a course | title, message, date posted | Announcement 0..* to 1 Course |
| CourseMaterial (added in 5.3) | A page, note or syllabus a student can read in a course | title, content | CourseMaterial 0..* to 1 Course; CourseMaterial 0..* to 0..* Answer (supports) |
| Question (added in 5.3) | A question a student asks about a course | text, time asked | Question 0..* to 1 Course (is about); Question 1 to 0..1 Answer (receives) |
| Answer (added in 5.3) | The response to a question, grounded in course material | text, source reference | Answer 0..* to 1..* CourseMaterial (is based on) |
| PracticeQuestion (added in 5.3) | A self-study question generated from course material (UC-04) | text, topic | PracticeQuestion 0..* to 1 Course (is drawn from) |
