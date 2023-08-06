def inspect_template(inspect_project, inspect_dataset, table, result_project, result_dataset):
    return {
        "storage_config": {
                    "big_query_options": {
                        "table_reference": {
                            "project_id": inspect_project,
                            "dataset_id": inspect_dataset,
                            "table_id": table
                        },
                        "identifying_fields": [],
                        "excluded_fields": [],
                        "included_fields": [],
                        "sample_method": "RANDOM_START",
                        "rows_limit": "10"
                    }
                },
        'inspect_config': {
            "info_types": [
                {
                    "name": "CREDIT_CARD_NUMBER"
                },
                {
                    "name": "EMAIL_ADDRESS"
                },
                {
                    "name": "STREET_ADDRESS"
                },
                {
                    "name": "PHONE_NUMBER"
                },
                {
                    "name": "PERSON_NAME"
                },
                {
                    "name": "FIRST_NAME"
                },
                {
                    "name": "LAST_NAME"
                },
                {
                    "name": "GENDER"
                },
                {
                    "name": "DATE_OF_BIRTH"
                },
                {
                    "name": "AGE"
                },
                {
                    "name": "ETHNIC_GROUP"
                },
                {
                    "name": "LOCATION_COORDINATES"
                },
                {
                    "name": "IP_ADDRESS"
                }
            ],
            "min_likelihood": "VERY_LIKELY",
        },
        'actions': [
            {
                'save_findings': {
                    'output_config': {
                        'table': {
                            'project_id': result_project,
                            'dataset_id': result_dataset,
                            'table_id': 'dataflow_template_tmp_dataflow_inspect_job_result'
                        }
                    }

                },
            },
        ]}

