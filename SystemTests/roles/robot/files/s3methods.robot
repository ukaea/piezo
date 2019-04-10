###############################################################################
*** Settings ***
Documentation     Test resources for interacting with the S3 storage.
Library           OperatingSystem

###############################################################################
*** Variables ***
${MINIO_ROOT}     /opt/minio/data/
${S3_LOCATION}    http://172.16.113.201:9000/

###############################################################################
*** Keywords ***
Directory Should Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${dir-path}
    Directory Should Exist   ${MINIO_ROOT}/${bucket-name}/${dir-path}

Directory Should Not Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${dir-path}
    Directory Should Not Exist   ${MINIO_ROOT}/${bucket-name}/${dir-path}

Directory Should Not Be Empty In S3 Bucket
    [Arguments]   ${bucket-name}    ${dir-path}
    Directory Should Not Be Empty     ${MINIO_ROOT}/${bucket-name}/${dir-path}

Download From Temporary URL
    [Arguments]   ${url}
    ${file_loc}=    Set Variable    ~/temp.txt
    ${rc}   ${output}=    Run And Return Rc And Output    wget -O ${file_loc} "${url}"
    ${file}=    Get File    ${file_loc}
    Remove File   ${file_loc}
    [return]    ${file}

File Should Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${file-path}
    File Should Exist   ${MINIO_ROOT}/${bucket-name}/${file-path}

File Should Not Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${file-path}
    File Should Not Exist   ${MINIO_ROOT}/${bucket-name}/${file-path}

Get File In S3 Bucket
    [Arguments]   ${bucket-name}    ${file-path}
    ${file}=    Get File   ${MINIO_ROOT}/${bucket-name}/${file-path}
    [return]    ${file}
