
from apache_beam.options.pipeline_options import PipelineOptions


class UserOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--dataset',
            # required=True,
            help='dataset name to inspect and tagging policy tags'
        )
        parser.add_value_provider_argument(
            '--taxonomy_id',
            # required=True,
            help='format projects/{}/locations/{}/taxonomies/{}'
        )
        parser.add_value_provider_argument(
            '--tag_mapping',
            help='version of templates'
        )
        parser.add_value_provider_argument(
            '--inspect_region',
            # required=True,
            help='version of templates'
        )
        parser.add_value_provider_argument(
            '--version',
            help='version of templates'
        )
        parser.add_value_provider_argument(
            '--table',
            help='table name for custom case'
        )
        parser.add_value_provider_argument(
            '--custom_tags',
            help='table name for custom case'
        )



