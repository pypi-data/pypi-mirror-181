from typing import Union

from pyguarantees.exceptions.constraints import \
    ParameterGuaranteesTypeError, ParameterGuaranteesValueError, \
    ReturnGuaranteesValueError, ReturnGuaranteesTypeError, \
    FunctionalGuaranteesUserTypeError, FunctionalGuaranteesUserValueError

from pyguarantees import severity


class ErrorHandler:
    def __init__(
            self,
            where: str,
            type_or_value: str,
            guarantee,
            parameter_name: str,
            what_dict: dict
    ):
        self.guarantee = guarantee
        self.exception = self.make_exception(where, type_or_value, parameter_name, what_dict)

    def make_exception(
            self,
            where: str,
            type_or_value: str,
            parameter_name: str,
            what_dict: dict
    ) -> Union[
        ParameterGuaranteesTypeError,
        ParameterGuaranteesValueError,
        ReturnGuaranteesValueError,
        ReturnGuaranteesTypeError,
        FunctionalGuaranteesUserTypeError,
        FunctionalGuaranteesUserValueError
    ]:
        exception = ErrorHandler.choose_exception(where, type_or_value)
        return exception(
            guarantee=self.guarantee,
            parameter_name=parameter_name,
            what_dict=what_dict
        )

    @staticmethod
    def choose_exception(
            where: str,
            type_or_value: str
    ) -> Union[
        ParameterGuaranteesTypeError,
        ParameterGuaranteesValueError,
        ReturnGuaranteesValueError,
        ReturnGuaranteesTypeError,
        FunctionalGuaranteesUserTypeError,
        FunctionalGuaranteesUserValueError
    ]:
        exception_dict = {
            "parameter": {
                "type": ParameterGuaranteesTypeError,
                "value": ParameterGuaranteesValueError
            },
            "return": {
                "type": ReturnGuaranteesTypeError,
                "value": ReturnGuaranteesValueError
            },
            "internal": {
                "type": FunctionalGuaranteesUserTypeError,
                "value": FunctionalGuaranteesUserValueError
            }
        }

        return exception_dict[where][type_or_value]

    def output_exception(self):
        if self.guarantee is None:
            raise self.exception

        err_str = "\nThere was an error in pyguarantees.constraints: " + self.exception.err_str

        if self.guarantee.logger is not None:
            self._log(err_str)
            if self.guarantee.logger_only:
                return

        self._print_or_raise(err_str)

    def _log(self, err_str: str):
        if self.guarantee.error_severity == severity.DEBUG:
            self.guarantee.logger.debug(err_str)
        elif self.guarantee.error_severity == severity.INFO:
            self.guarantee.logger.info(err_str)
        elif self.guarantee.error_severity == severity.WARNING:
            self.guarantee.logger.warning(err_str)
        elif self.guarantee.error_severity == severity.ERROR:
            self.guarantee.logger.error(err_str)
        else:
            self.guarantee.logger.critical(err_str)

    def _print_or_raise(self, err_str):
        def esc(code):
            return f'\033[{code}m'

        if self.guarantee.error_severity == severity.DEBUG:
            print(esc(32) + err_str + esc(0))  # green
        elif self.guarantee.error_severity == severity.INFO:
            print(err_str)  # default
        elif self.guarantee.error_severity == severity.WARNING:
            print(esc(31) + err_str + esc(0))  # red
        else:
            raise self.exception


def handle_error(
        where: str,
        type_or_value: str,
        guarantee,
        parameter_name: str,
        what_dict: dict
) -> None:
    """
    Call this function when an error occurred.

    Creates the appropriate exception. If there is an `error_callback`,
    `handle_error` will call it with the exception. Else, it will handle it
    with the appropriate severity (printing for severity up to `severity.WARN`,
    raising the exception from there).

    Parameters
    __________

    where:  "parameter", "return", or "internal".
            Independent of the `guarantee` parameter, because that one can only
            include one of the first two options and `handle_error` should be
            usable for internal errors as well.

    type_or_value: "type" or "value".

    guarantee: The guarantee.

    parameter_name: The name of the parameter. Independent of `guarantee`
                    to make it usable for internal errors.

    what_dict:  A dictionary for all other information.
    """
    error_handler = ErrorHandler(where, type_or_value, guarantee, parameter_name, what_dict)

    if guarantee is not None and guarantee.error_callback is not None:
        guarantee.error_callback(error_handler.exception)
    elif guarantee is not None:
        error_handler.output_exception()
    else:
        raise error_handler.exception
