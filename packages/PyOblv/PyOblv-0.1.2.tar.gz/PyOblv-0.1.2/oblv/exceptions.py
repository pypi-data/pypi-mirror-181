
def _exception_from_packed_args(exception_cls, args=None, kwargs=None):
    # This is helpful for reducing Exceptions that only accept kwargs as
    # only positional arguments can be provided for __reduce__
    # Ideally, this would also be a class method on the OblvError
    # but instance methods cannot be pickled.
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    return exception_cls(*args, **kwargs)


class OblvError(Exception):
    """
    The base exception class for Oblivious exceptions.

    :ivar msg: The descriptive message associated with the error.
    """

    fmt = 'An unspecified error occurred'

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs

    def __reduce__(self):
        return _exception_from_packed_args, (self.__class__, None, self.kwargs)


class HTTPClientError(OblvError):
    fmt = 'An HTTP Client raised an unhandled exception. Kindly raise a request to the support team, along with the {request_id} for resolution.'

    def __init__(self,request_id=""):
        super().__init__(request_id=request_id)

    # def __init__(self, request=None, response=None, **kwargs):
    #     self.request = request
    #     self.response = response
    #     super().__init__(**kwargs)

    # def __reduce__(self):
    #     return _exception_from_packed_args, (
    #         self.__class__,
    #         (self.request, self.response),
    #         self.kwargs,
    #     )


class ConnectionError(OblvError):
    fmt = 'An HTTP Client failed to establish a connection: {error}'

class MissingParametersError(OblvError):
    """
    One or more required parameters were not supplied.

    :ivar object: The object that has missing parameters.
        This can be an operation or a parameter (in the
        case of inner params).  The str() of this object
        will be used so it doesn't need to implement anything
        other than str().
    :ivar missing: The names of the missing parameters.
    """

    fmt = (
        'The following required parameters are missing for '
        '{object_name}: {missing}'
    )
    
    
    def __init__(self,object_name="",missing=""):
        super().__init__(object_name=object_name,missing=missing)


class ValidationError(OblvError):
    """
    An exception occurred validating parameters.

    Subclasses must accept a ``value`` and ``param``
    argument in their ``__init__``.

    :ivar value: The value that was being validated.
    :ivar param: The parameter that failed validation.
    :ivar type_name: The name of the underlying type.
    """

    fmt = "Invalid value ('{value}') for param {param} " "of type {type_name} "
    
    def __init__(self,value="",param="",type_name=""):
        super().__init__(value=value,param=param,type_name=type_name)


class ParamValidationError(OblvError):
    fmt = '{report}'

class MissingServiceIdError(OblvError):
    fmt = (
        "The model being used for the service {service_name} is missing the "
        "serviceId metadata property, which is required."
    )

    def __init__(self, service_name):
        super().__init__(service_name=service_name)
class UnauthorizedTokenError(OblvError):
    fmt = (
        "The session associated with this profile has expired or is "
        "otherwise invalid. To refresh this session use the authenticate method "
        "with the corresponding profile."
    )

class BadRequestError(OblvError):
    fmt = '{message}'
    
    def __init__(self,message=""):
        super().__init__(message=message)
    
class AuthenticationError(OblvError):
    fmt = 'Invalid credentials provided. Kindly verify the same and try again.'


class BadYamlData(OblvError):
    fmt = 'Validation failed for service yaml data with message - {message}'
    
    
    def __init__(self,message=""):
        super().__init__(message=message)
