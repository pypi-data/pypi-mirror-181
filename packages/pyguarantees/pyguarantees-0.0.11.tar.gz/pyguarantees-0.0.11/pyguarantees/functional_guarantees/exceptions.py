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
        qualname: str,
        module: str,
        guarantee_name: str,
        parameter_name: str,
        error_severity: int,
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
    err_str += f"\t\tModule: {module} \n"
    err_str += f"\t\tName: {qualname} \n"
    err_str += f"\tSeverity: {severity_str_dict[error_severity]} \n"
    err_str += f"\tGuarantee: {guarantee_name} \n"
    err_str += f"\tParameter: {parameter_name} \n"
    err_str += _parse_what_dict(what_dict)
    return err_str


class ParameterGuaranteesValueError(ValueError):
    def __init__(
            self,
            qualname="",
            module="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.qualname = qualname
        self.module = module
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            qualname=qualname,
            module=module,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ParameterGuaranteesTypeError(TypeError):
    def __init__(
            self,
            qualname="",
            module="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.qualname = qualname
        self.module = module
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            qualname=qualname,
            module=module,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesValueError(ValueError):
    def __init__(
            self,
            qualname="",
            module="",
            guarantee_name="",
            parameter_name="return",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.qualname = qualname
        self.module = module
        self.guarantee_name = guarantee_name
        parameter_name = "return"
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            qualname=qualname,
            module=module,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesTypeError(TypeError):
    def __init__(
            self,
            qualname="",
            module="",
            guarantee_name="",
            parameter_name="return",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.qualname = qualname
        self.module = module
        self.guarantee_name = guarantee_name
        parameter_name = "return"
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            qualname=qualname,
            module=module,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserValueError(ValueError):
    def __init__(
            self,
            qualname="",
            module="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.qualname = qualname
        self.module = module
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            qualname=qualname,
            module=module,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserTypeError(TypeError):
    def __init__(
            self,
            qualname="",
            module="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.qualname = qualname
        self.module = module
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            qualname=qualname,
            module=module,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)
