*** Settings ***
Documentation     A test suite with a single test for valid login.
Library           RequestsLibrary

*** Test Cases ***
Successful ping
    Create Session  google	http://www.google.com
    ${resp}=  Get Request	google	/
    Should Be Equal As Strings	${resp.status_code}	200
