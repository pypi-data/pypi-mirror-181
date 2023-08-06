import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from CentralPolicyTagsPackage.users_options import UserOptions
from CentralPolicyTagsPackage.CentralPolicyTags import ApplyCustomDataset
import json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/GCP_REPLATOFORMMING.json"


def run():
    # Get user definition
    with open('column_mapping.json', 'r') as f:
        custom_tags = json.loads(f.read())
        f.close()
    base_option = PipelineOptions()
    project = base_option.view_as(GoogleCloudOptions).project
    user_options = base_option.view_as(UserOptions)
    job_name = 'custom-policy-tags-application'
    options = {
        'runner': 'DirectRunner',
        'region': 'asia-southeast1',
        'project': project,
        'machine_type': 'n1-standard-4',
        'autoscaling_algorithm': 'THROUGHPUT_BASED',
        'setup_file': './setup.py',
        'max_num_workers': 10,
        'job_name': job_name,
        'temp_location': 'gs://{}-security-beam/tmp/'.format(project),
        'staging_location': 'gs://{}-security-beam/staging/'.format(project),
        'save_main_session': True
    }

    if base_option.view_as(UserOptions).version != 'NO_TEMPLATE':
        options['template_location'] = 'gs://{}-security-beam/{}/templates/CentralCustomDataPolicyTags'.format(
            project,
            base_option.view_as(UserOptions).version
        )

    pipeline_option = PipelineOptions(flags=[], **options)
    with beam.Pipeline(options=pipeline_option) as p:
        start = (p | "init" >> beam.Create([1])
                 | "Applying and tagging" >> beam.ParDo(ApplyCustomDataset(), user_options.dataset, project,
                                                        user_options.inspect_region,
                                                        user_options.table,
                                                        user_options.taxonomy_id,
                                                        custom_tags
                                                        ))


if __name__ == '__main__':
    print("START THE POLICY TAGS CUSTOM ON A TABLE")
    run()
