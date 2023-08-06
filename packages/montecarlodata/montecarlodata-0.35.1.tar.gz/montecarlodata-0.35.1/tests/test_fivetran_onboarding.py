from unittest import TestCase
from unittest.mock import Mock, patch

from montecarlodata.common.data import ValidationResult
from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.etl.fivetran import FivetranOnboardingService
from montecarlodata.integrations.onboarding.fields import EXPECTED_FIVETRAN_RESPONSE_FIELD, \
    EXPECTED_ADD_CONNECTION_RESPONSE_FIELD
from montecarlodata.queries.onboarding import TEST_FIVETRAN_CRED_MUTATION, ADD_CONNECTION_MUTATION
from montecarlodata.utils import GqlWrapper, AwsClientWrapper
from tests.test_common_user import _SAMPLE_CONFIG

_SAMPLE_WAREHOUSE = {
    'uuid': 'my-snowflake-warehouse-uuid',
    'name': 'snowflake',
    'connectionType': 'SNOWFLAKE',
    'connections': [
        {
            'uuid': 'my-snowflake-connection-uuid',
            'type': 'SNOWFLAKE',
            'createdOn': '2020-03-28T23:51:04.775647+00:00',
            'jobTypes': ['metadata', 'query_logs', 'sql_query', 'json_schema'],
            'connectionIdentifier': {
                'key': 'account',
                'value': 'hda34492.us-east-1'
            }
        }]
}


class FivetranOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = FivetranOnboardingService(
            _SAMPLE_CONFIG,
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock
        )
        self._service._disable_handle_errors = True

    @patch.object(FivetranOnboardingService, '_validate_connection')
    @patch('montecarlodata.integrations.onboarding.base.prompt_connection')
    def test_onboard_fivetran(self, prompt_mock, validation_mock):
        self._user_service_mock.warehouses = [
            _SAMPLE_WAREHOUSE
        ]
        validation_mock.return_value = ValidationResult(has_warnings=False, credentials_key='path')

        self._service.onboard_fivetran(warehouseName=_SAMPLE_WAREHOUSE['name'])

        validation_mock.assert_called_once_with(
            query=TEST_FIVETRAN_CRED_MUTATION,
            response_field=EXPECTED_FIVETRAN_RESPONSE_FIELD
        )

        self._request_wrapper_mock.make_request_v2.assert_called_with(
            operation=EXPECTED_ADD_CONNECTION_RESPONSE_FIELD,
            query=ADD_CONNECTION_MUTATION,
            variables={
                'key': 'path',
                'connectionType': 'fivetran',
                'name': _SAMPLE_WAREHOUSE['name'],
                'dwId': 'my-snowflake-warehouse-uuid'  # check that dwId is passed as a parameter
            })
