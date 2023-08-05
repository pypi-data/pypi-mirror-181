# -*- coding: UTF-8 -*-
import decimal
import datetime
from lxml import objectify
from enum import Enum, unique

_VALID_STATUS = {0, 1}


@unique
class MonedaType(Enum):
    MXN = 'MXN'
    USD = 'USD'


@unique
class PaymentMethodType(Enum):
    GPY = "GPY"
    APY = "APY"
    C2P = "C2P"
    COD = "COD"
    TCD = "TCD"
    BNPL = "BNPL"


class WppBuilder:
    def __init__(self, parent: "WppBuilder" =None) -> None:
        self._parent = parent

    def _getElement(self) -> objectify.ObjectifiedElement:
        pass

    def andParent(self) -> "WppBuilder":
        return self._parent

    def _clearEmptyTags(self, element: objectify.ObjectifiedElement) -> None:
        for i in element.getchildren():
            if i.text is None and len(i.getchildren()) <= 0:
                element.remove(i)

    def _deannotate(self) -> objectify.ObjectifiedElement:
        item = self._getElement()
        self._clearEmptyTags(item)
        objectify.deannotate(item, xsi_nil=True, cleanup_namespaces=True)
        return item

    def build(self) -> objectify.ObjectifiedElement:
        if self._parent is not None:
            self._parent._deannotate().append(self._deannotate())
        else:
            return self._deannotate()


class BusinessBuilder(WppBuilder):

    def __init__(self, parent: WppBuilder = None) -> None:
        super().__init__(parent)
        self._business = objectify.Element("business")
        self._business.id_company = None
        self._business.id_branch = None
        self._business.user = None
        self._business.pwd = None

    def _getElement(self) -> objectify.ObjectifiedElement:
        return self._business

    def idCompany(self, idCompany: str) -> "BusinessBuilder":
        self._business.id_company = idCompany
        return self

    def idBranch(self, idBranch: str) -> "BusinessBuilder":
        self._business.id_branch = idBranch
        return self

    def user(self, user: str) -> "BusinessBuilder":
        self._business.user = user
        return self

    def pwd(self, pwd: str) -> "BusinessBuilder":
        self._business.pwd = pwd
        return self


class UrlBuilder(WppBuilder):
    def __init__(self, parent: WppBuilder = None) -> None:
        super().__init__(parent)
        self._urldata = objectify.Element("url")
        self._urldata.reference = None
        self._urldata.amount = None
        self._urldata.moneda = None
        self._urldata.canal = "W"
        self._urldata.omitir_notif_default = None
        self._urldata.promociones = None
        self._urldata.id_promotion = None
        self._urldata.st_correo = None
        self._urldata.fh_vigencia = None
        self._urldata.mail_cliente = None
        self._urldata.prepago = None

    def _getElement(self) -> objectify.ObjectifiedElement:
        return self._urldata

    def reference(self, reference: str) -> "UrlBuilder":
        self._urldata.reference = reference
        return self

    def amount(self, amount: decimal) -> "UrlBuilder":
        self._urldata.amount = round(amount, 2)
        return self

    def moneda(self, moneda: MonedaType) -> "UrlBuilder":
        self._urldata.moneda = moneda.value
        return self

    def omitNotification(self, omitir: int) -> "UrlBuilder":
        if omitir not in _VALID_STATUS:
            raise ValueError(
                "results: omitir must be one of %r." % _VALID_STATUS)
        self._urldata.omitir_notif_default = omitir
        return self

    def promotions(self, *promotions: str) -> "UrlBuilder":
        promos = ""
        for promo in promotions:
            promos += promo + ","
        promos = promos[0:len(promos)-1]
        self._urldata.promociones = promos
        return self

    def idPromotion(self, idPromotion: str) -> "UrlBuilder":
        self._urldata.id_promotion = idPromotion
        return self

    def stEmail(self, stEmail: int) -> "UrlBuilder":
        if stEmail not in _VALID_STATUS:
            raise ValueError(
                "results: stEmail must be one of %r." % _VALID_STATUS)
        self._urldata.st_correo = stEmail
        return self

    def expirationDate(self, expirationDate: datetime.date) -> "UrlBuilder":
        self._urldata.fh_vigencia = expirationDate.strftime("%d/%m/%Y")
        return self

    def clientEmail(self, clientEmail: str) -> "UrlBuilder":
        self._urldata.mail_cliente = clientEmail
        return self

    def prepaid(self, prepaid: str) -> "UrlBuilder":
        if prepaid not in _VALID_STATUS:
            raise ValueError(
                "results: prepaid must be one of %r." % _VALID_STATUS)
        self._urldata.prepago = prepaid
        return self


class B3dsBuilder(WppBuilder):
    def __init__(self, parent: WppBuilder = None) -> None:
        super().__init__(parent)
        self._data3ds = objectify.Element("data3ds")

    def _getElement(self) -> objectify.ObjectifiedElement:
        return self._data3ds

    def email(self, email: str) -> "B3dsBuilder":
        self._data3ds.ml = email
        return self

    def phone(self, phone: str) -> "B3dsBuilder":
        self._data3ds.cl = phone
        return self

    def address(self, address: str) -> "B3dsBuilder":
        self._data3ds.dir = address
        return self

    def city(self, city: str) -> "B3dsBuilder":
        self._data3ds.cd = city
        return self

    def state(self, state: str) -> "B3dsBuilder":
        self._data3ds.est = state
        return self

    def zipCode(self, zipCode: str) -> "B3dsBuilder":
        self._data3ds.cp = zipCode
        return self

    def isoCountry(self, isoCountry: str) -> "B3dsBuilder":
        self._data3ds.idc = isoCountry
        return self


class AditionalDataArrayBuilder(WppBuilder):
    def __init__(self, parent: WppBuilder = None) -> None:
        super().__init__(parent)
        self._aditionalData = objectify.Element("datos_adicionales")

    def _getElement(self) -> objectify.ObjectifiedElement:
        return self._aditionalData

    def append(self, id: int, display: bool, label: str, value: str) -> "AditionalDataArrayBuilder":
        data = objectify.SubElement(self._aditionalData, "data")
        data.set("id", str(id))
        data.set("display", str(display).lower())
        data.label = label
        data.value = value
        return self


class PaymentBuilder(WppBuilder):
    def __init__(self, parent: WppBuilder = None) -> None:
        super().__init__(parent)
        self.__init_builders__()
        self._p = objectify.Element("P")
        self._p.business = None
        self._p.nb_fpago = None
        self._p.version = "IntegraWPP"
        self._p.url = None
        self._p.data3ds = None
        self._p.datos_adicionales = None

    def __init_builders__(self) -> None:
        self._businessBuilder = BusinessBuilder(self)
        self._urlBuilder = UrlBuilder(self)
        self._b3dsBuilder = B3dsBuilder(self)
        self._aditionalDataBuilder = AditionalDataArrayBuilder(self)

    def _getElement(self) -> objectify.ObjectifiedElement:
        return self._p

    def build(self) -> objectify.ObjectifiedElement:
        self._businessBuilder.build()
        self._urlBuilder.build()
        self._b3dsBuilder.build()
        self._aditionalDataBuilder.build()
        return self._p

    def withBusiness(self) -> BusinessBuilder:
        return self._businessBuilder

    def withUrl(self) -> UrlBuilder:
        return self._urlBuilder

    def withData3ds(self) -> B3dsBuilder:
        return self._b3dsBuilder

    def withAditionalData(self) -> AditionalDataArrayBuilder:
        return self._aditionalDataBuilder

    def paymentMethod(self, method: PaymentMethodType) -> "PaymentBuilder":
        self._p.nb_fpago = method.value
        return self


class _PgsBuilder_(WppBuilder):
    def __init__(self) -> None:
        super().__init__(None)
        self._pgs = objectify.Element("pgs")

    def _getElement(self) -> objectify.ObjectifiedElement:
        return self._pgs

    def data0(self, data: str) -> "_PgsBuilder_":
        self._pgs.data0 = data
        return self

    def data(self, data: str)-> "_PgsBuilder_":
        self._pgs.data = data
        return self
