 ## 1. Administrative Assignment
The school administration is responsible for assigning students to their respective courses. This is usually done during the admission process or at the start of a new semester.

Where it happens: In the Authority Dashboard under Courses -> Course Details, there is an "Assign Student" feature.
The Logic: When the Admin assigns a student to a course, a record is created in the 
CourseEnrollment
 database table, linking the student ID to the course ID.
2. Automatic Grade-Level Access
As a backup, if a student isn't manually enrolled in a specific course yet:

The system automatically shows them study materials (Notes/Videos) that match their Grade Level (e.g., Grade 10).
This ensures new students don't see a blank page while waiting for their official enrollment to be processed.
3. Student View
Once enrolled, the student will see the courses listed on their Courses page (/student/courses), and all relevant notes, videos, and assignments for those subjects will automatically populate their dashboard.

Would you like me to implement a "Self-Enrollment" or "Course Request" button for students so they can choose their own subjects?