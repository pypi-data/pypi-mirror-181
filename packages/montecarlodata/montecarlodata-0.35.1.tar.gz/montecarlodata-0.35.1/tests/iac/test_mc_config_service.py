import json
import os
import pathlib
from unittest import TestCase
from unittest.mock import Mock, patch, call, ANY

import click
from box import Box
from pycarlo.core import Client

from montecarlodata.common.data import MonolithResponse
from montecarlodata.iac.mc_config_service import MonteCarloConfigService
from montecarlodata.queries.iac import CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE
from montecarlodata.utils import GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG


class MonteCarloConfigServiceTest(TestCase):
    @patch('os.getcwd')
    def setUp(self, getcwd) -> None:
        self._request_wrapper_mock = Mock(spec=GqlWrapper)
        self._pycarlo_client = Mock(spec=Client)
        self._print_func = Mock(spec=click.echo)
        self.project_dir = self._get_project_dir('standalone_configs')
        getcwd.return_value = self.project_dir
        self.service = MonteCarloConfigService(_SAMPLE_CONFIG, self._request_wrapper_mock,
                                               pycarlo_client=self._pycarlo_client, print_func=self._print_func)

    def test_standalone_configs(self):
        files, template, _ = self.service.compile()
        self.assertEqual(len(files), 3)
        self.assertEqual(
            template,
            {
                'field_health': [{
                    'table': 'analytics:prod.client_hub',
                    'fields': ['account_id']
                }],
                'dimension_tracking': [{
                    'table': 'analytics:prod.customer_360',
                    'field': 'account_id'
                }]
            }
        )

    def test_embedded_dbt_configs(self):
        self.service = MonteCarloConfigService(_SAMPLE_CONFIG, self._request_wrapper_mock,
                                               project_dir=self._get_project_dir('embedded_dbt_configs'),
                                               pycarlo_client=self._pycarlo_client)
        files, template, _ = self.service.compile()

        self.assertEqual(len(files), 4)
        self.assertEqual(
            template,
            {
                'field_health': [{
                    'table': 'analytics:prod_lineage.lineage_nodes',
                    'timestamp_field': 'created'
                }, {
                    'table': 'analytics:prod.abc'
                }, {
                    'table': 'analytics:prod.client_hub',
                    'fields': ['account_id']
                }],
                'freshness': [{
                    'table': 'analytics:prod.abc',
                    'freshness_threshold': 30,
                    'schedule': {
                        'type': 'fixed',
                        'interval_minutes': 30,
                        'start_time': '2021-07-27T19:51:00'
                    }
                }],
                'dimension_tracking': [{
                    'table': 'analytics:prod.customer_360',
                    'field': 'account_id'
                }]
            }
        )

    def test_invalid_configs(self):
        self.service = MonteCarloConfigService(_SAMPLE_CONFIG, self._request_wrapper_mock,
                                               project_dir=self._get_project_dir('invalid_configs'),
                                               pycarlo_client=self._pycarlo_client)
        self.service._abort_on_error = False

        files, template, errors_by_file = self.service.compile(abort_on_error=False)
        errors = sorted(list(errors_by_file.items()), key=lambda x: x[0])

        file, error = errors[0]
        self.assertTrue(file.endswith('dir1/dir2/monitors.yml'))
        self.assertEqual(error, ['"custom_sql" property should be a list.'])
        file, error = errors[1]
        self.assertTrue(file.endswith('dir1/monitors.yml'))
        self.assertEqual(error, ['"field_health" property should be a list.'])

    def test_apply(self):
        namespace = 'foo'
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data={
                'response': {
                    'resourceModifications': [
                        {
                            'type': 'ResourceModificationType.UPDATE',
                            'description': 'Monitor: type=stats, table=analytics:prod.client_hub',
                            'resourceAsJson': '{"uuid": "ed4d07c3-58fd-44d0-8b2d-c1b020f45a69", "resource": null, "name": "monitor|type=stats|table=analytics:prod.client_hub|timestamp_field=<<NULL>>|where_condition=<<NULL>>", "table": "analytics:prod.customer_360", "type": "stats", "fields": [], "timestamp_field": null, "where_condition": null}'
                        }, {
                            'type': 'ResourceModificationType.UPDATE',
                            'description': 'Monitor: type=categories, table=analytics:prod.customer_360',
                            'resourceAsJson': '{"uuid": "ec3b0a80-d088-4dbe-acf5-150caf041574", "resource": null, "name": "monitor|type=categories|table=analytics:prod.customer_360|timestamp_field=<<NULL>>|where_condition=<<NULL>>|fields=account_id", "table": "analytics:prod.customer_360", "type": "categories", "fields": ["account_id"], "timestamp_field": null, "where_condition": null}'
                        }
                    ],
                    'changesApplied': True,
                    'errorsAsJson': '{}',
                    'warningsAsJson': '{}'
                }
            }
        )

        response = self.service.apply(namespace)

        config_template_as_dict = {
            'field_health': [{
                'table': 'analytics:prod.client_hub',
                'fields': ['account_id']
            }],
            'dimension_tracking': [{
                'table': 'analytics:prod.customer_360',
                'field': 'account_id'
            }]
        }

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE,
            operation='createOrUpdateMonteCarloConfigTemplate',
            variables=dict(
                namespace=namespace,
                configTemplateJson=json.dumps(config_template_as_dict),
                dryRun=False,
                misconfiguredAsWarning=True,
                resource=None
            )
        )

        self.assertEqual(response.errors, {})
        self.assertEqual(len(response.resource_modifications), 2)

    def test_apply_with_errors(self):
        namespace = 'foo'
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data={
                'response': {
                    'resourceModifications': [],
                    'changesApplied': False,
                    'errorsAsJson': '{"validation_errors": {"monitors": {"0": {"type": ["Unknown field."]}}}}'
                }
            })

        response = self.service.apply(namespace, abort_on_error=False)

        config_template_as_dict = {
            'field_health': [{
                'table': 'analytics:prod.client_hub',
                'fields': ['account_id']
            }],
            'dimension_tracking': [{
                'table': 'analytics:prod.customer_360',
                'field': 'account_id'
            }]
        }

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE,
            operation='createOrUpdateMonteCarloConfigTemplate',
            variables=dict(
                namespace=namespace,
                configTemplateJson=json.dumps(config_template_as_dict),
                dryRun=False,
                misconfiguredAsWarning=True,
                resource=None
            )
        )

        self.assertEqual(response.errors, {'validation_errors': {'monitors': {'0': {'type': ['Unknown field.']}}}})
        self.assertEqual(len(response.resource_modifications), 0)

    def test_misconfigured_warnings(self):
        namespace = 'foo'
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data={
                'response': {
                    'resourceModifications': [
                    {
                        "type": "ResourceModificationType.CREATE",
                        "description": "Freshness SLO: tables=['analytics:prod.client_hub', 'analytics:prod.client_warehouses'] freshness_threshold=1",
                        "resourceAsJson": "{\"uuid\": null, \"resource\": null, \"name\": \"freshnessrule|tables=(multiple)\", \"description\": null, \"notes\": null, \"labels\": [], \"schedule\": {\"type\": \"fixed\", \"interval_minutes\": 1, \"interval_crontab\": null, \"start_time\": \"2021-07-27T19:00:00\"}, \"table\": null, \"tables\": [\"analytics:prod.client_hub\", \"analytics:prod.client_warehouses\"], \"freshness_threshold\": 1}"
                    }
                    ],
                    'changesApplied': False,
                    "errorsAsJson": "{}",
                    "warningsAsJson": "{\"misconfigured_warnings\": [{\"title\": \"High breaching Freshness SLOs are defined, adjust freshness_threshold in\", \"items\": [\"analytics:prod.client_hub: freshness_threshold is 1, the expected minimum threshold is 464\", \"analytics:prod.client_warehouses: freshness_threshold is 1, the expected minimum threshold is 1440\"]}]}"
                }
            })

        response = self.service.apply(namespace, abort_on_error=False)

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE,
            operation='createOrUpdateMonteCarloConfigTemplate',
            variables=dict(
                namespace=namespace,
                configTemplateJson=ANY,
                dryRun=False,
                misconfiguredAsWarning=True,
                resource=None
            )
        )

        self.assertEqual(response.warnings,
                         {'misconfigured_warnings': [{
                             'items': ['analytics:prod.client_hub: freshness_threshold is 1, the expected '
                                       'minimum threshold is 464',
                                       'analytics:prod.client_warehouses: freshness_threshold is 1, the expected '
                                       'minimum threshold is 1440'],
                             'title': 'High breaching Freshness SLOs are defined, adjust freshness_threshold in'
                         }]})
        self.assertEqual(len(response.resource_modifications), 1)

    def _get_project_dir(self, dir_name: str):
        return os.path.join(pathlib.Path(__file__).parent.resolve(), 'test_resources', dir_name)

    LIMIT = 2
    NAMESPACES_TABLE = """\
╒═════════════╤══════════════════════════════════╕
│ Namespace   │ Last Update Time                 │
╞═════════════╪══════════════════════════════════╡
│ namespace_1 │ 2000-01-01 00:00:00.000000+00:00 │
├─────────────┼──────────────────────────────────┤
│ namespace_2 │ 2000-01-01 00:00:00.000000+00:00 │
╘═════════════╧══════════════════════════════════╛"""

    @staticmethod
    def _mc_config_templates_response(namespace_count):
        return Box(
            {
                "get_monte_carlo_config_templates": {
                    "edges": [
                        {
                            "node": {
                                "namespace": f"namespace_{i}",
                                "last_update_time": "2000-01-01 00:00:00.000000+00:00"
                            }
                        }
                        for i in range(1, namespace_count + 1)
                    ]
                }
            }
        )

    def test_list_namespaces(self):
        self._pycarlo_client.return_value = self._mc_config_templates_response(self.LIMIT)
        self.service.list_namespaces(self.LIMIT)
        self._print_func.assert_called_once_with(self.NAMESPACES_TABLE)

    def test_list_namespaces_with_more_available(self):
        self._pycarlo_client.return_value = self._mc_config_templates_response(self.LIMIT + 1)
        self.service.list_namespaces(self.LIMIT)
        expected_calls = [
            call(self.NAMESPACES_TABLE),
            call(self.service.MORE_NS_MESSAGE),
        ]
        self._print_func.assert_has_calls(expected_calls)
