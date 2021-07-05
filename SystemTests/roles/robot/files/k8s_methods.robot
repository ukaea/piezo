###############################################################################
*** Settings ***
Documentation     Test resources for interacting with the Kubernetes cluster.
Library           RequestsLibrary
Resource          requests_helpers.robot

###############################################################################
*** Variables ***
${K8S_ENDPOINT}     http://host-172-16-113-146.nubes.stfc.ac.uk:31856
${JOB_FINISH_CHECK_STEPS}   180
${JOB_FINISH_CHECK_INTERVAL}    1 seconds

###############################################################################
*** Keywords ***
Delete Request With Json Body
    [Arguments]   ${route}    ${body}
    ${headers}=   Json Header
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Delete Request   k8s   ${route}    headers=${headers}    json=${body}
    [return]  ${response}

Delete Spark Job
    [Arguments]   ${job_name}
    ${body}=    Create Dictionary   job_name=${job_name}
    ${response}=  Delete Request With Json Body   /piezo/deletejob    ${body}
    [return]    ${response}

Get Driver Name
    [Arguments]   ${job_name}
    ${driver_name}=   Catenate    SEPARATOR=    ${job_name}   -driver
    [return]    ${driver_name}

Get Logs For Spark Job
    [Arguments]   ${job_name}
    ${body}=    Create Dictionary   job_name=${job_name}
    ${response}=  Get Request With Json Body   /piezo/getlogs    ${body}
    [return]    ${response}

Get List Of Spark Jobs
    [Arguments]     ${body}
    ${response}=    Get Request With Json Body    /piezo/getjobs    ${body}
    [return]    ${response}

Get Request From Route
    [Arguments]   ${route}
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Get Request   k8s   ${route}
    [return]  ${response}

Get Request With Json Body
    [Arguments]   ${route}    ${body}
    ${headers}=   Json Header
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Get Request   k8s   ${route}    headers=${headers}    json=${body}
    [return]  ${response}

Get Status Of Spark Job
    [Arguments]   ${job_name}
    ${body}=    Create Dictionary   job_name=${job_name}
    ${response}=  Get Request With Json Body   /piezo/jobstatus    ${body}
    [return]    ${response}

Output Files Of Spark Job
    [Arguments]   ${job_name}
    ${body}=    Create Dictionary   job_name=${job_name}
    ${response}=  Get Request With Json Body   /piezo/outputfiles    ${body}
    [return]    ${response.json()["data"]["files"]}

Post Request With Json Body
    [Arguments]   ${route}    ${body}
    ${headers}=   Json Header
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Post Request   k8s   ${route}    headers=${headers}    json=${body}
    [return]  ${response}

Submit SparkPi Job
    [Arguments]   ${job_name}
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Python   python_version=2    path_to_main_app_file=s3a://kubernetes/inputs/pi.py    label=systemTest
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Submit SparkPi Job With Optional Parameters
    [Arguments]   ${job_name}
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Python   python_version=2    path_to_main_app_file=s3a://kubernetes/inputs/pi.py    driver_cores=0.2    driver_core_limit=1.4     driver_memory=1024m     executors=2      executor_cores=1     executor_core_limit=4.5     executor_memory=1024m      label=systemTest
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Submit SparkPi Python3 Job
    [Arguments]   ${job_name}
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Python   python_version=3    path_to_main_app_file=s3a://kubernetes/inputs/pi.py    label=systemTest
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Submit SparkPi Job With Label
    [Arguments]   ${job_name}   ${label}
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Python   python_version=2    path_to_main_app_file=s3a://kubernetes/inputs/pi.py    label=${label}
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Submit InputArgs Job With Arguments
    [Arguments]   ${job_name}
    ${arguments}=   Create List   A B C
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Python   python_version=2    path_to_main_app_file=s3a://kubernetes/inputs/input_args.py      label=systemTest      arguments=${arguments}
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Submit Wordcount On Minio Job
    [Arguments]   ${job_name}
    ${arguments}=   Create List   s3a://kubernetes/inputs/big.txt
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Python   python_version=2    path_to_main_app_file=s3a://kubernetes/inputs/wordcount.py     label=systemTest      arguments=${arguments}    executors=4
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Tidy jobs
    ${headers}=   Json Header
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Post Request   k8s   /piezo/tidyjobs    headers=${headers}
    [return]  ${response}


Wait For Spark Job To Finish
    [Arguments]    ${job_name}
    :For    ${i}    IN RANGE   0    ${JOB_FINISH_CHECK_STEPS}
    \   Sleep     ${JOB_FINISH_CHECK_INTERVAL}
    \   ${response}=   Get Status Of Spark Job   ${job_name}
    \   ${message}=  Get Response Job Status     ${response}
    \   ${finished}=    Set Variable If     '${message}'=='COMPLETED'   ${True}     ${False}
    \   Exit For Loop If    ${finished}
    [return]    ${finished}

Write Logs To Storage
    [arguments]   ${job_name}
    ${submitbody}=    Create Dictionary   job_name=${job_name}
    ${response}=    Post Request With Json Body   /piezo/writelogs    ${submitbody}
    [return]  ${response}
