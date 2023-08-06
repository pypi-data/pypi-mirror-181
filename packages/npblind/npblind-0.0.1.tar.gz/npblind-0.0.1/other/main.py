from CentralPolicyTagsPackage.CentralPolicyTags import CentralPolicyTagsClient
import json
import os
import base64
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/Admin.json"


def apply_custom_policy_tags(data, context):
    pubsub_message = base64.b64decode(data['data']).decode('utf-8')
    print(pubsub_message)
    data = json.loads(pubsub_message)
    project = data.get('project')
    dataset = data.get('dataset')
    central_policy_tags_client = CentralPolicyTagsClient(
        project=project,
        region=data.get('region'),
        inspect_ds=dataset,
        result_ds=dataset,
        result_table='inspect_policy_tags_result'
    )
    policy_tags = central_policy_tags_client.get_all_policy_tags_from_taxonomy(taxonomy_id=data.get('taxonomy_id'))
    tag_requests = []
    table = data.get('table')
    custom_tags = data.get('custom_tags')
    for column in list(custom_tags.keys()):
        tag_requests.append((column, policy_tags.get(custom_tags.get(column))))
    central_policy_tags_client.tag_table(table_id=f'{project}.{dataset}.{table}',
                                         policy_tag_requests=tag_requests,
                                         bigquery_region=data.get('region'))


