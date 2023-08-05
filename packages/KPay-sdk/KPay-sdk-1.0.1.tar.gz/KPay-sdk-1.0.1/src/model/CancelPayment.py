import json

class CancelPaymentRequest:
    transactionId: str

    def __init__(self, transactionId: str) -> None:
        self.transactionId = transactionId

    def __str__(self) -> str:
        return {
            "transactionId": self.transactionId
        }

class CancelPaymentResponse: 
    success: bool     

    def __str__(self) -> str:
        return {
            "success": self.success
        }
    
    def __init__(self, j) -> None:
        self.__dict__ = json.loads(j) 