###############################################################################
*** Settings ***
Documentation     Test resources for interacting with the Kubernetes cluster.
Library           RequestsLibrary

################################################################################################
*** Variables ***
${K8S_ENDPOINT}     http://host-172-16-113-146.nubes.stfc.ac.uk:31924

################################################################################################
*** Keywords ***
Check K8s Route Returns 200 Response
    [Arguments]   ${route}
    Create Session    k8s   ${K8S_ENDPOINT}
    ${resp}=  Get Request   k8s   ${route}
    Should Be Equal As Strings    ${resp.status_code}   200
