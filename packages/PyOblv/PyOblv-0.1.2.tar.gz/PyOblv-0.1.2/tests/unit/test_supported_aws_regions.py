import imp
import unittest
from http.client import FORBIDDEN
from unittest.mock import patch

from httpx import Response

from oblv.exceptions import (BadRequestError, HTTPClientError,
                             ParamValidationError, UnauthorizedTokenError)
from oblv.models.account import Account
from oblv.models.http_validation_error import HTTPValidationError
from oblv.models.validation_error import ValidationError
from oblv.oblv_client import OblvClient
from tests.unit.constants import (API_GW_REQUEST_ID, BAD_REQUEST_MESSAGE,
                                  DEPLOYMENT, EXCEPTION_OCCURED, GITHUB,
                                  GITHUB_USER_ID, GITHUB_USER_LOGIN,
                                  KEY_APIGW_REQUESTID, KEY_MESSAGE,
                                  KEY_VALID_ERROR_LOC, SUPPORTED_REGIONS,
                                  USER_ID, USER_TOKEN, VALID_ERROR_MESSAGE,
                                  VALID_ERROR_VALUE)


class TestSupportedAWSRegions(unittest.TestCase):

    client = OblvClient(token=USER_TOKEN, oblivious_user_id=USER_ID)

    def setUp(self) -> None:
        super().setUp()
        
    def getForbiddenResponse():
        res = Response(403, json=FORBIDDEN)
        return res

    def getSuccessResponse():
        res = Response(200, json=SUPPORTED_REGIONS)
        return res
    
    @patch("httpx.request", return_value=getForbiddenResponse())
    def test_bad_authentication_request(self, sync):
        with self.assertRaises(UnauthorizedTokenError):
            self.client.supported_aws_regions()

    @patch("httpx.request", return_value=getSuccessResponse())
    def test_success_request(self, sync):
        self.assertEqual(self.client.supported_aws_regions().to_dict(), SUPPORTED_REGIONS)


if __name__ == '__main__':
    unittest.main()
