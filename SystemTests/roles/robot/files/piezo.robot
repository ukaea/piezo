###############################################################################
*** Settings ***
Documentation     A test suite with for the Piezo system.
Resource          k8s_methods.robot
Resource          requests_helpers.robot
Resource          s3methods.robot

###############################################################################
*** Test Cases ***
Grafana Is Up
    ${response}=  Get Request From Route   /
    Confirm 200 Response  ${response}

Prometheus Is Up
    ${response}=  Get Request From Route   /prometheus/graph
    Confirm 200 Response  ${response}

Piezo Heartbeat Is Up
    ${response}=  Get Request From Route   /piezo/
    Confirm 200 Response  ${response}

Get Logs Of Non Job Returns 200 Response
    ${body}=    Create Dictionary   driver_name=dummy   namespace=default
    ${response}=  Get Request With Json Body   /piezo/getlogs    ${body}
    Confirm 200 Response  ${response}

Delete Job Of Non Job Returns 200 Response
    ${body}=    Create Dictionary   job_name=dummy   namespace=default
    ${response}=  Delete Request With Json Body   /piezo/deletejob    ${body}
    Confirm 200 Response  ${response}

Word Count Example
    # Check that the correct files are in S3
    File Should Exist In S3 Bucket    kubernetes   wordcount.py
    File Should Exist In S3 Bucket    kubernetes   big.txt
    File Should Not Exist In S3 Bucket    kubernetes  output
    # TODO
