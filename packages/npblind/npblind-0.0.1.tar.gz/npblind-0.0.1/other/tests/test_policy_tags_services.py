from CentralPolicyTagsPackage.CentralPolicyTags import CentralPolicyTagsClient
test = """{"project":"central-cto-data-admin-hub",
"dataset": "test_policy_tags",
"table": "sample_pii",
"taxonomy_id": "projects/chuongcentralpractice/locations/asia-southeast1/taxonomies/4847401218804767541",
"custom_tags": {"cc_number": "personal-data"},
"region": "asia-southeast1"}"""
apply_custom_policy_tags(test, None)