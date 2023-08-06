import imp
import unittest
from http.client import FORBIDDEN
from unittest.mock import patch

from httpx import Response

from oblv.exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from oblv.models.account import Account
from oblv.models.deployment_response import DeploymentResponse
from oblv.models.http_validation_error import HTTPValidationError
from oblv.models.validation_error import ValidationError
from oblv.oblv_client import OblvClient
from tests.unit.constants import (
    API_GW_REQUEST_ID,
    BAD_REQUEST_MESSAGE,
    DEPLOYMENT,
    EXCEPTION_OCCURED,
    GITHUB,
    GITHUB_USER_ID,
    GITHUB_USER_LOGIN,
    KEY_APIGW_REQUESTID,
    KEY_MESSAGE,
    KEY_VALID_ERROR_LOC,
    USER_ID,
    USER_TOKEN,
    VALID_ERROR_MESSAGE,
    VALID_ERROR_VALUE,
)


class TestUserDeployments(unittest.TestCase):

    client = OblvClient(token=USER_TOKEN, oblivious_user_id=USER_ID)

    def setUp(self) -> None:
        super().setUp()

    def getBadRequestResponse():
        res = Response(400, json={KEY_MESSAGE: BAD_REQUEST_MESSAGE})
        return res

    def getHTTPExceptionResponse():
        res = Response(500, json={KEY_MESSAGE: EXCEPTION_OCCURED}, headers={
                       KEY_APIGW_REQUESTID: API_GW_REQUEST_ID})
        return res

    def getFailedValidationResponse():
        data = HTTPValidationError(
            [ValidationError([KEY_VALID_ERROR_LOC], VALID_ERROR_MESSAGE, VALID_ERROR_VALUE)])
        res = Response(422, json=data.to_dict())
        return res

    def getForbiddenResponse():
        res = Response(403, json=FORBIDDEN)
        return res

    def getSuccessResponse():
        res = Response(200, json=[DEPLOYMENT])
        return res

    @patch("httpx.request", return_value=getBadRequestResponse())
    def test_bad_request(self, sync):
        with self.assertRaises(BadRequestError) as cm:
            self.client.deployments()

    @patch("httpx.request", return_value=getHTTPExceptionResponse())
    def test_http_exception_request(self, sync):
        with self.assertRaises(HTTPClientError) as cm:
            self.client.deployments()

    @patch("httpx.request", return_value=getFailedValidationResponse())
    def test_failed_validation_request(self, sync):
        with self.assertRaises(ParamValidationError) as cm:
            self.client.deployments()

        the_exception = cm.exception
        self.assertEqual(the_exception.__str__(),
                         "Invalid {} provided".format(KEY_VALID_ERROR_LOC))

    @patch("httpx.request", return_value=getForbiddenResponse())
    def test_bad_authentication_request(self, sync):
        with self.assertRaises(UnauthorizedTokenError):
            self.client.deployments()

    @patch("httpx.request", return_value=getSuccessResponse())
    def test_success_request(self, sync):
        deployments = [DeploymentResponse.from_dict(DEPLOYMENT)]
        self.assertEqual(self.client.deployments(), deployments)


if __name__ == '__main__':
    unittest.main()
