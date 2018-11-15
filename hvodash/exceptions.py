# -*- coding: utf-8 -*-


class SlapdashBaseException(Exception):
    pass


class ValidationError(SlapdashBaseException):
    pass


class HaltCallback(SlapdashBaseException):
    pass
