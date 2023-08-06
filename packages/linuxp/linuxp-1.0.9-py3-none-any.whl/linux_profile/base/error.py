from linux_profile.utils.text import color
from linux_profile.base.log import run_app

LOG_APP = run_app(name_log='app')


class ErrorLoadSettings(Exception):

    def __init__(self):
        message = "It is not possible to load the basic settings."
        LOG_APP.error(message)
        super(ErrorLoadSettings, self).__init__(message)


class ErrorOptionIsMissing(Exception):

    def __init__(self, parameter):
        message = f"Option [{parameter}] is missing!"
        LOG_APP.error(message)
        super(ErrorOptionIsMissing, self).__init__(message)


class ErrorOptionIsInvalid(Exception):

    def __init__(self, parameter, options):
        message = f"Option [{parameter}] invalid! Usage: {str(options)}"
        LOG_APP.error(message)
        super(ErrorOptionIsInvalid, self).__init__(message)


class ErrorInvalidValue(Exception):

    def __init__(self, parameter):
        message = f"Option [{parameter}] invalid value!"
        LOG_APP.error(message)
        super(ErrorInvalidValue, self).__init__(message)


class ErrorParameterIsMissing(Exception):

    def __init__(self, parameter):
        message = f"Parameter --{parameter} is missing"
        LOG_APP.error(message)
        super(ErrorParameterIsMissing, self).__init__(message)


def print_warning(parameter):
    print(
        color(
            text="WARNING: " + parameter,
            types=['bold', 'yellow']
        )
    )


def print_error(parameter):
    print(
        color(
            text="ERROR: " + parameter,
            types=['bold', 'red']
        )
    )
