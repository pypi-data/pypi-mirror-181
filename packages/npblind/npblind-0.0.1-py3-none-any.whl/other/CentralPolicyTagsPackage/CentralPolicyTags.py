from google.cloud import bigquery
from google.cloud import datacatalog_v1beta1
from google.cloud import dlp_v2
from CentralPolicyTagsPackage.template import inspect_template
# import apache_beam as beam
import time
import json

class CentralPolicyTagsClient:
    def __init__(self, project, region, inspect_ds, result_ds, result_table):
        self.project = project
        self.inspect_ds = inspect_ds
        self.result_ds = result_ds
        self.result_table = result_table
        self.region = region
        self.tag_mapping = {'CREDIT_CARD_NUMBER': 'high-sensitive-data'}

    def inspect_dataset_process(self):
        bq_client = bigquery.Client()
        tables = bq_client.list_tables(self.inspect_ds)
        for table in tables:
            print("scanning {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
            if table.table_type == 'TABLE':
                self.inspect_table_process(table_id=table.table_id)
            if table.table_type == 'EXTERNAL':
                self.inspect_table_process(table_id=table.table_id, is_external=True)

    def inspect_table_process(self, table_id, is_external=False):
        if is_external:
            self.create_temp_external_table(table_id)
            self.start_job(f'dataflow_template_tmp_{table_id}')
            self.delete_temp_external_table(table_id)
        else:
            self.start_job(table_id)
        pass

    def start_job(self, table):
        dlp_client = dlp_v2.DlpServiceClient()
        parent = 'projects/' + self.project + '/locations/' + self.region
        request = dlp_v2.CreateDlpJobRequest(parent=parent, inspect_job=inspect_template(
            inspect_project=self.project,
            inspect_dataset=self.inspect_ds,
            table=table,
            result_project=self.project,
            result_dataset=self.result_ds
        ))
        response = dlp_client.create_dlp_job(request=request)
        job_status = 'JobState.PENDING'
        while job_status != 'JobState.DONE':
            request = dlp_v2.GetDlpJobRequest(
                name=response.name
            )
            time.sleep(10)
            job_status = str(dlp_client.get_dlp_job(request=request).state)
            print(job_status)
        print("finish inspecting ")

    def create_temp_external_table(self, table_id):
        bq_client = bigquery.Client()
        query_txt = f"""
        CREATE OR REPLACE TABLE
          `{self.inspect_ds}.dataflow_template_tmp_{table_id}` AS
        SELECT
          *
        FROM
          `{self.inspect_ds}.{table_id}`
        LIMIT
        1000"""
        results = bq_client.query(query=query_txt).result()
        print(results)

    def delete_temp_external_table(self, table_id):
        bq_client = bigquery.Client()
        bq_client.delete_table(f'{self.project}.{self.inspect_ds}.dataflow_template_tmp_{table_id}', not_found_ok=True)

    def apply_policy_tags(self, taxonomy_id):
        policy_tags = self.get_all_policy_tags_from_taxonomy(taxonomy_id=taxonomy_id
                                                             )
        query_txt = """
        SELECT
          DISTINCT *
        FROM (
          SELECT
            location.content_locations[SAFE_OFFSET(0)].record_location.record_key.big_query_key.table_reference.table_id,
            location.content_locations[SAFE_OFFSET(0)].record_location.field_id.name column_name,
            info_type.name sensitive_type
          FROM
            `{}.{}.dataflow_template_tmp_dataflow_inspect_job_result`
          WHERE
            likelihood = 'VERY_LIKELY')
        """.format(self.project, self.result_ds)
        bq_client = bigquery.Client()
        query_job = bq_client.query(query_txt)
        results = query_job.result()
        for row in results:
            table_id = row.table_id.replace('dataflow_template_tmp_', '')
            self.tag_table(
                table_id=f'{self.project}.{self.inspect_ds}.{table_id}',
                policy_tag_requests=[(row.column_name,
                                      policy_tags.get(self.tag_mapping.get(row.sensitive_type),
                                                      policy_tags.get('personal-data')))],
                bigquery_region=self.region
            )

    def get_all_policy_tags_from_taxonomy(self,
                                          taxonomy_id):
        ptm_client = datacatalog_v1beta1.PolicyTagManagerClient()
        request = datacatalog_v1beta1.ListPolicyTagsRequest(
            parent=taxonomy_id
        )
        page_result = ptm_client.list_policy_tags(request=request)
        policy_tags = {}
        for response in page_result:
            policy_tags[response.display_name] = response.name
        return policy_tags

    def tag_table(self, table_id, policy_tag_requests, bigquery_region):
        print("tag_request ", policy_tag_requests)
        bq_client = bigquery.Client(location=bigquery_region)
        table = bq_client.get_table(table_id)
        schema = table.schema
        new_schema = []
        for field in schema:
            field_match = False
            for column, policy_tag_name in policy_tag_requests:
                if field.name == column:
                    policy = bigquery.schema.PolicyTagList(names=[policy_tag_name, ])
                    new_schema.append(
                        bigquery.schema.SchemaField(field.name, field.field_type, field.mode, policy_tags=policy))
                    field_match = True
                    break
            if not field_match:
                new_schema.append(field)
        table.schema = new_schema
        bq_client.update_table(table, ["schema"])


# class InspectAndApply(beam.DoFn):
#     def process(self, element, dataset, project, region, taxonomy_id):
#         dataset = dataset.get()
#         region = region.get()
#         taxonomy_id = taxonomy_id.get()
#         central_policy_tags_client = CentralPolicyTagsClient(project,
#                                                              region,
#                                                              dataset,
#                                                              dataset,
#                                                              'inspect_policy_tags_result')
#         central_policy_tags_client.inspect_dataset_process()
#         central_policy_tags_client.apply_policy_tags(taxonomy_id)
#         time.sleep(10)
#         central_policy_tags_client.delete_temp_external_table(table_id='dataflow_inspect_job_result')
#         print(dataset)
#         pass

# class ApplyCustomDataset(beam.DoFn):
#     def process(self, element, dataset, project, region, table, taxonomy_id, custom_tags):
#         central_policy_tags_client = CentralPolicyTagsClient(
#             project=project,
#             region=region.get(),
#             inspect_ds=dataset.get(),
#             result_ds=dataset.get(),
#             result_table='inspect_policy_tags_result'
#         )
#         policy_tags = central_policy_tags_client.get_all_policy_tags_from_taxonomy(taxonomy_id=taxonomy_id.get())
#         tag_requests = []
#         for column in list(custom_tags.keys()):
#             tag_requests.append((column, policy_tags.get(custom_tags.get(column))))
#         central_policy_tags_client.tag_table(table_id=f'{project}.{dataset}.{table.get()}',
#                                              policy_tag_requests=tag_requests,
#                                              bigquery_region=region)
