import requests
from kubernetes.client.rest import ApiException


url = 'http://localhost:8001/apis/sparkoperator.k8s.io/v1alpha1/namespaces/default/sparkapplications/spark-pi'

def delete():
    try: 
        api_response = requests.delete(url)
        print(api_response.status_code)
        print(api_response.content)
        return api_response.content
    except ApiException as e:
        print("Exception: %s\n" % e)
