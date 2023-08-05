class CustomerInfo: 
    fullName: str
    email: str
    phone: str
    address: str

    def __init__(self, fullName, email, phone, address):
        self.fullName = fullName
        self.email = email
        self.phone = phone
        self.address = address
        
    def __str__(self) -> str:
        return {
            "fullName": self.fullName,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }