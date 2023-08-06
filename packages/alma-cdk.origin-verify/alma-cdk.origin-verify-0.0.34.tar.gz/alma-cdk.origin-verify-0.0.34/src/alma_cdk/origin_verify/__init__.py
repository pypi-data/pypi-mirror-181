'''
<div align="center">
	<br/>
	<br/>
  <h1>
	<img height="140" src="assets/alma-cdk-origin-verify.svg" alt="Alma CDK Origin Verify" />
  <br/>
  <br/>
  </h1>

```sh
npm i -D @alma-cdk/origin-verify
```

  <div align="left">

Enforce API Gateway REST API, AppSync GraphQL API, or Application Load Balancer traffic via CloudFront by generating a Secrets Manager secret value which is used as a CloudFront Origin Custom header and a WAFv2 WebACL header match rule.

  </div>
  <br/>
</div><br/>

![diagram](assets/diagram.svg)

<br/>

Essentially this is an implementation of *AWS Solution* “[Enhance Amazon CloudFront Origin Security with AWS WAF and AWS Secrets Manager](https://aws.amazon.com/blogs/security/how-to-enhance-amazon-cloudfront-origin-security-with-aws-waf-and-aws-secrets-manager/)” without the secret rotation.

<br/>

## 🚧   Project Stability

![experimental](https://img.shields.io/badge/stability-experimental-yellow)

This construct is still versioned with `v0` major version and breaking changes might be introduced if necessary (without a major version bump), though we aim to keep the API as stable as possible (even within `v0` development). We aim to publish `v1.0.0` soon and after that breaking changes will be introduced via major version bumps.

<br/>

## Getting Started

```python
import { OriginVerify } from '@alma-cdk/origin-verify';
import { Distribution } from 'aws-cdk-lib/aws-cloudfront';
```

```python
const api: RestApi; // TODO: implement the RestApi
const apiDomain: string; // TODO: implement the domain

const verification = new OriginVerify(this, 'OriginVerify', {
  origin: api.deploymentStage,
});

new Distribution(this, 'CDN', {
  defaultBehavior: {
    origin: new HttpOrigin(apiDomain, {
      customHeaders: {
        [verification.headerName]: verification.headerValue,
      },
      protocolPolicy: OriginProtocolPolicy.HTTPS_ONLY,
    })
  },
})
```

For more detailed example usage see [`/examples`](https://github.com/alma-cdk/origin-verify/tree/main/examples/) directory.

<br/>

## Custom Secret Value

Additionally, you may pass in custom `secretValue` if you don't want to use a generated secret (which you should use in most cases):

```python
const myCustomValue = SecretValue.unsafePlainText('foobar');

const verification = new OriginVerify(this, 'OriginVerify', {
  origin: api.deploymentStage,
  secretValue: myCustomValue,
});
```

<br/>

## Notes

### Use `OriginProtocolPolicy.HTTPS_ONLY`!

In your CloudFront distribution Origin configuration use `OriginProtocolPolicy.HTTPS_ONLY` to avoid exposing the `verification.headerValue` secret to the world.

### Why `secretValue.unsafeUnwrap()`?

Internally this construct creates the `headerValue` by using AWS Secrets Manager but the secret value is exposed directly by using `secretValue.unsafeUnwrap()` method: This is:

* **required**, because we must be able to set it into the WAFv2 WebACL rule
* **required**, because you must be able to set it into the CloudFront Origin Custom Header
* **okay**, because it's meant to protect the API externally and it's *not* considered as a secret that should be kept – well – secret within *your* AWS account
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

import aws_cdk
import aws_cdk.aws_apigateway
import aws_cdk.aws_appsync
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_wafv2
import constructs


@jsii.interface(jsii_type="@alma-cdk/origin-verify.IVerification")
class IVerification(typing_extensions.Protocol):
    '''(experimental) Interface describing the "contract" of return values from the constructor.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        '''(experimental) CloudFront Origin Custom Header name used in the WAFv2 WebACL verification.

        :default: 'x-origin-verify'

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        '''(experimental) Secret Value used as the CloudFront Origin Custom Header value.

        :stability: experimental

        Example::

            'xxxxEXAMPLESECRET'
        '''
        ...


class _IVerificationProxy:
    '''(experimental) Interface describing the "contract" of return values from the constructor.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@alma-cdk/origin-verify.IVerification"

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        '''(experimental) CloudFront Origin Custom Header name used in the WAFv2 WebACL verification.

        :default: 'x-origin-verify'

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        '''(experimental) Secret Value used as the CloudFront Origin Custom Header value.

        :stability: experimental

        Example::

            'xxxxEXAMPLESECRET'
        '''
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVerification).__jsii_proxy_class__ = lambda : _IVerificationProxy


@jsii.implements(IVerification)
class OriginVerify(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alma-cdk/origin-verify.OriginVerify",
):
    '''(experimental) Associates an origin with WAFv2 WebACL to verify traffic contains specific header with a secret value.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        origin: typing.Union[aws_cdk.aws_apigateway.IStage, aws_cdk.aws_appsync.CfnGraphQLApi, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancer],
        acl_metric_name: typing.Optional[builtins.str] = None,
        header_name: typing.Optional[builtins.str] = None,
        rule_metric_name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_wafv2.CfnWebACL.RuleProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]] = None,
        secret_value: typing.Optional[aws_cdk.SecretValue] = None,
    ) -> None:
        '''(experimental) Associates an origin with WAFv2 WebACL to verify traffic contains specific header with a secret value.

        Use ``verifyHeader`` value to assign custom headers into CloudFront config.

        :param scope: -
        :param id: -
        :param origin: (experimental) Origin to protect. Accepted types: - ``IStage`` (from ``aws-cdk-lib/aws-apigateway``) - ``IApplicationLoadBalancer`` (from ``aws-cdk-lib/aws-elasticloadbalancingv2``)
        :param acl_metric_name: (experimental) Metric name for the WebACL. Default: 'OriginVerifyWebAcl'
        :param header_name: (experimental) By default ``x-origin-verify`` is used. To override it, provide a value for this. Recommendation is to use something with a ``x-`` prefix. Default: 'x-origin-verify'
        :param rule_metric_name: (experimental) Metric name for the allowed requests. Default: 'OriginVerifyAllowedRequests'
        :param rules: (experimental) Any additional rules to add into the created WAFv2 WebACL.
        :param secret_value: (experimental) The secret which is used to verify the CloudFront distribution. Optional: By default this construct will generate a ``new Secret``. Default: new Secret().secretValue

        :stability: experimental

        Example::

            import { OriginVerify } from '@alma-cdk/origin-verify';
            import { Distribution } from 'aws-cdk-lib/aws-cloudfront';
            
            const api: RestApi; // TODO: implement the RestApi
            const apiDomain: string; // TODO: implement the domain
            
            const verification = new OriginVerify(this, 'OriginVerify', {
            origin: api.deploymentStage,
            });
            
            new Distribution(this, 'CDN', {
            defaultBehavior: {
            origin: new HttpOrigin(apiDomain, {
            customHeaders: {
            [verification.headerName]: verification.headerValue,
            },
            protocolPolicy: OriginProtocolPolicy.HTTPS_ONLY,
            })
            },
            })
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                origin: typing.Union[aws_cdk.aws_apigateway.IStage, aws_cdk.aws_appsync.CfnGraphQLApi, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancer],
                acl_metric_name: typing.Optional[builtins.str] = None,
                header_name: typing.Optional[builtins.str] = None,
                rule_metric_name: typing.Optional[builtins.str] = None,
                rules: typing.Optional[typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_wafv2.CfnWebACL.RuleProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]] = None,
                secret_value: typing.Optional[aws_cdk.SecretValue] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = OriginVerifyProps(
            origin=origin,
            acl_metric_name=acl_metric_name,
            header_name=header_name,
            rule_metric_name=rule_metric_name,
            rules=rules,
            secret_value=secret_value,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="OriginVerifyHeader")
    def ORIGIN_VERIFY_HEADER(cls) -> builtins.str:
        '''(experimental) Origin Request Header Default Name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OriginVerifyHeader"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        '''(experimental) CloudFront Origin Custom Header name used in the WAFv2 WebACL verification.

        :default: 'x-origin-verify'

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        '''(experimental) Secret Value used as the CloudFront Origin Custom Header value.

        :stability: experimental

        Example::

            'xxxxEXAMPLESECRET'
        '''
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))


@jsii.data_type(
    jsii_type="@alma-cdk/origin-verify.OriginVerifyProps",
    jsii_struct_bases=[],
    name_mapping={
        "origin": "origin",
        "acl_metric_name": "aclMetricName",
        "header_name": "headerName",
        "rule_metric_name": "ruleMetricName",
        "rules": "rules",
        "secret_value": "secretValue",
    },
)
class OriginVerifyProps:
    def __init__(
        self,
        *,
        origin: typing.Union[aws_cdk.aws_apigateway.IStage, aws_cdk.aws_appsync.CfnGraphQLApi, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancer],
        acl_metric_name: typing.Optional[builtins.str] = None,
        header_name: typing.Optional[builtins.str] = None,
        rule_metric_name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_wafv2.CfnWebACL.RuleProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]] = None,
        secret_value: typing.Optional[aws_cdk.SecretValue] = None,
    ) -> None:
        '''(experimental) Properties for ``OriginVerify`` constructor.

        :param origin: (experimental) Origin to protect. Accepted types: - ``IStage`` (from ``aws-cdk-lib/aws-apigateway``) - ``IApplicationLoadBalancer`` (from ``aws-cdk-lib/aws-elasticloadbalancingv2``)
        :param acl_metric_name: (experimental) Metric name for the WebACL. Default: 'OriginVerifyWebAcl'
        :param header_name: (experimental) By default ``x-origin-verify`` is used. To override it, provide a value for this. Recommendation is to use something with a ``x-`` prefix. Default: 'x-origin-verify'
        :param rule_metric_name: (experimental) Metric name for the allowed requests. Default: 'OriginVerifyAllowedRequests'
        :param rules: (experimental) Any additional rules to add into the created WAFv2 WebACL.
        :param secret_value: (experimental) The secret which is used to verify the CloudFront distribution. Optional: By default this construct will generate a ``new Secret``. Default: new Secret().secretValue

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                origin: typing.Union[aws_cdk.aws_apigateway.IStage, aws_cdk.aws_appsync.CfnGraphQLApi, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancer],
                acl_metric_name: typing.Optional[builtins.str] = None,
                header_name: typing.Optional[builtins.str] = None,
                rule_metric_name: typing.Optional[builtins.str] = None,
                rules: typing.Optional[typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_wafv2.CfnWebACL.RuleProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]] = None,
                secret_value: typing.Optional[aws_cdk.SecretValue] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument acl_metric_name", value=acl_metric_name, expected_type=type_hints["acl_metric_name"])
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument rule_metric_name", value=rule_metric_name, expected_type=type_hints["rule_metric_name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
        self._values: typing.Dict[str, typing.Any] = {
            "origin": origin,
        }
        if acl_metric_name is not None:
            self._values["acl_metric_name"] = acl_metric_name
        if header_name is not None:
            self._values["header_name"] = header_name
        if rule_metric_name is not None:
            self._values["rule_metric_name"] = rule_metric_name
        if rules is not None:
            self._values["rules"] = rules
        if secret_value is not None:
            self._values["secret_value"] = secret_value

    @builtins.property
    def origin(
        self,
    ) -> typing.Union[aws_cdk.aws_apigateway.IStage, aws_cdk.aws_appsync.CfnGraphQLApi, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancer]:
        '''(experimental) Origin to protect.

        Accepted types:

        - ``IStage`` (from ``aws-cdk-lib/aws-apigateway``)
        - ``IApplicationLoadBalancer`` (from ``aws-cdk-lib/aws-elasticloadbalancingv2``)

        :stability: experimental
        '''
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return typing.cast(typing.Union[aws_cdk.aws_apigateway.IStage, aws_cdk.aws_appsync.CfnGraphQLApi, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancer], result)

    @builtins.property
    def acl_metric_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Metric name for the WebACL.

        :default: 'OriginVerifyWebAcl'

        :stability: experimental
        '''
        result = self._values.get("acl_metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) By default ``x-origin-verify`` is used.

        To override it, provide a value for
        this. Recommendation is to use something with a ``x-`` prefix.

        :default: 'x-origin-verify'

        :stability: experimental
        '''
        result = self._values.get("header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_metric_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Metric name for the allowed requests.

        :default: 'OriginVerifyAllowedRequests'

        :stability: experimental
        '''
        result = self._values.get("rule_metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.List[typing.Union[aws_cdk.aws_wafv2.CfnWebACL.RuleProperty, aws_cdk.IResolvable]]]:
        '''(experimental) Any additional rules to add into the created WAFv2 WebACL.

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List[typing.Union[aws_cdk.aws_wafv2.CfnWebACL.RuleProperty, aws_cdk.IResolvable]]], result)

    @builtins.property
    def secret_value(self) -> typing.Optional[aws_cdk.SecretValue]:
        '''(experimental) The secret which is used to verify the CloudFront distribution.

        Optional: By default this construct will generate a ``new Secret``.

        :default: new Secret().secretValue

        :stability: experimental
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional[aws_cdk.SecretValue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginVerifyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IVerification",
    "OriginVerify",
    "OriginVerifyProps",
]

publication.publish()
