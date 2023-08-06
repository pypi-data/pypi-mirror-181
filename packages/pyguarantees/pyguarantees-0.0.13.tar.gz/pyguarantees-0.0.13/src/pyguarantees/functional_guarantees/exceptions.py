from pyguarantees import severity


def _parse_what_dict(what_dict: dict, tabs: str = "\t") -> str:
    err_str = ""
    for key, val in what_dict.items():
        if type(val) is dict:
            err_str += f"{tabs}{key}: \n"
            err_str += _parse_what_dict(val, tabs + "\t")
        else:
            err_str += f"{tabs}{str(key)}: {str(val)} \n"

    return err_str


def construct_err_str(
        guarantee,
        parameter_name: str,
        what_dict: dict = None
) -> str:
    severity_str_dict = {
        severity.DEBUG: "DEBUG",
        severity.INFO: "INFO",
        severity.WARNING: "WARN",
        severity.ERROR: "ERROR",
        severity.CRITICAL: "FATAL"
    }
    err_str = f"\n\tWhere: \n"
    err_str += f"\t\tModule: {guarantee.module} \n"
    err_str += f"\t\tName: {guarantee.qualname} \n"
    err_str += f"\tSeverity: {severity_str_dict[guarantee.error_severity]} \n"
    err_str += f"\tGuarantee: {guarantee.guarantee_name} \n"
    err_str += f"\tParameter: {parameter_name} \n"
    err_str += _parse_what_dict(what_dict)
    return err_str


class ParameterGuaranteesValueError(ValueError):
    def __init__(
            self,
            guarantee,
            parameter_name="",
            what_dict=None
    ) -> None:
        self.guarantee = guarantee
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            guarantee=guarantee,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ParameterGuaranteesTypeError(TypeError):
    def __init__(
            self,
            guarantee,
            parameter_name="",
            what_dict=None
    ) -> None:
        self.guarantee = guarantee
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            guarantee=guarantee,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesValueError(ValueError):
    def __init__(
            self,
            guarantee,
            parameter_name="",
            what_dict=None
    ) -> None:
        self.guarantee = guarantee
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            guarantee=guarantee,
            parameter_name="return",
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesTypeError(TypeError):
    def __init__(
            self,
            guarantee,
            parameter_name="",
            what_dict=None
    ) -> None:
        self.guarantee = guarantee
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            guarantee=guarantee,
            parameter_name="return",
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserValueError(ValueError):
    def __init__(
            self,
            guarantee,
            parameter_name="",
            what_dict=None
    ) -> None:
        self.guarantee = guarantee
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            guarantee=guarantee,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserTypeError(TypeError):
    def __init__(
            self,
            guarantee,
            parameter_name="",
            what_dict=None
    ) -> None:
        self.guarantee = guarantee
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            guarantee=guarantee,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)
