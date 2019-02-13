###############################################################################
*** Settings ***
Documentation     A test suite with for the Piezo system.
Resource          s3methods.robot
Resource          k8s_methods.robot

###############################################################################
*** Test Cases ***
Grafana Is Up
    Check K8s Route Returns 200 Response    /

Prometheus Is Up
    Check K8s Route Returns 200 Response    /prometheus/graph

Word Count Example
    # Check that the correct files are in S3
    File Should Exist In S3 Bucket    kubernetes   wordcount.py
    File Should Exist In S3 Bucket    kubernetes   big.txt
    File Should Not Exist In S3 Bucket    kubernetes  output
    # TODO
