import logging
import os
from typing import Optional

import google.cloud.logging
from google.api_core import exceptions
from google.api_core.retry import Retry, if_exception_type
from google.cloud import datacatalog_v1, datacatalog_v1beta1
from google.cloud.dlp_v2 import DlpServiceClient
from npgbq import NPGBQ

_MY_RETRIABLE_TYPES = (
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
)


class NPBlind(object):
    def __init__(self, project_id, gcp_service_account_path: Optional[str] = None):
        self.project_id = project_id
        self.resource_id = f"projects/{project_id}"
        self.path_json_key = gcp_service_account_path
        self.__add_environment()
        self.client = self.__get_client()
        self.client_ptc = self.___get_policy_tag_manager_client()
        self.client_ptc_beta = self.___get_policy_tag_manager_client_beta()
        self.client_gbq = NPGBQ(
            project_id=project_id, gcp_service_account_path=gcp_service_account_path
        )

    def __add_environment(self):
        if self.path_json_key:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_json_key

    def __get_client(self) -> DlpServiceClient:
        client = google.cloud.logging.Client(project=self.project_id)
        client.setup_logging(log_level=logging.INFO)
        dlp = DlpServiceClient()
        return dlp

    def ___get_policy_tag_manager_client(self):
        # todo try PolicyTagManagerClient in async version
        return datacatalog_v1.PolicyTagManagerClient()

    def ___get_policy_tag_manager_client_beta(self):
        # todo try PolicyTagManagerClient in async version
        return datacatalog_v1beta1.PolicyTagManagerClient()

    # ================================= methods =================================

    def create_taxonomy(
        self, taxonomy_id: str = "my-taxonomy", location_id: str = "asia-southeast1"
    ):
        parent = self.client_ptc.common_location_path(self.project_id, location_id)
        taxonomy = datacatalog_v1.Taxonomy()
        taxonomy.display_name = taxonomy_id  # type: ignore
        taxonomy.description = "This Taxonomy represents ..."  # type: ignore
        try:
            taxonomy = self.client_ptc.create_taxonomy(parent=parent, taxonomy=taxonomy)
        except Exception as e:
            print(f"The taxonomy_id={taxonomy_id} is already exists")
            return False
        else:
            print(f"Created taxonomy {taxonomy.name}")
            return True

    # create a policy tag under target taxonomy in Google Cloud Data Catalog
    def create_policy_tag(
        self,
        taxonomy_id: str,
        policy_tag_id: str,
        description: str = "This Policy Tag represents ...",
        location_id: str = "asia-southeast1",
    ):
        parent = self.client_ptc.common_location_path(self.project_id, location_id)
        # create a policy tag
        policy_tag = datacatalog_v1.PolicyTag()
        policy_tag.name = policy_tag_id
        policy_tag.display_name = f"description_{policy_tag_id}"
        policy_tag.description = description
        policy_tag2 = datacatalog_v1.PolicyTag(
            name=policy_tag_id,
            display_name=f"description_{policy_tag_id}",
            description=description,
        )
        if policy_tag == policy_tag2:
            print("hi")
        request = datacatalog_v1.CreatePolicyTagRequest(
            parent=parent, policy_tag=policy_tag
        )
        self.client_ptc.create_policy_tag(request=request)
        request = datacatalog_v1.CreatePolicyTagRequest()

    def get_taxonomy_data(self, taxonomy_id, location_id):
        full_parent_id = self.__get_taxonomy_parent(taxonomy_id, location_id)
        request = datacatalog_v1.ListPolicyTagsRequest(parent=full_parent_id)
        response = self.client_ptc.list_policy_tags(request=request)._response.policy_tags
        taxonomy_data = {}
        for i in response:
            taxonomy_data[i.display_name] = {
                "id": i.name,
                "description": i.description,
                "parent": i.parent_policy_tag,
                "child": i.child_policy_tags,
            }
        return taxonomy_data

    def __get_taxonomy_parent(self, taxonomy_id, location_id):
        return (
            f"projects/{self.project_id}/locations/{location_id}/taxonomies/{taxonomy_id}"
        )

    def apply_policy_tag(
        self, dataset_name, table_name, taxonomy_data, policy_tag_id, column_to_tag
    ):
        table_id = self.client_gbq.get_full_qualified_table_name(
            self.project_id, dataset_name, table_name
        )
        table = self.client_gbq.client.get_table(table_id)
        schema = table.schema
        _schema = []
        for col in schema:
            if col.name == column_to_tag:
                res = self.client_gbq.get_schema_policy_tag(
                    column_to_tag, col.field_type, col.mode, policy_tag_id=policy_tag_id
                )
                _schema.append(res)
            else:
                _schema.append(col)
        table.schema = _schema
        self.client_gbq.client.update_table(table, ["schema"])
        return True


if __name__ == "__main__":
    gcp_sa = "../../tests/gcp_nplearn_serviceaccountkey.json"
    npb = NPBlind(project_id="nplearn", gcp_service_account_path=gcp_sa)
    dataset_name = "test_policy_tag"
    table_name = "customer"
    taxonomy_name = "nptag"
    taxonomy_id = "2421210100988381321"
    location_id = "asia-southeast1"
    column_to_tag = "cphone"
    policy_tag_to_use = "mobile_phone"
    policy_tag_to_use_id = "projects/nplearn/locations/asia-southeast1/taxonomies/2421210100988381321/policyTags/3601781208787418520"
    # get taxonomy data
    taxonomy_data = npb.get_taxonomy_data(taxonomy_id, location_id)
    res = npb.apply_policy_tag(
        dataset_name, table_name, taxonomy_data, policy_tag_to_use_id, column_to_tag
    )
    # npb.apply_tag_to_column()
