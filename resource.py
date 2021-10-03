import falcon
from .transaction import Transaction


class MerchantResource():

    def on_get(self, req, resp, merchantId):
        currency = req.get_param("currency")
        startDate = req.get_param("startDate")
        endDate = req.get_param("endDate")

        transaction = Transaction(merchantId, startDate, endDate, currency)
        data, code = self._get_res_and_code(transaction)

        resp.status = code
        resp.text = bytes(str(data), "utf-8")
    
    def _get_res_and_code(self, transaction):
        code = 200
        try:
            resp = transaction.calculate_transactions()
            if (not resp): 
                resp = {"message": "'{0}' not found".format(transaction.merchantId)}
                code = 404
        except ValueError as e:
            resp = {"message": "an error has occurred"}
            code = 400

        return resp, code



        
