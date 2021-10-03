from datetime import datetime
from .services import get_data


DEFAULT_CURRENCY = "GBP"


class Transaction:
    def __init__(self, merchantId, startDate=None, endDate=None, currency=None):
        self.merchantId = merchantId
        self.startDate = startDate
        self.endDate = endDate
        self.currency = currency or DEFAULT_CURRENCY
        self.data = get_data()
    

    def calculate_transactions(self):
        volume_transactions = 0
        value_transactions = 0

        if (not self._is_valid_merchant()): 
            return None

        for merchant in self.data["transactions"]:
            if merchant["merchantId"] == self.merchantId and self._is_date_between(merchant["datetime"]):
                volume_transactions += 1
                value_transactions += merchant["amount"]
        
        return {"valueTransactions": { "amount" : value_transactions, "currency": self.currency}, 
                "volumeTransactions": volume_transactions}
    
    def _is_date_between(self, merchantDate):
        if not self.startDate or not self.endDate or self.startDate > self.endDate:
            return True
        
        datetime_format = "%Y-%m-%dT%H:%M:%SZ"
        query_start_date = datetime.strptime(self.startDate, datetime_format)
        query_end_date = datetime.strptime(self.endDate, datetime_format)

        merchant_date = datetime.strptime(merchantDate, datetime_format)
        
        if(query_start_date <= merchant_date <= query_end_date):
            return True
        
        return False
    
    
    def _is_valid_merchant(self):
        for merchant in self.data["transactions"]:
            if self.merchantId == merchant["merchantId"]: return True
        return False