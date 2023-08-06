# Openmodule Testing
We provide multiple Mixins and Util classes for test purposes in openmodule-test.

::: warning
You need to set the environment variable TESTING=True for all tests!
:::


## Settings

The ZMQTestMixin already sets the settings up for you with the module defined in `src/config`.
* if you want to use the `tcp://` protocol, set the protocol variable and the mixin sets them automatically

To customize the settings during testing you have 3 options:

```python
# class decorator
@override_settings(A="B")
class Test(ZMQTestMixin):

    # function decorator
    @override_settings(B="C")
    def test(self):
        self.assertEqual("B", settings.A)
        self.assertEqual("C", settings.B)

        # context
        with override_context(B="A"):
            self.assertEqual("A", settings.B)
        self.assertEqual("C", settings.B)
```

The ZMQTestMixin also provides automatic settings override with the `zmq_config(**kwargs)` method

## Mixin
### OpenModuleCoreTestMixin 
Mixin for automatic core generation including health test utils and zmq utils 

```python
class Test(OpenModuleCoreTestMixin):
    topics = ["healthpong"]
```

### RPCServerTestMixin
Mixin providing rpc and messaging functionality 
```python
class Test(OpenModuleCoreTestMixin, RPCServerTestMixin):
    rpc_channels = ["backend"]
    
    def setUp(self):
        super().setUp()
        self.server = RPCServer(config=self.zmq_config(), context=self.zmq_context())
        self.server.run_as_thread()
        # register rpcs here
        self.server.register_handler("test", "dummy", OpenModuleModel, OpenModuleModel, self.dummy_callback)
        self.wait_for_rpc_server(self.server)

    def dummy_callback(self, request: OpenModuleModel, _) -> OpenModuleModel:
        """
        dummy callback. docs string MUST NOT be forgotten
        """
        return OpenModuleModel()
    
    def tearDown(self):
        self.server.shutdown()
        super().tearDown()
```

### SQLiteTestMixin 
Mixin that takes a database or creates one and cleans it up after each test.
```python
# base database that gets reset
class Test(SQLiteTestMixin):
    pass

# use other database
class Test(SQLiteTestMixin, OpenModuleCoreTestMixin):
    create_database = False
    init_kwargs = dict(database=True)
    
    def setUp(self):
        super().setUp()
        self.database = self.core.database
```

### AlertTestMixin 
Mixin to for dealing with alerts
```python
class AlertTestCase(AlertTestMixin):
    topics = ["alert"]
```
    
### BackendTestMixin 
Mixin with core creation, backend creation and backend util functions
```python
class Test(BackendTestMixin):
    backend_class = Backend
```

### HealthTestMixin 
Mixin for receiving and checking health status, included in CoreMixin
```python
class Test(HealthTestMixin):
    topics = ["healthpong"]
```


## Utils
### ApiMocker 
Base mocker class for simulating http requests
```python
class Mocker(ApiMocker):
    host = config.SERVER_URL
    def mock(self):
        def cb(request, context):
            return {}
        self.mocker.get(self.server_url("abc"), json=cb)

class Test(TestCase):
    @requests_mock.Mocker(real_http=False)
    def test_check_in_out(self, m):
        res = requests.get(config.host+"abc")
```

### MockEvent 
Check if function was called, i.e. in a listener -> do not forget resetting
```python
event = MockEvent()
some_event_listener.append(event)
do_trigger_event()
event.wait_for_call()
event.reset_call_count()
```

### VehicleBuilder 
Util class for generating vehicles
```python
vehicle = VehicleBuilder().lpr("A", "G ARIVO1")
```

### PresenceSimulator 
Util class for simulating presence messages
```python
presence_sim = PresenceSimulator("gate_in", Direction.IN, lambda x: self.zmq_client.send("presence", x))
presence_listener = PresenceListener(core.messages)
on_enter = MockEvent()
presence_listener.on_enter.append(on_enter)
presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
on_enter.wait_for_call()
```

### MockRPCClient
This is a fake RPCClient where you can either specify callback functions for RPCs or even the responses. 
It returns the result of the matching callback, if available, otherwise the value in the matching response else 
raises TimeoutError.
```python
def callback(res: SomeRequest, _):
    return SomeResponse()

rpc_client=MockRPCClient(callbacks={("channel", "type"): callback}, 
                         responses={("channel2", "type2"): SomeResponse2})
res = rpc_client.rpc("channel", "type", SomeRequest(), SomeResponse)  # returns result of callback
future = rpc_client.rpc_non_blocking("channel2", "type2", SomeRequest())  # returns result of callback
res = future.result(SomeResponse2)  # returns value of rpc_client.responses[("channel2", "type2")]

rpc_client.responses = {("channel2", "type2"): SomeResponse2}}  # you can edit responses and callbacks after creation
```

For integration test you can replace the RPCClient of the core
```python
core().rpc_client = MockRPCClient()
```

## Main Test
Minimal Example
```python
class MainTest(MainTestMixin):
    def test_keyboard(self):
        output = self.signal_in_function(main_wrapper, KeyboardInterrupt, raise_exception_after=2, shutdown_timeout=5)
        self.assertIn("Shutdown finished", output)
```
If you want to send RPCs to the app in testing or interact in another way: Either copy code in `signal_in_function` and 
add your stuff after `wait_for_setup` or start a thread before `signal_in_function` and do your stuff there after a 
short sleep. 

## Exit with Error 112
Whenever the RPCServer finds a RPCResponse model containing a `status` field, a log line is printed and the process is
terminated with error code 112. The log line might not be printed in some cases, so watch out for 112
