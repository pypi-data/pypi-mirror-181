from tkinter.messagebox import NO
from typing import List, TypeVar, Generic
from lxml import objectify


class Result:
    def __init__(self) -> None:
        self.message = ""

    def ok() -> "Result":
        r = Result()
        r.ok = True
        return r

    def error(msg: str) -> "Result":
        r = Result()
        r.ok = False
        r.message = msg
        return r


T = TypeVar("T")


def isValidator(value: any) -> bool:
    return isinstance(value, IValidator)


class IValidator(Generic[T]):
    def go(self, value: T) -> Result:
        ...


class CommonValidator(IValidator[T]):
    def __init__(self) -> None:
        self._rules = []
        self._optional = False

    def optional(self, flag: bool) -> "CommonValidator":
        self._optional = flag
        return self

    def equals(self, param: T) -> "CommonValidator":
        self._rules.append(lambda s: Result.ok() if s == param else Result.error(
            "Value was expected to be {}, but was {}".format(param, s)))
        return self

    def notEquals(self, param: T) -> "CommonValidator":
        self._rules.append(lambda s: Result.ok() if s != param else Result.error(
            "Value must not be {}".format(param)))
        return self

    def minLength(self, param: int) -> "CommonValidator":
        self._rules.append(lambda s: Result.ok() if len(str(s)) >= param else Result.error(
            "Length must be greater than or equal to {} but was {}".format(
                param, len(str(s)))
        ))
        return self

    def maxLength(self, param: int) -> "CommonValidator":
        self._rules.append(lambda s: Result.ok() if len(str(s)) <= param else Result.error(
            "Length must be less than or equal to {} but was {}".format(
                param, len(str(s)))
        ))
        return self

    def notEmpty(self) -> "CommonValidator":
        self.minLength(1)
        return self

    def empty(self) -> "CommonValidator":
        self.maxLength(0)
        return self

    def exists(self, *values: T) -> "CommonValidator":
        self._rules.append(lambda s: Result.ok() if s in values else Result.error(
            "Value was expected to be one of {}".format(values)
        ))
        return self

    def go(self, value: T) -> Result:
        result = Result.ok()
        if value is None:
            if self._optional:
                return result
            else:
                return Result.error("None value received")

        for rule in self._rules:
            result = rule(value)
            if result.ok == False:
                break
        return result


class StringValidator(CommonValidator[str]):
    ...


class NumberValidator(CommonValidator[int]):
    ...


class FloatValidator(CommonValidator[float]):
    ...

class AttributeValidator(CommonValidator[T]):

    def element(self, elemName: str, validator: IValidator) -> "AttributeValidator":
        self._rules.append(lambda item: validator.go(item.__dict__[elemName]) )
        return self

    def attribute(self, attribName: str, validator: IValidator) -> "AttributeValidator":
        self._rules.append(lambda item: validator.go(item.get(attribName)) )
        return self

    def go(self, value: T) -> Result:
        return super().go(value)

class ShapeValidator(IValidator[T]):
    def __init__(self) -> None:
        self._optional = False

    def optional(self, flag: bool) -> "ShapeValidator":
        self._optional = flag
        return self

    def go(self, value: T) -> Result:
        result = Result.ok()
        expectedKeys = self.__dict__.keys()
        actualKeys = value.__dict__.keys()

        for key in expectedKeys:
            validator = self.__dict__[key]
            if isinstance(validator, IValidator) == False:
                continue
            if key not in actualKeys:
                if  validator._optional == False:
                    return Result.error("Value is missing expected property {}".format(key))
                else:
                    continue
            result = validator.go(value.__dict__[key])
            if result.ok == False:
                result.message = "{}. ".format(key) + result.message
                break
        return result


class ArrayValidator(IValidator[T]):
    def optional(self, flag: bool) -> "ArrayValidator":
        self._optional = flag
        return self

    def go(self, value: T) -> Result:

        expectedKeys = self.__dict__.keys()
        output = Result.ok()
        for item in value:
            output = self._validate(item, expectedKeys)
            if output.ok == False:
                return output
        return output

    def _validate(self, item: T, expectedKeys: List[any]) -> Result:
        result = Result.ok()
        actualKeys = item.__dict__.keys()
        for key in expectedKeys:
            validator = self.__dict__[key]
            if isinstance(validator, IValidator) == False:
                continue
            if key not in actualKeys and validator._optional == False:
                return Result.error("Value is missing expected property {}".format(key))
            result = validator.go(item.__dict__[key])
            if result.ok == False:
                result.message = "{}. ".format(key) + result.message
                break
        return result


class PaymentValidator:
    def __init__(self) -> None:
        self.validator = self._buildValidator()

    def _businessValidator(self) -> ShapeValidator:
        bVal = ShapeValidator()
        bVal.id_company = StringValidator().minLength(4).maxLength(4)
        bVal.id_branch = StringValidator().notEmpty().minLength(1).maxLength(11)
        bVal.user = StringValidator().notEmpty().minLength(8).maxLength(11)
        bVal.pwd = StringValidator().notEmpty().minLength(1).maxLength(80)
        return bVal

    def _urlValidator(self) -> ShapeValidator:
        uVal = ShapeValidator()
        uVal.reference = StringValidator().notEmpty().minLength(1).maxLength(50)
        uVal.amount = NumberValidator().notEmpty().minLength(1).maxLength(11)
        uVal.moneda = StringValidator().notEmpty().exists('MXN', 'USD')
        uVal.canal = StringValidator().notEmpty().equals('W')
        uVal.omitir_notif_default = NumberValidator().optional(True).exists(0, 1)
        uVal.promociones = StringValidator().optional(True).maxLength(40)
        uVal.id_promotion = StringValidator().optional(True).maxLength(12)
        uVal.st_correo = NumberValidator().optional(True).exists(0, 1)
        uVal.fh_vigencia = StringValidator().optional(
            True).minLength(10).maxLength(14)
        uVal.mail_cliente = StringValidator().optional(True).maxLength(100)
        uVal.prepago = NumberValidator().optional(True).exists(0, 1)
        return uVal

    def _3dsValidator(self) -> ShapeValidator:
        dsVal = ShapeValidator().optional(True)
        dsVal.ml = StringValidator().notEmpty().minLength(1).maxLength(100)
        dsVal.cl = StringValidator().notEmpty().minLength(1).maxLength(20)
        dsVal.dir = StringValidator().maxLength(60)
        dsVal.cd = StringValidator().maxLength(30)
        dsVal.est = StringValidator().minLength(2).maxLength(2)
        dsVal.cp = StringValidator().maxLength(10)
        dsVal.idc = StringValidator().minLength(3).maxLength(3)
        return dsVal

    def _datoAdicionalValidator(self) -> ArrayValidator:
        # dataVal = ArrayValidator().optional(True)
        
        # dataVal.id = NumberValidator().notEmpty()
        # dataVal.display = CommonValidator().notEmpty()
        # dataVal.label = StringValidator().notEmpty().minLength(1).maxLength(30)
        # dataVal.value = StringValidator().notEmpty().minLength(1).maxLength(100)
        # addVal = ShapeValidator()
        # addVal.data = dataVal
        # return addVal
        
        addVal = ArrayValidator().optional(True)
        attVal = AttributeValidator().attribute("id", NumberValidator().notEmpty()).attribute("display", 
            CommonValidator().notEmpty()).element("label", StringValidator().notEmpty().minLength(1).maxLength(30)
            ).element("value", StringValidator().notEmpty().minLength(1).maxLength(100))
        addVal.data = attVal
        return addVal

    def _buildValidator(self) -> ShapeValidator:
        payVal = ShapeValidator()
        payVal.business = self._businessValidator()
        payVal.nb_fpago = StringValidator().optional(True).exists(
            'GPY', 'APY', 'C2P', 'COD', 'TCD', 'BNPL')
        payVal.version = StringValidator().notEmpty().equals('IntegraWPP')
        payVal.url = self._urlValidator()
        payVal.data3ds = self._3dsValidator()
        payVal.datos_adicionales = self._datoAdicionalValidator()
        return payVal

    def validate(self, payment: objectify.ObjectifiedElement) -> Result:
        return self.validator.go(payment)
