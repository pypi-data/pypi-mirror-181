'''
# replace this# data-cdk-constructs
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs as _constructs_77d1e7e8


class MyConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="data-cdk-constructs.MyConstruct",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a408c7178dc4cdfacd1a17035933586b3f43677a18bb3a720c605cdbf5a41a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


class NotifyingBucket(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="data-cdk-constructs.NotifyingBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc79e836f0e792fa027dc68106c2f3443073c321c09ca8a5b44d6e2fc230110a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NotifyingBucketProps(prefix=prefix)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="data-cdk-constructs.NotifyingBucketProps",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class NotifyingBucketProps:
    def __init__(self, *, prefix: typing.Optional[builtins.str] = None) -> None:
        '''
        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbac71290b24c17b418acab42f56529b0a6ecf4bfd0332adca3ab67eb845056)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotifyingBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MyConstruct",
    "NotifyingBucket",
    "NotifyingBucketProps",
]

publication.publish()

def _typecheckingstub__d2a408c7178dc4cdfacd1a17035933586b3f43677a18bb3a720c605cdbf5a41a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc79e836f0e792fa027dc68106c2f3443073c321c09ca8a5b44d6e2fc230110a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbac71290b24c17b418acab42f56529b0a6ecf4bfd0332adca3ab67eb845056(
    *,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
