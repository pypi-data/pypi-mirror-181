# NQ SDK

## Abstract Provider Classes

Construct your provider class using base provider class `nqsdk.abstract.provider.Provider` and appropriate mixin classes depending on what functionality is supported by your provider.

All abstract methods must be implemented.

## `nqsdk.abstract.provider.Provider`

Base provider class. All providers must be inherited from it.

## `nqsdk.abstract.provider.HealthCheckMixin`

Use if your provider supports health check requests.

## `nqsdk.abstract.provider.BalanceCheckMixin`

Use if your provider supports user's balance check requests.

## `nqsdk.abstract.provider.DeliveryCheckMixin`

Use if your provider supports delivery check requests.

## `nqsdk.abstract.provider.AckCheckMixin`

Use if your provider supports ack check requests.

## `nqsdk.abstract.provider.CallbackHandleMixin`

Use if your provider supports callbacks from your API with no difference b/w `message delivered` & `message ack` events. E.g. all events are sent to the same URL & provider can distinguish them from callback's payload.

## `nqsdk.abstract.provider.DeliveryHandleMixin`

Use if your provider supports `message delivered` event callbacks sent to a specific URL provided by NQ service.

## `nqsdk.abstract.provider.AckHandleMixin`

Use if your provider supports `message ack` event callbacks sent to a specific URL provided by NQ service.

## Dummy Provider

`nqsdk.dummy.provider.DummyProvider` is a dummy implementation of NQ Provider Interface. It does nothing but can be used for tests.

You can find it at `dummy/provider.py`.

## Tests

Run tests locally:

```shell script
./scripts/tests
```
