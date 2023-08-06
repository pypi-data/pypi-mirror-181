# The Healthz System

## Introduction

The healthz system is responsible for monitoring our services. Services can also indicate if a hardware component is
working properly or is reporting an error. Thus, a developer may consider two variants of checks:

* Software checks: These are checks that are checking about an erroneous state of the software: e.g. database
  inconsistent, something is misconfiguration, etc. These checks are not visible to the customer.
* Hardware checks: These are checks that are checking about a hardware component: e.g. Camera disconnected, the cash
  register is full, etc. These checks are visible to the customer.

A service which is not responding to healthz requests will be considered crashing. If a service has a parent hardware
component, e.g. the alpr service has the camera as its parent, then the alpr service is considered the "driver" of the
hardware component. If te driver of the hardware component is not running (i.e. it is crashing, or non-responsive), then
no checks will be visible or processed for the hardware component.

All checks should be registered as soon as possible (i.e. on startup). Before the check is firing or cleared it is
in the state "no-data" as we cannot decide it's state until the service has set it's state once.

## About Hardware Packages and Drivers

Every hardware component requires a so called "driver" which is the main indicator if the device is running.
A service is a driver for a hardware package if has it set as it's `PARENT`.

#### Services which are driver for multiple hardware packages

Due to limitations in the package format, we currently hack this by manually mapping such services to multiple hardware
packages. This is done in the health
poller [in service-misc/health.py](https://gitlab.com/accessio/openmodule/service-misc/-/blob/v2/src/refactor/health.py#L39)
.

## Examples

### Hardware check for my parent package

You would use this setup if you have 1 parent hardware package for which you are soley responsible

```python
core = init_openmodule(settings)
core.health.add_check("connected", "Camera Connection",
                      "This check monitors if the camera is connected and we receive a videostream.",
                      parent=True)  # note parent=True is the equivalent to "package=core.settings.PARENT"

while True:
    try:
        connect()
        core.health.check_success("connected", parent=True)  # after connecting we clear the check
        while is_connected():
            receive_images()
    except NetworkError:
        core.health.check_fail("connected", parent=True)  # we have lost connection -> fire the check!
        close_connection()

```

### Hardware check for a different hardware package

You would use this setup if you have some service which can detect errors at other hardware component, and this
component will always stay the same. E.g. the tracking service fires an check for it's camera.

```python

core = init_openmodule(settings)
tracking_config = load_config()

core.health.add_check("detection-rate", "Detection Rate",
                      "This check monitors if we are detecting license plates when vehicles are passing though.",
                      package=tracking_config.source_camera)

while True:
    do_tracking_stuff()
    if detection_rate < 0.9:
        core.health.check_fail("detection-rate", package=tracking_config.source_camera,
                               message=f"Detection may be as low as {(detection_rate * 100):.2f}%")
    else:
        core.health.check_success("detection-rate", package=tracking_config.source_camera)
```

### Hardware check for a dynamic number of hardware packages

You would use this setup if you have some service which can detect errors at other hardware components. For
example the camoperator could check an error condition for all cameras, but the number of cameras will
change during the runtime of the service.

**Note** in this case you may also want to read
about [services which are driver for multiple hardware packages](#services-which-are-driver-for-multiple-hardware-packages)

```python
core = init_openmodule(settings)
core.health.add_check_template("position-alarm", "Position Alarm",
                               "This check monitors if the camera was moved via the camera's position alarm function.")

while True:
    cameras_i_monitor = get_monitored_cameras()  # ["hw_avigilon_h5bullet_1", "hw_avigilon_h5bullet_2"]
    core.health.update_template_packages("position-alarm", packages=cameras_i_monitor)

    for camera in cameras_i_monitor:
        if camera_was_moved(camera):
            core.health.check_fail("position-alarm", package=camera)
        else:
            core.health.check_success("position-alarm", package=camera)
```

### Software checks for myself

You would use this for example if you have detected a software issue which warrants an check. Note that
in this case the service **must not** crash after setting the check, as it needs to be running in order
for checks to be processed. If it is so bad that you crash, you should rather just send a sentry exception and crash.

```python
core = init_openmodule(settings)
core.health.add_check("update-error", "Update Error",
                      "The updater fires this check if it is unable to install updates.")

try:
    update_software()
    core.health.check_success("update-error")
except Exception as e:
    core.health.check_fail("update-error", message=str(e))
```

## Technical details and quirks

* The `message` of an check is only displayed if the check is firing. While always the last message will be shown to the
  user, no effort is made to check if the message has changed (i.e. notify the user a second time if a different message
  occurs). So you probably only want to have one message.

* Some services are parent for multiple hardware devices, this is hot-fixed in service-misc which holds a list of
  such services and then constructs the health status accordingly. See "Hardware check for multiple parent packages".

* The difference between being the driver or not the driver of a package is that as described above the hardware
  component will be considered completely offline if the driver is not running. So for a high time check that some
  other service does, we do not consider it the "driver".

* checks are polled, so firing an check and crashing won't do much, it will just show your service as crashing.
* The `status` in `pong` is "error" if any check is status "fail" (not if "no_data"). There is also `message` in pong 
  which is set to the message of the first failed check.
