"""
Type annotations for backup-gateway service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/type_defs/)

Usage::

    ```python
    from mypy_boto3_backup_gateway.type_defs import AssociateGatewayToServerInputRequestTypeDef

    data: AssociateGatewayToServerInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import HypervisorStateType, SyncMetadataStatusType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateGatewayToServerInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BandwidthRateLimitIntervalTypeDef",
    "TagTypeDef",
    "DeleteGatewayInputRequestTypeDef",
    "DeleteHypervisorInputRequestTypeDef",
    "DisassociateGatewayFromServerInputRequestTypeDef",
    "MaintenanceStartTimeTypeDef",
    "GatewayTypeDef",
    "GetBandwidthRateLimitScheduleInputRequestTypeDef",
    "GetGatewayInputRequestTypeDef",
    "GetHypervisorInputRequestTypeDef",
    "HypervisorDetailsTypeDef",
    "GetHypervisorPropertyMappingsInputRequestTypeDef",
    "VmwareToAwsTagMappingTypeDef",
    "GetVirtualMachineInputRequestTypeDef",
    "HypervisorTypeDef",
    "PaginatorConfigTypeDef",
    "ListGatewaysInputRequestTypeDef",
    "ListHypervisorsInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListVirtualMachinesInputRequestTypeDef",
    "VirtualMachineTypeDef",
    "PutMaintenanceStartTimeInputRequestTypeDef",
    "StartVirtualMachinesMetadataSyncInputRequestTypeDef",
    "TestHypervisorConfigurationInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateGatewayInformationInputRequestTypeDef",
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    "UpdateHypervisorInputRequestTypeDef",
    "VmwareTagTypeDef",
    "AssociateGatewayToServerOutputTypeDef",
    "CreateGatewayOutputTypeDef",
    "DeleteGatewayOutputTypeDef",
    "DeleteHypervisorOutputTypeDef",
    "DisassociateGatewayFromServerOutputTypeDef",
    "ImportHypervisorConfigurationOutputTypeDef",
    "PutBandwidthRateLimitScheduleOutputTypeDef",
    "PutHypervisorPropertyMappingsOutputTypeDef",
    "PutMaintenanceStartTimeOutputTypeDef",
    "StartVirtualMachinesMetadataSyncOutputTypeDef",
    "TagResourceOutputTypeDef",
    "UntagResourceOutputTypeDef",
    "UpdateGatewayInformationOutputTypeDef",
    "UpdateGatewaySoftwareNowOutputTypeDef",
    "UpdateHypervisorOutputTypeDef",
    "GetBandwidthRateLimitScheduleOutputTypeDef",
    "PutBandwidthRateLimitScheduleInputRequestTypeDef",
    "CreateGatewayInputRequestTypeDef",
    "ImportHypervisorConfigurationInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "GatewayDetailsTypeDef",
    "ListGatewaysOutputTypeDef",
    "GetHypervisorOutputTypeDef",
    "GetHypervisorPropertyMappingsOutputTypeDef",
    "PutHypervisorPropertyMappingsInputRequestTypeDef",
    "ListHypervisorsOutputTypeDef",
    "ListGatewaysInputListGatewaysPaginateTypeDef",
    "ListHypervisorsInputListHypervisorsPaginateTypeDef",
    "ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef",
    "ListVirtualMachinesOutputTypeDef",
    "VirtualMachineDetailsTypeDef",
    "GetGatewayOutputTypeDef",
    "GetVirtualMachineOutputTypeDef",
)

AssociateGatewayToServerInputRequestTypeDef = TypedDict(
    "AssociateGatewayToServerInputRequestTypeDef",
    {
        "GatewayArn": str,
        "ServerArn": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredBandwidthRateLimitIntervalTypeDef = TypedDict(
    "_RequiredBandwidthRateLimitIntervalTypeDef",
    {
        "DaysOfWeek": List[int],
        "EndHourOfDay": int,
        "EndMinuteOfHour": int,
        "StartHourOfDay": int,
        "StartMinuteOfHour": int,
    },
)
_OptionalBandwidthRateLimitIntervalTypeDef = TypedDict(
    "_OptionalBandwidthRateLimitIntervalTypeDef",
    {
        "AverageUploadRateLimitInBitsPerSec": int,
    },
    total=False,
)


class BandwidthRateLimitIntervalTypeDef(
    _RequiredBandwidthRateLimitIntervalTypeDef, _OptionalBandwidthRateLimitIntervalTypeDef
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteGatewayInputRequestTypeDef = TypedDict(
    "DeleteGatewayInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

DeleteHypervisorInputRequestTypeDef = TypedDict(
    "DeleteHypervisorInputRequestTypeDef",
    {
        "HypervisorArn": str,
    },
)

DisassociateGatewayFromServerInputRequestTypeDef = TypedDict(
    "DisassociateGatewayFromServerInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

_RequiredMaintenanceStartTimeTypeDef = TypedDict(
    "_RequiredMaintenanceStartTimeTypeDef",
    {
        "HourOfDay": int,
        "MinuteOfHour": int,
    },
)
_OptionalMaintenanceStartTimeTypeDef = TypedDict(
    "_OptionalMaintenanceStartTimeTypeDef",
    {
        "DayOfMonth": int,
        "DayOfWeek": int,
    },
    total=False,
)


class MaintenanceStartTimeTypeDef(
    _RequiredMaintenanceStartTimeTypeDef, _OptionalMaintenanceStartTimeTypeDef
):
    pass


GatewayTypeDef = TypedDict(
    "GatewayTypeDef",
    {
        "GatewayArn": str,
        "GatewayDisplayName": str,
        "GatewayType": Literal["BACKUP_VM"],
        "HypervisorId": str,
        "LastSeenTime": datetime,
    },
    total=False,
)

GetBandwidthRateLimitScheduleInputRequestTypeDef = TypedDict(
    "GetBandwidthRateLimitScheduleInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

GetGatewayInputRequestTypeDef = TypedDict(
    "GetGatewayInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

GetHypervisorInputRequestTypeDef = TypedDict(
    "GetHypervisorInputRequestTypeDef",
    {
        "HypervisorArn": str,
    },
)

HypervisorDetailsTypeDef = TypedDict(
    "HypervisorDetailsTypeDef",
    {
        "Host": str,
        "HypervisorArn": str,
        "KmsKeyArn": str,
        "LastSuccessfulMetadataSyncTime": datetime,
        "LatestMetadataSyncStatus": SyncMetadataStatusType,
        "LatestMetadataSyncStatusMessage": str,
        "LogGroupArn": str,
        "Name": str,
        "State": HypervisorStateType,
    },
    total=False,
)

GetHypervisorPropertyMappingsInputRequestTypeDef = TypedDict(
    "GetHypervisorPropertyMappingsInputRequestTypeDef",
    {
        "HypervisorArn": str,
    },
)

VmwareToAwsTagMappingTypeDef = TypedDict(
    "VmwareToAwsTagMappingTypeDef",
    {
        "AwsTagKey": str,
        "AwsTagValue": str,
        "VmwareCategory": str,
        "VmwareTagName": str,
    },
)

GetVirtualMachineInputRequestTypeDef = TypedDict(
    "GetVirtualMachineInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

HypervisorTypeDef = TypedDict(
    "HypervisorTypeDef",
    {
        "Host": str,
        "HypervisorArn": str,
        "KmsKeyArn": str,
        "Name": str,
        "State": HypervisorStateType,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListGatewaysInputRequestTypeDef = TypedDict(
    "ListGatewaysInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListHypervisorsInputRequestTypeDef = TypedDict(
    "ListHypervisorsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListVirtualMachinesInputRequestTypeDef = TypedDict(
    "ListVirtualMachinesInputRequestTypeDef",
    {
        "HypervisorArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

VirtualMachineTypeDef = TypedDict(
    "VirtualMachineTypeDef",
    {
        "HostName": str,
        "HypervisorId": str,
        "LastBackupDate": datetime,
        "Name": str,
        "Path": str,
        "ResourceArn": str,
    },
    total=False,
)

_RequiredPutMaintenanceStartTimeInputRequestTypeDef = TypedDict(
    "_RequiredPutMaintenanceStartTimeInputRequestTypeDef",
    {
        "GatewayArn": str,
        "HourOfDay": int,
        "MinuteOfHour": int,
    },
)
_OptionalPutMaintenanceStartTimeInputRequestTypeDef = TypedDict(
    "_OptionalPutMaintenanceStartTimeInputRequestTypeDef",
    {
        "DayOfMonth": int,
        "DayOfWeek": int,
    },
    total=False,
)


class PutMaintenanceStartTimeInputRequestTypeDef(
    _RequiredPutMaintenanceStartTimeInputRequestTypeDef,
    _OptionalPutMaintenanceStartTimeInputRequestTypeDef,
):
    pass


StartVirtualMachinesMetadataSyncInputRequestTypeDef = TypedDict(
    "StartVirtualMachinesMetadataSyncInputRequestTypeDef",
    {
        "HypervisorArn": str,
    },
)

_RequiredTestHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_RequiredTestHypervisorConfigurationInputRequestTypeDef",
    {
        "GatewayArn": str,
        "Host": str,
    },
)
_OptionalTestHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_OptionalTestHypervisorConfigurationInputRequestTypeDef",
    {
        "Password": str,
        "Username": str,
    },
    total=False,
)


class TestHypervisorConfigurationInputRequestTypeDef(
    _RequiredTestHypervisorConfigurationInputRequestTypeDef,
    _OptionalTestHypervisorConfigurationInputRequestTypeDef,
):
    pass


UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateGatewayInformationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGatewayInformationInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)
_OptionalUpdateGatewayInformationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGatewayInformationInputRequestTypeDef",
    {
        "GatewayDisplayName": str,
    },
    total=False,
)


class UpdateGatewayInformationInputRequestTypeDef(
    _RequiredUpdateGatewayInformationInputRequestTypeDef,
    _OptionalUpdateGatewayInformationInputRequestTypeDef,
):
    pass


UpdateGatewaySoftwareNowInputRequestTypeDef = TypedDict(
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

_RequiredUpdateHypervisorInputRequestTypeDef = TypedDict(
    "_RequiredUpdateHypervisorInputRequestTypeDef",
    {
        "HypervisorArn": str,
    },
)
_OptionalUpdateHypervisorInputRequestTypeDef = TypedDict(
    "_OptionalUpdateHypervisorInputRequestTypeDef",
    {
        "Host": str,
        "LogGroupArn": str,
        "Name": str,
        "Password": str,
        "Username": str,
    },
    total=False,
)


class UpdateHypervisorInputRequestTypeDef(
    _RequiredUpdateHypervisorInputRequestTypeDef, _OptionalUpdateHypervisorInputRequestTypeDef
):
    pass


VmwareTagTypeDef = TypedDict(
    "VmwareTagTypeDef",
    {
        "VmwareCategory": str,
        "VmwareTagDescription": str,
        "VmwareTagName": str,
    },
    total=False,
)

AssociateGatewayToServerOutputTypeDef = TypedDict(
    "AssociateGatewayToServerOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGatewayOutputTypeDef = TypedDict(
    "CreateGatewayOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGatewayOutputTypeDef = TypedDict(
    "DeleteGatewayOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteHypervisorOutputTypeDef = TypedDict(
    "DeleteHypervisorOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateGatewayFromServerOutputTypeDef = TypedDict(
    "DisassociateGatewayFromServerOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportHypervisorConfigurationOutputTypeDef = TypedDict(
    "ImportHypervisorConfigurationOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutBandwidthRateLimitScheduleOutputTypeDef = TypedDict(
    "PutBandwidthRateLimitScheduleOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutHypervisorPropertyMappingsOutputTypeDef = TypedDict(
    "PutHypervisorPropertyMappingsOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutMaintenanceStartTimeOutputTypeDef = TypedDict(
    "PutMaintenanceStartTimeOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartVirtualMachinesMetadataSyncOutputTypeDef = TypedDict(
    "StartVirtualMachinesMetadataSyncOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceOutputTypeDef = TypedDict(
    "TagResourceOutputTypeDef",
    {
        "ResourceARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourceOutputTypeDef = TypedDict(
    "UntagResourceOutputTypeDef",
    {
        "ResourceARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewayInformationOutputTypeDef = TypedDict(
    "UpdateGatewayInformationOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewaySoftwareNowOutputTypeDef = TypedDict(
    "UpdateGatewaySoftwareNowOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateHypervisorOutputTypeDef = TypedDict(
    "UpdateHypervisorOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBandwidthRateLimitScheduleOutputTypeDef = TypedDict(
    "GetBandwidthRateLimitScheduleOutputTypeDef",
    {
        "BandwidthRateLimitIntervals": List[BandwidthRateLimitIntervalTypeDef],
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutBandwidthRateLimitScheduleInputRequestTypeDef = TypedDict(
    "PutBandwidthRateLimitScheduleInputRequestTypeDef",
    {
        "BandwidthRateLimitIntervals": Sequence[BandwidthRateLimitIntervalTypeDef],
        "GatewayArn": str,
    },
)

_RequiredCreateGatewayInputRequestTypeDef = TypedDict(
    "_RequiredCreateGatewayInputRequestTypeDef",
    {
        "ActivationKey": str,
        "GatewayDisplayName": str,
        "GatewayType": Literal["BACKUP_VM"],
    },
)
_OptionalCreateGatewayInputRequestTypeDef = TypedDict(
    "_OptionalCreateGatewayInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateGatewayInputRequestTypeDef(
    _RequiredCreateGatewayInputRequestTypeDef, _OptionalCreateGatewayInputRequestTypeDef
):
    pass


_RequiredImportHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_RequiredImportHypervisorConfigurationInputRequestTypeDef",
    {
        "Host": str,
        "Name": str,
    },
)
_OptionalImportHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_OptionalImportHypervisorConfigurationInputRequestTypeDef",
    {
        "KmsKeyArn": str,
        "Password": str,
        "Tags": Sequence[TagTypeDef],
        "Username": str,
    },
    total=False,
)


class ImportHypervisorConfigurationInputRequestTypeDef(
    _RequiredImportHypervisorConfigurationInputRequestTypeDef,
    _OptionalImportHypervisorConfigurationInputRequestTypeDef,
):
    pass


ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "ResourceArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

GatewayDetailsTypeDef = TypedDict(
    "GatewayDetailsTypeDef",
    {
        "GatewayArn": str,
        "GatewayDisplayName": str,
        "GatewayType": Literal["BACKUP_VM"],
        "HypervisorId": str,
        "LastSeenTime": datetime,
        "MaintenanceStartTime": MaintenanceStartTimeTypeDef,
        "NextUpdateAvailabilityTime": datetime,
        "VpcEndpoint": str,
    },
    total=False,
)

ListGatewaysOutputTypeDef = TypedDict(
    "ListGatewaysOutputTypeDef",
    {
        "Gateways": List[GatewayTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHypervisorOutputTypeDef = TypedDict(
    "GetHypervisorOutputTypeDef",
    {
        "Hypervisor": HypervisorDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHypervisorPropertyMappingsOutputTypeDef = TypedDict(
    "GetHypervisorPropertyMappingsOutputTypeDef",
    {
        "HypervisorArn": str,
        "IamRoleArn": str,
        "VmwareToAwsTagMappings": List[VmwareToAwsTagMappingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutHypervisorPropertyMappingsInputRequestTypeDef = TypedDict(
    "PutHypervisorPropertyMappingsInputRequestTypeDef",
    {
        "HypervisorArn": str,
        "IamRoleArn": str,
        "VmwareToAwsTagMappings": Sequence[VmwareToAwsTagMappingTypeDef],
    },
)

ListHypervisorsOutputTypeDef = TypedDict(
    "ListHypervisorsOutputTypeDef",
    {
        "Hypervisors": List[HypervisorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGatewaysInputListGatewaysPaginateTypeDef = TypedDict(
    "ListGatewaysInputListGatewaysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListHypervisorsInputListHypervisorsPaginateTypeDef = TypedDict(
    "ListHypervisorsInputListHypervisorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef = TypedDict(
    "ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef",
    {
        "HypervisorArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVirtualMachinesOutputTypeDef = TypedDict(
    "ListVirtualMachinesOutputTypeDef",
    {
        "NextToken": str,
        "VirtualMachines": List[VirtualMachineTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VirtualMachineDetailsTypeDef = TypedDict(
    "VirtualMachineDetailsTypeDef",
    {
        "HostName": str,
        "HypervisorId": str,
        "LastBackupDate": datetime,
        "Name": str,
        "Path": str,
        "ResourceArn": str,
        "VmwareTags": List[VmwareTagTypeDef],
    },
    total=False,
)

GetGatewayOutputTypeDef = TypedDict(
    "GetGatewayOutputTypeDef",
    {
        "Gateway": GatewayDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVirtualMachineOutputTypeDef = TypedDict(
    "GetVirtualMachineOutputTypeDef",
    {
        "VirtualMachine": VirtualMachineDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
