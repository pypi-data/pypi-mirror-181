import json
import math
from datetime import datetime
from typing import TypeVar

import requests

from src.exception.CustomException import CustomException
from src.model.CancelPayment import *
from src.model.CheckPayment import *
from src.model.CreatePayment import *
from src.service.security import Security

T = TypeVar('T')

class Payment:
    __baseUrl = "https://api-umeecore-dev.hcm.unicloud.ai/umee-pay"
    __endpointCreate = "/api/payment/v1/create"
    __endpointCheck = "/api/payment/v1/check"
    __endpointCancel = "/api/payment/v1/cancel"
    __clientId: str
    __secretKey: str
    __encryptKey: str
    __security: Security = Security()

    def __init__(self, clientId: str, encryptKey: str, secretKey: str):
        self.__clientId = clientId
        self.__secretKey = secretKey
        self.__encryptKey = encryptKey

    def __excute(self, url: str, data: T) -> str:
        dt = datetime.now()
        timestamp = math.floor(datetime.timestamp(dt) * 1000)
        print(data.__str__())
        dataJson = json.dumps(data.__str__())
        payload = self.__security.aesEcrypt(dataJson, self.__encryptKey).decode('UTF-8')
        apiValidate = self.__security.genarateSign(payload, self.__clientId, timestamp, self.__secretKey)
        requestData = {
            "data": payload
        }
        response = requests.post(url,  json.dumps(requestData), headers={
            'x-api-client': self.__clientId,
            'x-api-validate': apiValidate,
            'x-api-time': str(timestamp),
            'Content-Type': 'application/json',
        })
        responseData = response.content.decode('UTF-8')

        clientRes = str(response.headers['x-api-client'])
        dataValidateRes = str(response.headers['x-api-validate'])
        timestampRes = int(response.headers['x-api-time'])
        responseData = json.loads(responseData)

        dataDescrypt = responseData['data']

        if self.__clientId != clientRes:
            raise CustomException(1, "Invalid Client")

        if responseData['data'] == None:
            raise CustomException(responseData['code'], responseData['message'])

        if self.__security.verifySign(responseData['data'], dataValidateRes, clientRes, timestampRes, self.__secretKey) == False:
            raise CustomException(2, "Invalid Security")

        dateDecrypt = self.__security.aesDecrypt(dataDescrypt, self.__encryptKey)
        return dateDecrypt


    def create_payment(self, data: CreatePaymentRequest) -> CreatePaymentResponse:
        url = self.__baseUrl + self.__endpointCreate
        response: str = self.__excute(url,data)
        return CreatePaymentResponse(response)

    def check_payment(self, data: CheckPaymentRequest) -> CheckPaymentResponse:
        url = self.__baseUrl + self.__endpointCheck
        resposne: str = self.__excute(url, data)
        return CheckPaymentResponse(resposne)

    def cancel_payment(self, data: CancelPaymentRequest) -> CancelPaymentResponse:
        url = self.__baseUrl + self.__endpointCancel
        resposne: str = self.__excute(url, data)
        return CancelPaymentResponse(resposne)
