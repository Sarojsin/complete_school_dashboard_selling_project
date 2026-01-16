## Update the following routes:
student_test_list (renamed from 
student_tests
): Fetch available tests using TestRepository.get_available_tests_for_student.
student_take_test
: Fetch test details and ensure student is enrolled. Initialize or resume 
TestSubmission
.
student_test_result
: Fetch submission results and calculate statistics.
[NEW] student_submit_test: Handle POST request for test submission to /student/tests/{test_id}/submit, grade questions using TestService.grade_submission, and redirect to the result page.
[Frontend] Template Updates
[MODIFY] 
student/test_list.html
Display a list of available (upcoming, ongoing, and completed) tests.
Show test status (Start, Resume, Viewed Results).
[MODIFY] 
student/take_test.html
Implement question-by-question navigation or a single-page layout.
Add a countdown timer using JavaScript.
Handle auto-submission when timer expires.
[MODIFY] 
student/test_result.html
Show total score, percentage, and time taken.
Display a breakdown of correct/incorrect answers.
