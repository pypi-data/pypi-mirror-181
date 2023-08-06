'''
# cdk-s3-upload-presignedurl-api

cdk-s3-upload-presignedurl-api is AWS CDK construct library that create an API to get a presigned url to upload a file in S3.

## Background

In web and mobile applications, it's common to provide the ability to upload data (documents, images, ...). Uploading files on a web server can be challenging and AWS recommends to upload files directly to S3. To do that securely, you can use [pre-signed URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html). This [blog post](https://aws.amazon.com/blogs/compute/uploading-to-amazon-s3-directly-from-a-web-or-mobile-application/) provides some more details.

## Architecture

![Architecture](images/architecture.png)

1. The client makes a call to the API, specifying the "contentType" of the file to upload in request parameters (eg. `?contentType=image/png` in the URL)
2. API Gateway handles the request and execute the Lambda function.
3. The Lambda function makes a call to the [`getSignedUrl`](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html) api for a `putObject` operation.
4. The Lambda function returns the generated URL and the key of the object in S3 to API Gateway.
5. The API returns the generated URL and the key of the object in S3 to the client.
6. The client can now use this URL to upload a file, directly to S3.

## Getting Started

### TypeScript

#### Installation

```sh
$ npm install --save cdk-s3-upload-presignedurl-api
```

#### Usage

```python
import * as cdk from '@aws-cdk/core';
import { S3UploadPresignedUrlApi } from 'cdk-s3-upload-presignedurl-api';

const app = new cdk.App();
const stack = new cdk.Stack(app, '<your-stack-name>');

new S3UploadPresignedUrlApi(stack, 'S3UploadSignedUrl');
```

### Python

#### Installation

```sh
$ pip install cdk-s3-upload-presignedurl-api
```

#### Usage

```py
import aws_cdk.core as cdk
from cdk-s3-upload-presignedurl-api import S3UploadPresignedUrlApi

app = cdk.App()
stack = cdk.Stack(app, "<your-stack-name>")

S3UploadPresignedUrlApi(stack, 'S3UploadSignedUrl')
```
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

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_cognito as _aws_cdk_aws_cognito_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="cdk-s3-upload-presignedurl-api.IS3UploadSignedUrlApiProps")
class IS3UploadSignedUrlApiProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional CORS allowedOrigins.

        Should allow your domain(s) as allowed origin to request the API

        :default: ['*']
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="apiGatewayProps")
    def api_gateway_props(self) -> typing.Any:
        '''Optional user provided props to override the default props for the API Gateway.

        :default: - Default props are used
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="existingBucketObj")
    def existing_bucket_obj(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        '''Optional bucket where files should be uploaded to.

        Should contains the CORS properties

        :default: - Default Bucket is created
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="existingUserPoolObj")
    def existing_user_pool_obj(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool]:
        '''Optional Cognito User Pool to secure the API.

        You should have created a User Pool Client too.

        :default: - Default User Pool (and User Pool Client) are created
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> typing.Optional[jsii.Number]:
        '''Optional expiration time in second.

        Time before the presigned url expires.

        :default: 300
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logRetention")
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''Optional log retention time for Lambda and API Gateway.

        :default: one week
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secured")
    def secured(self) -> typing.Optional[builtins.bool]:
        '''Optional boolean to specify if the API is secured (with Cognito) or publicly open.

        :default: true
        '''
        ...


class _IS3UploadSignedUrlApiPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-s3-upload-presignedurl-api.IS3UploadSignedUrlApiProps"

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional CORS allowedOrigins.

        Should allow your domain(s) as allowed origin to request the API

        :default: ['*']
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOrigins"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayProps")
    def api_gateway_props(self) -> typing.Any:
        '''Optional user provided props to override the default props for the API Gateway.

        :default: - Default props are used
        '''
        return typing.cast(typing.Any, jsii.get(self, "apiGatewayProps"))

    @builtins.property
    @jsii.member(jsii_name="existingBucketObj")
    def existing_bucket_obj(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        '''Optional bucket where files should be uploaded to.

        Should contains the CORS properties

        :default: - Default Bucket is created
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket], jsii.get(self, "existingBucketObj"))

    @builtins.property
    @jsii.member(jsii_name="existingUserPoolObj")
    def existing_user_pool_obj(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool]:
        '''Optional Cognito User Pool to secure the API.

        You should have created a User Pool Client too.

        :default: - Default User Pool (and User Pool Client) are created
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool], jsii.get(self, "existingUserPoolObj"))

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> typing.Optional[jsii.Number]:
        '''Optional expiration time in second.

        Time before the presigned url expires.

        :default: 300
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expiration"))

    @builtins.property
    @jsii.member(jsii_name="logRetention")
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''Optional log retention time for Lambda and API Gateway.

        :default: one week
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], jsii.get(self, "logRetention"))

    @builtins.property
    @jsii.member(jsii_name="secured")
    def secured(self) -> typing.Optional[builtins.bool]:
        '''Optional boolean to specify if the API is secured (with Cognito) or publicly open.

        :default: true
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "secured"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IS3UploadSignedUrlApiProps).__jsii_proxy_class__ = lambda : _IS3UploadSignedUrlApiPropsProxy


class S3UploadPresignedUrlApi(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-s3-upload-presignedurl-api.S3UploadPresignedUrlApi",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Optional[IS3UploadSignedUrlApiProps] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacb99d5edf59176efece7d66cf3d220b3205f1ae22c487c18c831126c402698)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> _aws_cdk_aws_apigateway_ceddda9d.RestApi:
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RestApi, jsii.get(self, "restApi"))

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "userPool"))

    @builtins.property
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "userPoolClient"))


__all__ = [
    "IS3UploadSignedUrlApiProps",
    "S3UploadPresignedUrlApi",
]

publication.publish()

def _typecheckingstub__eacb99d5edf59176efece7d66cf3d220b3205f1ae22c487c18c831126c402698(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Optional[IS3UploadSignedUrlApiProps] = None,
) -> None:
    """Type checking stubs"""
    pass
