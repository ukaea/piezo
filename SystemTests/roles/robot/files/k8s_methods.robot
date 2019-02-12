###############################################################################
*** Settings ***
Documentation     Test resources for interacting with the Kubernetes cluster.
Library           RequestsLibrary

################################################################################################
*** Variables ***
${K8S_ENDPOINT}     http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo

################################################################################################
*** Keywords ***
Check k8s Connection
    Create Session    k8s   ${K8S_ENDPOINT}
    ${resp}=  Get Request   k8s   /runexample
    Should Be Equal As Strings    ${resp.status_code}   200
