from googleapiclient.discovery import build
import base64
import json

def apply_custom_policy_tags(data, context):
    print(pubsub_message)
    data = json.loads(pubsub_message)

    project = data.get('project')
    template = 'gs://chuongcentralpractice-security-beam/1.0.0/templates/CentralCustomDataPolicyTags'
    parameters = {
        'dataset': data.get('dataset'),
        'taxonomy_id': data.get('taxonomy_id'),
        'inspect_region': data.get('region'),
        'region': data.get('region'),
        'table': data.get('table')
    }
    job_name = f"apply-custom-policy-tags-{data.get('dataset')}-{data.get('table')}"
    dataflow = build('dataflow', 'v1b3')
    request = dataflow.projects().templates().launch(
        projectId=project,
        gcsPath=template,
        body={
            'jobName': job_name,
            'region': parameters.get('region'),
            'parameters': parameters
        }
    )

    response = request.execute()