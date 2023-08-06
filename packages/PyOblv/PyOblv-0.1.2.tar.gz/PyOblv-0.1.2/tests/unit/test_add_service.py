import unittest
from http.client import FORBIDDEN
from unittest.mock import patch

from httpx import Response

from oblv.exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from oblv.models.http_validation_error import HTTPValidationError
from oblv.models.service_validation_response import ServiceValidationResponse
from oblv.models.validation_error import ValidationError
from oblv.oblv_client import OblvClient
from tests.unit.constants import (
    API_GW_REQUEST_ID,
    BAD_REQUEST_MESSAGE,
    EXCEPTION_OCCURED,
    INVALID_PUBLIC_KEY,
    KEY_APIGW_REQUESTID,
    KEY_MESSAGE,
    KEY_VALID_ERROR_LOC,
    RANDOM_PUBLIC_KEY,
    REPO_SERVICES,
    SERVICE_YAML_CONTENT,
    SUCCESS,
    USER_ID,
    USER_TOKEN,
    VALID_ERROR_MESSAGE,
    VALID_ERROR_VALUE,
)


class TestAddService(unittest.TestCase):

    client = OblvClient(token=USER_TOKEN,oblivious_user_id=USER_ID)
    
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
        res = Response(200, json={KEY_MESSAGE: SUCCESS, "service": REPO_SERVICES[0]})
        return res

    @patch("httpx.request", return_value=getBadRequestResponse())
    def test_bad_request(self, sync):
        with self.assertRaises(BadRequestError) as cm:
            self.client.add_service(ref="master",repo_id="123456")

    @patch("httpx.request", return_value=getHTTPExceptionResponse())
    def test_http_exception_request(self, sync):
        with self.assertRaises(HTTPClientError) as cm:
            self.client.add_service(ref="master",repo_id="123456")

    @patch("httpx.request", return_value=getFailedValidationResponse())
    def test_failed_validation_request(self, sync):
        with self.assertRaises(ParamValidationError) as cm:
            self.client.add_service(ref="master",repo_id="123456")

        the_exception = cm.exception
        self.assertEqual(the_exception.__str__(), "Invalid {} provided".format(KEY_VALID_ERROR_LOC))

    @patch("httpx.request", return_value=getForbiddenResponse())
    def test_bad_authentication_request(self, sync):
        with self.assertRaises(UnauthorizedTokenError):
            self.client.add_service(ref="master",repo_id="123456")

    @patch("httpx.request", return_value=getSuccessResponse())
    def test_success_request(self, sync):
        obj = ServiceValidationResponse.from_dict({KEY_MESSAGE: SUCCESS, "service": REPO_SERVICES[0]})
        self.assertEqual(self.client.add_service(ref="master",repo_id="123456",repo_name="Repo_Name",repo_owner="Owner_Name"),obj)
        self.assertEqual(self.client.add_service(ref="master",repo_name="Repo_Name",repo_owner="Owner_Name"),obj)
        self.assertEqual(self.client.add_service(ref="master",repo_id="123456"),obj)
        self.assertEqual(self.client.add_service(ref="master",repo_id="123456",data=SERVICE_YAML_CONTENT),obj)
        with self.assertRaises(BadRequestError):
            self.client.add_service(ref="master")
        with self.assertRaises(BadRequestError):
            self.client.add_service(ref="master",repo_name="Repo_Name")
        with self.assertRaises(BadRequestError):
            self.client.add_service(ref="master",repo_owner="Owner_Name")
        


if __name__ == '__main__':
    unittest.main()
