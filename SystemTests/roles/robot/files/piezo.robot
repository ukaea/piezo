###############################################################################
*** Settings ***
Documentation     A test suite with for the Piezo system.
Library           Collections
Library           String
Resource          general_methods.robot
Resource          k8s_methods.robot
Resource          requests_helpers.robot
Resource          s3methods.robot

###############################################################################
*** Test Cases ***

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

Submitting Incorrect Argument Keys Are Caught In Same Error
    ${submitbody}=    Create Dictionary    language=test      label=systemTest
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    Confirm Bad Input Response    ${response}
    ${error}=   Get Response Data     ${response}
    Should Be One Line Containing String   ${error}   Missing required input \"name\"
    Should Be One Line Containing String   ${error}   Missing required input \"name\"
    Should Be One Line Containing String   ${error}   Missing required input \"path_to_main_app_file\"
    Should Be One Line Containing String   ${error}   Unsupported language \"test\"

Submitting Multiple Incorrect Argument Values Are Caught In Same error
    ${submitbody}=    Create Dictionary    name=test-job    language=Scala    executors=15    executor_memory=200m      driver_cores=5      main_class=org.apache.spark.examples.SparkPi    path_to_main_app_file=local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar    label=systemTest
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    Confirm Bad Input Response    ${response}
    ${error}=   Get Response Data     ${response}
    Should Be Equal As Strings    ${error}    The following errors were found:\n\"executors\" input must be in range [1, 10]\n\"executor_memory\" input must be in range [512m, 4096m]\n\"driver_cores\" input must be in range [0.1, 1]\n

Submit Spark Pi Job Returns Ok Response
    ${response}=    Submit SparkPi Job    spark-pi
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    Should Match Regexp   ${job_name}   spark-pi-[a-z0-9]{5}
    ${message}=   Get Response Data Message   ${response}
    Should Be Equal As Strings    ${message}    Job driver created successfully

Submit Two Jobs With Same Name Returns Ok Responses
    ${response1}=   Submit SparkPi Job    twin-job
    ${response2}=   Submit SparkPi Job    twin-job
    Confirm Ok Response  ${response1}
    Confirm Ok Response  ${response2}

Submit Job With 29 Character Name Runs Successfully
    ${response}=    Submit SparkPi Job    abcdefghijklmnopqrstuvwxyzabc
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True      ${finished}

Submit Job With 30 Character Name Fails
    ${response}=    Submit SparkPi Job    abcdefghijklmnopqrstuvwxyzabcd
    Confirm Bad Input Response  ${response}
    ${error}=   Get Response Data     ${response}
    Should Be Equal As Strings    ${error}    The following errors were found:\n\"name\" input must obey naming convention: see https://github.com/ukaea/piezo/wiki/WebAppUserGuide#submit-a-job\n

Can Run Python3 Jobs
    ${response}=    Submit SparkPi Python3 Job    spark-pi-py3
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    Should Match Regexp   ${job_name}   spark-pi-py3-[a-z0-9]{5}
    ${message}=   Get Response Data Message   ${response}
    Should Be Equal As Strings    ${message}    Job driver created successfully
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True      ${finished}

Submit Input Args Job With Arguments Returns Ok Response
    ${response}=    Submit InputArgs Job With Arguments   input-args-test
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    Should Match Regexp   ${job_name}   input-args-test-[a-z0-9]{5}
    ${message}=   Get Response Data Message   ${response}
    Should Be Equal As Strings    ${message}    Job driver created successfully

Can Get Logs Of Submitted Spark Job
    ${job_name}=     Set Variable   spark-pi
    ${response}=    Submit SparkPi Job    ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True      ${finished}
    ${response}=  Get Logs For Spark Job    ${job_name}
    ${joblog}=    Get Response Data Message   ${response}
    ${pi_lines}=    Get Lines Containing String   ${joblog}   Pi is roughly 3
    ${num_pi_lines}=    Get Line Count    ${pi_lines}
    Should Be Equal As Integers   ${num_pi_lines}   1

Arguments Have Been Read And Appear In Logs
    ${job_name}=  Set Variable  input-args-test
    ${response}=    Submit InputArgs Job With Arguments   ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    Confirm Ok Response  ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True      ${finished}
    ${logresponse}=  Get Logs For Spark Job    ${job_name}
    ${joblog}=  Get Response Data Message   ${logresponse}
    Should Be One Line Containing String   ${joblog}   First argument is s3a://kubernetes/outputs/${job_name}/
    Should Be One Line Containing String   ${joblog}   Second argument is A
    Should Be One Line Containing String   ${joblog}   Third argument is B
    Should Be One Line Containing String   ${joblog}   Fourth argument is C

Can Delete Submitted Spark Job
    ${job_name}=    Set Variable        spark-pi
    ${response}=    Submit SparkPi Job   ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True    ${finished}
    ${response}=  Delete Spark Job    ${job_name}
    Confirm Ok Response   ${response}

Can Get Status Of Submitted Spark Job
    ${job_name}=     Set Variable       spark-pi
    ${response}=    Submit SparkPi Job    ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    Sleep       5 seconds
    ${response}=  Get Status Of Spark Job   ${job_name}
    Confirm Ok Response     ${response}

Status Of Job Immediately After Submission is Unknown
    ${job_name}=     Set Variable       spark-pi
    ${response}=    Submit SparkPi Job    ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    ${response}=  Get Status Of Spark Job   ${job_name}
    Confirm Ok Response     ${response}
    ${data}=    Get Response Data     ${response}
    Dictionary Should Contain Item    ${data}   message     Job status for "${job_name}"
    Dictionary Should Contain Item    ${data}   job_status    UNKNOWN
    Dictionary Should Contain Item    ${data}   submission_attempts     UNKNOWN
    Dictionary Should Contain Item    ${data}   last_submitted      UNKNOWN
    Dictionary Should Contain Item    ${data}   terminated      UNKNOWN
    Dictionary Should Contain Item    ${data}   error_messages      UNKNOWN
    ${created}=     Get From Dictionary    ${data}   created
    Should Match Regexp   ${created}   [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z

Status Of Job Contains All Information
    ${job_name}=     Set Variable       spark-pi
    ${response}=    Submit SparkPi Job    ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    Sleep   10 seconds
    ${response}=  Get Status Of Spark Job   ${job_name}
    Confirm Ok Response     ${response}
    ${data}=    Get Response Data     ${response}
    Dictionary Should Contain Key   ${data}   message
    Dictionary Should Contain Key   ${data}   job_status
    Dictionary Should Contain Key   ${data}   created
    Dictionary Should Contain Key   ${data}   submission_attempts
    Dictionary Should Contain Key   ${data}   last_submitted
    Dictionary Should Contain Key   ${data}   terminated
    Dictionary Should Contain Key   ${data}   error_messages

Job Can Use Data And Code On S3 And Write Back Results
    ${job_name}=    Set Variable      wordcount
    ${response}=    Submit Wordcount On Minio Job   ${job_name}
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True    ${finished}
    Directory Should Exist In S3 Bucket   kubernetes    outputs/${job_name}
    Directory Should Not Be Empty In S3 bucket  kubernetes    outputs/${job_name}
    File Should Exist In S3 Bucket    kubernetes      outputs/${job_name}/_SUCCESS

Get List Of SparkApplications Includes Submitted Jobs
    ${response1}=   Submit SparkPi Job    job1
    ${response2}=   Submit SparkPi Job    job2
    ${response3}=   Submit SparkPi Job    job3
    Confirm Ok Response  ${response1}
    Confirm Ok Response  ${response2}
    Confirm Ok Response  ${response3}
    ${job_name_1}=    Get Response Job Name   ${response1}
    ${job_name_2}=    Get Response Job Name   ${response2}
    ${job_name_3}=    Get Response Job Name   ${response3}
    Sleep     5 seconds
    ${body}=    Create Dictionary
    ${request_response}=    Get List Of Spark Jobs    ${body}
    Confirm Ok Response     ${request_response}
    ${jobs}=    Get Response Spark Jobs     ${request_response}
    Dictionary Should Contain Key   ${jobs}   ${job_name_1}
    Dictionary Should Contain Key   ${jobs}   ${job_name_2}
    Dictionary Should Contain Key   ${jobs}   ${job_name_3}

Get List Of SparkApplications Filters By Label
    ${response1}=   Submit SparkPi Job With Label    job1    test-label
    ${response2}=   Submit SparkPi Job   job2
    ${response3}=   Submit SparkPi Job With Label    job3    test-label
    Confirm Ok Response  ${response1}
    Confirm Ok Response  ${response2}
    Confirm Ok Response  ${response3}
    ${job_name_1}=    Get Response Job Name   ${response1}
    ${job_name_2}=    Get Response Job Name   ${response2}
    ${job_name_3}=    Get Response Job Name   ${response3}
    Sleep     5 seconds
    ${body}=    Create Dictionary   label=test-label
    ${request_response}=    Get List Of Spark Jobs    ${body}
    Confirm Ok Response     ${request_response}
    ${jobs}=    Get Response Spark Jobs     ${request_response}
    Dictionary Should Contain Key   ${jobs}   ${job_name_1}
    Dictionary Should Contain Key   ${jobs}   ${job_name_3}
    Dictionary Should Not Contain Key   ${jobs}   ${job_name_2}

Write Logs Of Completed Jobs Appears In S3
    ${response}=    Submit SparkPi Job    spark-pi
    ${new_job_name}=    Get Response Job Name   ${response}
    Wait For Spark Job To Finish        ${new_job_name}
    Write Logs To Storage   ${new_job_name}
    File Should Exist In S3 Bucket    kubernetes      outputs/${new_job_name}/log.txt
    ${joblog}=    Get File In S3 Bucket    kubernetes      outputs/${new_job_name}/log.txt
    ${pi_lines}=    Get Lines Containing String   ${joblog}   Pi is roughly 3
    ${num_pi_lines}=    Get Line Count    ${pi_lines}
    Should Be Equal As Integers   ${num_pi_lines}   1

Tidy Jobs Does Not Affect Unfinished Jobs
    ${response1}=    Submit SparkPi Job    spark-pi-1
    Submit SparkPi Job    spark-pi-2
    Submit SparkPi Job    spark-pi-3
    Submit SparkPi Job    spark-pi-4
    Submit SparkPi Job    spark-pi-5
    ${new_job_name1}=    Get Response Job Name   ${response1}
    Wait For Spark Job To Finish        ${new_job_name1}
    ${response2}=    Submit SparkPi Job    spark-pi-6
    ${new_job_name2}=    Get Response Job Name   ${response2}
    ${request_response}=    Tidy Jobs
    Confirm Ok Response     ${request_response}
    ${tidied_jobs}=    Get Response Tidied Jobs     ${request_response}
    ${skipped_jobs}=    Get Response Skipped Jobs     ${request_response}
    Dictionary Should Contain Item    ${tidied_jobs}    ${new_job_name1}    COMPLETED
    Dictionary Should Contain Key   ${skipped_jobs}    ${new_job_name2}
    Dictionary Should Not Contain Value   ${skipped_jobs}     COMPLETED
    Dictionary Should Not Contain Value   ${skipped_jobs}     FAILED
    Dictionary Should Not Contain Value    ${tidied_jobs}    RUNNING
    Dictionary Should Not Contain Value    ${tidied_jobs}    PENDING
    Dictionary Should Not Contain Value    ${tidied_jobs}    UNKNOWN
    Dictionary Should Not Contain Value    ${tidied_jobs}    CrashLoopBackOff
    Dictionary Should Not Contain Value    ${tidied_jobs}    SUCCEEDED

Tidy Jobs Writes Logs And Deletes Completed Jobs
    ${response1}=    Submit SparkPi Job    spark-pi-1
    ${new_job_name1}=    Get Response Job Name   ${response1}
    ${response2}=    Submit SparkPi Job    spark-pi-2
    ${new_job_name2}=    Get Response Job Name   ${response2}
    Wait For Spark Job To Finish        ${new_job_name1}
    Wait For Spark Job To Finish        ${new_job_name2}
    ${request_response}=    Tidy Jobs
    Confirm Ok Response     ${request_response}
    ${tidied_jobs}=    Get Response Tidied Jobs     ${request_response}
    Dictionary Should Contain Item    ${tidied_jobs}    ${new_job_name1}    COMPLETED
    Dictionary Should Contain Item    ${tidied_jobs}    ${new_job_name2}    COMPLETED

Output Files Provides Temporary URLs
    ${job_name}=    Set Variable   wordcount-tempurl
    ${response}=    Submit Wordcount On Minio Job   ${job_name}
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}
    Should Be True    ${finished}
    Write Logs To Storage   ${job_name}
    ${output_files}=    Output Files Of Spark Job   ${job_name}
    ${success_file}=    Download From Temporary URL   ${output_files["_SUCCESS"]}
    ${line_count}=    Get Line Count    ${success_file}
    Should Be Equal As Integers   ${line_count}   0
    ${part0_file}=    Download From Temporary URL   ${output_files["part-00000"]}
    ${line_count}=    Get Line Count    ${part0_file}
    Should Be True   ${line_count} > 0
    ${part1_file}=    Download From Temporary URL   ${output_files["part-00001"]}
    ${line_count}=    Get Line Count    ${part1_file}
    Should Be True   ${line_count} > 0
    ${output_files}=    Output Files Of Spark Job   ${job_name}
    ${log_file}=    Download From Temporary URL   ${output_files["log.txt"]}
    ${line_count}=    Get Line Count    ${log_file}
    Should Be True   ${line_count} > 0

Spark UI From Submission Is Accessible While A Spark Job Is Running
    ${response}=    Submit Wordcount On Minio Job With Spark UI   wordcount-ui-job
    Confirm Ok Response  ${response}
    ${spark_ui}=    Get Response Spark UI   ${response}
    Sleep   20 seconds
    Create Session    spark_ui    ${spark_ui}
    ${ui_response}=   Get Request    spark_ui   /
    Confirm Ok Response   ${ui_response}

Spark UI From Submission Is Not Returned When Not Requested
    ${response}=    Submit Wordcount On Minio Job   wordcount-ui-job
    Confirm Ok Response  ${response}
    Dictionary Should Not Contain Key   ${response}   spark_ui

Spark UI From Status Is Accessible While A Spark Job Is Running
    ${response}=    Submit Wordcount On Minio Job With Spark UI   wordcount-ui-job
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    Sleep   20 seconds
    ${response}=  Get Status Of Spark Job    ${job_name}
    ${spark_ui}=    Get Response Spark UI   ${response}
    Create Session    spark_ui    ${spark_ui}
    ${ui_response}=   Get Request    spark_ui   /
    Confirm Ok Response   ${ui_response}

Spark UI From Status Is Not Available If Not Requested On Submission
    ${response}=    Submit Wordcount On Minio Job   wordcount-ui-job
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    Sleep   20 seconds
    ${response}=  Get Status Of Spark Job    ${job_name}
    ${spark_ui}=    Get Response Spark UI   ${response}
    Should Be Equal As Strings    ${spark_ui}    Unavailable
