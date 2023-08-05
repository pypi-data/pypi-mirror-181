from src.model.CustomerInfo import *
import json

class CreatePaymentRequest :
    refTransactionId: str
    amount: int
    description: str
    timeout: int
    title: str
    language: str
    customerInfo: CustomerInfo
    successUrl: str
    failUrl: str
    redirectAfter: int
    bankAccountId: str

    def __init__(self, refTransactionId: str, amount: int, description: str, timeout: str, title: str, customerInfo: CustomerInfo,
    successUrl: str, failUrl: str, redirectAfter: str, language: str = None, bankAccountId: str = None) -> None:
        self.refTransactionId = refTransactionId
        self.amount = amount
        self.description = description
        self.timeout = timeout
        self.title = title
        self.customerInfo = customerInfo
        self.successUrl = successUrl
        self.failUrl = failUrl
        self.redirectAfter = redirectAfter
        self.language = language
        self.bankAccountId = bankAccountId

    def __str__(self) -> str:
        return {
            "refTransactionId": self.refTransactionId,
            "amount": self.amount,
            "description": self.description,
            "timeout": self.timeout,
            "title": self.title,
            "language": self.language,
            "customerInfo": self.customerInfo.__str__(),
            "successUrl": self.successUrl,
            "failUrl": self.failUrl,
            "redirectAfter": self.redirectAfter,
        }


class CreatePaymentResponse: 
    transactionId: str
    refTransactionId: str
    payLinkCode: str
    timeout: int
    url: str
    virtualAccount: str
    description: str
    amount: int
    qrCodeString: str
    status: str
    time: str

    def __init__(self, transactionId, refTransactionId, payLinkCode, timeout, url, virtualAccount, description, amount, qrCodeString, status, time) -> None:
        self.transactionId = transactionId
        self.refTransactionId = refTransactionId
        self.payLinkCode = payLinkCode
        self.timeout = timeout
        self.url = url
        self.virtualAccount = virtualAccount
        self.description = description
        self.amount = amount
        self.qrCodeString = qrCodeString
        self.status = status
        self.time = time

    def __init__(self, j) -> None:
        self.__dict__ = json.loads(j)