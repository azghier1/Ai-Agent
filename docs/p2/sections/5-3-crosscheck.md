## 5.3 Consistency cross-check

| Check | Result (pass, or what failed) | Fixed in |
|---|---|---|
| K1 Every item in an actor column (4.2) is an attribute in the domain model (5.1) | Failed at first: the domain model drawn for 5.1 had no class for the question, the answer with its source, the course pages a student reads, or practice questions, although UC-01 and UC-04 name them | 5.1: Question, Answer, CourseMaterial and PracticeQuestion added to the class table |
| K2 Every object on a sequence diagram is a domain class or a declared interaction object | Pass: UC-01 uses Student, Course, CourseMaterial, Question, Answer plus AssistantInterface and QuestionAnswerer; UC-02 uses Student, Course, Assignment, Submission plus AssistantInterface and AssignmentOrganizer, all declared in 5.2 | n/a |
| K3 Every message on a sequence diagram corresponds to exactly one scenario-table row | Pass for UC-01 (20 rows, 20 messages) and UC-02 (checked in the review of PR #3) | n/a |
| K4 Every non-trivial step in 5.2 (a) has at least one scenario-table row | Pass: UC-01 steps 2, 4, 6 (rows 2.1 to 6.4) and A1; UC-02 steps 2, 4 and A3 | n/a |
| K5 Every analyzed use case traces to at least one functional requirement | Pass: UC-01 to FR-01, FR-02, FR-03, FR-07; UC-02 to FR-02, FR-04, FR-05, FR-07; UC-04 to FR-08 | n/a |
| K6 The last messages of each diagram make the use case postcondition true | Pass: UC-01 ends with 6.4 showing the source (or A1.2 explaining no answer); UC-02 ends with 4.5 confirming the details (or A3.3 explaining the failure) | n/a |
