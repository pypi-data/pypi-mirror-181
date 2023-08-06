import logging
from collections import namedtuple
from datetime import datetime
from enum import Enum
from typing import Optional, Callable, Union, List, Dict, Tuple, Set
from typing import TYPE_CHECKING

from pydantic import Field

from openmodule.models.base import ZMQMessage, OpenModuleModel, datetime_to_timestamp, timezone_validator

if TYPE_CHECKING:  # pragma: no cover
    from openmodule.core import OpenModuleCore


class HealthPongPayload(OpenModuleModel):
    status: str = "ok"
    version: str
    name: str
    startup: datetime
    message: Optional[str]

    _tz_last_update = timezone_validator("startup")

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data["startup"] = datetime_to_timestamp(data["startup"])
        return data


class HealthMetricType(str, Enum):
    count: str = "count"
    gauge: str = "gauge"
    str: str = "str"


class HealthMetric(OpenModuleModel):
    description: str
    type: HealthMetricType
    value: Union[float, int, str]
    package: str
    source: Optional[str]


class HealthCheckState(str, Enum):
    ok = "ok"
    fail = "fail"
    no_data = "no-data"


class HealthCheck(OpenModuleModel):
    id: str = Field(..., description="A identifier for this check. Must be unique per `package` this check is "
                                     "assigned to, independently of the source service which is returning the check.")
    package: str = Field(..., description="The package this check is assigned to. It may be your own service"
                                          "but can also be any other hardware or software service.")
    state: HealthCheckState = Field("no-data", description="The state of this check")
    name: str = Field(..., description="Human readable name of the check. ")
    description: Optional[str] = Field(...,
                                       description="Human-readable description of the check. The same description"
                                                   "will be displayed when the check fails or succeeds. Consider this"
                                                   "when coosing the wording.")
    message: Optional[str] = Field(None,
                                   description="A human readable text which is displayed next to the check in the "
                                               "user interface. Can be used to convey more information. Please "
                                               "note that no efforts are taken to notify the user about changes "
                                               "in this value (i.e. no new e-mails are sent if the message "
                                               "changes).")
    source: Optional[str] = Field(None,
                                  description="The service which reported the health check. This value is "
                                              "automatically set by health service and must not be set manually.")


class HealthPongMessage(ZMQMessage):
    type: str = "healthz"
    pong: HealthPongPayload
    metrics: Optional[List[HealthMetric]]
    checks: Optional[List[HealthCheck]]


class HealthPingMessage(ZMQMessage):
    type: str = "ping"


startup = datetime.utcnow()

HealthResult = namedtuple("HealthResult", "status,message,meta")

HealthHandlerType = Callable[[], HealthResult]


class Healthz:
    health_handler: HealthHandlerType

    templates: Dict[str, Tuple[str, str]] = {}
    metrics: Dict[Tuple[str, str], HealthMetric] = {}
    checks: Dict[Tuple[str, str], HealthCheck] = {}

    def __init__(self, core: 'OpenModuleCore'):
        self.core = core
        self.log = logging.getLogger(self.__class__.__name__)
        self.metrics = {}
        self.checks = {}

    def _check_id(self, check_id: str, parent: Optional[bool] = False, package: Optional[str] = None):
        if parent:
            package = self.core.config.PARENT
            assert package, "no parent is set"
        else:
            package = package or self.core.config.NAME
        return check_id, package

    def add_check_template(self, check_id: str, name: str, description: str = None):
        self.templates[check_id] = (name, description)

    def update_template_packages(self, check_id: str, packages: Union[List[str], Set[str]]):
        existing_packages = set(x[1] for x in self.checks if x[0] == check_id)
        packages_set = set(packages)
        for package in existing_packages - packages_set:
            self.checks.pop((check_id, package))
        for package in packages_set - existing_packages:
            name, description = self.templates[check_id]
            self.add_check(check_id, name, description, package=package)

    def add_check(self, check_id: str, name: str, description: str, *, parent: Optional[bool] = False,
                  package: Optional[str] = None):
        key = self._check_id(check_id, parent, package)
        self.checks[key] = HealthCheck(
            id=check_id,
            package=key[1],
            name=name,
            description=description,
            state=HealthCheckState.no_data
        )

    def remove_check(self, check_id, *, parent: Optional[bool] = False, package: Optional[str] = None):
        key = self._check_id(check_id, parent, package)
        self.checks.pop(key, None)

    def set_check_state(self, check_id: str, state: HealthCheckState, *, parent: Optional[bool] = False,
                        package: Optional[str] = None, message: Optional[str] = None):
        key = self._check_id(check_id, parent, package)
        check = self.checks.get(key)
        if check:
            check.state = state
            if state == HealthCheckState.fail:
                check.message = message
            else:
                check.message = None
        else:
            if self.core.config.DEBUG or self.core.config.TESTING:
                assert False, "please ensure you register your checks properly beforehand"
            self.log.warning(f"Check {key} not found, the check state will not be set")

    def check_fail(self, check_id: str, *, parent: Optional[bool] = False, package: Optional[str] = None,
                   message: Optional[str] = None):
        self.set_check_state(check_id, HealthCheckState.fail, parent=parent, package=package, message=message)

    def check_success(self, check_id: str, *, parent: Optional[bool] = False, package: Optional[str] = None,
                      message: Optional[str] = None):
        self.set_check_state(check_id, HealthCheckState.ok, parent=parent, package=package, message=message)

    def process_message(self, _: HealthPingMessage):
        checks = list(self.checks.values())
        status = "ok"
        message = None
        for check in checks:
            if check.state == HealthCheckState.fail:
                status = "error"
                message = check.message
        response = HealthPongMessage(
            name=self.core.config.NAME,
            pong=HealthPongPayload(status=status, version=self.core.config.VERSION, name=self.core.config.NAME,
                                   startup=startup, message=message),
            checks=checks
        )
        self.core.publish(response, "healthpong")
