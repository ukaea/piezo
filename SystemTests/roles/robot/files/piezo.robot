###############################################################################
*** Settings ***
Documentation     A test suite with for the Piezo system.
Library           Collections
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
    ${data}=    Get Response Data   ${response}
    ${expected}=    Create Dictionary   running=true
    Dictionaries Should Be Equal    ${data}   ${expected}

Get Logs Of Non Job Returns Not Found Response
    ${response}=  Get Logs For Spark Job    dummy
    Confirm Not Found Response  ${response}

Get Status Of Non Job Returns Not Found Response
    ${response}=  Get Status Of Spark Job    dummy
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

Submit GroupByTest Spark Job With Arguments Returns Ok Response
    ${response}=    Submit SparkGroupByTest Job With Arguments   spark-group-by-test-8s2xp
    Confirm Ok Response  ${response}
    ${data}=    Get Response Data   ${response}
    Should Be Equal As Strings    ${data["message"]}    Job driver created successfully
    Should Be Equal As Strings    ${data["driver_name"]}   spark-group-by-test-8s2xp-driver

Can Get Logs Of Submitted Spark Job
    ${job_name}=     Set Variable   spark-pi-fe244
    Submit SparkPi Job    ${job_name}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True      ${finished}
    ${response}=  Get Logs For Spark Job    ${job_name}
    ${joblog}=    Get Response Data Message   ${response}
    ${pi_lines}=    Get Lines Containing String   ${joblog}   Pi is roughly 3
    ${num_pi_lines}=    Get Line Count    ${pi_lines}
    Should Be Equal As Integers   ${num_pi_lines}   1

Arguments Have Been Read And Appear In Logs
    ${job_name}=  Set Variable  spark-group-by-test-3ewc7
    ${response}=    Submit SparkGroupByTest Job With Arguments   ${job_name}
    Confirm Ok Response  ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True      ${finished}
    ${logresponse}=  Get Logs For Spark Job    ${job_name}
    ${joblog}=  Get Response Data Message   ${logresponse}
    ${arg_1_lines}=    Get Lines Containing String   ${joblog}   Adding task set 0.0 with 10 tasks
    ${arg_4_lines}=    Get Lines Containing String   ${joblog}   Adding task set 2.0 with 3 tasks
    ${num_arg_1_lines}=    Get Line Count    ${arg_1_lines}
    ${num_arg_4_lines}=    Get Line Count    ${arg_4_lines}
    Should Be Equal As Integers   ${num_arg_1_lines}   1
    Should Be Equal As Integers   ${num_arg_4_lines}   1

Can Delete Submitted Spark Job
    ${job_name}=    Set Variable        spark-pi-83783
    Submit SparkPi Job   ${job_name}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True    ${finished}
    ${response}=  Delete Spark Job    ${job_name}
    Confirm Ok Response   ${response}

Can Get Status Of Submitted Spark Job
    ${job_name}=     Set Variable       spark-pi-5jk23s
    Submit SparkPi Job    ${job_name}
    Sleep       5 seconds
    ${response}=  Get Status Of Spark Job   ${job_name}
    Confirm Ok Response     ${response}

Job Can Use Data And Code On S3 And Write Back Results
    ${job_name}=    Set Variable      wordcount-9lkw3w
    ${output-folder}=   Set Variable    ${job_name}-output
    Directory Should Not Exist In S3 Bucket   kubernetes    outputs/${output-folder}
    ${response}=    Submit Wordcount On Minio Job   ${job_name}   ${output-folder}
    Confirm Ok Response  ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True    ${finished}
    Directory Should Exist In S3 Bucket   kubernetes    outputs/${output-folder}
    Directory Should Not Be Empty In S3 bucket  kubernetes    outputs/${output-folder}
    File Should Exist In S3 Bucket    kubernetes      outputs/${output-folder}/_SUCCESS
