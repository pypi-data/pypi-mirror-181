'''
# CDK ECS CodeDeploy

[![npm version](https://badge.fury.io/js/@cdklabs%2Fcdk-ecs-codedeploy.svg)](https://badge.fury.io/js/@cdklabs%2Fcdk-ecs-codedeploy)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/io.github.cdklabs/cdk-ecs-codedeploy/badge.svg)](https://maven-badges.herokuapp.com/maven-central/io.github.cdklabs/cdk-ecs-codedeploy)
[![PyPI version](https://badge.fury.io/py/cdklabs.ecs-codedeploy.svg)](https://badge.fury.io/py/cdklabs.ecs-codedeploy)
[![NuGet version](https://badge.fury.io/nu/Cdklabs.CdkEcsCodeDeploy.svg)](https://badge.fury.io/nu/Cdklabs.CdkEcsCodeDeploy)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/cdklabs/cdk-ecs-codedeploy)
[![Mergify](https://img.shields.io/endpoint.svg?url=https://api.mergify.com/badges/cdklabs/cdk-ecs-codedeploy&style=flat)](https://mergify.io)

This project contains CDK constructs to create CodeDeploy ECS deployments.

## Installation

<details><summary><strong>TypeScript</strong></summary>

```bash
yarn add @cdklabs/cdk-ecs-codedeploy
```

</details><details><summary><strong>Java</strong></summary>

See https://mvnrepository.com/artifact/io.github.cdklabs/cdk-ecs-codedeploy

</details><details><summary><strong>Python</strong></summary>

See https://pypi.org/project/cdklabs.ecs-codedeploy/

</details><details><summary><strong>C#</strong></summary>

See https://www.nuget.org/packages/Cdklabs.CdkEcsCodeDeploy/

</details>

## Getting Started

You can browse the documentation at https://constructs.dev/packages/cdk-ecs-codedeploy/

CodeDeploy for ECS can manage the deployment of new task definitions to ECS services.  Only 1 deployment construct can be defined for a given EcsDeploymentGroup.

```python
declare const deploymentGroup: codeDeploy.IEcsDeploymentGroup;
declare const taskDefinition: ecs.ITaskDefinition;

EcsDeployment.forDeploymentGroup({
  deploymentGroup,
  appspec: new codedeploy.EcsAppSpec({
    taskDefinition,
    containerName: 'mycontainer',
    containerPort: 80,
  }),
});
```

The deployment will use the AutoRollbackConfig for the EcsDeploymentGroup unless it is overridden in the deployment:

```python
EcsDeployment.forDeploymentGroup({
  deploymentGroup,
  appspec: new codedeploy.EcsAppSpec({
    taskDefinition,
    containerName: 'mycontainer',
    containerPort: 80,
  }),
  autoRollback: {
    failedDeployment: true,
    deploymentInAlarm: true,
    stoppedDeployment: false,
  },
});
```

By default, the deployment will timeout after 30 minutes. The timeout value can be overridden:

```python
EcsDeployment.forDeploymentGroup({
  deploymentGroup,
  appspec: new codedeploy.EcsAppSpec({
    taskDefinition,
    containerName: 'mycontainer',
    containerPort: 80,
  }),
  timeout: Duration.minutes(60),
});
```

## Local Development

```bash
yarn install
yarn build
yarn test
```

To run an integration test and update the snapshot, run:

```bash
yarn integ:deployment:deploy
```

To recreate snapshots for integration tests, run:

```bash
yarn integ:snapshot-all
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_codedeploy as _aws_cdk_aws_codedeploy_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@cdklabs/cdk-ecs-codedeploy.AwsvpcConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assign_public_ip": "assignPublicIp",
        "security_groups": "securityGroups",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class AwsvpcConfiguration:
    def __init__(
        self,
        *,
        assign_public_ip: builtins.bool,
        security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Network configuration for ECS services that have a network type of ``awsvpc``.

        :param assign_public_ip: (experimental) Assign a public IP address to the task.
        :param security_groups: (experimental) The Security Groups to use for the task.
        :param vpc: (experimental) The VPC to use for the task.
        :param vpc_subnets: (experimental) The Subnets to use for the task.

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51ce7b060a2cbe6ceabb5d4b6d2ebb95a67fd6a0f1ffeb644b04fd89070e6f5)
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assign_public_ip": assign_public_ip,
            "security_groups": security_groups,
            "vpc": vpc,
            "vpc_subnets": vpc_subnets,
        }

    @builtins.property
    def assign_public_ip(self) -> builtins.bool:
        '''(experimental) Assign a public IP address to the task.

        :stability: experimental
        '''
        result = self._values.get("assign_public_ip")
        assert result is not None, "Required property 'assign_public_ip' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) The Security Groups to use for the task.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The VPC to use for the task.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''(experimental) The Subnets to use for the task.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        assert result is not None, "Required property 'vpc_subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsvpcConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsAppSpec(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-ecs-codedeploy.EcsAppSpec",
):
    '''(experimental) Represents an AppSpec to be used for ECS services.

    see: https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-resources.html#reference-appspec-file-structure-resources-ecs

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        container_name: builtins.str,
        container_port: jsii.Number,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.ITaskDefinition,
        awsvpc_configuration: typing.Optional[typing.Union[AwsvpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        capacity_provider_strategy: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
    ) -> None:
        '''
        :param container_name: (experimental) The name of the Amazon ECS container that contains your Amazon ECS application. It must be a container specified in your Amazon ECS task definition.
        :param container_port: (experimental) The port on the container where traffic will be routed to.
        :param task_definition: (experimental) The TaskDefintion to deploy to the target services.
        :param awsvpc_configuration: (experimental) Network configuration for ECS services that have a network type of ``awsvpc``. Default: reuse current network settings for ECS service.
        :param capacity_provider_strategy: (experimental) A list of Amazon ECS capacity providers to use for the deployment. Default: reuse current capcity provider strategy for ECS service.
        :param platform_version: (experimental) The platform version of the Fargate tasks in the deployed Amazon ECS service. see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html Default: LATEST

        :stability: experimental
        '''
        target_service = TargetService(
            container_name=container_name,
            container_port=container_port,
            task_definition=task_definition,
            awsvpc_configuration=awsvpc_configuration,
            capacity_provider_strategy=capacity_provider_strategy,
            platform_version=platform_version,
        )

        jsii.create(self.__class__, self, [target_service])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Render JSON string for this AppSpec to be used.

        :return: string representation of this AppSpec

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


class EcsDeployment(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-ecs-codedeploy.EcsDeployment",
):
    '''(experimental) A CodeDeploy Deployment for a Amazon ECS service DeploymentGroup.

    An EcsDeploymentGroup
    must only have 1 EcsDeployment. This limit is enforced by making the constructor protected
    and requiring the use of a static method such as ``EcsDeploymentGroup.forDeploymentGroup()`` to initialize.
    The scope will always be set to the EcsDeploymentGroup and the id will always
    be set to the string 'Deployment' to force an error if mulitiple EcsDeployment constructs
    are created for a single EcsDeploymentGroup.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        appspec: EcsAppSpec,
        deployment_group: _aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentGroup,
        auto_rollback: typing.Optional[typing.Union[_aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param appspec: (experimental) The AppSpec to use for the deployment. see: https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-resources.html#reference-appspec-file-structure-resources-ecs
        :param deployment_group: (experimental) The deployment group to target for this deployment.
        :param auto_rollback: (experimental) The configuration for rollback in the event that a deployment fails. Default: : no automatic rollback triggered
        :param description: (experimental) The description for the deployment. Default: no description
        :param timeout: (experimental) The timeout for the deployment. If the timeout is reached, it will trigger a rollback of the stack. Default: 30 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9130b9e1d5d7c0b87ae443c0d7d614dbb6702cb90c851e3fbd9884a74fc3c424)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsDeploymentProps(
            appspec=appspec,
            deployment_group=deployment_group,
            auto_rollback=auto_rollback,
            description=description,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="forDeploymentGroup")
    @builtins.classmethod
    def for_deployment_group(
        cls,
        *,
        appspec: EcsAppSpec,
        deployment_group: _aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentGroup,
        auto_rollback: typing.Optional[typing.Union[_aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> "EcsDeployment":
        '''(experimental) Create a new deployment for a given ``EcsDeploymentGroup``.

        :param appspec: (experimental) The AppSpec to use for the deployment. see: https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-resources.html#reference-appspec-file-structure-resources-ecs
        :param deployment_group: (experimental) The deployment group to target for this deployment.
        :param auto_rollback: (experimental) The configuration for rollback in the event that a deployment fails. Default: : no automatic rollback triggered
        :param description: (experimental) The description for the deployment. Default: no description
        :param timeout: (experimental) The timeout for the deployment. If the timeout is reached, it will trigger a rollback of the stack. Default: 30 minutes

        :stability: experimental
        '''
        props = EcsDeploymentProps(
            appspec=appspec,
            deployment_group=deployment_group,
            auto_rollback=auto_rollback,
            description=description,
            timeout=timeout,
        )

        return typing.cast("EcsDeployment", jsii.sinvoke(cls, "forDeploymentGroup", [props]))

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        '''(experimental) The id of the deployment that was created.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc273145c81a5b3feb82f0113f771182606a96ee3a6e364449af965eb95ad92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value)


@jsii.data_type(
    jsii_type="@cdklabs/cdk-ecs-codedeploy.EcsDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "appspec": "appspec",
        "deployment_group": "deploymentGroup",
        "auto_rollback": "autoRollback",
        "description": "description",
        "timeout": "timeout",
    },
)
class EcsDeploymentProps:
    def __init__(
        self,
        *,
        appspec: EcsAppSpec,
        deployment_group: _aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentGroup,
        auto_rollback: typing.Optional[typing.Union[_aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''(experimental) Construction properties of EcsDeployment.

        :param appspec: (experimental) The AppSpec to use for the deployment. see: https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-resources.html#reference-appspec-file-structure-resources-ecs
        :param deployment_group: (experimental) The deployment group to target for this deployment.
        :param auto_rollback: (experimental) The configuration for rollback in the event that a deployment fails. Default: : no automatic rollback triggered
        :param description: (experimental) The description for the deployment. Default: no description
        :param timeout: (experimental) The timeout for the deployment. If the timeout is reached, it will trigger a rollback of the stack. Default: 30 minutes

        :stability: experimental
        '''
        if isinstance(auto_rollback, dict):
            auto_rollback = _aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig(**auto_rollback)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf38974d86829a66d2716f1cb94150364c1bbca49159ddfb7ca3933cbcc14cb)
            check_type(argname="argument appspec", value=appspec, expected_type=type_hints["appspec"])
            check_type(argname="argument deployment_group", value=deployment_group, expected_type=type_hints["deployment_group"])
            check_type(argname="argument auto_rollback", value=auto_rollback, expected_type=type_hints["auto_rollback"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "appspec": appspec,
            "deployment_group": deployment_group,
        }
        if auto_rollback is not None:
            self._values["auto_rollback"] = auto_rollback
        if description is not None:
            self._values["description"] = description
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def appspec(self) -> EcsAppSpec:
        '''(experimental) The AppSpec to use for the deployment.

        see: https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-resources.html#reference-appspec-file-structure-resources-ecs

        :stability: experimental
        '''
        result = self._values.get("appspec")
        assert result is not None, "Required property 'appspec' is missing"
        return typing.cast(EcsAppSpec, result)

    @builtins.property
    def deployment_group(self) -> _aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentGroup:
        '''(experimental) The deployment group to target for this deployment.

        :stability: experimental
        '''
        result = self._values.get("deployment_group")
        assert result is not None, "Required property 'deployment_group' is missing"
        return typing.cast(_aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentGroup, result)

    @builtins.property
    def auto_rollback(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig]:
        '''(experimental) The configuration for rollback in the event that a deployment fails.

        :default: : no automatic rollback triggered

        :stability: experimental
        '''
        result = self._values.get("auto_rollback")
        return typing.cast(typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description for the deployment.

        :default: no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout for the deployment.

        If the timeout is reached, it will trigger a rollback of the stack.

        :default: 30 minutes

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-ecs-codedeploy.TargetService",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "container_port": "containerPort",
        "task_definition": "taskDefinition",
        "awsvpc_configuration": "awsvpcConfiguration",
        "capacity_provider_strategy": "capacityProviderStrategy",
        "platform_version": "platformVersion",
    },
)
class TargetService:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        container_port: jsii.Number,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.ITaskDefinition,
        awsvpc_configuration: typing.Optional[typing.Union[AwsvpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        capacity_provider_strategy: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
    ) -> None:
        '''(experimental) Describe the target for CodeDeploy to use when creating a deployment for an ecs.EcsDeploymentGroup.

        :param container_name: (experimental) The name of the Amazon ECS container that contains your Amazon ECS application. It must be a container specified in your Amazon ECS task definition.
        :param container_port: (experimental) The port on the container where traffic will be routed to.
        :param task_definition: (experimental) The TaskDefintion to deploy to the target services.
        :param awsvpc_configuration: (experimental) Network configuration for ECS services that have a network type of ``awsvpc``. Default: reuse current network settings for ECS service.
        :param capacity_provider_strategy: (experimental) A list of Amazon ECS capacity providers to use for the deployment. Default: reuse current capcity provider strategy for ECS service.
        :param platform_version: (experimental) The platform version of the Fargate tasks in the deployed Amazon ECS service. see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html Default: LATEST

        :stability: experimental
        '''
        if isinstance(awsvpc_configuration, dict):
            awsvpc_configuration = AwsvpcConfiguration(**awsvpc_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7eb4e0817d1687cd8f3473d1eb1b9ce0f34b1150ba396c6c7b62edcdef0342)
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument awsvpc_configuration", value=awsvpc_configuration, expected_type=type_hints["awsvpc_configuration"])
            check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_name": container_name,
            "container_port": container_port,
            "task_definition": task_definition,
        }
        if awsvpc_configuration is not None:
            self._values["awsvpc_configuration"] = awsvpc_configuration
        if capacity_provider_strategy is not None:
            self._values["capacity_provider_strategy"] = capacity_provider_strategy
        if platform_version is not None:
            self._values["platform_version"] = platform_version

    @builtins.property
    def container_name(self) -> builtins.str:
        '''(experimental) The name of the Amazon ECS container that contains your Amazon ECS application.

        It must be a container specified in your Amazon ECS task definition.

        :stability: experimental
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_port(self) -> jsii.Number:
        '''(experimental) The port on the container where traffic will be routed to.

        :stability: experimental
        '''
        result = self._values.get("container_port")
        assert result is not None, "Required property 'container_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def task_definition(self) -> _aws_cdk_aws_ecs_ceddda9d.ITaskDefinition:
        '''(experimental) The TaskDefintion to deploy to the target services.

        :stability: experimental
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ITaskDefinition, result)

    @builtins.property
    def awsvpc_configuration(self) -> typing.Optional[AwsvpcConfiguration]:
        '''(experimental) Network configuration for ECS services that have a network type of ``awsvpc``.

        :default: reuse current network settings for ECS service.

        :stability: experimental
        '''
        result = self._values.get("awsvpc_configuration")
        return typing.cast(typing.Optional[AwsvpcConfiguration], result)

    @builtins.property
    def capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]]:
        '''(experimental) A list of Amazon ECS capacity providers to use for the deployment.

        :default: reuse current capcity provider strategy for ECS service.

        :stability: experimental
        '''
        result = self._values.get("capacity_provider_strategy")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion]:
        '''(experimental) The platform version of the Fargate tasks in the deployed Amazon ECS service.

        see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html

        :default: LATEST

        :stability: experimental
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsvpcConfiguration",
    "EcsAppSpec",
    "EcsDeployment",
    "EcsDeploymentProps",
    "TargetService",
]

publication.publish()

def _typecheckingstub__b51ce7b060a2cbe6ceabb5d4b6d2ebb95a67fd6a0f1ffeb644b04fd89070e6f5(
    *,
    assign_public_ip: builtins.bool,
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9130b9e1d5d7c0b87ae443c0d7d614dbb6702cb90c851e3fbd9884a74fc3c424(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    appspec: EcsAppSpec,
    deployment_group: _aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentGroup,
    auto_rollback: typing.Optional[typing.Union[_aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc273145c81a5b3feb82f0113f771182606a96ee3a6e364449af965eb95ad92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf38974d86829a66d2716f1cb94150364c1bbca49159ddfb7ca3933cbcc14cb(
    *,
    appspec: EcsAppSpec,
    deployment_group: _aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentGroup,
    auto_rollback: typing.Optional[typing.Union[_aws_cdk_aws_codedeploy_ceddda9d.AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7eb4e0817d1687cd8f3473d1eb1b9ce0f34b1150ba396c6c7b62edcdef0342(
    *,
    container_name: builtins.str,
    container_port: jsii.Number,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.ITaskDefinition,
    awsvpc_configuration: typing.Optional[typing.Union[AwsvpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capacity_provider_strategy: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
) -> None:
    """Type checking stubs"""
    pass
