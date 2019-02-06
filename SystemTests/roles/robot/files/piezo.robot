###############################################################################
*** Settings ***
Documentation     A test suite with a single test for valid login.
Library           RequestsLibrary
Resource          resource.robot
resource          s3methods.robot

###############################################################################
*** Test Cases ***
Successful ping
    Create Session  google	http://www.google.com
    Confirm 200 Response	google

S3 File Exists
    File Should Exist In S3 Bucket    test-bucket   test1.txt
    File Should Not Exist In S3 Bucket    non-bucket   test1.txt
    File Should Not Exist In S3 Bucket    test-bucket   no-file.txt
