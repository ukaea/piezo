###############################################################################
*** Settings ***
Documentation     Test resources for interacting with the S3 storage.
Library           OperatingSystem

###############################################################################
*** Variables ***
${MINIO_ROOT}     /opt/minio/data/

###############################################################################
*** Keywords ***
File Should Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${file-path}
    File Should Exist   ${MINIO_ROOT}/${bucket-name}/${file-path}

File Should Not Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${file-path}
    File Should Not Exist   ${MINIO_ROOT}/${bucket-name}/${file-path}

Directory Should Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${dir-path}
    Directory Should Exist   ${MINIO_ROOT}/${bucket-name}/${dir-path}

Directory Should Not Exist In S3 Bucket
    [Arguments]   ${bucket-name}    ${dir-path}
    Directory Should Not Exist   ${MINIO_ROOT}/${bucket-name}/${dir-path}

Directory Should Not Be Empty In S3 Bucket
    [Arguments]   ${bucket-name}    ${dir-path}
    Directory Should Not Be Empty     ${MINIO_ROOT}/${bucket-name}/${dir-path}
