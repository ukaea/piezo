###############################################################################
*** Settings ***
Documentation     A test suite with for the Piezo system.
Library           String
Resource          k8s_methods.robot
Resource          requests_helpers.robot
Resource          s3methods.robot

###############################################################################
*** Test Cases ***
Grafana Returns Ok Response
    ${response}=  Get Request From Route   /
    Confirm Ok Response  ${response}

Prometheus Returns Ok Response
    ${response}=  Get Request From Route   /prometheus/graph
    Confirm Ok Response  ${response}

Piezo Heartbeat Returns Ok Response
    ${response}=  Get Request From Route   /piezo/
    Confirm Ok Response  ${response}

Get Logs Of Non Job Returns Not Found Response
    ${response}=  Get Logs From Spark Driver    dummy
    Confirm Not Found Response  ${response}

Delete Job Of Non Job Returns Not Found Response
    ${response}=    Delete Spark Job    dummy
    Confirm Not Found Response  ${response}

Submit Spark Pi Job Returns Ok Response
    ${response}=    Submit SparkPi Job    spark-pi-3f69c
    Confirm Ok Response  ${response}
    ${data}=    Get Response Data   ${response}
    Should Be Equal As Strings    ${data["message"]}    Job driver created successfully
    Should Be Equal As Strings    ${data["driver_name"]}   spark-pi-3f69c-driver

Can Get Logs Of Submitted Spark Job
    ${job_name}=     Set Variable   spark-pi-fe244
    ${driver_name}=   Get Driver Name   ${job_name}
    Submit SparkPi Job    ${job_name}
    Sleep   30 seconds
    ${response}=  Get Logs From Spark Driver    ${driver_name}
    ${joblog}=    Get Response Data Message   ${response}
    ${pi_lines}=    Get Lines Containing String   ${joblog}   Pi is roughly 3.14
    ${num_pi_lines}=    Get Line Count    ${pi_lines}
    Should Be Equal As Strings   ${num_pi_lines}   1

Can Delete Submitted Spark Job
    Submit SparkPi Job    spark-pi-83783
    Sleep   30 seconds
    ${response}=  Delete Spark Job    ${job_name}
    Confirm Ok Response   ${response}
