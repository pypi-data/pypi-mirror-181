'''
# `cloudflare_pages_project`

Refer to the Terraform Registory for docs: [`cloudflare_pages_project`](https://www.terraform.io/docs/providers/cloudflare/r/pages_project).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class PagesProject(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProject",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project cloudflare_pages_project}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        name: builtins.str,
        production_branch: builtins.str,
        build_config: typing.Optional[typing.Union["PagesProjectBuildConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_configs: typing.Optional[typing.Union["PagesProjectDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["PagesProjectSource", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project cloudflare_pages_project} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#account_id PagesProject#account_id}
        :param name: Name of the project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#name PagesProject#name}
        :param production_branch: The name of the branch that is used for the production environment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_branch PagesProject#production_branch}
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#build_config PagesProject#build_config}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#deployment_configs PagesProject#deployment_configs}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#id PagesProject#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source: source block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#source PagesProject#source}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c8bd3ba18e0650df846b2d2e37dfef810ae73f984dcc34617f1efd60225d71)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PagesProjectConfig(
            account_id=account_id,
            name=name,
            production_branch=production_branch,
            build_config=build_config,
            deployment_configs=deployment_configs,
            id=id,
            source=source,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putBuildConfig")
    def put_build_config(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        destination_dir: typing.Optional[builtins.str] = None,
        root_dir: typing.Optional[builtins.str] = None,
        web_analytics_tag: typing.Optional[builtins.str] = None,
        web_analytics_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_command: Command used to build project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#build_command PagesProject#build_command}
        :param destination_dir: Output directory of the build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#destination_dir PagesProject#destination_dir}
        :param root_dir: Directory to run the command. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#root_dir PagesProject#root_dir}
        :param web_analytics_tag: The classifying tag for analytics. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#web_analytics_tag PagesProject#web_analytics_tag}
        :param web_analytics_token: The auth token for analytics. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#web_analytics_token PagesProject#web_analytics_token}
        '''
        value = PagesProjectBuildConfig(
            build_command=build_command,
            destination_dir=destination_dir,
            root_dir=root_dir,
            web_analytics_tag=web_analytics_tag,
            web_analytics_token=web_analytics_token,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildConfig", [value]))

    @jsii.member(jsii_name="putDeploymentConfigs")
    def put_deployment_configs(
        self,
        *,
        preview: typing.Optional[typing.Union["PagesProjectDeploymentConfigsPreview", typing.Dict[builtins.str, typing.Any]]] = None,
        production: typing.Optional[typing.Union["PagesProjectDeploymentConfigsProduction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param preview: preview block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview PagesProject#preview}
        :param production: production block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production PagesProject#production}
        '''
        value = PagesProjectDeploymentConfigs(preview=preview, production=production)

        return typing.cast(None, jsii.invoke(self, "putDeploymentConfigs", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        config: typing.Optional[typing.Union["PagesProjectSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#config PagesProject#config}
        :param type: Project host type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#type PagesProject#type}
        '''
        value = PagesProjectSource(config=config, type=type)

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetBuildConfig")
    def reset_build_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildConfig", []))

    @jsii.member(jsii_name="resetDeploymentConfigs")
    def reset_deployment_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentConfigs", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="buildConfig")
    def build_config(self) -> "PagesProjectBuildConfigOutputReference":
        return typing.cast("PagesProjectBuildConfigOutputReference", jsii.get(self, "buildConfig"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigs")
    def deployment_configs(self) -> "PagesProjectDeploymentConfigsOutputReference":
        return typing.cast("PagesProjectDeploymentConfigsOutputReference", jsii.get(self, "deploymentConfigs"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "PagesProjectSourceOutputReference":
        return typing.cast("PagesProjectSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="subdomain")
    def subdomain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subdomain"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="buildConfigInput")
    def build_config_input(self) -> typing.Optional["PagesProjectBuildConfig"]:
        return typing.cast(typing.Optional["PagesProjectBuildConfig"], jsii.get(self, "buildConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigsInput")
    def deployment_configs_input(
        self,
    ) -> typing.Optional["PagesProjectDeploymentConfigs"]:
        return typing.cast(typing.Optional["PagesProjectDeploymentConfigs"], jsii.get(self, "deploymentConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="productionBranchInput")
    def production_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productionBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["PagesProjectSource"]:
        return typing.cast(typing.Optional["PagesProjectSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25d24d3b5e4450d1d1b773c3f5902e9faec8325dd51fa04efa4d99ffdce1420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492d7148c8029e959b254a35bdfa2fd8f846ae24bcf32a90ecd2808b99c6822b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcae619adfa6aa5276e7477d32740b0f98c950ea03e86467e16d2f2afa4af2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="productionBranch")
    def production_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productionBranch"))

    @production_branch.setter
    def production_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6748f02b291e15157b0dfdadc8ffde3dfabf3d9c406daafd12d4c241863b058c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productionBranch", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectBuildConfig",
    jsii_struct_bases=[],
    name_mapping={
        "build_command": "buildCommand",
        "destination_dir": "destinationDir",
        "root_dir": "rootDir",
        "web_analytics_tag": "webAnalyticsTag",
        "web_analytics_token": "webAnalyticsToken",
    },
)
class PagesProjectBuildConfig:
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        destination_dir: typing.Optional[builtins.str] = None,
        root_dir: typing.Optional[builtins.str] = None,
        web_analytics_tag: typing.Optional[builtins.str] = None,
        web_analytics_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_command: Command used to build project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#build_command PagesProject#build_command}
        :param destination_dir: Output directory of the build. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#destination_dir PagesProject#destination_dir}
        :param root_dir: Directory to run the command. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#root_dir PagesProject#root_dir}
        :param web_analytics_tag: The classifying tag for analytics. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#web_analytics_tag PagesProject#web_analytics_tag}
        :param web_analytics_token: The auth token for analytics. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#web_analytics_token PagesProject#web_analytics_token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ddb1767df2790103b319dd95302c1ef2dcfeee4080c9df13a6923c7f947ef6)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument destination_dir", value=destination_dir, expected_type=type_hints["destination_dir"])
            check_type(argname="argument root_dir", value=root_dir, expected_type=type_hints["root_dir"])
            check_type(argname="argument web_analytics_tag", value=web_analytics_tag, expected_type=type_hints["web_analytics_tag"])
            check_type(argname="argument web_analytics_token", value=web_analytics_token, expected_type=type_hints["web_analytics_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_command is not None:
            self._values["build_command"] = build_command
        if destination_dir is not None:
            self._values["destination_dir"] = destination_dir
        if root_dir is not None:
            self._values["root_dir"] = root_dir
        if web_analytics_tag is not None:
            self._values["web_analytics_tag"] = web_analytics_tag
        if web_analytics_token is not None:
            self._values["web_analytics_token"] = web_analytics_token

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Command used to build project.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#build_command PagesProject#build_command}
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_dir(self) -> typing.Optional[builtins.str]:
        '''Output directory of the build.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#destination_dir PagesProject#destination_dir}
        '''
        result = self._values.get("destination_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to run the command.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#root_dir PagesProject#root_dir}
        '''
        result = self._values.get("root_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_analytics_tag(self) -> typing.Optional[builtins.str]:
        '''The classifying tag for analytics.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#web_analytics_tag PagesProject#web_analytics_tag}
        '''
        result = self._values.get("web_analytics_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_analytics_token(self) -> typing.Optional[builtins.str]:
        '''The auth token for analytics.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#web_analytics_token PagesProject#web_analytics_token}
        '''
        result = self._values.get("web_analytics_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesProjectBuildConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PagesProjectBuildConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectBuildConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a960c98b224c6cf61805a912db83a0d50aa489fd1ddff0a1969c14872ac349d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBuildCommand")
    def reset_build_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildCommand", []))

    @jsii.member(jsii_name="resetDestinationDir")
    def reset_destination_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationDir", []))

    @jsii.member(jsii_name="resetRootDir")
    def reset_root_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootDir", []))

    @jsii.member(jsii_name="resetWebAnalyticsTag")
    def reset_web_analytics_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebAnalyticsTag", []))

    @jsii.member(jsii_name="resetWebAnalyticsToken")
    def reset_web_analytics_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebAnalyticsToken", []))

    @builtins.property
    @jsii.member(jsii_name="buildCommandInput")
    def build_command_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildCommandInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationDirInput")
    def destination_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationDirInput"))

    @builtins.property
    @jsii.member(jsii_name="rootDirInput")
    def root_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootDirInput"))

    @builtins.property
    @jsii.member(jsii_name="webAnalyticsTagInput")
    def web_analytics_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webAnalyticsTagInput"))

    @builtins.property
    @jsii.member(jsii_name="webAnalyticsTokenInput")
    def web_analytics_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webAnalyticsTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="buildCommand")
    def build_command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildCommand"))

    @build_command.setter
    def build_command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7be84ce85b9c62ce32b5dc2e25735ef178a42ae6c4e9c1119dfd8daf83ded4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildCommand", value)

    @builtins.property
    @jsii.member(jsii_name="destinationDir")
    def destination_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationDir"))

    @destination_dir.setter
    def destination_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5424df13dad2e1fd5edffc5ddcc1e83930ce5a31274ecb5d8574ef5c73362c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationDir", value)

    @builtins.property
    @jsii.member(jsii_name="rootDir")
    def root_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootDir"))

    @root_dir.setter
    def root_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4625699986a8ee4c0655efa7eeabca037c039abe2c03b7d7bcf3b7602be7d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootDir", value)

    @builtins.property
    @jsii.member(jsii_name="webAnalyticsTag")
    def web_analytics_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webAnalyticsTag"))

    @web_analytics_tag.setter
    def web_analytics_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3a0913a4c6ccf4b97d8ec54a927ea9f9838b946db5e9009609ac0ce769a21a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webAnalyticsTag", value)

    @builtins.property
    @jsii.member(jsii_name="webAnalyticsToken")
    def web_analytics_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webAnalyticsToken"))

    @web_analytics_token.setter
    def web_analytics_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76185d7b63462d674120a4c7e55a708a813fbeeaeb708206c04147ae22731b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webAnalyticsToken", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PagesProjectBuildConfig]:
        return typing.cast(typing.Optional[PagesProjectBuildConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PagesProjectBuildConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2551caeefe9277427f352093f8384ff5673336bce649412aec8f7afec41509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "name": "name",
        "production_branch": "productionBranch",
        "build_config": "buildConfig",
        "deployment_configs": "deploymentConfigs",
        "id": "id",
        "source": "source",
    },
)
class PagesProjectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        account_id: builtins.str,
        name: builtins.str,
        production_branch: builtins.str,
        build_config: typing.Optional[typing.Union[PagesProjectBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_configs: typing.Optional[typing.Union["PagesProjectDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["PagesProjectSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#account_id PagesProject#account_id}
        :param name: Name of the project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#name PagesProject#name}
        :param production_branch: The name of the branch that is used for the production environment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_branch PagesProject#production_branch}
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#build_config PagesProject#build_config}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#deployment_configs PagesProject#deployment_configs}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#id PagesProject#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source: source block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#source PagesProject#source}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(build_config, dict):
            build_config = PagesProjectBuildConfig(**build_config)
        if isinstance(deployment_configs, dict):
            deployment_configs = PagesProjectDeploymentConfigs(**deployment_configs)
        if isinstance(source, dict):
            source = PagesProjectSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0094d200e654f606607f96b58892accd8ce9d503242b6f5c7d06a2ae11897e53)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument production_branch", value=production_branch, expected_type=type_hints["production_branch"])
            check_type(argname="argument build_config", value=build_config, expected_type=type_hints["build_config"])
            check_type(argname="argument deployment_configs", value=deployment_configs, expected_type=type_hints["deployment_configs"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "name": name,
            "production_branch": production_branch,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if build_config is not None:
            self._values["build_config"] = build_config
        if deployment_configs is not None:
            self._values["deployment_configs"] = deployment_configs
        if id is not None:
            self._values["id"] = id
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#account_id PagesProject#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the project.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#name PagesProject#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def production_branch(self) -> builtins.str:
        '''The name of the branch that is used for the production environment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_branch PagesProject#production_branch}
        '''
        result = self._values.get("production_branch")
        assert result is not None, "Required property 'production_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_config(self) -> typing.Optional[PagesProjectBuildConfig]:
        '''build_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#build_config PagesProject#build_config}
        '''
        result = self._values.get("build_config")
        return typing.cast(typing.Optional[PagesProjectBuildConfig], result)

    @builtins.property
    def deployment_configs(self) -> typing.Optional["PagesProjectDeploymentConfigs"]:
        '''deployment_configs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#deployment_configs PagesProject#deployment_configs}
        '''
        result = self._values.get("deployment_configs")
        return typing.cast(typing.Optional["PagesProjectDeploymentConfigs"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#id PagesProject#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional["PagesProjectSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#source PagesProject#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["PagesProjectSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectDeploymentConfigs",
    jsii_struct_bases=[],
    name_mapping={"preview": "preview", "production": "production"},
)
class PagesProjectDeploymentConfigs:
    def __init__(
        self,
        *,
        preview: typing.Optional[typing.Union["PagesProjectDeploymentConfigsPreview", typing.Dict[builtins.str, typing.Any]]] = None,
        production: typing.Optional[typing.Union["PagesProjectDeploymentConfigsProduction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param preview: preview block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview PagesProject#preview}
        :param production: production block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production PagesProject#production}
        '''
        if isinstance(preview, dict):
            preview = PagesProjectDeploymentConfigsPreview(**preview)
        if isinstance(production, dict):
            production = PagesProjectDeploymentConfigsProduction(**production)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7823fdc9b0a09eac3b8f24725ee9162c17ddca7ff78a36cba5175fe819813991)
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument production", value=production, expected_type=type_hints["production"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preview is not None:
            self._values["preview"] = preview
        if production is not None:
            self._values["production"] = production

    @builtins.property
    def preview(self) -> typing.Optional["PagesProjectDeploymentConfigsPreview"]:
        '''preview block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview PagesProject#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional["PagesProjectDeploymentConfigsPreview"], result)

    @builtins.property
    def production(self) -> typing.Optional["PagesProjectDeploymentConfigsProduction"]:
        '''production block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production PagesProject#production}
        '''
        result = self._values.get("production")
        return typing.cast(typing.Optional["PagesProjectDeploymentConfigsProduction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesProjectDeploymentConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PagesProjectDeploymentConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectDeploymentConfigsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfb360ea6a026f85cc04fa09830e4f97ca1f925ad9c49edc82b2bf67135a9d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPreview")
    def put_preview(
        self,
        *,
        compatibility_date: typing.Optional[builtins.str] = None,
        compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        d1_databases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        durable_object_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kv_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        r2_buckets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param compatibility_date: Compatibility date used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_date PagesProject#compatibility_date}
        :param compatibility_flags: Compatibility flags used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_flags PagesProject#compatibility_flags}
        :param d1_databases: D1 Databases used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#d1_databases PagesProject#d1_databases}
        :param durable_object_namespaces: Durable Object namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#durable_object_namespaces PagesProject#durable_object_namespaces}
        :param environment_variables: Environment variables for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#environment_variables PagesProject#environment_variables}
        :param kv_namespaces: KV namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#kv_namespaces PagesProject#kv_namespaces}
        :param r2_buckets: R2 Buckets used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#r2_buckets PagesProject#r2_buckets}
        '''
        value = PagesProjectDeploymentConfigsPreview(
            compatibility_date=compatibility_date,
            compatibility_flags=compatibility_flags,
            d1_databases=d1_databases,
            durable_object_namespaces=durable_object_namespaces,
            environment_variables=environment_variables,
            kv_namespaces=kv_namespaces,
            r2_buckets=r2_buckets,
        )

        return typing.cast(None, jsii.invoke(self, "putPreview", [value]))

    @jsii.member(jsii_name="putProduction")
    def put_production(
        self,
        *,
        compatibility_date: typing.Optional[builtins.str] = None,
        compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        d1_databases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        durable_object_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kv_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        r2_buckets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param compatibility_date: Compatibility date used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_date PagesProject#compatibility_date}
        :param compatibility_flags: Compatibility flags used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_flags PagesProject#compatibility_flags}
        :param d1_databases: D1 Databases used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#d1_databases PagesProject#d1_databases}
        :param durable_object_namespaces: Durable Object namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#durable_object_namespaces PagesProject#durable_object_namespaces}
        :param environment_variables: Environment variables for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#environment_variables PagesProject#environment_variables}
        :param kv_namespaces: KV namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#kv_namespaces PagesProject#kv_namespaces}
        :param r2_buckets: R2 Buckets used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#r2_buckets PagesProject#r2_buckets}
        '''
        value = PagesProjectDeploymentConfigsProduction(
            compatibility_date=compatibility_date,
            compatibility_flags=compatibility_flags,
            d1_databases=d1_databases,
            durable_object_namespaces=durable_object_namespaces,
            environment_variables=environment_variables,
            kv_namespaces=kv_namespaces,
            r2_buckets=r2_buckets,
        )

        return typing.cast(None, jsii.invoke(self, "putProduction", [value]))

    @jsii.member(jsii_name="resetPreview")
    def reset_preview(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreview", []))

    @jsii.member(jsii_name="resetProduction")
    def reset_production(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProduction", []))

    @builtins.property
    @jsii.member(jsii_name="preview")
    def preview(self) -> "PagesProjectDeploymentConfigsPreviewOutputReference":
        return typing.cast("PagesProjectDeploymentConfigsPreviewOutputReference", jsii.get(self, "preview"))

    @builtins.property
    @jsii.member(jsii_name="production")
    def production(self) -> "PagesProjectDeploymentConfigsProductionOutputReference":
        return typing.cast("PagesProjectDeploymentConfigsProductionOutputReference", jsii.get(self, "production"))

    @builtins.property
    @jsii.member(jsii_name="previewInput")
    def preview_input(self) -> typing.Optional["PagesProjectDeploymentConfigsPreview"]:
        return typing.cast(typing.Optional["PagesProjectDeploymentConfigsPreview"], jsii.get(self, "previewInput"))

    @builtins.property
    @jsii.member(jsii_name="productionInput")
    def production_input(
        self,
    ) -> typing.Optional["PagesProjectDeploymentConfigsProduction"]:
        return typing.cast(typing.Optional["PagesProjectDeploymentConfigsProduction"], jsii.get(self, "productionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PagesProjectDeploymentConfigs]:
        return typing.cast(typing.Optional[PagesProjectDeploymentConfigs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PagesProjectDeploymentConfigs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bda509eaf75eb329c80e5e350ce8997a151563c736cfdcf50a669a795ffaa07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectDeploymentConfigsPreview",
    jsii_struct_bases=[],
    name_mapping={
        "compatibility_date": "compatibilityDate",
        "compatibility_flags": "compatibilityFlags",
        "d1_databases": "d1Databases",
        "durable_object_namespaces": "durableObjectNamespaces",
        "environment_variables": "environmentVariables",
        "kv_namespaces": "kvNamespaces",
        "r2_buckets": "r2Buckets",
    },
)
class PagesProjectDeploymentConfigsPreview:
    def __init__(
        self,
        *,
        compatibility_date: typing.Optional[builtins.str] = None,
        compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        d1_databases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        durable_object_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kv_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        r2_buckets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param compatibility_date: Compatibility date used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_date PagesProject#compatibility_date}
        :param compatibility_flags: Compatibility flags used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_flags PagesProject#compatibility_flags}
        :param d1_databases: D1 Databases used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#d1_databases PagesProject#d1_databases}
        :param durable_object_namespaces: Durable Object namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#durable_object_namespaces PagesProject#durable_object_namespaces}
        :param environment_variables: Environment variables for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#environment_variables PagesProject#environment_variables}
        :param kv_namespaces: KV namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#kv_namespaces PagesProject#kv_namespaces}
        :param r2_buckets: R2 Buckets used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#r2_buckets PagesProject#r2_buckets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e03862ac074ef15f724d9cc40bca42af7e9390d107765128d30dfa4a96e2ff)
            check_type(argname="argument compatibility_date", value=compatibility_date, expected_type=type_hints["compatibility_date"])
            check_type(argname="argument compatibility_flags", value=compatibility_flags, expected_type=type_hints["compatibility_flags"])
            check_type(argname="argument d1_databases", value=d1_databases, expected_type=type_hints["d1_databases"])
            check_type(argname="argument durable_object_namespaces", value=durable_object_namespaces, expected_type=type_hints["durable_object_namespaces"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument kv_namespaces", value=kv_namespaces, expected_type=type_hints["kv_namespaces"])
            check_type(argname="argument r2_buckets", value=r2_buckets, expected_type=type_hints["r2_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatibility_date is not None:
            self._values["compatibility_date"] = compatibility_date
        if compatibility_flags is not None:
            self._values["compatibility_flags"] = compatibility_flags
        if d1_databases is not None:
            self._values["d1_databases"] = d1_databases
        if durable_object_namespaces is not None:
            self._values["durable_object_namespaces"] = durable_object_namespaces
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if kv_namespaces is not None:
            self._values["kv_namespaces"] = kv_namespaces
        if r2_buckets is not None:
            self._values["r2_buckets"] = r2_buckets

    @builtins.property
    def compatibility_date(self) -> typing.Optional[builtins.str]:
        '''Compatibility date used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_date PagesProject#compatibility_date}
        '''
        result = self._values.get("compatibility_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compatibility_flags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Compatibility flags used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_flags PagesProject#compatibility_flags}
        '''
        result = self._values.get("compatibility_flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def d1_databases(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''D1 Databases used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#d1_databases PagesProject#d1_databases}
        '''
        result = self._values.get("d1_databases")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def durable_object_namespaces(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Durable Object namespaces used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#durable_object_namespaces PagesProject#durable_object_namespaces}
        '''
        result = self._values.get("durable_object_namespaces")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#environment_variables PagesProject#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kv_namespaces(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''KV namespaces used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#kv_namespaces PagesProject#kv_namespaces}
        '''
        result = self._values.get("kv_namespaces")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def r2_buckets(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''R2 Buckets used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#r2_buckets PagesProject#r2_buckets}
        '''
        result = self._values.get("r2_buckets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesProjectDeploymentConfigsPreview(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PagesProjectDeploymentConfigsPreviewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectDeploymentConfigsPreviewOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1a53fd86f66b2bd391be423e5c8d24aeb47824bd64d504a301cf722c043d66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompatibilityDate")
    def reset_compatibility_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompatibilityDate", []))

    @jsii.member(jsii_name="resetCompatibilityFlags")
    def reset_compatibility_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompatibilityFlags", []))

    @jsii.member(jsii_name="resetD1Databases")
    def reset_d1_databases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetD1Databases", []))

    @jsii.member(jsii_name="resetDurableObjectNamespaces")
    def reset_durable_object_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurableObjectNamespaces", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetKvNamespaces")
    def reset_kv_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKvNamespaces", []))

    @jsii.member(jsii_name="resetR2Buckets")
    def reset_r2_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetR2Buckets", []))

    @builtins.property
    @jsii.member(jsii_name="compatibilityDateInput")
    def compatibility_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compatibilityDateInput"))

    @builtins.property
    @jsii.member(jsii_name="compatibilityFlagsInput")
    def compatibility_flags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "compatibilityFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="d1DatabasesInput")
    def d1_databases_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "d1DatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="durableObjectNamespacesInput")
    def durable_object_namespaces_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "durableObjectNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="kvNamespacesInput")
    def kv_namespaces_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "kvNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="r2BucketsInput")
    def r2_buckets_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "r2BucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="compatibilityDate")
    def compatibility_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compatibilityDate"))

    @compatibility_date.setter
    def compatibility_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32865b61c6888db2bacfa85645fe28c8b167deb8ea98040548aefe9babd5762b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibilityDate", value)

    @builtins.property
    @jsii.member(jsii_name="compatibilityFlags")
    def compatibility_flags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "compatibilityFlags"))

    @compatibility_flags.setter
    def compatibility_flags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7134d0cb1462ec7eb665fd47f1f671843e450543c55d25eeefb57ec5363f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibilityFlags", value)

    @builtins.property
    @jsii.member(jsii_name="d1Databases")
    def d1_databases(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "d1Databases"))

    @d1_databases.setter
    def d1_databases(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad63f1044df17fe8ae94fbd4d63bccbf6d48a8f1ed944411add80c3153365674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "d1Databases", value)

    @builtins.property
    @jsii.member(jsii_name="durableObjectNamespaces")
    def durable_object_namespaces(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "durableObjectNamespaces"))

    @durable_object_namespaces.setter
    def durable_object_namespaces(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bb333283a4484bc9d8bae5685d56b3cf0275d0d6e92805948f8906596e0d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durableObjectNamespaces", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097ce8028e1dbd748366235c81f3e0314d9bb7c016fddca1daa31cc05c31effd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="kvNamespaces")
    def kv_namespaces(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "kvNamespaces"))

    @kv_namespaces.setter
    def kv_namespaces(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a6994bcb95a5de1f6856c21153f6c0fa14bed518cf92b4e28c190cb234683d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kvNamespaces", value)

    @builtins.property
    @jsii.member(jsii_name="r2Buckets")
    def r2_buckets(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "r2Buckets"))

    @r2_buckets.setter
    def r2_buckets(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299679c6be59c45d6db5d4b5f6bd124e8f75f895526a79192e563f3f2e1310cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "r2Buckets", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PagesProjectDeploymentConfigsPreview]:
        return typing.cast(typing.Optional[PagesProjectDeploymentConfigsPreview], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PagesProjectDeploymentConfigsPreview],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fc5ad9dba9a0aa13954ab41f376699bde856670f046d16f6a4d579da2f821d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectDeploymentConfigsProduction",
    jsii_struct_bases=[],
    name_mapping={
        "compatibility_date": "compatibilityDate",
        "compatibility_flags": "compatibilityFlags",
        "d1_databases": "d1Databases",
        "durable_object_namespaces": "durableObjectNamespaces",
        "environment_variables": "environmentVariables",
        "kv_namespaces": "kvNamespaces",
        "r2_buckets": "r2Buckets",
    },
)
class PagesProjectDeploymentConfigsProduction:
    def __init__(
        self,
        *,
        compatibility_date: typing.Optional[builtins.str] = None,
        compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        d1_databases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        durable_object_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kv_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        r2_buckets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param compatibility_date: Compatibility date used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_date PagesProject#compatibility_date}
        :param compatibility_flags: Compatibility flags used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_flags PagesProject#compatibility_flags}
        :param d1_databases: D1 Databases used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#d1_databases PagesProject#d1_databases}
        :param durable_object_namespaces: Durable Object namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#durable_object_namespaces PagesProject#durable_object_namespaces}
        :param environment_variables: Environment variables for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#environment_variables PagesProject#environment_variables}
        :param kv_namespaces: KV namespaces used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#kv_namespaces PagesProject#kv_namespaces}
        :param r2_buckets: R2 Buckets used for Pages Functions. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#r2_buckets PagesProject#r2_buckets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336477b4868198acb01a1b41c8690524ec7ae03a6fd6dc2340a5ffb5c86959e1)
            check_type(argname="argument compatibility_date", value=compatibility_date, expected_type=type_hints["compatibility_date"])
            check_type(argname="argument compatibility_flags", value=compatibility_flags, expected_type=type_hints["compatibility_flags"])
            check_type(argname="argument d1_databases", value=d1_databases, expected_type=type_hints["d1_databases"])
            check_type(argname="argument durable_object_namespaces", value=durable_object_namespaces, expected_type=type_hints["durable_object_namespaces"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument kv_namespaces", value=kv_namespaces, expected_type=type_hints["kv_namespaces"])
            check_type(argname="argument r2_buckets", value=r2_buckets, expected_type=type_hints["r2_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatibility_date is not None:
            self._values["compatibility_date"] = compatibility_date
        if compatibility_flags is not None:
            self._values["compatibility_flags"] = compatibility_flags
        if d1_databases is not None:
            self._values["d1_databases"] = d1_databases
        if durable_object_namespaces is not None:
            self._values["durable_object_namespaces"] = durable_object_namespaces
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if kv_namespaces is not None:
            self._values["kv_namespaces"] = kv_namespaces
        if r2_buckets is not None:
            self._values["r2_buckets"] = r2_buckets

    @builtins.property
    def compatibility_date(self) -> typing.Optional[builtins.str]:
        '''Compatibility date used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_date PagesProject#compatibility_date}
        '''
        result = self._values.get("compatibility_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compatibility_flags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Compatibility flags used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#compatibility_flags PagesProject#compatibility_flags}
        '''
        result = self._values.get("compatibility_flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def d1_databases(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''D1 Databases used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#d1_databases PagesProject#d1_databases}
        '''
        result = self._values.get("d1_databases")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def durable_object_namespaces(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Durable Object namespaces used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#durable_object_namespaces PagesProject#durable_object_namespaces}
        '''
        result = self._values.get("durable_object_namespaces")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#environment_variables PagesProject#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kv_namespaces(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''KV namespaces used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#kv_namespaces PagesProject#kv_namespaces}
        '''
        result = self._values.get("kv_namespaces")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def r2_buckets(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''R2 Buckets used for Pages Functions.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#r2_buckets PagesProject#r2_buckets}
        '''
        result = self._values.get("r2_buckets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesProjectDeploymentConfigsProduction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PagesProjectDeploymentConfigsProductionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectDeploymentConfigsProductionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7265aa8b15c3914638516c9c006481db3073e868d9989557acf0a5b26b6db6e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompatibilityDate")
    def reset_compatibility_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompatibilityDate", []))

    @jsii.member(jsii_name="resetCompatibilityFlags")
    def reset_compatibility_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompatibilityFlags", []))

    @jsii.member(jsii_name="resetD1Databases")
    def reset_d1_databases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetD1Databases", []))

    @jsii.member(jsii_name="resetDurableObjectNamespaces")
    def reset_durable_object_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurableObjectNamespaces", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetKvNamespaces")
    def reset_kv_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKvNamespaces", []))

    @jsii.member(jsii_name="resetR2Buckets")
    def reset_r2_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetR2Buckets", []))

    @builtins.property
    @jsii.member(jsii_name="compatibilityDateInput")
    def compatibility_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compatibilityDateInput"))

    @builtins.property
    @jsii.member(jsii_name="compatibilityFlagsInput")
    def compatibility_flags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "compatibilityFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="d1DatabasesInput")
    def d1_databases_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "d1DatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="durableObjectNamespacesInput")
    def durable_object_namespaces_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "durableObjectNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="kvNamespacesInput")
    def kv_namespaces_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "kvNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="r2BucketsInput")
    def r2_buckets_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "r2BucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="compatibilityDate")
    def compatibility_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compatibilityDate"))

    @compatibility_date.setter
    def compatibility_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0595cb8eff7f6b8d6e0bab4a75c9b33e7b8167dc670154c5d5ac8894ac886abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibilityDate", value)

    @builtins.property
    @jsii.member(jsii_name="compatibilityFlags")
    def compatibility_flags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "compatibilityFlags"))

    @compatibility_flags.setter
    def compatibility_flags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b984d2023ef3ff4c5e45625bd77fdd6b826d1556ca0e3b9d429b11e166f501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibilityFlags", value)

    @builtins.property
    @jsii.member(jsii_name="d1Databases")
    def d1_databases(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "d1Databases"))

    @d1_databases.setter
    def d1_databases(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72eae0b9fb40004097f6a7ce41e30fbc14326d75a8e8a28d4c23ef5d532b91c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "d1Databases", value)

    @builtins.property
    @jsii.member(jsii_name="durableObjectNamespaces")
    def durable_object_namespaces(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "durableObjectNamespaces"))

    @durable_object_namespaces.setter
    def durable_object_namespaces(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83862e07b097584ad169856e274afb876914de2143d94a69ffdea18590b374e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durableObjectNamespaces", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f75f0494da5237422cee37810bd1c00a9c4cabc2088bf4c1b04dca96e08087d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="kvNamespaces")
    def kv_namespaces(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "kvNamespaces"))

    @kv_namespaces.setter
    def kv_namespaces(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a48a56d9aee557c4e75403620428f4757e8a926ebc85aa313c234937ca129a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kvNamespaces", value)

    @builtins.property
    @jsii.member(jsii_name="r2Buckets")
    def r2_buckets(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "r2Buckets"))

    @r2_buckets.setter
    def r2_buckets(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66192263d06345a413de57fc01fa11468a4a21f754cbdf91893a405a353cd80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "r2Buckets", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PagesProjectDeploymentConfigsProduction]:
        return typing.cast(typing.Optional[PagesProjectDeploymentConfigsProduction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PagesProjectDeploymentConfigsProduction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35175326b28b2f7fe96351b76ce3c7430ea6837f3eac340d2f6d3655d52f0adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectSource",
    jsii_struct_bases=[],
    name_mapping={"config": "config", "type": "type"},
)
class PagesProjectSource:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["PagesProjectSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#config PagesProject#config}
        :param type: Project host type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#type PagesProject#type}
        '''
        if isinstance(config, dict):
            config = PagesProjectSourceConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a350c38bdfe501fc470a31a735e7a18ea66fce4461f5ea5e2cc2002d90fe57)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def config(self) -> typing.Optional["PagesProjectSourceConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#config PagesProject#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["PagesProjectSourceConfig"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Project host type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#type PagesProject#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesProjectSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "production_branch": "productionBranch",
        "deployments_enabled": "deploymentsEnabled",
        "owner": "owner",
        "pr_comments_enabled": "prCommentsEnabled",
        "preview_branch_excludes": "previewBranchExcludes",
        "preview_branch_includes": "previewBranchIncludes",
        "preview_deployment_setting": "previewDeploymentSetting",
        "production_deployment_enabled": "productionDeploymentEnabled",
        "repo_name": "repoName",
    },
)
class PagesProjectSourceConfig:
    def __init__(
        self,
        *,
        production_branch: builtins.str,
        deployments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        owner: typing.Optional[builtins.str] = None,
        pr_comments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preview_branch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        preview_branch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        preview_deployment_setting: typing.Optional[builtins.str] = None,
        production_deployment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repo_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param production_branch: Project production branch name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_branch PagesProject#production_branch}
        :param deployments_enabled: Toggle deployments on this repo. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#deployments_enabled PagesProject#deployments_enabled}
        :param owner: Project owner username. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#owner PagesProject#owner}
        :param pr_comments_enabled: Enable Pages to comment on Pull Requests. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#pr_comments_enabled PagesProject#pr_comments_enabled}
        :param preview_branch_excludes: Branches will be excluded from automatic deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_branch_excludes PagesProject#preview_branch_excludes}
        :param preview_branch_includes: Branches will be included for automatic deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_branch_includes PagesProject#preview_branch_includes}
        :param preview_deployment_setting: Preview Deployment Setting. Defaults to ``all``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_deployment_setting PagesProject#preview_deployment_setting}
        :param production_deployment_enabled: Enable production deployments. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_deployment_enabled PagesProject#production_deployment_enabled}
        :param repo_name: Project repository name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#repo_name PagesProject#repo_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39510fd2d65da87e37b9b4d6793fb57e2ac525a07c5a2da44593f385253a285)
            check_type(argname="argument production_branch", value=production_branch, expected_type=type_hints["production_branch"])
            check_type(argname="argument deployments_enabled", value=deployments_enabled, expected_type=type_hints["deployments_enabled"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument pr_comments_enabled", value=pr_comments_enabled, expected_type=type_hints["pr_comments_enabled"])
            check_type(argname="argument preview_branch_excludes", value=preview_branch_excludes, expected_type=type_hints["preview_branch_excludes"])
            check_type(argname="argument preview_branch_includes", value=preview_branch_includes, expected_type=type_hints["preview_branch_includes"])
            check_type(argname="argument preview_deployment_setting", value=preview_deployment_setting, expected_type=type_hints["preview_deployment_setting"])
            check_type(argname="argument production_deployment_enabled", value=production_deployment_enabled, expected_type=type_hints["production_deployment_enabled"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "production_branch": production_branch,
        }
        if deployments_enabled is not None:
            self._values["deployments_enabled"] = deployments_enabled
        if owner is not None:
            self._values["owner"] = owner
        if pr_comments_enabled is not None:
            self._values["pr_comments_enabled"] = pr_comments_enabled
        if preview_branch_excludes is not None:
            self._values["preview_branch_excludes"] = preview_branch_excludes
        if preview_branch_includes is not None:
            self._values["preview_branch_includes"] = preview_branch_includes
        if preview_deployment_setting is not None:
            self._values["preview_deployment_setting"] = preview_deployment_setting
        if production_deployment_enabled is not None:
            self._values["production_deployment_enabled"] = production_deployment_enabled
        if repo_name is not None:
            self._values["repo_name"] = repo_name

    @builtins.property
    def production_branch(self) -> builtins.str:
        '''Project production branch name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_branch PagesProject#production_branch}
        '''
        result = self._values.get("production_branch")
        assert result is not None, "Required property 'production_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployments_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Toggle deployments on this repo. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#deployments_enabled PagesProject#deployments_enabled}
        '''
        result = self._values.get("deployments_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Project owner username.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#owner PagesProject#owner}
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pr_comments_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Pages to comment on Pull Requests. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#pr_comments_enabled PagesProject#pr_comments_enabled}
        '''
        result = self._values.get("pr_comments_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def preview_branch_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Branches will be excluded from automatic deployment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_branch_excludes PagesProject#preview_branch_excludes}
        '''
        result = self._values.get("preview_branch_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preview_branch_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Branches will be included for automatic deployment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_branch_includes PagesProject#preview_branch_includes}
        '''
        result = self._values.get("preview_branch_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preview_deployment_setting(self) -> typing.Optional[builtins.str]:
        '''Preview Deployment Setting. Defaults to ``all``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_deployment_setting PagesProject#preview_deployment_setting}
        '''
        result = self._values.get("preview_deployment_setting")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def production_deployment_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable production deployments. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_deployment_enabled PagesProject#production_deployment_enabled}
        '''
        result = self._values.get("production_deployment_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def repo_name(self) -> typing.Optional[builtins.str]:
        '''Project repository name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#repo_name PagesProject#repo_name}
        '''
        result = self._values.get("repo_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesProjectSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PagesProjectSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectSourceConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6049651f4254f7dec38652d77a1f1e865a9d1754ffdcd26b2a942a078f6ec45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeploymentsEnabled")
    def reset_deployments_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentsEnabled", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetPrCommentsEnabled")
    def reset_pr_comments_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrCommentsEnabled", []))

    @jsii.member(jsii_name="resetPreviewBranchExcludes")
    def reset_preview_branch_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviewBranchExcludes", []))

    @jsii.member(jsii_name="resetPreviewBranchIncludes")
    def reset_preview_branch_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviewBranchIncludes", []))

    @jsii.member(jsii_name="resetPreviewDeploymentSetting")
    def reset_preview_deployment_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviewDeploymentSetting", []))

    @jsii.member(jsii_name="resetProductionDeploymentEnabled")
    def reset_production_deployment_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProductionDeploymentEnabled", []))

    @jsii.member(jsii_name="resetRepoName")
    def reset_repo_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepoName", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentsEnabledInput")
    def deployments_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deploymentsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="prCommentsEnabledInput")
    def pr_comments_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "prCommentsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="previewBranchExcludesInput")
    def preview_branch_excludes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "previewBranchExcludesInput"))

    @builtins.property
    @jsii.member(jsii_name="previewBranchIncludesInput")
    def preview_branch_includes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "previewBranchIncludesInput"))

    @builtins.property
    @jsii.member(jsii_name="previewDeploymentSettingInput")
    def preview_deployment_setting_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "previewDeploymentSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="productionBranchInput")
    def production_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productionBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="productionDeploymentEnabledInput")
    def production_deployment_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "productionDeploymentEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="repoNameInput")
    def repo_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentsEnabled")
    def deployments_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deploymentsEnabled"))

    @deployments_enabled.setter
    def deployments_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17a6b5a6165242dbb5797b2b5d2df31416edc2f5f28e9245480e0bb6c5fa69f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d721940abeacc9462b79b6f086f6dbbf1d7454721a984d5187109d1ef9781d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value)

    @builtins.property
    @jsii.member(jsii_name="prCommentsEnabled")
    def pr_comments_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "prCommentsEnabled"))

    @pr_comments_enabled.setter
    def pr_comments_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41d919260e3ac5408ba48074e89b050cd52867bc3825b78a1bf50163ad428e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prCommentsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="previewBranchExcludes")
    def preview_branch_excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "previewBranchExcludes"))

    @preview_branch_excludes.setter
    def preview_branch_excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba229809a5fe0048e0ce26e352e0de0bcf8088b4f24001998c7080c4dc257d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previewBranchExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="previewBranchIncludes")
    def preview_branch_includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "previewBranchIncludes"))

    @preview_branch_includes.setter
    def preview_branch_includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2558db516c416a760e87375b1f8367a6f5e8ebbe22a7dacd81184c2847e69a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previewBranchIncludes", value)

    @builtins.property
    @jsii.member(jsii_name="previewDeploymentSetting")
    def preview_deployment_setting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "previewDeploymentSetting"))

    @preview_deployment_setting.setter
    def preview_deployment_setting(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__919ee77dafbac4b4c1b808b5947dc7d331dd0a3260f97bd376b0a602679c1e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previewDeploymentSetting", value)

    @builtins.property
    @jsii.member(jsii_name="productionBranch")
    def production_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productionBranch"))

    @production_branch.setter
    def production_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa3d224dfc5c35aa7075d25ba015b53024e435701789a7bcf699dedb9a84cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productionBranch", value)

    @builtins.property
    @jsii.member(jsii_name="productionDeploymentEnabled")
    def production_deployment_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "productionDeploymentEnabled"))

    @production_deployment_enabled.setter
    def production_deployment_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cfd38250883d54efeb250104ca1f8f711b7a66b582fdfbd0b169f1f1a8b55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productionDeploymentEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @repo_name.setter
    def repo_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72212d6f12c26a75e6ed310b2afc8cae7bc0cbfe25fda3fa46def92734f10257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PagesProjectSourceConfig]:
        return typing.cast(typing.Optional[PagesProjectSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PagesProjectSourceConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03af7feda072e1d2e219e793730f3f542b45975a2d8c485b137295111325a197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PagesProjectSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.pagesProject.PagesProjectSourceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6379b8db0604424167bff638ef02c874d65dcbf77b00e94de1c3401ab4859708)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        production_branch: builtins.str,
        deployments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        owner: typing.Optional[builtins.str] = None,
        pr_comments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preview_branch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        preview_branch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        preview_deployment_setting: typing.Optional[builtins.str] = None,
        production_deployment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repo_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param production_branch: Project production branch name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_branch PagesProject#production_branch}
        :param deployments_enabled: Toggle deployments on this repo. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#deployments_enabled PagesProject#deployments_enabled}
        :param owner: Project owner username. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#owner PagesProject#owner}
        :param pr_comments_enabled: Enable Pages to comment on Pull Requests. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#pr_comments_enabled PagesProject#pr_comments_enabled}
        :param preview_branch_excludes: Branches will be excluded from automatic deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_branch_excludes PagesProject#preview_branch_excludes}
        :param preview_branch_includes: Branches will be included for automatic deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_branch_includes PagesProject#preview_branch_includes}
        :param preview_deployment_setting: Preview Deployment Setting. Defaults to ``all``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#preview_deployment_setting PagesProject#preview_deployment_setting}
        :param production_deployment_enabled: Enable production deployments. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#production_deployment_enabled PagesProject#production_deployment_enabled}
        :param repo_name: Project repository name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/pages_project#repo_name PagesProject#repo_name}
        '''
        value = PagesProjectSourceConfig(
            production_branch=production_branch,
            deployments_enabled=deployments_enabled,
            owner=owner,
            pr_comments_enabled=pr_comments_enabled,
            preview_branch_excludes=preview_branch_excludes,
            preview_branch_includes=preview_branch_includes,
            preview_deployment_setting=preview_deployment_setting,
            production_deployment_enabled=production_deployment_enabled,
            repo_name=repo_name,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> PagesProjectSourceConfigOutputReference:
        return typing.cast(PagesProjectSourceConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional[PagesProjectSourceConfig]:
        return typing.cast(typing.Optional[PagesProjectSourceConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2374ff2f25e189caef442453f610fe93ddcfdce036acafa4b58f1ed30940fda0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PagesProjectSource]:
        return typing.cast(typing.Optional[PagesProjectSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PagesProjectSource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee731c9c2f91c73570681f8265ad04919cb4f0058b752c89b6b5136784fa3a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "PagesProject",
    "PagesProjectBuildConfig",
    "PagesProjectBuildConfigOutputReference",
    "PagesProjectConfig",
    "PagesProjectDeploymentConfigs",
    "PagesProjectDeploymentConfigsOutputReference",
    "PagesProjectDeploymentConfigsPreview",
    "PagesProjectDeploymentConfigsPreviewOutputReference",
    "PagesProjectDeploymentConfigsProduction",
    "PagesProjectDeploymentConfigsProductionOutputReference",
    "PagesProjectSource",
    "PagesProjectSourceConfig",
    "PagesProjectSourceConfigOutputReference",
    "PagesProjectSourceOutputReference",
]

publication.publish()

def _typecheckingstub__32c8bd3ba18e0650df846b2d2e37dfef810ae73f984dcc34617f1efd60225d71(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    name: builtins.str,
    production_branch: builtins.str,
    build_config: typing.Optional[typing.Union[PagesProjectBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_configs: typing.Optional[typing.Union[PagesProjectDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[PagesProjectSource, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25d24d3b5e4450d1d1b773c3f5902e9faec8325dd51fa04efa4d99ffdce1420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492d7148c8029e959b254a35bdfa2fd8f846ae24bcf32a90ecd2808b99c6822b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcae619adfa6aa5276e7477d32740b0f98c950ea03e86467e16d2f2afa4af2f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6748f02b291e15157b0dfdadc8ffde3dfabf3d9c406daafd12d4c241863b058c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ddb1767df2790103b319dd95302c1ef2dcfeee4080c9df13a6923c7f947ef6(
    *,
    build_command: typing.Optional[builtins.str] = None,
    destination_dir: typing.Optional[builtins.str] = None,
    root_dir: typing.Optional[builtins.str] = None,
    web_analytics_tag: typing.Optional[builtins.str] = None,
    web_analytics_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a960c98b224c6cf61805a912db83a0d50aa489fd1ddff0a1969c14872ac349d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7be84ce85b9c62ce32b5dc2e25735ef178a42ae6c4e9c1119dfd8daf83ded4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5424df13dad2e1fd5edffc5ddcc1e83930ce5a31274ecb5d8574ef5c73362c58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4625699986a8ee4c0655efa7eeabca037c039abe2c03b7d7bcf3b7602be7d76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3a0913a4c6ccf4b97d8ec54a927ea9f9838b946db5e9009609ac0ce769a21a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76185d7b63462d674120a4c7e55a708a813fbeeaeb708206c04147ae22731b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2551caeefe9277427f352093f8384ff5673336bce649412aec8f7afec41509(
    value: typing.Optional[PagesProjectBuildConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0094d200e654f606607f96b58892accd8ce9d503242b6f5c7d06a2ae11897e53(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    name: builtins.str,
    production_branch: builtins.str,
    build_config: typing.Optional[typing.Union[PagesProjectBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_configs: typing.Optional[typing.Union[PagesProjectDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[PagesProjectSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7823fdc9b0a09eac3b8f24725ee9162c17ddca7ff78a36cba5175fe819813991(
    *,
    preview: typing.Optional[typing.Union[PagesProjectDeploymentConfigsPreview, typing.Dict[builtins.str, typing.Any]]] = None,
    production: typing.Optional[typing.Union[PagesProjectDeploymentConfigsProduction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfb360ea6a026f85cc04fa09830e4f97ca1f925ad9c49edc82b2bf67135a9d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bda509eaf75eb329c80e5e350ce8997a151563c736cfdcf50a669a795ffaa07(
    value: typing.Optional[PagesProjectDeploymentConfigs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e03862ac074ef15f724d9cc40bca42af7e9390d107765128d30dfa4a96e2ff(
    *,
    compatibility_date: typing.Optional[builtins.str] = None,
    compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    d1_databases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    durable_object_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kv_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    r2_buckets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1a53fd86f66b2bd391be423e5c8d24aeb47824bd64d504a301cf722c043d66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32865b61c6888db2bacfa85645fe28c8b167deb8ea98040548aefe9babd5762b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7134d0cb1462ec7eb665fd47f1f671843e450543c55d25eeefb57ec5363f35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad63f1044df17fe8ae94fbd4d63bccbf6d48a8f1ed944411add80c3153365674(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bb333283a4484bc9d8bae5685d56b3cf0275d0d6e92805948f8906596e0d0b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097ce8028e1dbd748366235c81f3e0314d9bb7c016fddca1daa31cc05c31effd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a6994bcb95a5de1f6856c21153f6c0fa14bed518cf92b4e28c190cb234683d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299679c6be59c45d6db5d4b5f6bd124e8f75f895526a79192e563f3f2e1310cb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fc5ad9dba9a0aa13954ab41f376699bde856670f046d16f6a4d579da2f821d(
    value: typing.Optional[PagesProjectDeploymentConfigsPreview],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336477b4868198acb01a1b41c8690524ec7ae03a6fd6dc2340a5ffb5c86959e1(
    *,
    compatibility_date: typing.Optional[builtins.str] = None,
    compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    d1_databases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    durable_object_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kv_namespaces: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    r2_buckets: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7265aa8b15c3914638516c9c006481db3073e868d9989557acf0a5b26b6db6e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0595cb8eff7f6b8d6e0bab4a75c9b33e7b8167dc670154c5d5ac8894ac886abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b984d2023ef3ff4c5e45625bd77fdd6b826d1556ca0e3b9d429b11e166f501(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eae0b9fb40004097f6a7ce41e30fbc14326d75a8e8a28d4c23ef5d532b91c3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83862e07b097584ad169856e274afb876914de2143d94a69ffdea18590b374e2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f75f0494da5237422cee37810bd1c00a9c4cabc2088bf4c1b04dca96e08087d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a48a56d9aee557c4e75403620428f4757e8a926ebc85aa313c234937ca129a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66192263d06345a413de57fc01fa11468a4a21f754cbdf91893a405a353cd80c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35175326b28b2f7fe96351b76ce3c7430ea6837f3eac340d2f6d3655d52f0adf(
    value: typing.Optional[PagesProjectDeploymentConfigsProduction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a350c38bdfe501fc470a31a735e7a18ea66fce4461f5ea5e2cc2002d90fe57(
    *,
    config: typing.Optional[typing.Union[PagesProjectSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39510fd2d65da87e37b9b4d6793fb57e2ac525a07c5a2da44593f385253a285(
    *,
    production_branch: builtins.str,
    deployments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    owner: typing.Optional[builtins.str] = None,
    pr_comments_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preview_branch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    preview_branch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    preview_deployment_setting: typing.Optional[builtins.str] = None,
    production_deployment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    repo_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6049651f4254f7dec38652d77a1f1e865a9d1754ffdcd26b2a942a078f6ec45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17a6b5a6165242dbb5797b2b5d2df31416edc2f5f28e9245480e0bb6c5fa69f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d721940abeacc9462b79b6f086f6dbbf1d7454721a984d5187109d1ef9781d6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41d919260e3ac5408ba48074e89b050cd52867bc3825b78a1bf50163ad428e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba229809a5fe0048e0ce26e352e0de0bcf8088b4f24001998c7080c4dc257d54(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2558db516c416a760e87375b1f8367a6f5e8ebbe22a7dacd81184c2847e69a26(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919ee77dafbac4b4c1b808b5947dc7d331dd0a3260f97bd376b0a602679c1e67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa3d224dfc5c35aa7075d25ba015b53024e435701789a7bcf699dedb9a84cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cfd38250883d54efeb250104ca1f8f711b7a66b582fdfbd0b169f1f1a8b55b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72212d6f12c26a75e6ed310b2afc8cae7bc0cbfe25fda3fa46def92734f10257(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03af7feda072e1d2e219e793730f3f542b45975a2d8c485b137295111325a197(
    value: typing.Optional[PagesProjectSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6379b8db0604424167bff638ef02c874d65dcbf77b00e94de1c3401ab4859708(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2374ff2f25e189caef442453f610fe93ddcfdce036acafa4b58f1ed30940fda0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee731c9c2f91c73570681f8265ad04919cb4f0058b752c89b6b5136784fa3a5(
    value: typing.Optional[PagesProjectSource],
) -> None:
    """Type checking stubs"""
    pass
