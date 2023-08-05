from mitWppSdk.builders import _PgsBuilder_
from mitWppSdk.WppException import WppException
from mitWppSdk.util import WppHttpHelper, AesHelper, isBase64
from mitWppSdk.validators import PaymentValidator
from lxml import objectify, etree
from urllib.parse import quote_plus, unquote_plus
import re

class WppResponse:
    ...

class WppClient:
    def __init__(self, endpoint: str, id: str, key: str) -> None:
        self._httpHelper = WppHttpHelper(endpoint)
        self._aesHelper = AesHelper(bytes.fromhex(key))
        self._id = id
        self._validator = PaymentValidator()
    
    def getUrlPayment(self, payment: objectify.ObjectifiedElement ) -> str:
        self._validator.validate(payment)
        xml = self._buildRequest(payment)
        xml = self._sendRequest(xml)
        response = self.processAfterPaymentResponse(xml)
        if "success" != response["cd_response"]:
            raise WppException(response["nb_response"])
        return response["nb_url"]


    def _buildRequest(self, payment: objectify.ObjectifiedElement) -> str:
        xml = etree.tostring(payment, xml_declaration=True, encoding="UTF-8", standalone=True).decode("utf-8")
        xml = self._aesHelper.encrypt(xml)

        pgs = _PgsBuilder_().data0(self._id).data(xml).build()
        return etree.tostring(pgs).decode("utf-8")

    def _sendRequest(self, xml: str) -> str:
        xml = quote_plus(xml)
        return self._httpHelper.post( "xml={}".format(xml))

    def _decryptResponse(self, bodyResponse : str) -> str:
        if "strResponse=" in bodyResponse:
            bodyResponse[12:]
        
        if "%" in bodyResponse:
            bodyResponse = unquote_plus(bodyResponse)
            bodyResponse = re.sub("[\r\n\s]", "", bodyResponse)
        
        if not isBase64(bodyResponse):
            raise WppException(bodyResponse)

        return self._aesHelper.decrypt(bodyResponse)

    def processAfterPaymentResponse(self, xmlResponse: str) -> dict:
        xmlResponse = self._decryptResponse(xmlResponse)
        bodyResponse = etree.fromstring(xmlResponse)
        wppResponse = {}
        for child in bodyResponse.getchildren():
            wppResponse[child.tag] = child.text
        return wppResponse