import json

class CheckPaymentRequest: 
    transactionId: str

    def __init__(self, transactionId: str) -> None:
        self.transactionId = transactionId

    def __str__(self) -> str:
        return {
            "transactionId": self.transactionId
        }

class CheckPaymentResponse:
    status: str
    refTransactionId: str
    amount: int

    def __str__(self) -> str:
        return {
            "status": self.status,
            "refTransactionId": self.refTransactionId,
            "amount": self.amount
        }

    def __init__(self, j) -> None:
        self.__dict__ = json.loads(j) 