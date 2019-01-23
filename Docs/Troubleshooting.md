# Possible issues

## My application won't run
The best way to debug your spark application is to check the logs of the spark driver pod by using `kubectl logs {name of driver pod}`. If this includes a line saying "local jar {name of jar} doesn't exist", check you have first have completed the required steps before running the application so that the data files are in the correct locations on the required nodes.

If you get a warning including `java.lang.ClassNotFoundException` it is likely your image being run in your spark pods is missing some of the requirments for your spark job. This can be fixed by adding these requirments over the top of your docker image (see setting up a docker registory and building custom docker images). 

## My persietent volume won't delete and hangs
Check if the application still exists that the persistent volume is connected to, if so the application must be deleted first before the persistent volume can be deleted

## I deleted my spark pods but when I try to run the application again it says it still exists
You need to delete the actual application not just the pods by using the command `kubectl delete sparkapplications {name of application}`. This will automatically delete the pods in the process