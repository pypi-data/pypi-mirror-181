'''
# `google_data_loss_prevention_deidentify_template`

Refer to the Terraform Registory for docs: [`google_data_loss_prevention_deidentify_template`](https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template).
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


class DataLossPreventionDeidentifyTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplate",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template google_data_loss_prevention_deidentify_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        deidentify_config: typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfig", typing.Dict[builtins.str, typing.Any]],
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template google_data_loss_prevention_deidentify_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param deidentify_config: deidentify_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#deidentify_config DataLossPreventionDeidentifyTemplate#deidentify_config}
        :param parent: The parent of the template in any of the following formats:. 'projects/{{project}}' 'projects/{{project}}/locations/{{location}}' 'organizations/{{organization_id}}' 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#parent DataLossPreventionDeidentifyTemplate#parent}
        :param description: A description of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#description DataLossPreventionDeidentifyTemplate#description}
        :param display_name: User set display name of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#display_name DataLossPreventionDeidentifyTemplate#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#id DataLossPreventionDeidentifyTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#timeouts DataLossPreventionDeidentifyTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6f5efc1c8e63859b44a0bd6ee94588c0f54772881c8a60cdd39275c0ddb874)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLossPreventionDeidentifyTemplateConfig(
            deidentify_config=deidentify_config,
            parent=parent,
            description=description,
            display_name=display_name,
            id=id,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putDeidentifyConfig")
    def put_deidentify_config(
        self,
        *,
        info_type_transformations: typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param info_type_transformations: info_type_transformations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#info_type_transformations DataLossPreventionDeidentifyTemplate#info_type_transformations}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfig(
            info_type_transformations=info_type_transformations
        )

        return typing.cast(None, jsii.invoke(self, "putDeidentifyConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#create DataLossPreventionDeidentifyTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#delete DataLossPreventionDeidentifyTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#update DataLossPreventionDeidentifyTemplate#update}.
        '''
        value = DataLossPreventionDeidentifyTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyConfig")
    def deidentify_config(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigOutputReference", jsii.get(self, "deidentifyConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataLossPreventionDeidentifyTemplateTimeoutsOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyConfigInput")
    def deidentify_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfig"], jsii.get(self, "deidentifyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3f7588f289d32348bf1a48da84c4495558851f53178efd4764b5b8e968a440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d181c6397e3e96372f61766f54eb9f00455a0d1c871829be60a057a09ad859fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10142721e91be8e4c6ac1d10847ad8b3278ed9f961b609aa273f9238bffca8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1584dc113a40112ba6fca702783a3adfecb8a0441703b56eaf3802f73e5b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "deidentify_config": "deidentifyConfig",
        "parent": "parent",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DataLossPreventionDeidentifyTemplateConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        deidentify_config: typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfig", typing.Dict[builtins.str, typing.Any]],
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param deidentify_config: deidentify_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#deidentify_config DataLossPreventionDeidentifyTemplate#deidentify_config}
        :param parent: The parent of the template in any of the following formats:. 'projects/{{project}}' 'projects/{{project}}/locations/{{location}}' 'organizations/{{organization_id}}' 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#parent DataLossPreventionDeidentifyTemplate#parent}
        :param description: A description of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#description DataLossPreventionDeidentifyTemplate#description}
        :param display_name: User set display name of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#display_name DataLossPreventionDeidentifyTemplate#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#id DataLossPreventionDeidentifyTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#timeouts DataLossPreventionDeidentifyTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deidentify_config, dict):
            deidentify_config = DataLossPreventionDeidentifyTemplateDeidentifyConfig(**deidentify_config)
        if isinstance(timeouts, dict):
            timeouts = DataLossPreventionDeidentifyTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d4228ecebba24a8247a0b74680daaf904fa71db8719430538d2953e99deae7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument deidentify_config", value=deidentify_config, expected_type=type_hints["deidentify_config"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deidentify_config": deidentify_config,
            "parent": parent,
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
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def deidentify_config(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfig":
        '''deidentify_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#deidentify_config DataLossPreventionDeidentifyTemplate#deidentify_config}
        '''
        result = self._values.get("deidentify_config")
        assert result is not None, "Required property 'deidentify_config' is missing"
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfig", result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent of the template in any of the following formats:.

        'projects/{{project}}'
        'projects/{{project}}/locations/{{location}}'
        'organizations/{{organization_id}}'
        'organizations/{{organization_id}}/locations/{{location}}'

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#parent DataLossPreventionDeidentifyTemplate#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#description DataLossPreventionDeidentifyTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User set display name of the template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#display_name DataLossPreventionDeidentifyTemplate#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#id DataLossPreventionDeidentifyTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#timeouts DataLossPreventionDeidentifyTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfig",
    jsii_struct_bases=[],
    name_mapping={"info_type_transformations": "infoTypeTransformations"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfig:
    def __init__(
        self,
        *,
        info_type_transformations: typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param info_type_transformations: info_type_transformations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#info_type_transformations DataLossPreventionDeidentifyTemplate#info_type_transformations}
        '''
        if isinstance(info_type_transformations, dict):
            info_type_transformations = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations(**info_type_transformations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ef9751a86cc88eb79013d4f41d8ef0769beb28b247712f464328afd7270475)
            check_type(argname="argument info_type_transformations", value=info_type_transformations, expected_type=type_hints["info_type_transformations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_type_transformations": info_type_transformations,
        }

    @builtins.property
    def info_type_transformations(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations":
        '''info_type_transformations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#info_type_transformations DataLossPreventionDeidentifyTemplate#info_type_transformations}
        '''
        result = self._values.get("info_type_transformations")
        assert result is not None, "Required property 'info_type_transformations' is missing"
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations",
    jsii_struct_bases=[],
    name_mapping={"transformations": "transformations"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations:
    def __init__(
        self,
        *,
        transformations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param transformations: transformations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transformations DataLossPreventionDeidentifyTemplate#transformations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7c48b9dfc14971580b6d65c192696626024a96cde15077a3f0d67f67cfc177)
            check_type(argname="argument transformations", value=transformations, expected_type=type_hints["transformations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transformations": transformations,
        }

    @builtins.property
    def transformations(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations"]]:
        '''transformations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transformations DataLossPreventionDeidentifyTemplate#transformations}
        '''
        result = self._values.get("transformations")
        assert result is not None, "Required property 'transformations' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c96f15eb324ba2084e9a8219199f8e21c282e326aefbe7b740b3751f7ce78adc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTransformations")
    def put_transformations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e83f2bb468a00421cd6a743067cdc1eec4d72f803d705bd0a2f56f2a4a55593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransformations", [value]))

    @builtins.property
    @jsii.member(jsii_name="transformations")
    def transformations(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsList":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsList", jsii.get(self, "transformations"))

    @builtins.property
    @jsii.member(jsii_name="transformationsInput")
    def transformations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations"]]], jsii.get(self, "transformationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4730be65480bbf6d13efd477e5c944e1493fcba98c43dfbf27ec7c27620e0ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations",
    jsii_struct_bases=[],
    name_mapping={
        "primitive_transformation": "primitiveTransformation",
        "info_types": "infoTypes",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations:
    def __init__(
        self,
        *,
        primitive_transformation: typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation", typing.Dict[builtins.str, typing.Any]],
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param primitive_transformation: primitive_transformation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#primitive_transformation DataLossPreventionDeidentifyTemplate#primitive_transformation}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#info_types DataLossPreventionDeidentifyTemplate#info_types}
        '''
        if isinstance(primitive_transformation, dict):
            primitive_transformation = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation(**primitive_transformation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e102ce66c08283bc89e09ac7a5ebc171bac8b65ea1d868ec122ff7d721c362c)
            check_type(argname="argument primitive_transformation", value=primitive_transformation, expected_type=type_hints["primitive_transformation"])
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primitive_transformation": primitive_transformation,
        }
        if info_types is not None:
            self._values["info_types"] = info_types

    @builtins.property
    def primitive_transformation(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation":
        '''primitive_transformation block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#primitive_transformation DataLossPreventionDeidentifyTemplate#primitive_transformation}
        '''
        result = self._values.get("primitive_transformation")
        assert result is not None, "Required property 'primitive_transformation' is missing"
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation", result)

    @builtins.property
    def info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes"]]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#info_types DataLossPreventionDeidentifyTemplate#info_types}
        '''
        result = self._values.get("info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the information type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93761c4b821d2dc605054e7dc72c33b56794d38b7d4f913c694d603bb76284db)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867b518b9b15676fa465431a18d5990725ce446aeb8b5a858af63e44dab1c824)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75895254c10848f3f46ad9164982f01c84a1f25ee04e1732225444445a5e2c8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3853a02b316ecd427796ce4a67856e5179059a986bfae5c7abf7e082e3361b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbb43efa134befc981696b3fce38e5a28e908d7ea268d7887e427b54b4af016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762b2bc6a4dd1a1ed73cb3981db96969a48b31cdebab3406bc42e5bd765da767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06f317a0c9bd7804e48e5a1a1b651e40de92bb3e0b115d7dc3c10f2b9ebad4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f81b46481b5521e5602de0ada5d37ff259026d9ed680f7a82a89863cfa9c82a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0aa2668b313774913898c6538c90637c6c6dd679405a438d641bbf75edb14e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20e817ed370ba02f5c80f6746147a1ca5e68b4a71ee552b564b116ec28e456b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b39c32cd937ed47106ff1b15ae971bb30f8edd2db0dc1fdd8a7a3ec26fd3fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe5bfa532a42a7c8d341325068083e23de4143bcd07c140498814b39365c20e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9aa49a4f19c16223840843216d64c8b91a47531696137b5b0180f4a242e3104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac8e16c431dd7cf625266de0fcf94abaa895714f05da65d6ca1575efbe29440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4de7e4f94798400d14523dacce9edc2d5c761e98e8549d37ac0b2fbf05e0ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced639a6c4ffe0acecaa21bd8cf806f078c0809373b24bba98545c7e37717be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ace4632c0882853891f35c5809d631d1c9d3368ae493b95566f45be306b51e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2ea878d4ffdcc23c7b22e9b0bd5a2537cf19982ab08f96b31e9af9435722ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putPrimitiveTransformation")
    def put_primitive_transformation(
        self,
        *,
        character_mask_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_deterministic_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_replace_ffx_fpe_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replace_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replace_with_info_type_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param character_mask_config: character_mask_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#character_mask_config DataLossPreventionDeidentifyTemplate#character_mask_config}
        :param crypto_deterministic_config: crypto_deterministic_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_deterministic_config DataLossPreventionDeidentifyTemplate#crypto_deterministic_config}
        :param crypto_replace_ffx_fpe_config: crypto_replace_ffx_fpe_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_replace_ffx_fpe_config DataLossPreventionDeidentifyTemplate#crypto_replace_ffx_fpe_config}
        :param replace_config: replace_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#replace_config DataLossPreventionDeidentifyTemplate#replace_config}
        :param replace_with_info_type_config: Replace each matching finding with the name of the info type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#replace_with_info_type_config DataLossPreventionDeidentifyTemplate#replace_with_info_type_config}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation(
            character_mask_config=character_mask_config,
            crypto_deterministic_config=crypto_deterministic_config,
            crypto_replace_ffx_fpe_config=crypto_replace_ffx_fpe_config,
            replace_config=replace_config,
            replace_with_info_type_config=replace_with_info_type_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimitiveTransformation", [value]))

    @jsii.member(jsii_name="resetInfoTypes")
    def reset_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfoTypes", []))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesList:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="primitiveTransformation")
    def primitive_transformation(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationOutputReference", jsii.get(self, "primitiveTransformation"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="primitiveTransformationInput")
    def primitive_transformation_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation"], jsii.get(self, "primitiveTransformationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e53dc79dc759151fa9b44444393f3454168c79f9b0bdecaa3bb98a06bcca79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation",
    jsii_struct_bases=[],
    name_mapping={
        "character_mask_config": "characterMaskConfig",
        "crypto_deterministic_config": "cryptoDeterministicConfig",
        "crypto_replace_ffx_fpe_config": "cryptoReplaceFfxFpeConfig",
        "replace_config": "replaceConfig",
        "replace_with_info_type_config": "replaceWithInfoTypeConfig",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation:
    def __init__(
        self,
        *,
        character_mask_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_deterministic_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_replace_ffx_fpe_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replace_config: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replace_with_info_type_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param character_mask_config: character_mask_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#character_mask_config DataLossPreventionDeidentifyTemplate#character_mask_config}
        :param crypto_deterministic_config: crypto_deterministic_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_deterministic_config DataLossPreventionDeidentifyTemplate#crypto_deterministic_config}
        :param crypto_replace_ffx_fpe_config: crypto_replace_ffx_fpe_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_replace_ffx_fpe_config DataLossPreventionDeidentifyTemplate#crypto_replace_ffx_fpe_config}
        :param replace_config: replace_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#replace_config DataLossPreventionDeidentifyTemplate#replace_config}
        :param replace_with_info_type_config: Replace each matching finding with the name of the info type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#replace_with_info_type_config DataLossPreventionDeidentifyTemplate#replace_with_info_type_config}
        '''
        if isinstance(character_mask_config, dict):
            character_mask_config = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig(**character_mask_config)
        if isinstance(crypto_deterministic_config, dict):
            crypto_deterministic_config = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig(**crypto_deterministic_config)
        if isinstance(crypto_replace_ffx_fpe_config, dict):
            crypto_replace_ffx_fpe_config = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig(**crypto_replace_ffx_fpe_config)
        if isinstance(replace_config, dict):
            replace_config = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig(**replace_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281548a2f50fe011498c4537c38a173cbc57de372bcc3831a8e1c0393c4a9ebc)
            check_type(argname="argument character_mask_config", value=character_mask_config, expected_type=type_hints["character_mask_config"])
            check_type(argname="argument crypto_deterministic_config", value=crypto_deterministic_config, expected_type=type_hints["crypto_deterministic_config"])
            check_type(argname="argument crypto_replace_ffx_fpe_config", value=crypto_replace_ffx_fpe_config, expected_type=type_hints["crypto_replace_ffx_fpe_config"])
            check_type(argname="argument replace_config", value=replace_config, expected_type=type_hints["replace_config"])
            check_type(argname="argument replace_with_info_type_config", value=replace_with_info_type_config, expected_type=type_hints["replace_with_info_type_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if character_mask_config is not None:
            self._values["character_mask_config"] = character_mask_config
        if crypto_deterministic_config is not None:
            self._values["crypto_deterministic_config"] = crypto_deterministic_config
        if crypto_replace_ffx_fpe_config is not None:
            self._values["crypto_replace_ffx_fpe_config"] = crypto_replace_ffx_fpe_config
        if replace_config is not None:
            self._values["replace_config"] = replace_config
        if replace_with_info_type_config is not None:
            self._values["replace_with_info_type_config"] = replace_with_info_type_config

    @builtins.property
    def character_mask_config(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig"]:
        '''character_mask_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#character_mask_config DataLossPreventionDeidentifyTemplate#character_mask_config}
        '''
        result = self._values.get("character_mask_config")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig"], result)

    @builtins.property
    def crypto_deterministic_config(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig"]:
        '''crypto_deterministic_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_deterministic_config DataLossPreventionDeidentifyTemplate#crypto_deterministic_config}
        '''
        result = self._values.get("crypto_deterministic_config")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig"], result)

    @builtins.property
    def crypto_replace_ffx_fpe_config(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig"]:
        '''crypto_replace_ffx_fpe_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_replace_ffx_fpe_config DataLossPreventionDeidentifyTemplate#crypto_replace_ffx_fpe_config}
        '''
        result = self._values.get("crypto_replace_ffx_fpe_config")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig"], result)

    @builtins.property
    def replace_config(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig"]:
        '''replace_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#replace_config DataLossPreventionDeidentifyTemplate#replace_config}
        '''
        result = self._values.get("replace_config")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig"], result)

    @builtins.property
    def replace_with_info_type_config(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Replace each matching finding with the name of the info type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#replace_with_info_type_config DataLossPreventionDeidentifyTemplate#replace_with_info_type_config}
        '''
        result = self._values.get("replace_with_info_type_config")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "characters_to_ignore": "charactersToIgnore",
        "masking_character": "maskingCharacter",
        "number_to_mask": "numberToMask",
        "reverse_order": "reverseOrder",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig:
    def __init__(
        self,
        *,
        characters_to_ignore: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore", typing.Dict[builtins.str, typing.Any]]]]] = None,
        masking_character: typing.Optional[builtins.str] = None,
        number_to_mask: typing.Optional[jsii.Number] = None,
        reverse_order: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param characters_to_ignore: characters_to_ignore block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#characters_to_ignore DataLossPreventionDeidentifyTemplate#characters_to_ignore}
        :param masking_character: Character to use to mask the sensitive values—for example, * for an alphabetic string such as a name, or 0 for a numeric string such as ZIP code or credit card number. This string must have a length of 1. If not supplied, this value defaults to * for strings, and 0 for digits. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#masking_character DataLossPreventionDeidentifyTemplate#masking_character}
        :param number_to_mask: Number of characters to mask. If not set, all matching chars will be masked. Skipped characters do not count towards this tally. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#number_to_mask DataLossPreventionDeidentifyTemplate#number_to_mask}
        :param reverse_order: Mask characters in reverse order. For example, if masking_character is 0, number_to_mask is 14, and reverse_order is 'false', then the input string '1234-5678-9012-3456' is masked as '00000000000000-3456'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#reverse_order DataLossPreventionDeidentifyTemplate#reverse_order}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdeb383b4e0077f6f8fa0e14c433f38a7f76c7ece9603ee789fab5a3bf5c061)
            check_type(argname="argument characters_to_ignore", value=characters_to_ignore, expected_type=type_hints["characters_to_ignore"])
            check_type(argname="argument masking_character", value=masking_character, expected_type=type_hints["masking_character"])
            check_type(argname="argument number_to_mask", value=number_to_mask, expected_type=type_hints["number_to_mask"])
            check_type(argname="argument reverse_order", value=reverse_order, expected_type=type_hints["reverse_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if characters_to_ignore is not None:
            self._values["characters_to_ignore"] = characters_to_ignore
        if masking_character is not None:
            self._values["masking_character"] = masking_character
        if number_to_mask is not None:
            self._values["number_to_mask"] = number_to_mask
        if reverse_order is not None:
            self._values["reverse_order"] = reverse_order

    @builtins.property
    def characters_to_ignore(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore"]]]:
        '''characters_to_ignore block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#characters_to_ignore DataLossPreventionDeidentifyTemplate#characters_to_ignore}
        '''
        result = self._values.get("characters_to_ignore")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore"]]], result)

    @builtins.property
    def masking_character(self) -> typing.Optional[builtins.str]:
        '''Character to use to mask the sensitive values—for example, * for an alphabetic string such as a name, or 0 for a numeric string such as ZIP code or credit card number.

        This string must have a length of 1. If not supplied, this value defaults to * for
        strings, and 0 for digits.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#masking_character DataLossPreventionDeidentifyTemplate#masking_character}
        '''
        result = self._values.get("masking_character")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def number_to_mask(self) -> typing.Optional[jsii.Number]:
        '''Number of characters to mask.

        If not set, all matching chars will be masked. Skipped characters do not count towards this tally.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#number_to_mask DataLossPreventionDeidentifyTemplate#number_to_mask}
        '''
        result = self._values.get("number_to_mask")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reverse_order(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Mask characters in reverse order.

        For example, if masking_character is 0, number_to_mask is 14, and reverse_order is 'false', then the
        input string '1234-5678-9012-3456' is masked as '00000000000000-3456'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#reverse_order DataLossPreventionDeidentifyTemplate#reverse_order}
        '''
        result = self._values.get("reverse_order")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore",
    jsii_struct_bases=[],
    name_mapping={
        "characters_to_skip": "charactersToSkip",
        "common_characters_to_ignore": "commonCharactersToIgnore",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore:
    def __init__(
        self,
        *,
        characters_to_skip: typing.Optional[builtins.str] = None,
        common_characters_to_ignore: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param characters_to_skip: Characters to not transform when masking. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#characters_to_skip DataLossPreventionDeidentifyTemplate#characters_to_skip}
        :param common_characters_to_ignore: Common characters to not transform when masking. Useful to avoid removing punctuation. Possible values: ["NUMERIC", "ALPHA_UPPER_CASE", "ALPHA_LOWER_CASE", "PUNCTUATION", "WHITESPACE"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#common_characters_to_ignore DataLossPreventionDeidentifyTemplate#common_characters_to_ignore}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0292d579db2e96f1bdf05bfbbbff0ef095c96bf16893b225161d60c439bc3718)
            check_type(argname="argument characters_to_skip", value=characters_to_skip, expected_type=type_hints["characters_to_skip"])
            check_type(argname="argument common_characters_to_ignore", value=common_characters_to_ignore, expected_type=type_hints["common_characters_to_ignore"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if characters_to_skip is not None:
            self._values["characters_to_skip"] = characters_to_skip
        if common_characters_to_ignore is not None:
            self._values["common_characters_to_ignore"] = common_characters_to_ignore

    @builtins.property
    def characters_to_skip(self) -> typing.Optional[builtins.str]:
        '''Characters to not transform when masking.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#characters_to_skip DataLossPreventionDeidentifyTemplate#characters_to_skip}
        '''
        result = self._values.get("characters_to_skip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def common_characters_to_ignore(self) -> typing.Optional[builtins.str]:
        '''Common characters to not transform when masking. Useful to avoid removing punctuation. Possible values: ["NUMERIC", "ALPHA_UPPER_CASE", "ALPHA_LOWER_CASE", "PUNCTUATION", "WHITESPACE"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#common_characters_to_ignore DataLossPreventionDeidentifyTemplate#common_characters_to_ignore}
        '''
        result = self._values.get("common_characters_to_ignore")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be4685f03d74eefcd779bf88c75e19a55b442c3e719961b1f450279a8592c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9d94343ab4beffc8afba37cb3f4d51d118a1db48a03371edd4bce18bc4b186)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624839077779b46788088f91e65200c9bf41cec2f7a78a37e4ec2e0b89d78c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056f82a7b96bdfdbbfb6c23a4ae4079095506d0660ab076358bc34d5ecc14d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c64cbf19b20de7919f4e77e1bb659f7fcb1277f2a64edf5d130481122c6e471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f75b6cfb3ab5b0514d43503f1157908c40b551c61cbb0453ada2be7e0ceea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8162c6c6b00a5cf908f4f130d7bc2a4d9da0bb4efd0b520d2cda59ae0b916b19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCharactersToSkip")
    def reset_characters_to_skip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCharactersToSkip", []))

    @jsii.member(jsii_name="resetCommonCharactersToIgnore")
    def reset_common_characters_to_ignore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonCharactersToIgnore", []))

    @builtins.property
    @jsii.member(jsii_name="charactersToSkipInput")
    def characters_to_skip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "charactersToSkipInput"))

    @builtins.property
    @jsii.member(jsii_name="commonCharactersToIgnoreInput")
    def common_characters_to_ignore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonCharactersToIgnoreInput"))

    @builtins.property
    @jsii.member(jsii_name="charactersToSkip")
    def characters_to_skip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "charactersToSkip"))

    @characters_to_skip.setter
    def characters_to_skip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1040588465595c9e731db1b59079f2353fb83c55eefae7367ab5ac27253b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "charactersToSkip", value)

    @builtins.property
    @jsii.member(jsii_name="commonCharactersToIgnore")
    def common_characters_to_ignore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonCharactersToIgnore"))

    @common_characters_to_ignore.setter
    def common_characters_to_ignore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccee178229f55235d71ceb4c1b52a06e42a6db52f81d077aa8fe48c4a39206fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonCharactersToIgnore", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769a3702303027c718c2a440ab277c4cbffb8a0bc962f92480fc15f611b6ceff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__024898f2491a09a359075061b823aab893c57b0b00f08262437ac3c7c1bc93f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCharactersToIgnore")
    def put_characters_to_ignore(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf30c013b87984003655c04a0c5f41ed4256e52ce24a36c90743662e15323892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCharactersToIgnore", [value]))

    @jsii.member(jsii_name="resetCharactersToIgnore")
    def reset_characters_to_ignore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCharactersToIgnore", []))

    @jsii.member(jsii_name="resetMaskingCharacter")
    def reset_masking_character(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaskingCharacter", []))

    @jsii.member(jsii_name="resetNumberToMask")
    def reset_number_to_mask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberToMask", []))

    @jsii.member(jsii_name="resetReverseOrder")
    def reset_reverse_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReverseOrder", []))

    @builtins.property
    @jsii.member(jsii_name="charactersToIgnore")
    def characters_to_ignore(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreList:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreList, jsii.get(self, "charactersToIgnore"))

    @builtins.property
    @jsii.member(jsii_name="charactersToIgnoreInput")
    def characters_to_ignore_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore]]], jsii.get(self, "charactersToIgnoreInput"))

    @builtins.property
    @jsii.member(jsii_name="maskingCharacterInput")
    def masking_character_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maskingCharacterInput"))

    @builtins.property
    @jsii.member(jsii_name="numberToMaskInput")
    def number_to_mask_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberToMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="reverseOrderInput")
    def reverse_order_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reverseOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="maskingCharacter")
    def masking_character(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maskingCharacter"))

    @masking_character.setter
    def masking_character(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6de070ea09866c5dc91a830f6ac1da778bbec407c60de674a9b09122c5aa8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maskingCharacter", value)

    @builtins.property
    @jsii.member(jsii_name="numberToMask")
    def number_to_mask(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberToMask"))

    @number_to_mask.setter
    def number_to_mask(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0546bb90b3f6d36265b3ab891ade41dfa98458bf739b60ba3837d2d7f0fa39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberToMask", value)

    @builtins.property
    @jsii.member(jsii_name="reverseOrder")
    def reverse_order(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reverseOrder"))

    @reverse_order.setter
    def reverse_order(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39160968b461fd895e9b942566fa19e3a8b1bb254b0063c79837a8e04a77cf2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reverseOrder", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c2f5ed83103ffdcf5c3e0798733279bd32a2109c8f8cb5db8d962f0f7fe527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig",
    jsii_struct_bases=[],
    name_mapping={
        "context": "context",
        "crypto_key": "cryptoKey",
        "surrogate_info_type": "surrogateInfoType",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig:
    def __init__(
        self,
        *,
        context: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey", typing.Dict[builtins.str, typing.Any]]] = None,
        surrogate_info_type: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param context: context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#context DataLossPreventionDeidentifyTemplate#context}
        :param crypto_key: crypto_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key DataLossPreventionDeidentifyTemplate#crypto_key}
        :param surrogate_info_type: surrogate_info_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#surrogate_info_type DataLossPreventionDeidentifyTemplate#surrogate_info_type}
        '''
        if isinstance(context, dict):
            context = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext(**context)
        if isinstance(crypto_key, dict):
            crypto_key = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey(**crypto_key)
        if isinstance(surrogate_info_type, dict):
            surrogate_info_type = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType(**surrogate_info_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63d352d56f6cbe205137d68f27171bf696a24010d9d6bb64d3e3c94cfa3aae6)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument crypto_key", value=crypto_key, expected_type=type_hints["crypto_key"])
            check_type(argname="argument surrogate_info_type", value=surrogate_info_type, expected_type=type_hints["surrogate_info_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if context is not None:
            self._values["context"] = context
        if crypto_key is not None:
            self._values["crypto_key"] = crypto_key
        if surrogate_info_type is not None:
            self._values["surrogate_info_type"] = surrogate_info_type

    @builtins.property
    def context(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext"]:
        '''context block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#context DataLossPreventionDeidentifyTemplate#context}
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext"], result)

    @builtins.property
    def crypto_key(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey"]:
        '''crypto_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key DataLossPreventionDeidentifyTemplate#crypto_key}
        '''
        result = self._values.get("crypto_key")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey"], result)

    @builtins.property
    def surrogate_info_type(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType"]:
        '''surrogate_info_type block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#surrogate_info_type DataLossPreventionDeidentifyTemplate#surrogate_info_type}
        '''
        result = self._values.get("surrogate_info_type")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1a6388a65c51ec019cee0fad6c748505f0a513454a8a3451759a892ad7df2a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name describing the field.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baac8b19e2205d3f87e1d66d785a465d16da877f08eec50f6bc18ccb8a009e81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acab88b171199b1ff30a70d9b05b51cf06d718531f024ea874cc85dad2d6319c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3fd204c0c438713926fc16f0c46acbe8b1e7a6733d1aea1fffb8e9f73a578c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_wrapped": "kmsWrapped",
        "transient": "transient",
        "unwrapped": "unwrapped",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey:
    def __init__(
        self,
        *,
        kms_wrapped: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped", typing.Dict[builtins.str, typing.Any]]] = None,
        transient: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient", typing.Dict[builtins.str, typing.Any]]] = None,
        unwrapped: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kms_wrapped: kms_wrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#kms_wrapped DataLossPreventionDeidentifyTemplate#kms_wrapped}
        :param transient: transient block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transient DataLossPreventionDeidentifyTemplate#transient}
        :param unwrapped: unwrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#unwrapped DataLossPreventionDeidentifyTemplate#unwrapped}
        '''
        if isinstance(kms_wrapped, dict):
            kms_wrapped = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped(**kms_wrapped)
        if isinstance(transient, dict):
            transient = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient(**transient)
        if isinstance(unwrapped, dict):
            unwrapped = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped(**unwrapped)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ba4275a261991d76ebb2fe979631f5e7ea3867427a9d54f5cf1b7ecb5ce133)
            check_type(argname="argument kms_wrapped", value=kms_wrapped, expected_type=type_hints["kms_wrapped"])
            check_type(argname="argument transient", value=transient, expected_type=type_hints["transient"])
            check_type(argname="argument unwrapped", value=unwrapped, expected_type=type_hints["unwrapped"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_wrapped is not None:
            self._values["kms_wrapped"] = kms_wrapped
        if transient is not None:
            self._values["transient"] = transient
        if unwrapped is not None:
            self._values["unwrapped"] = unwrapped

    @builtins.property
    def kms_wrapped(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped"]:
        '''kms_wrapped block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#kms_wrapped DataLossPreventionDeidentifyTemplate#kms_wrapped}
        '''
        result = self._values.get("kms_wrapped")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped"], result)

    @builtins.property
    def transient(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient"]:
        '''transient block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transient DataLossPreventionDeidentifyTemplate#transient}
        '''
        result = self._values.get("transient")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient"], result)

    @builtins.property
    def unwrapped(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped"]:
        '''unwrapped block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#unwrapped DataLossPreventionDeidentifyTemplate#unwrapped}
        '''
        result = self._values.get("unwrapped")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped",
    jsii_struct_bases=[],
    name_mapping={"crypto_key_name": "cryptoKeyName", "wrapped_key": "wrappedKey"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped:
    def __init__(
        self,
        *,
        crypto_key_name: builtins.str,
        wrapped_key: builtins.str,
    ) -> None:
        '''
        :param crypto_key_name: The resource name of the KMS CryptoKey to use for unwrapping. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key_name DataLossPreventionDeidentifyTemplate#crypto_key_name}
        :param wrapped_key: The wrapped data crypto key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#wrapped_key DataLossPreventionDeidentifyTemplate#wrapped_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b092be71d960e672d1c67242c5ae810c6d74abf404f853c5dc1ae42e5a4434)
            check_type(argname="argument crypto_key_name", value=crypto_key_name, expected_type=type_hints["crypto_key_name"])
            check_type(argname="argument wrapped_key", value=wrapped_key, expected_type=type_hints["wrapped_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crypto_key_name": crypto_key_name,
            "wrapped_key": wrapped_key,
        }

    @builtins.property
    def crypto_key_name(self) -> builtins.str:
        '''The resource name of the KMS CryptoKey to use for unwrapping.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key_name DataLossPreventionDeidentifyTemplate#crypto_key_name}
        '''
        result = self._values.get("crypto_key_name")
        assert result is not None, "Required property 'crypto_key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wrapped_key(self) -> builtins.str:
        '''The wrapped data crypto key.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#wrapped_key DataLossPreventionDeidentifyTemplate#wrapped_key}
        '''
        result = self._values.get("wrapped_key")
        assert result is not None, "Required property 'wrapped_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrappedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrappedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be4e25df129e1f494f6d53966a989b4a1e55758277b96ae08e691f708e6879bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyNameInput")
    def crypto_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cryptoKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="wrappedKeyInput")
    def wrapped_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wrappedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyName")
    def crypto_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cryptoKeyName"))

    @crypto_key_name.setter
    def crypto_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b934811443f9691d2e4ad79b80b98d687e550bf5a41efa710946cdaacc5ecbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cryptoKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="wrappedKey")
    def wrapped_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wrappedKey"))

    @wrapped_key.setter
    def wrapped_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d15698eda798f5c8f29ac8033f9591b194d2deeedac28123d269f59be6ea471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrappedKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89039ccdc980f8803590d1e2985acc6dcc01311c6d277e52da5729153491fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0748f018dc781012f427a91c70054a5953eb0acf4cb4404f545eaf28bd9b8e47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKmsWrapped")
    def put_kms_wrapped(
        self,
        *,
        crypto_key_name: builtins.str,
        wrapped_key: builtins.str,
    ) -> None:
        '''
        :param crypto_key_name: The resource name of the KMS CryptoKey to use for unwrapping. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key_name DataLossPreventionDeidentifyTemplate#crypto_key_name}
        :param wrapped_key: The wrapped data crypto key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#wrapped_key DataLossPreventionDeidentifyTemplate#wrapped_key}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped(
            crypto_key_name=crypto_key_name, wrapped_key=wrapped_key
        )

        return typing.cast(None, jsii.invoke(self, "putKmsWrapped", [value]))

    @jsii.member(jsii_name="putTransient")
    def put_transient(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the key. This is an arbitrary string used to differentiate different keys. A unique key is generated per name: two separate 'TransientCryptoKey' protos share the same generated key if their names are the same. When the data crypto key is generated, this name is not used in any way (repeating the api call will result in a different key being generated). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTransient", [value]))

    @jsii.member(jsii_name="putUnwrapped")
    def put_unwrapped(self, *, key: builtins.str) -> None:
        '''
        :param key: A 128/192/256 bit key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#key DataLossPreventionDeidentifyTemplate#key}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped(
            key=key
        )

        return typing.cast(None, jsii.invoke(self, "putUnwrapped", [value]))

    @jsii.member(jsii_name="resetKmsWrapped")
    def reset_kms_wrapped(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsWrapped", []))

    @jsii.member(jsii_name="resetTransient")
    def reset_transient(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransient", []))

    @jsii.member(jsii_name="resetUnwrapped")
    def reset_unwrapped(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnwrapped", []))

    @builtins.property
    @jsii.member(jsii_name="kmsWrapped")
    def kms_wrapped(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrappedOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrappedOutputReference, jsii.get(self, "kmsWrapped"))

    @builtins.property
    @jsii.member(jsii_name="transient")
    def transient(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransientOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransientOutputReference", jsii.get(self, "transient"))

    @builtins.property
    @jsii.member(jsii_name="unwrapped")
    def unwrapped(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrappedOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrappedOutputReference", jsii.get(self, "unwrapped"))

    @builtins.property
    @jsii.member(jsii_name="kmsWrappedInput")
    def kms_wrapped_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped], jsii.get(self, "kmsWrappedInput"))

    @builtins.property
    @jsii.member(jsii_name="transientInput")
    def transient_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient"], jsii.get(self, "transientInput"))

    @builtins.property
    @jsii.member(jsii_name="unwrappedInput")
    def unwrapped_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped"], jsii.get(self, "unwrappedInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2caca3a8dae16a5d7e1abbf3b277e994b3ea02f7872ff1a34fef72290e71a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the key. This is an arbitrary string used to differentiate different keys. A unique key is generated per name: two separate 'TransientCryptoKey' protos share the same generated key if their names are the same. When the data crypto key is generated, this name is not used in any way (repeating the api call will result in a different key being generated). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53d356028df3c640df6ad4c87fc4f872b5ec0e5ec1a29f211c295c9deb908c8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the key.

        This is an arbitrary string used to differentiate different keys. A unique key is generated per name: two separate 'TransientCryptoKey' protos share the same generated key if their names are the same. When the data crypto key is generated, this name is not used in any way (repeating the api call will result in a different key being generated).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransientOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransientOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a196e719a93e603e49aa9fbbce0d67a0ccf8328f69f2be9ee486c113e421781)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac50542264d6e2d1bfd7c8fa755b93c32f73370d74379819f7bfaacff8708dcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a120541c4902312a5ef21adf9b7c6210b62c870b9ba7eae430bf361799bc03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped",
    jsii_struct_bases=[],
    name_mapping={"key": "key"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped:
    def __init__(self, *, key: builtins.str) -> None:
        '''
        :param key: A 128/192/256 bit key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#key DataLossPreventionDeidentifyTemplate#key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7801658292b82a119d5d9ce88c3468805233deb2ad25ebbe48bd3d372a3a1f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''A 128/192/256 bit key.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#key DataLossPreventionDeidentifyTemplate#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrappedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrappedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af066a49c9053f3089c0d95f714eb2d7d6917ef6cc442dad13079b6dcdd0074f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70111a32c953a829e8fbf3da6424a6842c2987126e563975a756d7b9c8054a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a909f17cfa377873c4e5d1802735320ef9654f4c2bded0f3873549acf7d38dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e13bd32963d7126724dac8b730ab931b8e048c0166449393f2a30d7dfd7fe6bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContext")
    def put_context(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putContext", [value]))

    @jsii.member(jsii_name="putCryptoKey")
    def put_crypto_key(
        self,
        *,
        kms_wrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped, typing.Dict[builtins.str, typing.Any]]] = None,
        transient: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient, typing.Dict[builtins.str, typing.Any]]] = None,
        unwrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kms_wrapped: kms_wrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#kms_wrapped DataLossPreventionDeidentifyTemplate#kms_wrapped}
        :param transient: transient block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transient DataLossPreventionDeidentifyTemplate#transient}
        :param unwrapped: unwrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#unwrapped DataLossPreventionDeidentifyTemplate#unwrapped}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey(
            kms_wrapped=kms_wrapped, transient=transient, unwrapped=unwrapped
        )

        return typing.cast(None, jsii.invoke(self, "putCryptoKey", [value]))

    @jsii.member(jsii_name="putSurrogateInfoType")
    def put_surrogate_info_type(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at `https://cloud.google.com/dlp/docs/infotypes-reference <https://cloud.google.com/dlp/docs/infotypes-reference>`_ when specifying a built-in type. When sending Cloud DLP results to Data Catalog, infoType names should conform to the pattern '[A-Za-z0-9$-_]{1,64}'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putSurrogateInfoType", [value]))

    @jsii.member(jsii_name="resetContext")
    def reset_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContext", []))

    @jsii.member(jsii_name="resetCryptoKey")
    def reset_crypto_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoKey", []))

    @jsii.member(jsii_name="resetSurrogateInfoType")
    def reset_surrogate_info_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSurrogateInfoType", []))

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContextOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContextOutputReference, jsii.get(self, "context"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKey")
    def crypto_key(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyOutputReference, jsii.get(self, "cryptoKey"))

    @builtins.property
    @jsii.member(jsii_name="surrogateInfoType")
    def surrogate_info_type(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoTypeOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoTypeOutputReference", jsii.get(self, "surrogateInfoType"))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyInput")
    def crypto_key_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey], jsii.get(self, "cryptoKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="surrogateInfoTypeInput")
    def surrogate_info_type_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType"], jsii.get(self, "surrogateInfoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75e971486d005a54edc43cd5fd3b5a6b6689e4d19dd819d8b2333d94f8122a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at `https://cloud.google.com/dlp/docs/infotypes-reference <https://cloud.google.com/dlp/docs/infotypes-reference>`_ when specifying a built-in type. When sending Cloud DLP results to Data Catalog, infoType names should conform to the pattern '[A-Za-z0-9$-_]{1,64}'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c6c72d843e79dae13d92773ad1234e20ed149400fffafd97df76cd5eb5392a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed at `https://cloud.google.com/dlp/docs/infotypes-reference <https://cloud.google.com/dlp/docs/infotypes-reference>`_ when specifying a built-in type. When sending Cloud DLP results to Data Catalog, infoType names should conform to the pattern '[A-Za-z0-9$-_]{1,64}'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8bb39f7bf5f7bd51983722480f54209ae90aa2d25ff98879936bb54bf9d1250)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35706f3a8ca835ffd24c991527ac20e4c61172938877b141b9b536a6bdcae22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfaf8e9019230f69f7956ff471097f5b9de47cc244c4720358150a542de625b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "common_alphabet": "commonAlphabet",
        "context": "context",
        "crypto_key": "cryptoKey",
        "custom_alphabet": "customAlphabet",
        "radix": "radix",
        "surrogate_info_type": "surrogateInfoType",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig:
    def __init__(
        self,
        *,
        common_alphabet: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_alphabet: typing.Optional[builtins.str] = None,
        radix: typing.Optional[jsii.Number] = None,
        surrogate_info_type: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param common_alphabet: Common alphabets. Possible values: ["FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED", "NUMERIC", "HEXADECIMAL", "UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#common_alphabet DataLossPreventionDeidentifyTemplate#common_alphabet}
        :param context: context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#context DataLossPreventionDeidentifyTemplate#context}
        :param crypto_key: crypto_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key DataLossPreventionDeidentifyTemplate#crypto_key}
        :param custom_alphabet: This is supported by mapping these to the alphanumeric characters that the FFX mode natively supports. This happens before/after encryption/decryption. Each character listed must appear only once. Number of characters must be in the range [2, 95]. This must be encoded as ASCII. The order of characters does not matter. The full list of allowed characters is: ''0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ~'!@#$%^&*()_-+={[}]|:;"'<,>.?/'' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#custom_alphabet DataLossPreventionDeidentifyTemplate#custom_alphabet}
        :param radix: The native way to select the alphabet. Must be in the range [2, 95]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#radix DataLossPreventionDeidentifyTemplate#radix}
        :param surrogate_info_type: surrogate_info_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#surrogate_info_type DataLossPreventionDeidentifyTemplate#surrogate_info_type}
        '''
        if isinstance(context, dict):
            context = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext(**context)
        if isinstance(crypto_key, dict):
            crypto_key = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey(**crypto_key)
        if isinstance(surrogate_info_type, dict):
            surrogate_info_type = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType(**surrogate_info_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d5fef9cb45ff890eec16e6587a1fd11b1c60bbb0120b9488f96f54355eddf7)
            check_type(argname="argument common_alphabet", value=common_alphabet, expected_type=type_hints["common_alphabet"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument crypto_key", value=crypto_key, expected_type=type_hints["crypto_key"])
            check_type(argname="argument custom_alphabet", value=custom_alphabet, expected_type=type_hints["custom_alphabet"])
            check_type(argname="argument radix", value=radix, expected_type=type_hints["radix"])
            check_type(argname="argument surrogate_info_type", value=surrogate_info_type, expected_type=type_hints["surrogate_info_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if common_alphabet is not None:
            self._values["common_alphabet"] = common_alphabet
        if context is not None:
            self._values["context"] = context
        if crypto_key is not None:
            self._values["crypto_key"] = crypto_key
        if custom_alphabet is not None:
            self._values["custom_alphabet"] = custom_alphabet
        if radix is not None:
            self._values["radix"] = radix
        if surrogate_info_type is not None:
            self._values["surrogate_info_type"] = surrogate_info_type

    @builtins.property
    def common_alphabet(self) -> typing.Optional[builtins.str]:
        '''Common alphabets. Possible values: ["FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED", "NUMERIC", "HEXADECIMAL", "UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#common_alphabet DataLossPreventionDeidentifyTemplate#common_alphabet}
        '''
        result = self._values.get("common_alphabet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext"]:
        '''context block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#context DataLossPreventionDeidentifyTemplate#context}
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext"], result)

    @builtins.property
    def crypto_key(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey"]:
        '''crypto_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key DataLossPreventionDeidentifyTemplate#crypto_key}
        '''
        result = self._values.get("crypto_key")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey"], result)

    @builtins.property
    def custom_alphabet(self) -> typing.Optional[builtins.str]:
        '''This is supported by mapping these to the alphanumeric characters that the FFX mode natively supports.

        This happens before/after encryption/decryption. Each character listed must appear only once. Number of characters must be in the range [2, 95]. This must be encoded as ASCII. The order of characters does not matter. The full list of allowed characters is:

        ''0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ~'!@#$%^&*()_-+={[}]|:;"'<,>.?/''

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#custom_alphabet DataLossPreventionDeidentifyTemplate#custom_alphabet}
        '''
        result = self._values.get("custom_alphabet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def radix(self) -> typing.Optional[jsii.Number]:
        '''The native way to select the alphabet. Must be in the range [2, 95].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#radix DataLossPreventionDeidentifyTemplate#radix}
        '''
        result = self._values.get("radix")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def surrogate_info_type(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType"]:
        '''surrogate_info_type block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#surrogate_info_type DataLossPreventionDeidentifyTemplate#surrogate_info_type}
        '''
        result = self._values.get("surrogate_info_type")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341432daf25ab00ff81695bd7c01407e7422497d6698538cbe6b951815c79989)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name describing the field.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48632123032fcd33c94b17559fba37fc54a4c87aedfd1d86d395cadc33e860cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0d0312a25dda77f305c912112b074521ce584f6590590b392f52c6b37ab983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9f8ab0af0156d7a931b07857714ec596f27501661440b8caa535c185c9d1b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_wrapped": "kmsWrapped",
        "transient": "transient",
        "unwrapped": "unwrapped",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey:
    def __init__(
        self,
        *,
        kms_wrapped: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped", typing.Dict[builtins.str, typing.Any]]] = None,
        transient: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient", typing.Dict[builtins.str, typing.Any]]] = None,
        unwrapped: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kms_wrapped: kms_wrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#kms_wrapped DataLossPreventionDeidentifyTemplate#kms_wrapped}
        :param transient: transient block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transient DataLossPreventionDeidentifyTemplate#transient}
        :param unwrapped: unwrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#unwrapped DataLossPreventionDeidentifyTemplate#unwrapped}
        '''
        if isinstance(kms_wrapped, dict):
            kms_wrapped = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped(**kms_wrapped)
        if isinstance(transient, dict):
            transient = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient(**transient)
        if isinstance(unwrapped, dict):
            unwrapped = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped(**unwrapped)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c833f8be98ffc0fa9b9f6a6e5613014836172cbc9e61a7823168d8d2ab7b872)
            check_type(argname="argument kms_wrapped", value=kms_wrapped, expected_type=type_hints["kms_wrapped"])
            check_type(argname="argument transient", value=transient, expected_type=type_hints["transient"])
            check_type(argname="argument unwrapped", value=unwrapped, expected_type=type_hints["unwrapped"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_wrapped is not None:
            self._values["kms_wrapped"] = kms_wrapped
        if transient is not None:
            self._values["transient"] = transient
        if unwrapped is not None:
            self._values["unwrapped"] = unwrapped

    @builtins.property
    def kms_wrapped(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped"]:
        '''kms_wrapped block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#kms_wrapped DataLossPreventionDeidentifyTemplate#kms_wrapped}
        '''
        result = self._values.get("kms_wrapped")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped"], result)

    @builtins.property
    def transient(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient"]:
        '''transient block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transient DataLossPreventionDeidentifyTemplate#transient}
        '''
        result = self._values.get("transient")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient"], result)

    @builtins.property
    def unwrapped(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped"]:
        '''unwrapped block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#unwrapped DataLossPreventionDeidentifyTemplate#unwrapped}
        '''
        result = self._values.get("unwrapped")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped",
    jsii_struct_bases=[],
    name_mapping={"crypto_key_name": "cryptoKeyName", "wrapped_key": "wrappedKey"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped:
    def __init__(
        self,
        *,
        crypto_key_name: builtins.str,
        wrapped_key: builtins.str,
    ) -> None:
        '''
        :param crypto_key_name: The resource name of the KMS CryptoKey to use for unwrapping. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key_name DataLossPreventionDeidentifyTemplate#crypto_key_name}
        :param wrapped_key: The wrapped data crypto key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#wrapped_key DataLossPreventionDeidentifyTemplate#wrapped_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b6f3dd10cb36e21651554e0e92bd80d80d2cc3d7837f74ad63d122c2bc6d38)
            check_type(argname="argument crypto_key_name", value=crypto_key_name, expected_type=type_hints["crypto_key_name"])
            check_type(argname="argument wrapped_key", value=wrapped_key, expected_type=type_hints["wrapped_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crypto_key_name": crypto_key_name,
            "wrapped_key": wrapped_key,
        }

    @builtins.property
    def crypto_key_name(self) -> builtins.str:
        '''The resource name of the KMS CryptoKey to use for unwrapping.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key_name DataLossPreventionDeidentifyTemplate#crypto_key_name}
        '''
        result = self._values.get("crypto_key_name")
        assert result is not None, "Required property 'crypto_key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wrapped_key(self) -> builtins.str:
        '''The wrapped data crypto key.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#wrapped_key DataLossPreventionDeidentifyTemplate#wrapped_key}
        '''
        result = self._values.get("wrapped_key")
        assert result is not None, "Required property 'wrapped_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrappedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrappedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ef4e6db699ef0fe723cc2c82f2a41429dd6e35d6011c84e62caa8f4101acba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyNameInput")
    def crypto_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cryptoKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="wrappedKeyInput")
    def wrapped_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wrappedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyName")
    def crypto_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cryptoKeyName"))

    @crypto_key_name.setter
    def crypto_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d336a9b71db1ef454c8f57681d1f59ea9991e211de764b4b71c8afb678cc75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cryptoKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="wrappedKey")
    def wrapped_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wrappedKey"))

    @wrapped_key.setter
    def wrapped_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d06c03369fe29e99f8f03cb4850bf0392d75d9224f9d5fa1cff7976dd84edcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrappedKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6aa3bb67cee71087cff4002fcf2444df4aae73d3870af90afd3fa3ac3273a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1be5a7c089a8580b8ce6faa1d013d2c10675a2cde7ed5e0408fe5b36bf5c1c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKmsWrapped")
    def put_kms_wrapped(
        self,
        *,
        crypto_key_name: builtins.str,
        wrapped_key: builtins.str,
    ) -> None:
        '''
        :param crypto_key_name: The resource name of the KMS CryptoKey to use for unwrapping. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key_name DataLossPreventionDeidentifyTemplate#crypto_key_name}
        :param wrapped_key: The wrapped data crypto key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#wrapped_key DataLossPreventionDeidentifyTemplate#wrapped_key}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped(
            crypto_key_name=crypto_key_name, wrapped_key=wrapped_key
        )

        return typing.cast(None, jsii.invoke(self, "putKmsWrapped", [value]))

    @jsii.member(jsii_name="putTransient")
    def put_transient(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the key. This is an arbitrary string used to differentiate different keys. A unique key is generated per name: two separate 'TransientCryptoKey' protos share the same generated key if their names are the same. When the data crypto key is generated, this name is not used in any way (repeating the api call will result in a different key being generated). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTransient", [value]))

    @jsii.member(jsii_name="putUnwrapped")
    def put_unwrapped(self, *, key: builtins.str) -> None:
        '''
        :param key: A 128/192/256 bit key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#key DataLossPreventionDeidentifyTemplate#key}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped(
            key=key
        )

        return typing.cast(None, jsii.invoke(self, "putUnwrapped", [value]))

    @jsii.member(jsii_name="resetKmsWrapped")
    def reset_kms_wrapped(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsWrapped", []))

    @jsii.member(jsii_name="resetTransient")
    def reset_transient(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransient", []))

    @jsii.member(jsii_name="resetUnwrapped")
    def reset_unwrapped(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnwrapped", []))

    @builtins.property
    @jsii.member(jsii_name="kmsWrapped")
    def kms_wrapped(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrappedOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrappedOutputReference, jsii.get(self, "kmsWrapped"))

    @builtins.property
    @jsii.member(jsii_name="transient")
    def transient(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransientOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransientOutputReference", jsii.get(self, "transient"))

    @builtins.property
    @jsii.member(jsii_name="unwrapped")
    def unwrapped(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrappedOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrappedOutputReference", jsii.get(self, "unwrapped"))

    @builtins.property
    @jsii.member(jsii_name="kmsWrappedInput")
    def kms_wrapped_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped], jsii.get(self, "kmsWrappedInput"))

    @builtins.property
    @jsii.member(jsii_name="transientInput")
    def transient_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient"], jsii.get(self, "transientInput"))

    @builtins.property
    @jsii.member(jsii_name="unwrappedInput")
    def unwrapped_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped"], jsii.get(self, "unwrappedInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186eab9ee75aff9d2476915f4e8b4e784a4e987361856263f12634d8948f7717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the key. This is an arbitrary string used to differentiate different keys. A unique key is generated per name: two separate 'TransientCryptoKey' protos share the same generated key if their names are the same. When the data crypto key is generated, this name is not used in any way (repeating the api call will result in a different key being generated). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eaeb162026d06d9879ddaa261e17da2713643d05324571d6cc58c0b7e0f171a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the key.

        This is an arbitrary string used to differentiate different keys. A unique key is generated per name: two separate 'TransientCryptoKey' protos share the same generated key if their names are the same. When the data crypto key is generated, this name is not used in any way (repeating the api call will result in a different key being generated).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransientOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransientOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f06c584cf7cf9fa80db3c3229edff93d29fd591e1d2f18fbee2d65227267bc81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e839dab15283de0e9df6800160e9d04c3814ed6abb434f069278b7cf1949f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175f85c2ca75239fbe6bf2730ee10614538c582a1ca02b273622e7178aa34e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped",
    jsii_struct_bases=[],
    name_mapping={"key": "key"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped:
    def __init__(self, *, key: builtins.str) -> None:
        '''
        :param key: A 128/192/256 bit key. A base64-encoded string. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#key DataLossPreventionDeidentifyTemplate#key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113c434f328952324aa3fa00e291c16242ba95a9fbed9f01c091e948be9cfd8f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''A 128/192/256 bit key.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#key DataLossPreventionDeidentifyTemplate#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrappedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrappedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce33ff090f147ae866ec032809531b7280c62099be3c45624b60c1668bc932df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0e020a2d1398a262c5473d64e5320738c2ecfb589cfb132d35c1eab8d82d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531cbb938c6e4180c62765e1c987eedd2e3437ed6422e2e98f68f8c5cd7fbf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba34bfec41e8574ec9aac95062dce75844f384bdb8b6f94b53c1add2878ecb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContext")
    def put_context(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name describing the field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putContext", [value]))

    @jsii.member(jsii_name="putCryptoKey")
    def put_crypto_key(
        self,
        *,
        kms_wrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped, typing.Dict[builtins.str, typing.Any]]] = None,
        transient: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient, typing.Dict[builtins.str, typing.Any]]] = None,
        unwrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kms_wrapped: kms_wrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#kms_wrapped DataLossPreventionDeidentifyTemplate#kms_wrapped}
        :param transient: transient block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transient DataLossPreventionDeidentifyTemplate#transient}
        :param unwrapped: unwrapped block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#unwrapped DataLossPreventionDeidentifyTemplate#unwrapped}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey(
            kms_wrapped=kms_wrapped, transient=transient, unwrapped=unwrapped
        )

        return typing.cast(None, jsii.invoke(self, "putCryptoKey", [value]))

    @jsii.member(jsii_name="putSurrogateInfoType")
    def put_surrogate_info_type(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at `https://cloud.google.com/dlp/docs/infotypes-reference <https://cloud.google.com/dlp/docs/infotypes-reference>`_ when specifying a built-in type. When sending Cloud DLP results to Data Catalog, infoType names should conform to the pattern '[A-Za-z0-9$-_]{1,64}'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putSurrogateInfoType", [value]))

    @jsii.member(jsii_name="resetCommonAlphabet")
    def reset_common_alphabet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonAlphabet", []))

    @jsii.member(jsii_name="resetContext")
    def reset_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContext", []))

    @jsii.member(jsii_name="resetCryptoKey")
    def reset_crypto_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoKey", []))

    @jsii.member(jsii_name="resetCustomAlphabet")
    def reset_custom_alphabet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAlphabet", []))

    @jsii.member(jsii_name="resetRadix")
    def reset_radix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRadix", []))

    @jsii.member(jsii_name="resetSurrogateInfoType")
    def reset_surrogate_info_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSurrogateInfoType", []))

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContextOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContextOutputReference, jsii.get(self, "context"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKey")
    def crypto_key(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyOutputReference, jsii.get(self, "cryptoKey"))

    @builtins.property
    @jsii.member(jsii_name="surrogateInfoType")
    def surrogate_info_type(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoTypeOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoTypeOutputReference", jsii.get(self, "surrogateInfoType"))

    @builtins.property
    @jsii.member(jsii_name="commonAlphabetInput")
    def common_alphabet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonAlphabetInput"))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyInput")
    def crypto_key_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey], jsii.get(self, "cryptoKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="customAlphabetInput")
    def custom_alphabet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customAlphabetInput"))

    @builtins.property
    @jsii.member(jsii_name="radixInput")
    def radix_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "radixInput"))

    @builtins.property
    @jsii.member(jsii_name="surrogateInfoTypeInput")
    def surrogate_info_type_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType"], jsii.get(self, "surrogateInfoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="commonAlphabet")
    def common_alphabet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonAlphabet"))

    @common_alphabet.setter
    def common_alphabet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56420ec3910749446b64563890d532c8cb0209a1cbe1c82249f6332f1d99024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonAlphabet", value)

    @builtins.property
    @jsii.member(jsii_name="customAlphabet")
    def custom_alphabet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customAlphabet"))

    @custom_alphabet.setter
    def custom_alphabet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17f3909f38a0f09c0ab5c73bb769610a0d4d91dc3766e4b7c8cf44c9d042b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAlphabet", value)

    @builtins.property
    @jsii.member(jsii_name="radix")
    def radix(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "radix"))

    @radix.setter
    def radix(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee5cc5632f33bc44493e26e15240dbea70052cc14584ff51e4361deda74ebbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "radix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20be6a520cebc32c7062d70a4b9c62b5778d15f19cefaaeaca8a56257058483a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at `https://cloud.google.com/dlp/docs/infotypes-reference <https://cloud.google.com/dlp/docs/infotypes-reference>`_ when specifying a built-in type. When sending Cloud DLP results to Data Catalog, infoType names should conform to the pattern '[A-Za-z0-9$-_]{1,64}'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bce2169aba9f2d940664a32bf3087d1b85d00da3e814a609eab5afab0a3890b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed at `https://cloud.google.com/dlp/docs/infotypes-reference <https://cloud.google.com/dlp/docs/infotypes-reference>`_ when specifying a built-in type. When sending Cloud DLP results to Data Catalog, infoType names should conform to the pattern '[A-Za-z0-9$-_]{1,64}'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#name DataLossPreventionDeidentifyTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a01593cab2fa26accf4901b302a36b3bc21c0de216d42d0c33e3a58b83f3ab48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e1fbcceb18467eab93c2ecc19df5a6f3fae43111e9dd11dad07cd4ec2667dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225b1c98f34074312b10c7173319c06264fce509c6147fb94fa8ed4ba31265be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df6451d90642f096b8b505a936151b179d42a04e51d0eb3db387dc147f3a524f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCharacterMaskConfig")
    def put_character_mask_config(
        self,
        *,
        characters_to_ignore: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, typing.Dict[builtins.str, typing.Any]]]]] = None,
        masking_character: typing.Optional[builtins.str] = None,
        number_to_mask: typing.Optional[jsii.Number] = None,
        reverse_order: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param characters_to_ignore: characters_to_ignore block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#characters_to_ignore DataLossPreventionDeidentifyTemplate#characters_to_ignore}
        :param masking_character: Character to use to mask the sensitive values—for example, * for an alphabetic string such as a name, or 0 for a numeric string such as ZIP code or credit card number. This string must have a length of 1. If not supplied, this value defaults to * for strings, and 0 for digits. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#masking_character DataLossPreventionDeidentifyTemplate#masking_character}
        :param number_to_mask: Number of characters to mask. If not set, all matching chars will be masked. Skipped characters do not count towards this tally. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#number_to_mask DataLossPreventionDeidentifyTemplate#number_to_mask}
        :param reverse_order: Mask characters in reverse order. For example, if masking_character is 0, number_to_mask is 14, and reverse_order is 'false', then the input string '1234-5678-9012-3456' is masked as '00000000000000-3456'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#reverse_order DataLossPreventionDeidentifyTemplate#reverse_order}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig(
            characters_to_ignore=characters_to_ignore,
            masking_character=masking_character,
            number_to_mask=number_to_mask,
            reverse_order=reverse_order,
        )

        return typing.cast(None, jsii.invoke(self, "putCharacterMaskConfig", [value]))

    @jsii.member(jsii_name="putCryptoDeterministicConfig")
    def put_crypto_deterministic_config(
        self,
        *,
        context: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext, typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey, typing.Dict[builtins.str, typing.Any]]] = None,
        surrogate_info_type: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param context: context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#context DataLossPreventionDeidentifyTemplate#context}
        :param crypto_key: crypto_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key DataLossPreventionDeidentifyTemplate#crypto_key}
        :param surrogate_info_type: surrogate_info_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#surrogate_info_type DataLossPreventionDeidentifyTemplate#surrogate_info_type}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig(
            context=context,
            crypto_key=crypto_key,
            surrogate_info_type=surrogate_info_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCryptoDeterministicConfig", [value]))

    @jsii.member(jsii_name="putCryptoReplaceFfxFpeConfig")
    def put_crypto_replace_ffx_fpe_config(
        self,
        *,
        common_alphabet: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext, typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_alphabet: typing.Optional[builtins.str] = None,
        radix: typing.Optional[jsii.Number] = None,
        surrogate_info_type: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param common_alphabet: Common alphabets. Possible values: ["FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED", "NUMERIC", "HEXADECIMAL", "UPPER_CASE_ALPHA_NUMERIC", "ALPHA_NUMERIC"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#common_alphabet DataLossPreventionDeidentifyTemplate#common_alphabet}
        :param context: context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#context DataLossPreventionDeidentifyTemplate#context}
        :param crypto_key: crypto_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#crypto_key DataLossPreventionDeidentifyTemplate#crypto_key}
        :param custom_alphabet: This is supported by mapping these to the alphanumeric characters that the FFX mode natively supports. This happens before/after encryption/decryption. Each character listed must appear only once. Number of characters must be in the range [2, 95]. This must be encoded as ASCII. The order of characters does not matter. The full list of allowed characters is: ''0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ~'!@#$%^&*()_-+={[}]|:;"'<,>.?/'' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#custom_alphabet DataLossPreventionDeidentifyTemplate#custom_alphabet}
        :param radix: The native way to select the alphabet. Must be in the range [2, 95]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#radix DataLossPreventionDeidentifyTemplate#radix}
        :param surrogate_info_type: surrogate_info_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#surrogate_info_type DataLossPreventionDeidentifyTemplate#surrogate_info_type}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig(
            common_alphabet=common_alphabet,
            context=context,
            crypto_key=crypto_key,
            custom_alphabet=custom_alphabet,
            radix=radix,
            surrogate_info_type=surrogate_info_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCryptoReplaceFfxFpeConfig", [value]))

    @jsii.member(jsii_name="putReplaceConfig")
    def put_replace_config(
        self,
        *,
        new_value: typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param new_value: new_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#new_value DataLossPreventionDeidentifyTemplate#new_value}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig(
            new_value=new_value
        )

        return typing.cast(None, jsii.invoke(self, "putReplaceConfig", [value]))

    @jsii.member(jsii_name="resetCharacterMaskConfig")
    def reset_character_mask_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCharacterMaskConfig", []))

    @jsii.member(jsii_name="resetCryptoDeterministicConfig")
    def reset_crypto_deterministic_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoDeterministicConfig", []))

    @jsii.member(jsii_name="resetCryptoReplaceFfxFpeConfig")
    def reset_crypto_replace_ffx_fpe_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoReplaceFfxFpeConfig", []))

    @jsii.member(jsii_name="resetReplaceConfig")
    def reset_replace_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplaceConfig", []))

    @jsii.member(jsii_name="resetReplaceWithInfoTypeConfig")
    def reset_replace_with_info_type_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplaceWithInfoTypeConfig", []))

    @builtins.property
    @jsii.member(jsii_name="characterMaskConfig")
    def character_mask_config(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigOutputReference, jsii.get(self, "characterMaskConfig"))

    @builtins.property
    @jsii.member(jsii_name="cryptoDeterministicConfig")
    def crypto_deterministic_config(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigOutputReference, jsii.get(self, "cryptoDeterministicConfig"))

    @builtins.property
    @jsii.member(jsii_name="cryptoReplaceFfxFpeConfig")
    def crypto_replace_ffx_fpe_config(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigOutputReference, jsii.get(self, "cryptoReplaceFfxFpeConfig"))

    @builtins.property
    @jsii.member(jsii_name="replaceConfig")
    def replace_config(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigOutputReference", jsii.get(self, "replaceConfig"))

    @builtins.property
    @jsii.member(jsii_name="characterMaskConfigInput")
    def character_mask_config_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig], jsii.get(self, "characterMaskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoDeterministicConfigInput")
    def crypto_deterministic_config_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig], jsii.get(self, "cryptoDeterministicConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoReplaceFfxFpeConfigInput")
    def crypto_replace_ffx_fpe_config_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig], jsii.get(self, "cryptoReplaceFfxFpeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceConfigInput")
    def replace_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig"], jsii.get(self, "replaceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceWithInfoTypeConfigInput")
    def replace_with_info_type_config_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceWithInfoTypeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceWithInfoTypeConfig")
    def replace_with_info_type_config(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replaceWithInfoTypeConfig"))

    @replace_with_info_type_config.setter
    def replace_with_info_type_config(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d929d83c8fe52abde3c68226b1ad4a254e12869d1b6ebfe65915513910cfdf67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceWithInfoTypeConfig", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5577a1862fcc26e15478148378f338bde264048f6cd4c65e4dbe76ddd98cdfdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig",
    jsii_struct_bases=[],
    name_mapping={"new_value": "newValue"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig:
    def __init__(
        self,
        *,
        new_value: typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param new_value: new_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#new_value DataLossPreventionDeidentifyTemplate#new_value}
        '''
        if isinstance(new_value, dict):
            new_value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue(**new_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257f1f092aa76c4bea296d5f9ab60bf0d70f24d131810ad25c7dd1ceb6dad467)
            check_type(argname="argument new_value", value=new_value, expected_type=type_hints["new_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "new_value": new_value,
        }

    @builtins.property
    def new_value(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue":
        '''new_value block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#new_value DataLossPreventionDeidentifyTemplate#new_value}
        '''
        result = self._values.get("new_value")
        assert result is not None, "Required property 'new_value' is missing"
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue",
    jsii_struct_bases=[],
    name_mapping={
        "boolean_value": "booleanValue",
        "date_value": "dateValue",
        "day_of_week_value": "dayOfWeekValue",
        "float_value": "floatValue",
        "integer_value": "integerValue",
        "string_value": "stringValue",
        "timestamp_value": "timestampValue",
        "time_value": "timeValue",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue:
    def __init__(
        self,
        *,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        date_value: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue", typing.Dict[builtins.str, typing.Any]]] = None,
        day_of_week_value: typing.Optional[builtins.str] = None,
        float_value: typing.Optional[jsii.Number] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        string_value: typing.Optional[builtins.str] = None,
        timestamp_value: typing.Optional[builtins.str] = None,
        time_value: typing.Optional[typing.Union["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param boolean_value: A boolean value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#boolean_value DataLossPreventionDeidentifyTemplate#boolean_value}
        :param date_value: date_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#date_value DataLossPreventionDeidentifyTemplate#date_value}
        :param day_of_week_value: Represents a day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#day_of_week_value DataLossPreventionDeidentifyTemplate#day_of_week_value}
        :param float_value: A float value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#float_value DataLossPreventionDeidentifyTemplate#float_value}
        :param integer_value: An integer value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#integer_value DataLossPreventionDeidentifyTemplate#integer_value}
        :param string_value: A string value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#string_value DataLossPreventionDeidentifyTemplate#string_value}
        :param timestamp_value: A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#timestamp_value DataLossPreventionDeidentifyTemplate#timestamp_value}
        :param time_value: time_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#time_value DataLossPreventionDeidentifyTemplate#time_value}
        '''
        if isinstance(date_value, dict):
            date_value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue(**date_value)
        if isinstance(time_value, dict):
            time_value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue(**time_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e9e2f701c0cd0a3184cad2a214257f9c5dd6f791c80e98d6b2c6b42c9c578a)
            check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument day_of_week_value", value=day_of_week_value, expected_type=type_hints["day_of_week_value"])
            check_type(argname="argument float_value", value=float_value, expected_type=type_hints["float_value"])
            check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            check_type(argname="argument timestamp_value", value=timestamp_value, expected_type=type_hints["timestamp_value"])
            check_type(argname="argument time_value", value=time_value, expected_type=type_hints["time_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boolean_value is not None:
            self._values["boolean_value"] = boolean_value
        if date_value is not None:
            self._values["date_value"] = date_value
        if day_of_week_value is not None:
            self._values["day_of_week_value"] = day_of_week_value
        if float_value is not None:
            self._values["float_value"] = float_value
        if integer_value is not None:
            self._values["integer_value"] = integer_value
        if string_value is not None:
            self._values["string_value"] = string_value
        if timestamp_value is not None:
            self._values["timestamp_value"] = timestamp_value
        if time_value is not None:
            self._values["time_value"] = time_value

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#boolean_value DataLossPreventionDeidentifyTemplate#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def date_value(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue"]:
        '''date_value block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#date_value DataLossPreventionDeidentifyTemplate#date_value}
        '''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue"], result)

    @builtins.property
    def day_of_week_value(self) -> typing.Optional[builtins.str]:
        '''Represents a day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#day_of_week_value DataLossPreventionDeidentifyTemplate#day_of_week_value}
        '''
        result = self._values.get("day_of_week_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def float_value(self) -> typing.Optional[jsii.Number]:
        '''A float value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#float_value DataLossPreventionDeidentifyTemplate#float_value}
        '''
        result = self._values.get("float_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''An integer value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#integer_value DataLossPreventionDeidentifyTemplate#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''A string value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#string_value DataLossPreventionDeidentifyTemplate#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_value(self) -> typing.Optional[builtins.str]:
        '''A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#timestamp_value DataLossPreventionDeidentifyTemplate#timestamp_value}
        '''
        result = self._values.get("timestamp_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_value(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue"]:
        '''time_value block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#time_value DataLossPreventionDeidentifyTemplate#time_value}
        '''
        result = self._values.get("time_value")
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month, or 0 if specifying a year by itself or a year and month where the day is not significant. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#day DataLossPreventionDeidentifyTemplate#day}
        :param month: Month of year. Must be from 1 to 12, or 0 if specifying a year without a month and day. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#month DataLossPreventionDeidentifyTemplate#month}
        :param year: Year of date. Must be from 1 to 9999, or 0 if specifying a date without a year. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#year DataLossPreventionDeidentifyTemplate#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c0c1dfc6340aecb89308bad96b0dacbeb768f7ca50b84760b7a3e878a62d95)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of month.

        Must be from 1 to 31 and valid for the year and month, or 0 if specifying a
        year by itself or a year and month where the day is not significant.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#day DataLossPreventionDeidentifyTemplate#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of year.

        Must be from 1 to 12, or 0 if specifying a year without a month and day.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#month DataLossPreventionDeidentifyTemplate#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of date. Must be from 1 to 9999, or 0 if specifying a date without a year.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#year DataLossPreventionDeidentifyTemplate#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76a3329dc4bee858a9a331eb322fca6897c4712c45d357113aff94f456c9c417)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e0b2577ed9638894bdec0e1795907e279b1f420eb3029f1fdeddd28e9423d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value)

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd51e3d2fb91c35c3262208a24ab0645aa8430448d71e049061ad6f5fb42848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value)

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31f6d5032d2c90f8f7c9f0b1af5057434dbd262b8b063ddf779c319182c10ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3bfea7ddbb33839e4ab5456b13c78948b7238829ecbed4d26a590b36065055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__decf46d91548a8fe55272c94a2535ce59fa31bc05f3f72a99dc95744140cab35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDateValue")
    def put_date_value(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of month. Must be from 1 to 31 and valid for the year and month, or 0 if specifying a year by itself or a year and month where the day is not significant. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#day DataLossPreventionDeidentifyTemplate#day}
        :param month: Month of year. Must be from 1 to 12, or 0 if specifying a year without a month and day. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#month DataLossPreventionDeidentifyTemplate#month}
        :param year: Year of date. Must be from 1 to 9999, or 0 if specifying a date without a year. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#year DataLossPreventionDeidentifyTemplate#year}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putDateValue", [value]))

    @jsii.member(jsii_name="putTimeValue")
    def put_time_value(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#hours DataLossPreventionDeidentifyTemplate#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#minutes DataLossPreventionDeidentifyTemplate#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#nanos DataLossPreventionDeidentifyTemplate#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#seconds DataLossPreventionDeidentifyTemplate#seconds}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putTimeValue", [value]))

    @jsii.member(jsii_name="resetBooleanValue")
    def reset_boolean_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBooleanValue", []))

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetDayOfWeekValue")
    def reset_day_of_week_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOfWeekValue", []))

    @jsii.member(jsii_name="resetFloatValue")
    def reset_float_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloatValue", []))

    @jsii.member(jsii_name="resetIntegerValue")
    def reset_integer_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @jsii.member(jsii_name="resetTimestampValue")
    def reset_timestamp_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampValue", []))

    @jsii.member(jsii_name="resetTimeValue")
    def reset_time_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValueOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValueOutputReference, jsii.get(self, "dateValue"))

    @builtins.property
    @jsii.member(jsii_name="timeValue")
    def time_value(
        self,
    ) -> "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValueOutputReference":
        return typing.cast("DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValueOutputReference", jsii.get(self, "timeValue"))

    @builtins.property
    @jsii.member(jsii_name="booleanValueInput")
    def boolean_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "booleanValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekValueInput")
    def day_of_week_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekValueInput"))

    @builtins.property
    @jsii.member(jsii_name="floatValueInput")
    def float_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "floatValueInput"))

    @builtins.property
    @jsii.member(jsii_name="integerValueInput")
    def integer_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "integerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampValueInput")
    def timestamp_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampValueInput"))

    @builtins.property
    @jsii.member(jsii_name="timeValueInput")
    def time_value_input(
        self,
    ) -> typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue"]:
        return typing.cast(typing.Optional["DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue"], jsii.get(self, "timeValueInput"))

    @builtins.property
    @jsii.member(jsii_name="booleanValue")
    def boolean_value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "booleanValue"))

    @boolean_value.setter
    def boolean_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e24dfcf9f7cc9d8972fbc8c1ae73630693615abbaa3c45976e9dfa3c0859064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value)

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekValue")
    def day_of_week_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeekValue"))

    @day_of_week_value.setter
    def day_of_week_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4928a7b6c063d0d49e3e77c25a76457594ce70418cb1c89c09204d83285706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeekValue", value)

    @builtins.property
    @jsii.member(jsii_name="floatValue")
    def float_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "floatValue"))

    @float_value.setter
    def float_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3e273ec51b4e85051327fd12cfb7b4ec5deb9f35b85a283de7af9313dad3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatValue", value)

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5c6bb7ef25c092871f4c0ac78bfca3b87dbac39937a7408e14b1fc46cfd2be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value)

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d75e412eef8bfa1314b057935839218bf4df5d4e1e795835e16ba6e7c629e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value)

    @builtins.property
    @jsii.member(jsii_name="timestampValue")
    def timestamp_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampValue"))

    @timestamp_value.setter
    def timestamp_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc82aac74621886da9e1c4bb210cc05d2d54ae968e412d1b99b80b8cf95b51cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d3f3d8f9c1ebefae1bef3a4fc93f04638955973c028be938def7652a0fdcb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#hours DataLossPreventionDeidentifyTemplate#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#minutes DataLossPreventionDeidentifyTemplate#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#nanos DataLossPreventionDeidentifyTemplate#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#seconds DataLossPreventionDeidentifyTemplate#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4e3dc05ff013842cb7d80e0d0ca882b92ec4b9b98b7e8c0b9b3338dc7d4034)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#hours DataLossPreventionDeidentifyTemplate#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#minutes DataLossPreventionDeidentifyTemplate#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#nanos DataLossPreventionDeidentifyTemplate#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Must normally be from 0 to 59.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#seconds DataLossPreventionDeidentifyTemplate#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae021c2726f901fab5ab36488e2d9a7b2ab6538c119afb5752eb7c3e9633f03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d908574f0c4c27fe0e2d790ce476963add846ccefaf50d4280476c79040837a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value)

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbe97aee38344e19ac2fcaa5dc8a621e7e605a7c1910f230cde04c9c3ab6335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value)

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d56c1895f34ba410bb9ba4bb25bd92b8a5c05a97b457f7ba8274cf02b85c496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value)

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c37fed03f6c43dc85fe6858bda5276e3d73de44e2de376534e910d6d66ed2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6133c058c812c33bc84ad07f5f94878f0cb6668a4b4b06ea9ff87fe53496b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f439bfe94bfda3779a0a1105ce59e3575b2d04675b491475b06c1943ce04dab9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNewValue")
    def put_new_value(
        self,
        *,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        date_value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue, typing.Dict[builtins.str, typing.Any]]] = None,
        day_of_week_value: typing.Optional[builtins.str] = None,
        float_value: typing.Optional[jsii.Number] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        string_value: typing.Optional[builtins.str] = None,
        timestamp_value: typing.Optional[builtins.str] = None,
        time_value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param boolean_value: A boolean value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#boolean_value DataLossPreventionDeidentifyTemplate#boolean_value}
        :param date_value: date_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#date_value DataLossPreventionDeidentifyTemplate#date_value}
        :param day_of_week_value: Represents a day of the week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#day_of_week_value DataLossPreventionDeidentifyTemplate#day_of_week_value}
        :param float_value: A float value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#float_value DataLossPreventionDeidentifyTemplate#float_value}
        :param integer_value: An integer value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#integer_value DataLossPreventionDeidentifyTemplate#integer_value}
        :param string_value: A string value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#string_value DataLossPreventionDeidentifyTemplate#string_value}
        :param timestamp_value: A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#timestamp_value DataLossPreventionDeidentifyTemplate#timestamp_value}
        :param time_value: time_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#time_value DataLossPreventionDeidentifyTemplate#time_value}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue(
            boolean_value=boolean_value,
            date_value=date_value,
            day_of_week_value=day_of_week_value,
            float_value=float_value,
            integer_value=integer_value,
            string_value=string_value,
            timestamp_value=timestamp_value,
            time_value=time_value,
        )

        return typing.cast(None, jsii.invoke(self, "putNewValue", [value]))

    @builtins.property
    @jsii.member(jsii_name="newValue")
    def new_value(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueOutputReference, jsii.get(self, "newValue"))

    @builtins.property
    @jsii.member(jsii_name="newValueInput")
    def new_value_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue], jsii.get(self, "newValueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980ffcb2dc9db7651a9a6db142c8eb40d00f92b9ca320bf0585beff01feff8d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDeidentifyTemplateDeidentifyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateDeidentifyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f86322367c9ed1c4dcf43efc992630a669b1317d0d433e14895d5ee0977f896)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfoTypeTransformations")
    def put_info_type_transformations(
        self,
        *,
        transformations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param transformations: transformations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#transformations DataLossPreventionDeidentifyTemplate#transformations}
        '''
        value = DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations(
            transformations=transformations
        )

        return typing.cast(None, jsii.invoke(self, "putInfoTypeTransformations", [value]))

    @builtins.property
    @jsii.member(jsii_name="infoTypeTransformations")
    def info_type_transformations(
        self,
    ) -> DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsOutputReference:
        return typing.cast(DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsOutputReference, jsii.get(self, "infoTypeTransformations"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeTransformationsInput")
    def info_type_transformations_input(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations], jsii.get(self, "infoTypeTransformationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53cc4a7ad7d91c08b2ee964ca70e598346041946bf69684127578fc6f720da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataLossPreventionDeidentifyTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#create DataLossPreventionDeidentifyTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#delete DataLossPreventionDeidentifyTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#update DataLossPreventionDeidentifyTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408149af513352549b48f8bc277a15ede8ed1fd2a2f60649c321170030cfc3c2)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#create DataLossPreventionDeidentifyTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#delete DataLossPreventionDeidentifyTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/data_loss_prevention_deidentify_template#update DataLossPreventionDeidentifyTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDeidentifyTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDeidentifyTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDeidentifyTemplate.DataLossPreventionDeidentifyTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c37f761b3a358ff36d72d8e75bb433a6840ba0dd030f64df8180007847574c1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6316612dda0d8f74a197b263e8f934e0c07a4af483939e3dbb2c0902f270656c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeacd9bd4e147776b8a94a918f71bc89024704651be09c6411dad163e3c5baa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f58f67769eeac865bc1e3ce827ea93c2fb3df59f8fb60d88317996c61daaff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b76a3c2e131cae27999bc0f893e7b43334a4d7117714ad7aa1316ce8fc81d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataLossPreventionDeidentifyTemplate",
    "DataLossPreventionDeidentifyTemplateConfig",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfig",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesList",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypesOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsList",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreList",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnoreOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContextOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrappedOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransientOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrappedOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoTypeOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContextOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrappedOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransientOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrappedOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoTypeOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValueOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValueOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigOutputReference",
    "DataLossPreventionDeidentifyTemplateDeidentifyConfigOutputReference",
    "DataLossPreventionDeidentifyTemplateTimeouts",
    "DataLossPreventionDeidentifyTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dd6f5efc1c8e63859b44a0bd6ee94588c0f54772881c8a60cdd39275c0ddb874(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    deidentify_config: typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfig, typing.Dict[builtins.str, typing.Any]],
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fe3f7588f289d32348bf1a48da84c4495558851f53178efd4764b5b8e968a440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d181c6397e3e96372f61766f54eb9f00455a0d1c871829be60a057a09ad859fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10142721e91be8e4c6ac1d10847ad8b3278ed9f961b609aa273f9238bffca8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1584dc113a40112ba6fca702783a3adfecb8a0441703b56eaf3802f73e5b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d4228ecebba24a8247a0b74680daaf904fa71db8719430538d2953e99deae7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deidentify_config: typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfig, typing.Dict[builtins.str, typing.Any]],
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ef9751a86cc88eb79013d4f41d8ef0769beb28b247712f464328afd7270475(
    *,
    info_type_transformations: typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7c48b9dfc14971580b6d65c192696626024a96cde15077a3f0d67f67cfc177(
    *,
    transformations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96f15eb324ba2084e9a8219199f8e21c282e326aefbe7b740b3751f7ce78adc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e83f2bb468a00421cd6a743067cdc1eec4d72f803d705bd0a2f56f2a4a55593(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4730be65480bbf6d13efd477e5c944e1493fcba98c43dfbf27ec7c27620e0ca(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e102ce66c08283bc89e09ac7a5ebc171bac8b65ea1d868ec122ff7d721c362c(
    *,
    primitive_transformation: typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation, typing.Dict[builtins.str, typing.Any]],
    info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93761c4b821d2dc605054e7dc72c33b56794d38b7d4f913c694d603bb76284db(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867b518b9b15676fa465431a18d5990725ce446aeb8b5a858af63e44dab1c824(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75895254c10848f3f46ad9164982f01c84a1f25ee04e1732225444445a5e2c8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3853a02b316ecd427796ce4a67856e5179059a986bfae5c7abf7e082e3361b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbb43efa134befc981696b3fce38e5a28e908d7ea268d7887e427b54b4af016(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762b2bc6a4dd1a1ed73cb3981db96969a48b31cdebab3406bc42e5bd765da767(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06f317a0c9bd7804e48e5a1a1b651e40de92bb3e0b115d7dc3c10f2b9ebad4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f81b46481b5521e5602de0ada5d37ff259026d9ed680f7a82a89863cfa9c82a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0aa2668b313774913898c6538c90637c6c6dd679405a438d641bbf75edb14e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20e817ed370ba02f5c80f6746147a1ca5e68b4a71ee552b564b116ec28e456b(
    value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b39c32cd937ed47106ff1b15ae971bb30f8edd2db0dc1fdd8a7a3ec26fd3fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe5bfa532a42a7c8d341325068083e23de4143bcd07c140498814b39365c20e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9aa49a4f19c16223840843216d64c8b91a47531696137b5b0180f4a242e3104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac8e16c431dd7cf625266de0fcf94abaa895714f05da65d6ca1575efbe29440(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4de7e4f94798400d14523dacce9edc2d5c761e98e8549d37ac0b2fbf05e0ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced639a6c4ffe0acecaa21bd8cf806f078c0809373b24bba98545c7e37717be5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ace4632c0882853891f35c5809d631d1c9d3368ae493b95566f45be306b51e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2ea878d4ffdcc23c7b22e9b0bd5a2537cf19982ab08f96b31e9af9435722ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e53dc79dc759151fa9b44444393f3454168c79f9b0bdecaa3bb98a06bcca79(
    value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformations, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281548a2f50fe011498c4537c38a173cbc57de372bcc3831a8e1c0393c4a9ebc(
    *,
    character_mask_config: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_deterministic_config: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_replace_ffx_fpe_config: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    replace_config: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    replace_with_info_type_config: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdeb383b4e0077f6f8fa0e14c433f38a7f76c7ece9603ee789fab5a3bf5c061(
    *,
    characters_to_ignore: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, typing.Dict[builtins.str, typing.Any]]]]] = None,
    masking_character: typing.Optional[builtins.str] = None,
    number_to_mask: typing.Optional[jsii.Number] = None,
    reverse_order: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0292d579db2e96f1bdf05bfbbbff0ef095c96bf16893b225161d60c439bc3718(
    *,
    characters_to_skip: typing.Optional[builtins.str] = None,
    common_characters_to_ignore: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be4685f03d74eefcd779bf88c75e19a55b442c3e719961b1f450279a8592c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9d94343ab4beffc8afba37cb3f4d51d118a1db48a03371edd4bce18bc4b186(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624839077779b46788088f91e65200c9bf41cec2f7a78a37e4ec2e0b89d78c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056f82a7b96bdfdbbfb6c23a4ae4079095506d0660ab076358bc34d5ecc14d8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c64cbf19b20de7919f4e77e1bb659f7fcb1277f2a64edf5d130481122c6e471(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f75b6cfb3ab5b0514d43503f1157908c40b551c61cbb0453ada2be7e0ceea4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8162c6c6b00a5cf908f4f130d7bc2a4d9da0bb4efd0b520d2cda59ae0b916b19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1040588465595c9e731db1b59079f2353fb83c55eefae7367ab5ac27253b69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccee178229f55235d71ceb4c1b52a06e42a6db52f81d077aa8fe48c4a39206fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769a3702303027c718c2a440ab277c4cbffb8a0bc962f92480fc15f611b6ceff(
    value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024898f2491a09a359075061b823aab893c57b0b00f08262437ac3c7c1bc93f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf30c013b87984003655c04a0c5f41ed4256e52ce24a36c90743662e15323892(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfigCharactersToIgnore, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6de070ea09866c5dc91a830f6ac1da778bbec407c60de674a9b09122c5aa8e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0546bb90b3f6d36265b3ab891ade41dfa98458bf739b60ba3837d2d7f0fa39(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39160968b461fd895e9b942566fa19e3a8b1bb254b0063c79837a8e04a77cf2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c2f5ed83103ffdcf5c3e0798733279bd32a2109c8f8cb5db8d962f0f7fe527(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCharacterMaskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63d352d56f6cbe205137d68f27171bf696a24010d9d6bb64d3e3c94cfa3aae6(
    *,
    context: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_key: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey, typing.Dict[builtins.str, typing.Any]]] = None,
    surrogate_info_type: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1a6388a65c51ec019cee0fad6c748505f0a513454a8a3451759a892ad7df2a(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baac8b19e2205d3f87e1d66d785a465d16da877f08eec50f6bc18ccb8a009e81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acab88b171199b1ff30a70d9b05b51cf06d718531f024ea874cc85dad2d6319c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3fd204c0c438713926fc16f0c46acbe8b1e7a6733d1aea1fffb8e9f73a578c(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ba4275a261991d76ebb2fe979631f5e7ea3867427a9d54f5cf1b7ecb5ce133(
    *,
    kms_wrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped, typing.Dict[builtins.str, typing.Any]]] = None,
    transient: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient, typing.Dict[builtins.str, typing.Any]]] = None,
    unwrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b092be71d960e672d1c67242c5ae810c6d74abf404f853c5dc1ae42e5a4434(
    *,
    crypto_key_name: builtins.str,
    wrapped_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4e25df129e1f494f6d53966a989b4a1e55758277b96ae08e691f708e6879bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b934811443f9691d2e4ad79b80b98d687e550bf5a41efa710946cdaacc5ecbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d15698eda798f5c8f29ac8033f9591b194d2deeedac28123d269f59be6ea471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89039ccdc980f8803590d1e2985acc6dcc01311c6d277e52da5729153491fc6(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyKmsWrapped],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0748f018dc781012f427a91c70054a5953eb0acf4cb4404f545eaf28bd9b8e47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2caca3a8dae16a5d7e1abbf3b277e994b3ea02f7872ff1a34fef72290e71a7f(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53d356028df3c640df6ad4c87fc4f872b5ec0e5ec1a29f211c295c9deb908c8(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a196e719a93e603e49aa9fbbce0d67a0ccf8328f69f2be9ee486c113e421781(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac50542264d6e2d1bfd7c8fa755b93c32f73370d74379819f7bfaacff8708dcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a120541c4902312a5ef21adf9b7c6210b62c870b9ba7eae430bf361799bc03(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyTransient],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7801658292b82a119d5d9ce88c3468805233deb2ad25ebbe48bd3d372a3a1f(
    *,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af066a49c9053f3089c0d95f714eb2d7d6917ef6cc442dad13079b6dcdd0074f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70111a32c953a829e8fbf3da6424a6842c2987126e563975a756d7b9c8054a0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a909f17cfa377873c4e5d1802735320ef9654f4c2bded0f3873549acf7d38dbf(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigCryptoKeyUnwrapped],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13bd32963d7126724dac8b730ab931b8e048c0166449393f2a30d7dfd7fe6bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75e971486d005a54edc43cd5fd3b5a6b6689e4d19dd819d8b2333d94f8122a8(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c6c72d843e79dae13d92773ad1234e20ed149400fffafd97df76cd5eb5392a(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bb39f7bf5f7bd51983722480f54209ae90aa2d25ff98879936bb54bf9d1250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35706f3a8ca835ffd24c991527ac20e4c61172938877b141b9b536a6bdcae22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfaf8e9019230f69f7956ff471097f5b9de47cc244c4720358150a542de625b4(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoDeterministicConfigSurrogateInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d5fef9cb45ff890eec16e6587a1fd11b1c60bbb0120b9488f96f54355eddf7(
    *,
    common_alphabet: typing.Optional[builtins.str] = None,
    context: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_key: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_alphabet: typing.Optional[builtins.str] = None,
    radix: typing.Optional[jsii.Number] = None,
    surrogate_info_type: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341432daf25ab00ff81695bd7c01407e7422497d6698538cbe6b951815c79989(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48632123032fcd33c94b17559fba37fc54a4c87aedfd1d86d395cadc33e860cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0d0312a25dda77f305c912112b074521ce584f6590590b392f52c6b37ab983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9f8ab0af0156d7a931b07857714ec596f27501661440b8caa535c185c9d1b0(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c833f8be98ffc0fa9b9f6a6e5613014836172cbc9e61a7823168d8d2ab7b872(
    *,
    kms_wrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped, typing.Dict[builtins.str, typing.Any]]] = None,
    transient: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient, typing.Dict[builtins.str, typing.Any]]] = None,
    unwrapped: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b6f3dd10cb36e21651554e0e92bd80d80d2cc3d7837f74ad63d122c2bc6d38(
    *,
    crypto_key_name: builtins.str,
    wrapped_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ef4e6db699ef0fe723cc2c82f2a41429dd6e35d6011c84e62caa8f4101acba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d336a9b71db1ef454c8f57681d1f59ea9991e211de764b4b71c8afb678cc75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d06c03369fe29e99f8f03cb4850bf0392d75d9224f9d5fa1cff7976dd84edcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6aa3bb67cee71087cff4002fcf2444df4aae73d3870af90afd3fa3ac3273a3c(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyKmsWrapped],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1be5a7c089a8580b8ce6faa1d013d2c10675a2cde7ed5e0408fe5b36bf5c1c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186eab9ee75aff9d2476915f4e8b4e784a4e987361856263f12634d8948f7717(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eaeb162026d06d9879ddaa261e17da2713643d05324571d6cc58c0b7e0f171a(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06c584cf7cf9fa80db3c3229edff93d29fd591e1d2f18fbee2d65227267bc81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e839dab15283de0e9df6800160e9d04c3814ed6abb434f069278b7cf1949f30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175f85c2ca75239fbe6bf2730ee10614538c582a1ca02b273622e7178aa34e43(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyTransient],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113c434f328952324aa3fa00e291c16242ba95a9fbed9f01c091e948be9cfd8f(
    *,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce33ff090f147ae866ec032809531b7280c62099be3c45624b60c1668bc932df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0e020a2d1398a262c5473d64e5320738c2ecfb589cfb132d35c1eab8d82d7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531cbb938c6e4180c62765e1c987eedd2e3437ed6422e2e98f68f8c5cd7fbf92(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigCryptoKeyUnwrapped],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba34bfec41e8574ec9aac95062dce75844f384bdb8b6f94b53c1add2878ecb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56420ec3910749446b64563890d532c8cb0209a1cbe1c82249f6332f1d99024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17f3909f38a0f09c0ab5c73bb769610a0d4d91dc3766e4b7c8cf44c9d042b1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee5cc5632f33bc44493e26e15240dbea70052cc14584ff51e4361deda74ebbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20be6a520cebc32c7062d70a4b9c62b5778d15f19cefaaeaca8a56257058483a(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bce2169aba9f2d940664a32bf3087d1b85d00da3e814a609eab5afab0a3890b(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01593cab2fa26accf4901b302a36b3bc21c0de216d42d0c33e3a58b83f3ab48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e1fbcceb18467eab93c2ecc19df5a6f3fae43111e9dd11dad07cd4ec2667dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225b1c98f34074312b10c7173319c06264fce509c6147fb94fa8ed4ba31265be(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationCryptoReplaceFfxFpeConfigSurrogateInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6451d90642f096b8b505a936151b179d42a04e51d0eb3db387dc147f3a524f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d929d83c8fe52abde3c68226b1ad4a254e12869d1b6ebfe65915513910cfdf67(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5577a1862fcc26e15478148378f338bde264048f6cd4c65e4dbe76ddd98cdfdc(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257f1f092aa76c4bea296d5f9ab60bf0d70f24d131810ad25c7dd1ceb6dad467(
    *,
    new_value: typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e9e2f701c0cd0a3184cad2a214257f9c5dd6f791c80e98d6b2c6b42c9c578a(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    date_value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue, typing.Dict[builtins.str, typing.Any]]] = None,
    day_of_week_value: typing.Optional[builtins.str] = None,
    float_value: typing.Optional[jsii.Number] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    string_value: typing.Optional[builtins.str] = None,
    timestamp_value: typing.Optional[builtins.str] = None,
    time_value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c0c1dfc6340aecb89308bad96b0dacbeb768f7ca50b84760b7a3e878a62d95(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a3329dc4bee858a9a331eb322fca6897c4712c45d357113aff94f456c9c417(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e0b2577ed9638894bdec0e1795907e279b1f420eb3029f1fdeddd28e9423d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd51e3d2fb91c35c3262208a24ab0645aa8430448d71e049061ad6f5fb42848(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31f6d5032d2c90f8f7c9f0b1af5057434dbd262b8b063ddf779c319182c10ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3bfea7ddbb33839e4ab5456b13c78948b7238829ecbed4d26a590b36065055(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueDateValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decf46d91548a8fe55272c94a2535ce59fa31bc05f3f72a99dc95744140cab35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e24dfcf9f7cc9d8972fbc8c1ae73630693615abbaa3c45976e9dfa3c0859064(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4928a7b6c063d0d49e3e77c25a76457594ce70418cb1c89c09204d83285706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3e273ec51b4e85051327fd12cfb7b4ec5deb9f35b85a283de7af9313dad3e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5c6bb7ef25c092871f4c0ac78bfca3b87dbac39937a7408e14b1fc46cfd2be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d75e412eef8bfa1314b057935839218bf4df5d4e1e795835e16ba6e7c629e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc82aac74621886da9e1c4bb210cc05d2d54ae968e412d1b99b80b8cf95b51cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d3f3d8f9c1ebefae1bef3a4fc93f04638955973c028be938def7652a0fdcb8(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4e3dc05ff013842cb7d80e0d0ca882b92ec4b9b98b7e8c0b9b3338dc7d4034(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae021c2726f901fab5ab36488e2d9a7b2ab6538c119afb5752eb7c3e9633f03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d908574f0c4c27fe0e2d790ce476963add846ccefaf50d4280476c79040837a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbe97aee38344e19ac2fcaa5dc8a621e7e605a7c1910f230cde04c9c3ab6335(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d56c1895f34ba410bb9ba4bb25bd92b8a5c05a97b457f7ba8274cf02b85c496(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c37fed03f6c43dc85fe6858bda5276e3d73de44e2de376534e910d6d66ed2bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6133c058c812c33bc84ad07f5f94878f0cb6668a4b4b06ea9ff87fe53496b8(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfigNewValueTimeValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f439bfe94bfda3779a0a1105ce59e3575b2d04675b491475b06c1943ce04dab9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980ffcb2dc9db7651a9a6db142c8eb40d00f92b9ca320bf0585beff01feff8d2(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfigInfoTypeTransformationsTransformationsPrimitiveTransformationReplaceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f86322367c9ed1c4dcf43efc992630a669b1317d0d433e14895d5ee0977f896(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53cc4a7ad7d91c08b2ee964ca70e598346041946bf69684127578fc6f720da2(
    value: typing.Optional[DataLossPreventionDeidentifyTemplateDeidentifyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408149af513352549b48f8bc277a15ede8ed1fd2a2f60649c321170030cfc3c2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37f761b3a358ff36d72d8e75bb433a6840ba0dd030f64df8180007847574c1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6316612dda0d8f74a197b263e8f934e0c07a4af483939e3dbb2c0902f270656c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeacd9bd4e147776b8a94a918f71bc89024704651be09c6411dad163e3c5baa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f58f67769eeac865bc1e3ce827ea93c2fb3df59f8fb60d88317996c61daaff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b76a3c2e131cae27999bc0f893e7b43334a4d7117714ad7aa1316ce8fc81d4(
    value: typing.Optional[typing.Union[DataLossPreventionDeidentifyTemplateTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
