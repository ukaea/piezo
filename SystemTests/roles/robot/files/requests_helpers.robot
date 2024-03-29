###############################################################################
*** Settings ***
Documentation     Helper methods for sending HTTP requests.

###############################################################################
*** Keywords ***
Confirm Conflict Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   409

Confirm Not Found Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   404

Confirm Bad Input Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   400

Confirm Ok Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   200

Get Response Data
  [Arguments]   ${response}
  [return]    ${response.json()["data"]}

Get Response Data Message
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["message"]}

Get Response Job Status
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["job_status"]}

Get Response Spark Jobs
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["spark_jobs"]}

Get Response Tidied Jobs
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["jobs_tidied"]}

Get Response Skipped Jobs
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["jobs_skipped"]}

Get Response Job Name
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["job_name"]}

Get Response Spark UI
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["spark_ui"]}

Json Header
  ${header}=  Create Dictionary   Content-Type=application/json
  [return]    ${header}
