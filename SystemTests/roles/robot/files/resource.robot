###############################################################################
*** Settings ***
Documentation     Commonly used test resources
Library           RequestsLibrary

###############################################################################
*** Variables ***
${API_ENDPOINT}     http://www.google.com

###############################################################################
*** Keywords ***
Confirm 200 Response
    [Arguments]     ${session}
    ${resp}=  Get Request	${session}	/
    Should Be Equal As Strings	${resp.status_code}	200
