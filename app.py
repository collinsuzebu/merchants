import falcon

from .resource import MerchantResource

app = falcon.App()

app.add_route("/transactions/all/{merchantId}", MerchantResource())