###############################################################################
*** Settings ***
Documentation     A test suite with a single test for valid login.
Library           RequestsLibrary
Resource          resource.robot

###############################################################################
*** Test Cases ***
Successful ping
    Create Session  google	http://www.google.com
    Confirm 200 Response	google

