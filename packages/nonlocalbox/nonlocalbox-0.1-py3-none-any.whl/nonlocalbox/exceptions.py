class NonlocalBoxExceptions(Exception):
    ...


class ServiceError(NonlocalBoxExceptions):
    ...


class StatusError(NonlocalBoxExceptions):
    ...


class UninitializedBoxError(NonlocalBoxExceptions):
    ...
