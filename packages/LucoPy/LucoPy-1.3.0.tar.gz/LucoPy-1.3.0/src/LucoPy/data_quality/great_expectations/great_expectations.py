from great_expectations.expectations.registry import get_renderer_impl
from great_expectations.core import ExpectationValidationResult, ExpectationSuiteValidationResult, ExpectationConfiguration
from datetime import datetime
from ..data_quality import CheckResult, CollectionResult

def process_meta_field(meta, mappings):

    mapped_metadata = {'metadata': {}}

    # Invert keys and values to make mapping easier
    mappings = {v: k for k, v in mappings.items()}

    for k, v in meta.items():
        if k in mappings:
            mapped_metadata[mappings[k]] = v
        elif k in mappings.values():
            mapped_metadata[k] = v
        else:
            mapped_metadata['metadata'][k] = v

    return mapped_metadata

class ExpectationResult:

    def __init__(self, expectation_results, metadata_mappings={}):

        if isinstance(expectation_results, dict):
            self.expectation = ExpectationValidationResult(**expectation_results)
            self.expectation.expectation_config = ExpectationConfiguration(
                                                    **expectation_results['expectation_config'])
        else:
            self.expectation = expectation_results

        self.result_format = self.expectation.expectation_config.kwargs['result_format']
        self.result = self.expectation.result
        self.custom_mappings = metadata_mappings

    def convert_to_check(self):
        """
        Convert expectation into a Check
        """
        rendered_expectation = {}

        rendered_expectation['success'] = self.expectation.success
        rendered_expectation['check'] = self.expectation.expectation_config.expectation_type

        # Render expectation config to templated string with args
        rendered_expectation.update(self.render_expectation_config())

        # Render results based on format
        rendered_expectation.update(self.render_results(self.result, self.result_format))

        # Default metadata mappings for recognised fields
        metadata_mappings = {
            'onFail': 'onFail',
            'referenceUrl': 'referenceUrl',
            'tags': 'tags'
        }

        # Update custom metadata mappings if provided
        for k, v in self.custom_mappings.items():
            if k in metadata_mappings:
                metadata_mappings[k] = v

        # Process meta field
        rendered_expectation.update(process_meta_field(self.expectation.expectation_config['meta'], metadata_mappings))

        return CheckResult(rendered_expectation)

    def render_expectation_config(self):
        """
        For a single expectation get the unique renderer method and call this
        to generate a rendered, parameterised expectation name with args.
        """
        string_render_method = get_renderer_impl(
            object_name=self.expectation.expectation_config.expectation_type,
            renderer_type='renderer.prescriptive'
        )[1]

        rendered_expectation = string_render_method(
            configuration=self.expectation.expectation_config
        )[0]

        rendered_expectation_str = {'check': rendered_expectation.string_template['template'],
                                    'checkArgs': rendered_expectation.string_template['params']}

        return self.filter_rendered_expectation(rendered_expectation_str)

    def filter_rendered_expectation(self, rendered_expectation):
        """
        Remove unused keys from check_args
        """
        filtered_args = {}

        for k, v in rendered_expectation['checkArgs'].items():
            if k in rendered_expectation['check'] and isinstance(v, str):
                filtered_args[k] = v

        rendered_expectation['checkArgs'] = filtered_args

        return rendered_expectation

    def render_results(self, result, result_format):
        """
        Render the result set of an expectation
        """
        if result_format == 'BOOLEAN_ONLY' or len(result) == 0:
            return {}
        elif result.get('observed_value'):
            # If an observed value is provided then use this
            
            # If string, format value as a percentage
            if isinstance(result['observed_value'], str):
                return {'observed': self.percentage_as_string(result['observed_value'])}
            
            # If list, return whole observed list
            # TODO: Do we want to cap the length of this?
            elif isinstance(result['observed_value'], list):
                return {'observed': result['observed_value']}
        else:
            # Otherwise, map result stats
            # TODO: Parse the full unexpected lists but with a length cap?
            result_mappings = {
                'element_count': 'elementCount',
                'unexpected_percent_total': 'failedPercentage',
                'partial_unexpected_list': 'partialFailedRecordsList',
                'partial_unexpected_index_list': 'partialFailedRecordsIndexList',
                'partial_unexpected_counts': 'partialUnexpectedCounts'
            }

            mapped_result = {}
            for k, v in result.items():
                if k in result_mappings:

                    if 'percent' in k:
                        mapped_result[result_mappings[k]] = self.percentage_as_string(v)
                    else:
                        mapped_result[result_mappings[k]] = v

            return {'observed': mapped_result}

    def percentage_as_string(self, value):
        return f'{round(value, 2)}%'

class ExpectationSuiteResult:

    def __init__(self, suite_results, suite_mappings={}, expectation_mappings={}):

        if isinstance(suite_results, dict):
            self.suite_results = ExpectationSuiteValidationResult(**suite_results)
        else:
            self.suite_results = suite_results

        self.meta = self.suite_results.to_json_dict()['meta']
        self.suite_mappings = suite_mappings
        self.expectation_mappings = expectation_mappings

    def convert_to_collection(self):
        """
        Construct JSON dictionary of collection from expectation suite results.
        """
        # Initialise object with required keys
        collection = {'checks': []}

        # Convert each expectation result to a check
        for expectation in self.suite_results['results']:
            collection['checks'].append(
                ExpectationResult(expectation, self.expectation_mappings)
                    .convert_to_check())

        collection['tool'] = 'Great Expectations'

        metadata_mappings = {
            'toolVersion': 'great_expectations_version',
            'name': 'expectation_suite_name',
            'start': 'validation_time',
            'referenceUrl': 'referenceUrl',
            'tags': 'tags'
        }

        # Update metadata mappings if provided
        for k, v in self.suite_mappings.items():
            if k in metadata_mappings:
                metadata_mappings[k] = v

        collection.update(process_meta_field(self.meta, metadata_mappings))

        collection['start'] = self.validate_start_time(collection['start'])

        return CollectionResult(collection)

    def validate_start_time(self, ts):
        # Converts timestamps to ISO
        dt = datetime.strptime(ts, '%Y%m%dT%H%M%S.%fZ')
        return dt.isoformat()