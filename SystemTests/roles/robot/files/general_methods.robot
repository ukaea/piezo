###############################################################################
*** Settings ***
Documentation     General resources for system tests

###############################################################################
*** Keywords ***
Should Be One Line Containing String
    [Arguments]   ${file}   ${string}
    ${lines}=   Get Lines Containing String   ${file}   ${string}
    ${num_lines}=   Get Line Count    ${lines}
    Should Be Equal As Integers   ${num_lines}   1
