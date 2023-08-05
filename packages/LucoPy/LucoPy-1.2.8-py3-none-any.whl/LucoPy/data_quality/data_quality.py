import json

class CheckResult:

    def __init__(self, results):
        self.__results = results

        # Set Collection attributes from results
        # Required - will throw exception if not present
        required_args = ['check', 'success']
        for k in required_args:
            if k not in results:
                raise Exception(f'Required arg not present: {k}')

        for k, v in results.items():
            setattr(self, k, v)

    def __str__(self):
        return json.dumps(self.__results)

    def to_json_dict(self):
        return self.__results

class CollectionResult:

    def __init__(self, results):
        self.__results = self.__build_json_dict(results)

        # Set Collection attributes from results
        # Required - will throw exception if not present
        required_args = ['checks']
        for k in required_args:
            if k not in results:
                # TODO: return all missing required args
                raise Exception(f'Required arg not present: {k}')

        for k, v in results.items():
            setattr(self, k, v)

    def __build_json_dict(self, results):

        results_json = results
        checks_as_json = []

        for check in results_json['checks']:
            checks_as_json.append(check.to_json_dict())

        results_json['checks'] = checks_as_json  
        return results_json

    def to_json_dict(self):
        return self.__results