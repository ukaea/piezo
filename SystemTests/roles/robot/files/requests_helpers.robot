###############################################################################
*** Settings ***
Documentation     Helper methods for sending HTTP requests.

###############################################################################
*** Keywords ***
Json Header
    ${header}=  Create Dictionary   Content-Type=application/json
    [return]    ${header}

Confirm 200 Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   200
