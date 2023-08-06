# This is spectacularly generated code by spectacular v0.8.0 based on
# Qlik Cloud Services 0.529.8

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource
from .Qix import Doc


@dataclass
class NxApp(Doc):
    """
    Application attributes and user privileges.

    Attributes
    ----------
    attributes: NxAttributes
      App attributes. This structure can also contain extra user-defined attributes.
    create: list[NxAppCreatePrivileges]
      Object create privileges. Hints to the client what type of objects the user is allowed to create.
    privileges: list[str]
      Application privileges.
      Hints to the client what actions the user is allowed to perform.
      Could be any of:

      • read

      • create

      • update

      • delete

      • reload

      • import

      • publish

      • duplicate

      • export

      • exportdata

      • change_owner

      • change_space
    """

    attributes: NxAttributes = None
    create: list[NxAppCreatePrivileges] = None
    privileges: list[str] = None

    def __init__(self_, **kvargs):

        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == NxApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = NxAttributes(**kvargs["attributes"])
        if "create" in kvargs and kvargs["create"] is not None:
            if (
                len(kvargs["create"]) > 0
                and f"list[{type(kvargs['create'][0]).__name__}]"
                == NxApp.__annotations__["create"]
            ):
                self_.create = kvargs["create"]
            else:
                self_.create = [NxAppCreatePrivileges(**e) for e in kvargs["create"]]
        if "privileges" in kvargs and kvargs["privileges"] is not None:
            if (
                type(kvargs["privileges"]).__name__
                == NxApp.__annotations__["privileges"]
            ):
                self_.privileges = kvargs["privileges"]
            else:
                self_.privileges = kvargs["privileges"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def create_copy(self, data: CreateApp) -> NxApp:
        """
        Copies a specific app.

        Parameters
        ----------
        data: CreateApp
          Attributes that should be set in the copy.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/copy".replace("{appId}", self.attributes.id),
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_data_lineages(self) -> list[LineageInfoRest]:
        """
        Retrieves the lineage for an app.
        Returns a JSON-formatted array of strings describing the lineage of the app.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/data/lineage".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        return [LineageInfoRest(**e) for e in response.json()]

    def get_data_metadata(self) -> DataModelMetadata:
        """
        Retrieves the data model and reload statistics metadata of an app.
        An empty metadata structure is returned if the metadata is not available in the app.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/data/metadata".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        obj = DataModelMetadata(**response.json())
        obj.auth = self.auth
        return obj

    def export(self, NoData: bool = None) -> str:
        """
        Exports a specific app.

        Parameters
        ----------
        NoData: bool = None
          The flag indicating if only object contents should be exported.
        """
        query_params = {}
        if NoData is not None:
            query_params["NoData"] = NoData
        response = self.auth.rest(
            path="/apps/{appId}/export".replace("{appId}", self.attributes.id),
            method="POST",
            params=query_params,
            data=None,
        )
        return response.headers["Location"]

    def get_media_thumbnail(self) -> str:
        """
        Gets media content from file currently used as application thumbnail.
        Returns a stream of bytes containing the media file content on success, or error if file is not found.
        The image selected as thumbnail is only updated when application is saved.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/media/thumbnail".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def set_owner(self, data: UpdateOwner) -> NxApp:
        """
        Changes owner of the app.

        Parameters
        ----------
        data: UpdateOwner
          New owner.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/owner".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def publish(self, data: PublishApp) -> NxApp:
        """
        Publishes a specific app to a managed space.

        Parameters
        ----------
        data: PublishApp
          Publish information for the app.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/publish".replace("{appId}", self.attributes.id),
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def set_publish(self, data: RepublishApp) -> NxApp:
        """
        Republishes a published app to a managed space.

        Parameters
        ----------
        data: RepublishApp
          Republish information for the app.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/publish".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def get_reloads_logs(self) -> ScriptLogList:
        """
        Retrieves the metadata about all script logs stored for an app.
        Returns an array of ScriptLogMeta objects.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/reloads/logs".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        obj = ScriptLogList(**response.json())
        obj.auth = self.auth
        return obj

    def delete_space(self) -> NxApp:
        """
        Removes space from a specific app.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/space".replace("{appId}", self.attributes.id),
            method="DELETE",
            params={},
            data=None,
        )
        self.__init__(**response.json())
        return self

    def set_space(self, data: UpdateSpace) -> NxApp:
        """
        Sets space on a specific app.

        Parameters
        ----------
        data: UpdateSpace
          New space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/space".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def delete(self) -> None:
        """
        Deletes a specific app.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/apps/{appId}".replace("{appId}", self.attributes.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: UpdateApp) -> NxApp:
        """
        Updates the information for a specific app.

        Parameters
        ----------
        data: UpdateApp
          Attributes that user wants to set.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class AppAttributes:
    """

    Attributes
    ----------
    description: str
      The description of the application
    locale: str
      Set custom locale instead of the system default
    name: str
      The name (title) of the application
    spaceId: str
      The space ID of the application
    """

    description: str = None
    locale: str = None
    name: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == AppAttributes.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "locale" in kvargs and kvargs["locale"] is not None:
            if (
                type(kvargs["locale"]).__name__
                == AppAttributes.__annotations__["locale"]
            ):
                self_.locale = kvargs["locale"]
            else:
                self_.locale = kvargs["locale"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == AppAttributes.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            if (
                type(kvargs["spaceId"]).__name__
                == AppAttributes.__annotations__["spaceId"]
            ):
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppContentList:
    """

    Attributes
    ----------
    data: list[AppContentListItem]
      Content list items.
    library: str
      Content library name.
    subpath: str
      Content library relative listing path. Empty in case of root listed or representing actual subpath listed.
    """

    data: list[AppContentListItem] = None
    library: str = None
    subpath: str = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == AppContentList.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [AppContentListItem(**e) for e in kvargs["data"]]
        if "library" in kvargs and kvargs["library"] is not None:
            if (
                type(kvargs["library"]).__name__
                == AppContentList.__annotations__["library"]
            ):
                self_.library = kvargs["library"]
            else:
                self_.library = kvargs["library"]
        if "subpath" in kvargs and kvargs["subpath"] is not None:
            if (
                type(kvargs["subpath"]).__name__
                == AppContentList.__annotations__["subpath"]
            ):
                self_.subpath = kvargs["subpath"]
            else:
                self_.subpath = kvargs["subpath"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppContentListItem:
    """

    Attributes
    ----------
    id: str
      Unique content identifier.
    link: str
      Unique content link.
    name: str
      Content name.
    type: str
      Content type.
    """

    id: str = None
    link: str = None
    name: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == AppContentListItem.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "link" in kvargs and kvargs["link"] is not None:
            if (
                type(kvargs["link"]).__name__
                == AppContentListItem.__annotations__["link"]
            ):
                self_.link = kvargs["link"]
            else:
                self_.link = kvargs["link"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == AppContentListItem.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "type" in kvargs and kvargs["type"] is not None:
            if (
                type(kvargs["type"]).__name__
                == AppContentListItem.__annotations__["type"]
            ):
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppUpdateAttributes:
    """

    Attributes
    ----------
    description: str
      The description of the application.
    name: str
      The name (title) of the application.
    """

    description: str = None
    name: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == AppUpdateAttributes.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == AppUpdateAttributes.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CreateApp:
    """

    Attributes
    ----------
    attributes: AppAttributes
    """

    attributes: AppAttributes = None

    def __init__(self_, **kvargs):

        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == CreateApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppAttributes(**kvargs["attributes"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataModelMetadata:
    """

    Attributes
    ----------
    fields: list[FieldMetadata]
      List of field descriptions.
    has_section_access: bool
      If set to true, the app has section access configured.
    is_direct_query_mode: bool
    reload_meta: LastReloadMetadata
    static_byte_size: int
      Static memory usage for the app.
    tables: list[TableMetadata]
      List of table descriptions.
    tables_profiling_data: list[TableProfilingData]
      Profiling data of the tables in the app.
    """

    fields: list[FieldMetadata] = None
    has_section_access: bool = None
    is_direct_query_mode: bool = None
    reload_meta: LastReloadMetadata = None
    static_byte_size: int = None
    tables: list[TableMetadata] = None
    tables_profiling_data: list[TableProfilingData] = None

    def __init__(self_, **kvargs):

        if "fields" in kvargs and kvargs["fields"] is not None:
            if (
                len(kvargs["fields"]) > 0
                and f"list[{type(kvargs['fields'][0]).__name__}]"
                == DataModelMetadata.__annotations__["fields"]
            ):
                self_.fields = kvargs["fields"]
            else:
                self_.fields = [FieldMetadata(**e) for e in kvargs["fields"]]
        if "has_section_access" in kvargs and kvargs["has_section_access"] is not None:
            if (
                type(kvargs["has_section_access"]).__name__
                == DataModelMetadata.__annotations__["has_section_access"]
            ):
                self_.has_section_access = kvargs["has_section_access"]
            else:
                self_.has_section_access = kvargs["has_section_access"]
        if (
            "is_direct_query_mode" in kvargs
            and kvargs["is_direct_query_mode"] is not None
        ):
            if (
                type(kvargs["is_direct_query_mode"]).__name__
                == DataModelMetadata.__annotations__["is_direct_query_mode"]
            ):
                self_.is_direct_query_mode = kvargs["is_direct_query_mode"]
            else:
                self_.is_direct_query_mode = kvargs["is_direct_query_mode"]
        if "reload_meta" in kvargs and kvargs["reload_meta"] is not None:
            if (
                type(kvargs["reload_meta"]).__name__
                == DataModelMetadata.__annotations__["reload_meta"]
            ):
                self_.reload_meta = kvargs["reload_meta"]
            else:
                self_.reload_meta = LastReloadMetadata(**kvargs["reload_meta"])
        if "static_byte_size" in kvargs and kvargs["static_byte_size"] is not None:
            if (
                type(kvargs["static_byte_size"]).__name__
                == DataModelMetadata.__annotations__["static_byte_size"]
            ):
                self_.static_byte_size = kvargs["static_byte_size"]
            else:
                self_.static_byte_size = kvargs["static_byte_size"]
        if "tables" in kvargs and kvargs["tables"] is not None:
            if (
                len(kvargs["tables"]) > 0
                and f"list[{type(kvargs['tables'][0]).__name__}]"
                == DataModelMetadata.__annotations__["tables"]
            ):
                self_.tables = kvargs["tables"]
            else:
                self_.tables = [TableMetadata(**e) for e in kvargs["tables"]]
        if (
            "tables_profiling_data" in kvargs
            and kvargs["tables_profiling_data"] is not None
        ):
            if (
                len(kvargs["tables_profiling_data"]) > 0
                and f"list[{type(kvargs['tables_profiling_data'][0]).__name__}]"
                == DataModelMetadata.__annotations__["tables_profiling_data"]
            ):
                self_.tables_profiling_data = kvargs["tables_profiling_data"]
            else:
                self_.tables_profiling_data = [
                    TableProfilingData(**e) for e in kvargs["tables_profiling_data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldAttributes:
    """
    Sets the formatting of a field.
    The properties of qFieldAttributes and the formatting mechanism are described below.

     Formatting mechanism:
    The formatting mechanism depends on the type set in qType, as shown below:
    In case of inconsistencies between the type and the format pattern, the format pattern takes precedence over the type.

     Type is DATE, TIME, TIMESTAMP or INTERVAL:
    The following applies:

    • If a format pattern is defined in qFmt , the formatting is as defined in qFmt .

    • If qFmt is empty, the formatting is defined by the number interpretation variables included at the top of the script ( TimeFormat , DateFormat , TimeStampFormat ).

    • The properties qDec , qThou , qnDec , qUseThou are not used.

     Type is INTEGER:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the formatting mechanism uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , no formatting is applied. The properties qDec , qThou , qnDec , qUseThou and the number interpretation variables defined in the script are not used .

     Type is REAL:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , and if the value is almost an integer value (for example, 14,000012), the value is formatted as an integer. The properties qDec , qThou , qnDec , qUseThou are not used.

    • If no format pattern is defined in qFmt , and if qnDec is defined and not 0, the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

    • If no format pattern is defined in qFmt , and if qnDec is 0, the number of decimals is 14 and the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

     Type is FIX:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , the properties qDec and qnDec are used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

     Type is MONEY:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of any script ( MoneyDecimalSep and MoneyThousandSep ).

    • If no format pattern is defined in qFmt , the engine uses the number interpretation variables included at the top of the script ( MoneyDecimalSep and MoneyThousandSep ).

     Type is ASCII:
    No formatting, qFmt is ignored.

    Attributes
    ----------
    Dec: str
      Defines the decimal separator.
      Example: .
    Fmt: str
      Defines the format pattern that applies to qText .
      Is used in connection to the type of the field (parameter qType ).
      For more information, see Formatting mechanism.
      Example: YYYY-MM-DD for a date.
    Thou: str
      Defines the thousand separator (if any).
      Is used if qUseThou is set to 1.
      Example: ,
    Type: str
      Type of the field.
      Default is U.

      One of:

      • U or UNKNOWN

      • A or ASCII

      • I or INTEGER

      • R or REAL

      • F or FIX

      • M or MONEY

      • D or DATE

      • T or TIME

      • TS or TIMESTAMP

      • IV or INTERVAL
    UseThou: int
      Defines whether or not a thousands separator must be used.
      Default is 0.
    nDec: int
      Number of decimals.
      Default is 10.
    """

    Dec: str = None
    Fmt: str = None
    Thou: str = None
    Type: str = "UNKNOWN"
    UseThou: int = None
    nDec: int = 10

    def __init__(self_, **kvargs):

        if "Dec" in kvargs and kvargs["Dec"] is not None:
            if type(kvargs["Dec"]).__name__ == FieldAttributes.__annotations__["Dec"]:
                self_.Dec = kvargs["Dec"]
            else:
                self_.Dec = kvargs["Dec"]
        if "Fmt" in kvargs and kvargs["Fmt"] is not None:
            if type(kvargs["Fmt"]).__name__ == FieldAttributes.__annotations__["Fmt"]:
                self_.Fmt = kvargs["Fmt"]
            else:
                self_.Fmt = kvargs["Fmt"]
        if "Thou" in kvargs and kvargs["Thou"] is not None:
            if type(kvargs["Thou"]).__name__ == FieldAttributes.__annotations__["Thou"]:
                self_.Thou = kvargs["Thou"]
            else:
                self_.Thou = kvargs["Thou"]
        if "Type" in kvargs and kvargs["Type"] is not None:
            if type(kvargs["Type"]).__name__ == FieldAttributes.__annotations__["Type"]:
                self_.Type = kvargs["Type"]
            else:
                self_.Type = kvargs["Type"]
        if "UseThou" in kvargs and kvargs["UseThou"] is not None:
            if (
                type(kvargs["UseThou"]).__name__
                == FieldAttributes.__annotations__["UseThou"]
            ):
                self_.UseThou = kvargs["UseThou"]
            else:
                self_.UseThou = kvargs["UseThou"]
        if "nDec" in kvargs and kvargs["nDec"] is not None:
            if type(kvargs["nDec"]).__name__ == FieldAttributes.__annotations__["nDec"]:
                self_.nDec = kvargs["nDec"]
            else:
                self_.nDec = kvargs["nDec"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldInTableProfilingData:
    """

    Attributes
    ----------
    Average: float
      Average of all numerical values. NaN otherwise.
    AvgStringLen: float
      Average string length of textual values. 0 otherwise.
    DistinctNumericValues: int
      Number of distinct numeric values
    DistinctTextValues: int
      Number of distinct text values
    DistinctValues: int
      Number of distinct values
    EmptyStrings: int
      Number of empty strings
    FieldTags: list[str]
      List of tags related to the field.
    FirstSorted: str
      For textual values the first sorted string.
    Fractiles: list[float]
      The .01, .05, .1, .25, .5, .75, .9, .95, .99 fractiles. Array of NaN otherwise.
    FrequencyDistribution: FrequencyDistributionData
    Kurtosis: float
      Kurtosis of the numerical values. NaN otherwise.
    LastSorted: str
      For textual values the last sorted string.
    Max: float
      Maximum value of numerical values. NaN otherwise.
    MaxStringLen: int
      Maximum string length of textual values. 0 otherwise.
    Median: float
      Median of all numerical values. NaN otherwise.
    Min: float
      Minimum value of numerical values. NaN otherwise.
    MinStringLen: int
      Minimum string length of textual values. 0 otherwise.
    MostFrequent: list[SymbolFrequency]
      Three most frequent values and their frequencies
    Name: str
      Name of the field.
    NegValues: int
      Number of negative values
    NullValues: int
      Number of null values
    NumberFormat: FieldAttributes
      Sets the formatting of a field.
      The properties of qFieldAttributes and the formatting mechanism are described below.

       Formatting mechanism:
      The formatting mechanism depends on the type set in qType, as shown below:
      In case of inconsistencies between the type and the format pattern, the format pattern takes precedence over the type.

       Type is DATE, TIME, TIMESTAMP or INTERVAL:
      The following applies:

      • If a format pattern is defined in qFmt , the formatting is as defined in qFmt .

      • If qFmt is empty, the formatting is defined by the number interpretation variables included at the top of the script ( TimeFormat , DateFormat , TimeStampFormat ).

      • The properties qDec , qThou , qnDec , qUseThou are not used.

       Type is INTEGER:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the formatting mechanism uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , no formatting is applied. The properties qDec , qThou , qnDec , qUseThou and the number interpretation variables defined in the script are not used .

       Type is REAL:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , and if the value is almost an integer value (for example, 14,000012), the value is formatted as an integer. The properties qDec , qThou , qnDec , qUseThou are not used.

      • If no format pattern is defined in qFmt , and if qnDec is defined and not 0, the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

      • If no format pattern is defined in qFmt , and if qnDec is 0, the number of decimals is 14 and the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

       Type is FIX:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , the properties qDec and qnDec are used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

       Type is MONEY:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of any script ( MoneyDecimalSep and MoneyThousandSep ).

      • If no format pattern is defined in qFmt , the engine uses the number interpretation variables included at the top of the script ( MoneyDecimalSep and MoneyThousandSep ).

       Type is ASCII:
      No formatting, qFmt is ignored.
    NumericValues: int
      Number of numeric values
    PosValues: int
      Number of positive values
    Skewness: float
      Skewness of the numerical values. NaN otherwise.
    Std: float
      Standard deviation of numerical values. NaN otherwise.
    Sum: float
      Sum of all numerical values. NaN otherwise.
    Sum2: float
      Squared sum of all numerical values. NaN otherwise.
    SumStringLen: int
      Sum of all characters in strings in the field
    TextValues: int
      Number of textual values
    ZeroValues: int
      Number of zero values for numerical values
    """

    Average: float = None
    AvgStringLen: float = None
    DistinctNumericValues: int = None
    DistinctTextValues: int = None
    DistinctValues: int = None
    EmptyStrings: int = None
    FieldTags: list[str] = None
    FirstSorted: str = None
    Fractiles: list[float] = None
    FrequencyDistribution: FrequencyDistributionData = None
    Kurtosis: float = None
    LastSorted: str = None
    Max: float = None
    MaxStringLen: int = None
    Median: float = None
    Min: float = None
    MinStringLen: int = None
    MostFrequent: list[SymbolFrequency] = None
    Name: str = None
    NegValues: int = None
    NullValues: int = None
    NumberFormat: FieldAttributes = None
    NumericValues: int = None
    PosValues: int = None
    Skewness: float = None
    Std: float = None
    Sum: float = None
    Sum2: float = None
    SumStringLen: int = None
    TextValues: int = None
    ZeroValues: int = None

    def __init__(self_, **kvargs):

        if "Average" in kvargs and kvargs["Average"] is not None:
            if (
                type(kvargs["Average"]).__name__
                == FieldInTableProfilingData.__annotations__["Average"]
            ):
                self_.Average = kvargs["Average"]
            else:
                self_.Average = kvargs["Average"]
        if "AvgStringLen" in kvargs and kvargs["AvgStringLen"] is not None:
            if (
                type(kvargs["AvgStringLen"]).__name__
                == FieldInTableProfilingData.__annotations__["AvgStringLen"]
            ):
                self_.AvgStringLen = kvargs["AvgStringLen"]
            else:
                self_.AvgStringLen = kvargs["AvgStringLen"]
        if (
            "DistinctNumericValues" in kvargs
            and kvargs["DistinctNumericValues"] is not None
        ):
            if (
                type(kvargs["DistinctNumericValues"]).__name__
                == FieldInTableProfilingData.__annotations__["DistinctNumericValues"]
            ):
                self_.DistinctNumericValues = kvargs["DistinctNumericValues"]
            else:
                self_.DistinctNumericValues = kvargs["DistinctNumericValues"]
        if "DistinctTextValues" in kvargs and kvargs["DistinctTextValues"] is not None:
            if (
                type(kvargs["DistinctTextValues"]).__name__
                == FieldInTableProfilingData.__annotations__["DistinctTextValues"]
            ):
                self_.DistinctTextValues = kvargs["DistinctTextValues"]
            else:
                self_.DistinctTextValues = kvargs["DistinctTextValues"]
        if "DistinctValues" in kvargs and kvargs["DistinctValues"] is not None:
            if (
                type(kvargs["DistinctValues"]).__name__
                == FieldInTableProfilingData.__annotations__["DistinctValues"]
            ):
                self_.DistinctValues = kvargs["DistinctValues"]
            else:
                self_.DistinctValues = kvargs["DistinctValues"]
        if "EmptyStrings" in kvargs and kvargs["EmptyStrings"] is not None:
            if (
                type(kvargs["EmptyStrings"]).__name__
                == FieldInTableProfilingData.__annotations__["EmptyStrings"]
            ):
                self_.EmptyStrings = kvargs["EmptyStrings"]
            else:
                self_.EmptyStrings = kvargs["EmptyStrings"]
        if "FieldTags" in kvargs and kvargs["FieldTags"] is not None:
            if (
                type(kvargs["FieldTags"]).__name__
                == FieldInTableProfilingData.__annotations__["FieldTags"]
            ):
                self_.FieldTags = kvargs["FieldTags"]
            else:
                self_.FieldTags = kvargs["FieldTags"]
        if "FirstSorted" in kvargs and kvargs["FirstSorted"] is not None:
            if (
                type(kvargs["FirstSorted"]).__name__
                == FieldInTableProfilingData.__annotations__["FirstSorted"]
            ):
                self_.FirstSorted = kvargs["FirstSorted"]
            else:
                self_.FirstSorted = kvargs["FirstSorted"]
        if "Fractiles" in kvargs and kvargs["Fractiles"] is not None:
            if (
                type(kvargs["Fractiles"]).__name__
                == FieldInTableProfilingData.__annotations__["Fractiles"]
            ):
                self_.Fractiles = kvargs["Fractiles"]
            else:
                self_.Fractiles = kvargs["Fractiles"]
        if (
            "FrequencyDistribution" in kvargs
            and kvargs["FrequencyDistribution"] is not None
        ):
            if (
                type(kvargs["FrequencyDistribution"]).__name__
                == FieldInTableProfilingData.__annotations__["FrequencyDistribution"]
            ):
                self_.FrequencyDistribution = kvargs["FrequencyDistribution"]
            else:
                self_.FrequencyDistribution = FrequencyDistributionData(
                    **kvargs["FrequencyDistribution"]
                )
        if "Kurtosis" in kvargs and kvargs["Kurtosis"] is not None:
            if (
                type(kvargs["Kurtosis"]).__name__
                == FieldInTableProfilingData.__annotations__["Kurtosis"]
            ):
                self_.Kurtosis = kvargs["Kurtosis"]
            else:
                self_.Kurtosis = kvargs["Kurtosis"]
        if "LastSorted" in kvargs and kvargs["LastSorted"] is not None:
            if (
                type(kvargs["LastSorted"]).__name__
                == FieldInTableProfilingData.__annotations__["LastSorted"]
            ):
                self_.LastSorted = kvargs["LastSorted"]
            else:
                self_.LastSorted = kvargs["LastSorted"]
        if "Max" in kvargs and kvargs["Max"] is not None:
            if (
                type(kvargs["Max"]).__name__
                == FieldInTableProfilingData.__annotations__["Max"]
            ):
                self_.Max = kvargs["Max"]
            else:
                self_.Max = kvargs["Max"]
        if "MaxStringLen" in kvargs and kvargs["MaxStringLen"] is not None:
            if (
                type(kvargs["MaxStringLen"]).__name__
                == FieldInTableProfilingData.__annotations__["MaxStringLen"]
            ):
                self_.MaxStringLen = kvargs["MaxStringLen"]
            else:
                self_.MaxStringLen = kvargs["MaxStringLen"]
        if "Median" in kvargs and kvargs["Median"] is not None:
            if (
                type(kvargs["Median"]).__name__
                == FieldInTableProfilingData.__annotations__["Median"]
            ):
                self_.Median = kvargs["Median"]
            else:
                self_.Median = kvargs["Median"]
        if "Min" in kvargs and kvargs["Min"] is not None:
            if (
                type(kvargs["Min"]).__name__
                == FieldInTableProfilingData.__annotations__["Min"]
            ):
                self_.Min = kvargs["Min"]
            else:
                self_.Min = kvargs["Min"]
        if "MinStringLen" in kvargs and kvargs["MinStringLen"] is not None:
            if (
                type(kvargs["MinStringLen"]).__name__
                == FieldInTableProfilingData.__annotations__["MinStringLen"]
            ):
                self_.MinStringLen = kvargs["MinStringLen"]
            else:
                self_.MinStringLen = kvargs["MinStringLen"]
        if "MostFrequent" in kvargs and kvargs["MostFrequent"] is not None:
            if (
                len(kvargs["MostFrequent"]) > 0
                and f"list[{type(kvargs['MostFrequent'][0]).__name__}]"
                == FieldInTableProfilingData.__annotations__["MostFrequent"]
            ):
                self_.MostFrequent = kvargs["MostFrequent"]
            else:
                self_.MostFrequent = [
                    SymbolFrequency(**e) for e in kvargs["MostFrequent"]
                ]
        if "Name" in kvargs and kvargs["Name"] is not None:
            if (
                type(kvargs["Name"]).__name__
                == FieldInTableProfilingData.__annotations__["Name"]
            ):
                self_.Name = kvargs["Name"]
            else:
                self_.Name = kvargs["Name"]
        if "NegValues" in kvargs and kvargs["NegValues"] is not None:
            if (
                type(kvargs["NegValues"]).__name__
                == FieldInTableProfilingData.__annotations__["NegValues"]
            ):
                self_.NegValues = kvargs["NegValues"]
            else:
                self_.NegValues = kvargs["NegValues"]
        if "NullValues" in kvargs and kvargs["NullValues"] is not None:
            if (
                type(kvargs["NullValues"]).__name__
                == FieldInTableProfilingData.__annotations__["NullValues"]
            ):
                self_.NullValues = kvargs["NullValues"]
            else:
                self_.NullValues = kvargs["NullValues"]
        if "NumberFormat" in kvargs and kvargs["NumberFormat"] is not None:
            if (
                type(kvargs["NumberFormat"]).__name__
                == FieldInTableProfilingData.__annotations__["NumberFormat"]
            ):
                self_.NumberFormat = kvargs["NumberFormat"]
            else:
                self_.NumberFormat = FieldAttributes(**kvargs["NumberFormat"])
        if "NumericValues" in kvargs and kvargs["NumericValues"] is not None:
            if (
                type(kvargs["NumericValues"]).__name__
                == FieldInTableProfilingData.__annotations__["NumericValues"]
            ):
                self_.NumericValues = kvargs["NumericValues"]
            else:
                self_.NumericValues = kvargs["NumericValues"]
        if "PosValues" in kvargs and kvargs["PosValues"] is not None:
            if (
                type(kvargs["PosValues"]).__name__
                == FieldInTableProfilingData.__annotations__["PosValues"]
            ):
                self_.PosValues = kvargs["PosValues"]
            else:
                self_.PosValues = kvargs["PosValues"]
        if "Skewness" in kvargs and kvargs["Skewness"] is not None:
            if (
                type(kvargs["Skewness"]).__name__
                == FieldInTableProfilingData.__annotations__["Skewness"]
            ):
                self_.Skewness = kvargs["Skewness"]
            else:
                self_.Skewness = kvargs["Skewness"]
        if "Std" in kvargs and kvargs["Std"] is not None:
            if (
                type(kvargs["Std"]).__name__
                == FieldInTableProfilingData.__annotations__["Std"]
            ):
                self_.Std = kvargs["Std"]
            else:
                self_.Std = kvargs["Std"]
        if "Sum" in kvargs and kvargs["Sum"] is not None:
            if (
                type(kvargs["Sum"]).__name__
                == FieldInTableProfilingData.__annotations__["Sum"]
            ):
                self_.Sum = kvargs["Sum"]
            else:
                self_.Sum = kvargs["Sum"]
        if "Sum2" in kvargs and kvargs["Sum2"] is not None:
            if (
                type(kvargs["Sum2"]).__name__
                == FieldInTableProfilingData.__annotations__["Sum2"]
            ):
                self_.Sum2 = kvargs["Sum2"]
            else:
                self_.Sum2 = kvargs["Sum2"]
        if "SumStringLen" in kvargs and kvargs["SumStringLen"] is not None:
            if (
                type(kvargs["SumStringLen"]).__name__
                == FieldInTableProfilingData.__annotations__["SumStringLen"]
            ):
                self_.SumStringLen = kvargs["SumStringLen"]
            else:
                self_.SumStringLen = kvargs["SumStringLen"]
        if "TextValues" in kvargs and kvargs["TextValues"] is not None:
            if (
                type(kvargs["TextValues"]).__name__
                == FieldInTableProfilingData.__annotations__["TextValues"]
            ):
                self_.TextValues = kvargs["TextValues"]
            else:
                self_.TextValues = kvargs["TextValues"]
        if "ZeroValues" in kvargs and kvargs["ZeroValues"] is not None:
            if (
                type(kvargs["ZeroValues"]).__name__
                == FieldInTableProfilingData.__annotations__["ZeroValues"]
            ):
                self_.ZeroValues = kvargs["ZeroValues"]
            else:
                self_.ZeroValues = kvargs["ZeroValues"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldMetadata:
    """

    Attributes
    ----------
    always_one_selected: bool
      If set to true, the field has one and only one selection (not 0 and not more than 1).
      If this property is set to true, the field cannot be cleared anymore and no more selections can be performed in that field.
      The default value is false.
    byte_size: int
      Static RAM memory used in bytes.
    cardinal: int
      Number of distinct field values.
    comment: str
      Field comment.
    distinct_only: bool
      If set to true, only distinct field values are shown.
      The default value is false.
    hash: str
      Hash of the data in the field. If the data in a reload is the same, the hash will be consistent.
    is_hidden: bool
      If set to true, the field is hidden.
      The default value is false.
    is_locked: bool
      If set to true, the field is locked.
      The default value is false.
    is_numeric: bool
      Is set to true if the value is a numeric.
      The default value is false.
    is_semantic: bool
      If set to true, the field is semantic.
      The default value is false.
    is_system: bool
      If set to true, the field is a system field.
      The default value is false.
    name: str
      Name of the field.
    src_tables: list[str]
      List of table names.
    tags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII.
    total_count: int
      Total number of field values.
    """

    always_one_selected: bool = None
    byte_size: int = None
    cardinal: int = None
    comment: str = None
    distinct_only: bool = None
    hash: str = None
    is_hidden: bool = None
    is_locked: bool = None
    is_numeric: bool = None
    is_semantic: bool = None
    is_system: bool = None
    name: str = None
    src_tables: list[str] = None
    tags: list[str] = None
    total_count: int = None

    def __init__(self_, **kvargs):

        if (
            "always_one_selected" in kvargs
            and kvargs["always_one_selected"] is not None
        ):
            if (
                type(kvargs["always_one_selected"]).__name__
                == FieldMetadata.__annotations__["always_one_selected"]
            ):
                self_.always_one_selected = kvargs["always_one_selected"]
            else:
                self_.always_one_selected = kvargs["always_one_selected"]
        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            if (
                type(kvargs["byte_size"]).__name__
                == FieldMetadata.__annotations__["byte_size"]
            ):
                self_.byte_size = kvargs["byte_size"]
            else:
                self_.byte_size = kvargs["byte_size"]
        if "cardinal" in kvargs and kvargs["cardinal"] is not None:
            if (
                type(kvargs["cardinal"]).__name__
                == FieldMetadata.__annotations__["cardinal"]
            ):
                self_.cardinal = kvargs["cardinal"]
            else:
                self_.cardinal = kvargs["cardinal"]
        if "comment" in kvargs and kvargs["comment"] is not None:
            if (
                type(kvargs["comment"]).__name__
                == FieldMetadata.__annotations__["comment"]
            ):
                self_.comment = kvargs["comment"]
            else:
                self_.comment = kvargs["comment"]
        if "distinct_only" in kvargs and kvargs["distinct_only"] is not None:
            if (
                type(kvargs["distinct_only"]).__name__
                == FieldMetadata.__annotations__["distinct_only"]
            ):
                self_.distinct_only = kvargs["distinct_only"]
            else:
                self_.distinct_only = kvargs["distinct_only"]
        if "hash" in kvargs and kvargs["hash"] is not None:
            if type(kvargs["hash"]).__name__ == FieldMetadata.__annotations__["hash"]:
                self_.hash = kvargs["hash"]
            else:
                self_.hash = kvargs["hash"]
        if "is_hidden" in kvargs and kvargs["is_hidden"] is not None:
            if (
                type(kvargs["is_hidden"]).__name__
                == FieldMetadata.__annotations__["is_hidden"]
            ):
                self_.is_hidden = kvargs["is_hidden"]
            else:
                self_.is_hidden = kvargs["is_hidden"]
        if "is_locked" in kvargs and kvargs["is_locked"] is not None:
            if (
                type(kvargs["is_locked"]).__name__
                == FieldMetadata.__annotations__["is_locked"]
            ):
                self_.is_locked = kvargs["is_locked"]
            else:
                self_.is_locked = kvargs["is_locked"]
        if "is_numeric" in kvargs and kvargs["is_numeric"] is not None:
            if (
                type(kvargs["is_numeric"]).__name__
                == FieldMetadata.__annotations__["is_numeric"]
            ):
                self_.is_numeric = kvargs["is_numeric"]
            else:
                self_.is_numeric = kvargs["is_numeric"]
        if "is_semantic" in kvargs and kvargs["is_semantic"] is not None:
            if (
                type(kvargs["is_semantic"]).__name__
                == FieldMetadata.__annotations__["is_semantic"]
            ):
                self_.is_semantic = kvargs["is_semantic"]
            else:
                self_.is_semantic = kvargs["is_semantic"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            if (
                type(kvargs["is_system"]).__name__
                == FieldMetadata.__annotations__["is_system"]
            ):
                self_.is_system = kvargs["is_system"]
            else:
                self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == FieldMetadata.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "src_tables" in kvargs and kvargs["src_tables"] is not None:
            if (
                type(kvargs["src_tables"]).__name__
                == FieldMetadata.__annotations__["src_tables"]
            ):
                self_.src_tables = kvargs["src_tables"]
            else:
                self_.src_tables = kvargs["src_tables"]
        if "tags" in kvargs and kvargs["tags"] is not None:
            if type(kvargs["tags"]).__name__ == FieldMetadata.__annotations__["tags"]:
                self_.tags = kvargs["tags"]
            else:
                self_.tags = kvargs["tags"]
        if "total_count" in kvargs and kvargs["total_count"] is not None:
            if (
                type(kvargs["total_count"]).__name__
                == FieldMetadata.__annotations__["total_count"]
            ):
                self_.total_count = kvargs["total_count"]
            else:
                self_.total_count = kvargs["total_count"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FileData:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FrequencyDistributionData:
    """

    Attributes
    ----------
    BinsEdges: list[float]
      Bins edges.
    Frequencies: list[int]
      Bins frequencies.
    NumberOfBins: int
      Number of bins.
    """

    BinsEdges: list[float] = None
    Frequencies: list[int] = None
    NumberOfBins: int = None

    def __init__(self_, **kvargs):

        if "BinsEdges" in kvargs and kvargs["BinsEdges"] is not None:
            if (
                type(kvargs["BinsEdges"]).__name__
                == FrequencyDistributionData.__annotations__["BinsEdges"]
            ):
                self_.BinsEdges = kvargs["BinsEdges"]
            else:
                self_.BinsEdges = kvargs["BinsEdges"]
        if "Frequencies" in kvargs and kvargs["Frequencies"] is not None:
            if (
                type(kvargs["Frequencies"]).__name__
                == FrequencyDistributionData.__annotations__["Frequencies"]
            ):
                self_.Frequencies = kvargs["Frequencies"]
            else:
                self_.Frequencies = kvargs["Frequencies"]
        if "NumberOfBins" in kvargs and kvargs["NumberOfBins"] is not None:
            if (
                type(kvargs["NumberOfBins"]).__name__
                == FrequencyDistributionData.__annotations__["NumberOfBins"]
            ):
                self_.NumberOfBins = kvargs["NumberOfBins"]
            else:
                self_.NumberOfBins = kvargs["NumberOfBins"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HardwareMeta:
    """

    Attributes
    ----------
    logical_cores: int
      Number of logical cores available.
    total_memory: int
      RAM available.
    """

    logical_cores: int = None
    total_memory: int = None

    def __init__(self_, **kvargs):

        if "logical_cores" in kvargs and kvargs["logical_cores"] is not None:
            if (
                type(kvargs["logical_cores"]).__name__
                == HardwareMeta.__annotations__["logical_cores"]
            ):
                self_.logical_cores = kvargs["logical_cores"]
            else:
                self_.logical_cores = kvargs["logical_cores"]
        if "total_memory" in kvargs and kvargs["total_memory"] is not None:
            if (
                type(kvargs["total_memory"]).__name__
                == HardwareMeta.__annotations__["total_memory"]
            ):
                self_.total_memory = kvargs["total_memory"]
            else:
                self_.total_memory = kvargs["total_memory"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class JsonObject:
    """
    Contains dynamic JSON data specified by the client.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LastReloadMetadata:
    """

    Attributes
    ----------
    cpu_time_spent_ms: int
      Number of CPU milliseconds it took to reload the app.
    hardware: HardwareMeta
    peak_memory_bytes: int
      Maximum number of bytes used during reload of the app.
    """

    cpu_time_spent_ms: int = None
    hardware: HardwareMeta = None
    peak_memory_bytes: int = None

    def __init__(self_, **kvargs):

        if "cpu_time_spent_ms" in kvargs and kvargs["cpu_time_spent_ms"] is not None:
            if (
                type(kvargs["cpu_time_spent_ms"]).__name__
                == LastReloadMetadata.__annotations__["cpu_time_spent_ms"]
            ):
                self_.cpu_time_spent_ms = kvargs["cpu_time_spent_ms"]
            else:
                self_.cpu_time_spent_ms = kvargs["cpu_time_spent_ms"]
        if "hardware" in kvargs and kvargs["hardware"] is not None:
            if (
                type(kvargs["hardware"]).__name__
                == LastReloadMetadata.__annotations__["hardware"]
            ):
                self_.hardware = kvargs["hardware"]
            else:
                self_.hardware = HardwareMeta(**kvargs["hardware"])
        if "peak_memory_bytes" in kvargs and kvargs["peak_memory_bytes"] is not None:
            if (
                type(kvargs["peak_memory_bytes"]).__name__
                == LastReloadMetadata.__annotations__["peak_memory_bytes"]
            ):
                self_.peak_memory_bytes = kvargs["peak_memory_bytes"]
            else:
                self_.peak_memory_bytes = kvargs["peak_memory_bytes"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LineageInfoRest:
    """

    Attributes
    ----------
    discriminator: str
      A string indicating the origin of the data:

      • [filename]: the data comes from a local file.

      • INLINE: the data is entered inline in the load script.

      • RESIDENT: the data comes from a resident table. The table name is listed.

      • AUTOGENERATE: the data is generated from the load script (no external table of data source).

      • Provider: the data comes from a data connection. The connector source name is listed.

      • [webfile]: the data comes from a web-based file.

      • STORE: path to QVD or TXT file where data is stored.

      • EXTENSION: the data comes from a Server Side Extension (SSE).
    statement: str
      The LOAD and SELECT script statements from the data load script.
    """

    discriminator: str = None
    statement: str = None

    def __init__(self_, **kvargs):

        if "discriminator" in kvargs and kvargs["discriminator"] is not None:
            if (
                type(kvargs["discriminator"]).__name__
                == LineageInfoRest.__annotations__["discriminator"]
            ):
                self_.discriminator = kvargs["discriminator"]
            else:
                self_.discriminator = kvargs["discriminator"]
        if "statement" in kvargs and kvargs["statement"] is not None:
            if (
                type(kvargs["statement"]).__name__
                == LineageInfoRest.__annotations__["statement"]
            ):
                self_.statement = kvargs["statement"]
            else:
                self_.statement = kvargs["statement"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Log:
    """

    Attributes
    ----------
    log: str
      Provides a link to download the log file.
    """

    log: str = None

    def __init__(self_, **kvargs):

        if "log" in kvargs and kvargs["log"] is not None:
            if type(kvargs["log"]).__name__ == Log.__annotations__["log"]:
                self_.log = kvargs["log"]
            else:
                self_.log = kvargs["log"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppCreatePrivileges:
    """

    Attributes
    ----------
    canCreate: bool
      Is set to true if the user has privileges to create the resource.
    resource: str
      Type of resource. For example, sheet, story, bookmark, etc.
    """

    canCreate: bool = None
    resource: str = None

    def __init__(self_, **kvargs):

        if "canCreate" in kvargs and kvargs["canCreate"] is not None:
            if (
                type(kvargs["canCreate"]).__name__
                == NxAppCreatePrivileges.__annotations__["canCreate"]
            ):
                self_.canCreate = kvargs["canCreate"]
            else:
                self_.canCreate = kvargs["canCreate"]
        if "resource" in kvargs and kvargs["resource"] is not None:
            if (
                type(kvargs["resource"]).__name__
                == NxAppCreatePrivileges.__annotations__["resource"]
            ):
                self_.resource = kvargs["resource"]
            else:
                self_.resource = kvargs["resource"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttributes:
    """
    App attributes. This structure can also contain extra user-defined attributes.

    Attributes
    ----------
    createdDate: str
      The date and time when the app was created.
    custom: JsonObject
      Contains dynamic JSON data specified by the client.
    description: str
      App description.
    dynamicColor: str
      The dynamic color of the app.
    encrypted: bool
      If set to true, the app is encrypted.
    hasSectionAccess: bool
      If set to true, the app has section access configured,
    id: str
      The App ID.
    isDirectQueryMode: bool
      True if the app is a Direct Query app, false if not
    lastReloadTime: str
      Date and time of the last reload of the app.
    modifiedDate: str
      The date and time when the app was modified.
    name: str
      App name.
    originAppId: str
      The Origin App ID for published apps.
    owner: str
      The owner of the app.
    ownerId: str
    publishTime: str
      The date and time when the app was published, empty if unpublished.
    published: bool
      True if the app is published on-prem, distributed in QCS, false if not.
    thumbnail: str
      App thumbnail.
    """

    createdDate: str = None
    custom: JsonObject = None
    description: str = None
    dynamicColor: str = None
    encrypted: bool = None
    hasSectionAccess: bool = None
    id: str = None
    isDirectQueryMode: bool = None
    lastReloadTime: str = None
    modifiedDate: str = None
    name: str = None
    originAppId: str = None
    owner: str = None
    ownerId: str = None
    publishTime: str = None
    published: bool = None
    thumbnail: str = None

    def __init__(self_, **kvargs):

        if "createdDate" in kvargs and kvargs["createdDate"] is not None:
            if (
                type(kvargs["createdDate"]).__name__
                == NxAttributes.__annotations__["createdDate"]
            ):
                self_.createdDate = kvargs["createdDate"]
            else:
                self_.createdDate = kvargs["createdDate"]
        if "custom" in kvargs and kvargs["custom"] is not None:
            if (
                type(kvargs["custom"]).__name__
                == NxAttributes.__annotations__["custom"]
            ):
                self_.custom = kvargs["custom"]
            else:
                self_.custom = JsonObject(**kvargs["custom"])
        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == NxAttributes.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "dynamicColor" in kvargs and kvargs["dynamicColor"] is not None:
            if (
                type(kvargs["dynamicColor"]).__name__
                == NxAttributes.__annotations__["dynamicColor"]
            ):
                self_.dynamicColor = kvargs["dynamicColor"]
            else:
                self_.dynamicColor = kvargs["dynamicColor"]
        if "encrypted" in kvargs and kvargs["encrypted"] is not None:
            if (
                type(kvargs["encrypted"]).__name__
                == NxAttributes.__annotations__["encrypted"]
            ):
                self_.encrypted = kvargs["encrypted"]
            else:
                self_.encrypted = kvargs["encrypted"]
        if "hasSectionAccess" in kvargs and kvargs["hasSectionAccess"] is not None:
            if (
                type(kvargs["hasSectionAccess"]).__name__
                == NxAttributes.__annotations__["hasSectionAccess"]
            ):
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
            else:
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == NxAttributes.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "isDirectQueryMode" in kvargs and kvargs["isDirectQueryMode"] is not None:
            if (
                type(kvargs["isDirectQueryMode"]).__name__
                == NxAttributes.__annotations__["isDirectQueryMode"]
            ):
                self_.isDirectQueryMode = kvargs["isDirectQueryMode"]
            else:
                self_.isDirectQueryMode = kvargs["isDirectQueryMode"]
        if "lastReloadTime" in kvargs and kvargs["lastReloadTime"] is not None:
            if (
                type(kvargs["lastReloadTime"]).__name__
                == NxAttributes.__annotations__["lastReloadTime"]
            ):
                self_.lastReloadTime = kvargs["lastReloadTime"]
            else:
                self_.lastReloadTime = kvargs["lastReloadTime"]
        if "modifiedDate" in kvargs and kvargs["modifiedDate"] is not None:
            if (
                type(kvargs["modifiedDate"]).__name__
                == NxAttributes.__annotations__["modifiedDate"]
            ):
                self_.modifiedDate = kvargs["modifiedDate"]
            else:
                self_.modifiedDate = kvargs["modifiedDate"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == NxAttributes.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "originAppId" in kvargs and kvargs["originAppId"] is not None:
            if (
                type(kvargs["originAppId"]).__name__
                == NxAttributes.__annotations__["originAppId"]
            ):
                self_.originAppId = kvargs["originAppId"]
            else:
                self_.originAppId = kvargs["originAppId"]
        if "owner" in kvargs and kvargs["owner"] is not None:
            if type(kvargs["owner"]).__name__ == NxAttributes.__annotations__["owner"]:
                self_.owner = kvargs["owner"]
            else:
                self_.owner = kvargs["owner"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            if (
                type(kvargs["ownerId"]).__name__
                == NxAttributes.__annotations__["ownerId"]
            ):
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "publishTime" in kvargs and kvargs["publishTime"] is not None:
            if (
                type(kvargs["publishTime"]).__name__
                == NxAttributes.__annotations__["publishTime"]
            ):
                self_.publishTime = kvargs["publishTime"]
            else:
                self_.publishTime = kvargs["publishTime"]
        if "published" in kvargs and kvargs["published"] is not None:
            if (
                type(kvargs["published"]).__name__
                == NxAttributes.__annotations__["published"]
            ):
                self_.published = kvargs["published"]
            else:
                self_.published = kvargs["published"]
        if "thumbnail" in kvargs and kvargs["thumbnail"] is not None:
            if (
                type(kvargs["thumbnail"]).__name__
                == NxAttributes.__annotations__["thumbnail"]
            ):
                self_.thumbnail = kvargs["thumbnail"]
            else:
                self_.thumbnail = kvargs["thumbnail"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PublishApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    data: str
      The published app will have data from source or target app.
      The default is source.


      • source: Publish with source data

      • target: Publish with target data
    spaceId: str
      The managed space ID where the app will be published.
    """

    attributes: AppUpdateAttributes = None
    data: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):

        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == PublishApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        if "data" in kvargs and kvargs["data"] is not None:
            if type(kvargs["data"]).__name__ == PublishApp.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            if (
                type(kvargs["spaceId"]).__name__
                == PublishApp.__annotations__["spaceId"]
            ):
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RepublishApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    checkOriginAppId: bool
      Validate that source app is same as originally published.
    data: str
      The republished app will have data from source or target app.
      The default is source.


      • source: Publish with source data

      • target: Publish with target data
    targetId: str
      The target ID to be republished.
    """

    attributes: AppUpdateAttributes = None
    checkOriginAppId: bool = True
    data: str = None
    targetId: str = None

    def __init__(self_, **kvargs):

        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == RepublishApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        if "checkOriginAppId" in kvargs and kvargs["checkOriginAppId"] is not None:
            if (
                type(kvargs["checkOriginAppId"]).__name__
                == RepublishApp.__annotations__["checkOriginAppId"]
            ):
                self_.checkOriginAppId = kvargs["checkOriginAppId"]
            else:
                self_.checkOriginAppId = kvargs["checkOriginAppId"]
        if "data" in kvargs and kvargs["data"] is not None:
            if type(kvargs["data"]).__name__ == RepublishApp.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]
        if "targetId" in kvargs and kvargs["targetId"] is not None:
            if (
                type(kvargs["targetId"]).__name__
                == RepublishApp.__annotations__["targetId"]
            ):
                self_.targetId = kvargs["targetId"]
            else:
                self_.targetId = kvargs["targetId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptLogList:
    """

    Attributes
    ----------
    data: list[ScriptLogMeta]
      Array of scriptLogMeta.
    """

    data: list[ScriptLogMeta] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == ScriptLogList.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ScriptLogMeta(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptLogMeta:
    """

    Attributes
    ----------
    duration: int
      Duration of reload (ms).
    endTime: str
      Time when reload ended.
    links: Log
    reloadId: str
      Reload identifier.
    success: bool
      True if the reload was successful.
    """

    duration: int = None
    endTime: str = None
    links: Log = None
    reloadId: str = None
    success: bool = None

    def __init__(self_, **kvargs):

        if "duration" in kvargs and kvargs["duration"] is not None:
            if (
                type(kvargs["duration"]).__name__
                == ScriptLogMeta.__annotations__["duration"]
            ):
                self_.duration = kvargs["duration"]
            else:
                self_.duration = kvargs["duration"]
        if "endTime" in kvargs and kvargs["endTime"] is not None:
            if (
                type(kvargs["endTime"]).__name__
                == ScriptLogMeta.__annotations__["endTime"]
            ):
                self_.endTime = kvargs["endTime"]
            else:
                self_.endTime = kvargs["endTime"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == ScriptLogMeta.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = Log(**kvargs["links"])
        if "reloadId" in kvargs and kvargs["reloadId"] is not None:
            if (
                type(kvargs["reloadId"]).__name__
                == ScriptLogMeta.__annotations__["reloadId"]
            ):
                self_.reloadId = kvargs["reloadId"]
            else:
                self_.reloadId = kvargs["reloadId"]
        if "success" in kvargs and kvargs["success"] is not None:
            if (
                type(kvargs["success"]).__name__
                == ScriptLogMeta.__annotations__["success"]
            ):
                self_.success = kvargs["success"]
            else:
                self_.success = kvargs["success"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolFrequency:
    """

    Attributes
    ----------
    Frequency: int
      Frequency of the above symbol in the field
    Symbol: SymbolValue
    """

    Frequency: int = None
    Symbol: SymbolValue = None

    def __init__(self_, **kvargs):

        if "Frequency" in kvargs and kvargs["Frequency"] is not None:
            if (
                type(kvargs["Frequency"]).__name__
                == SymbolFrequency.__annotations__["Frequency"]
            ):
                self_.Frequency = kvargs["Frequency"]
            else:
                self_.Frequency = kvargs["Frequency"]
        if "Symbol" in kvargs and kvargs["Symbol"] is not None:
            if (
                type(kvargs["Symbol"]).__name__
                == SymbolFrequency.__annotations__["Symbol"]
            ):
                self_.Symbol = kvargs["Symbol"]
            else:
                self_.Symbol = SymbolValue(**kvargs["Symbol"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolValue:
    """

    Attributes
    ----------
    Number: float
      Numeric value of the symbol. NaN otherwise.
    Text: str
      String value of the symbol. This parameter is optional and present only if Symbol is a string.
    """

    Number: float = None
    Text: str = None

    def __init__(self_, **kvargs):

        if "Number" in kvargs and kvargs["Number"] is not None:
            if type(kvargs["Number"]).__name__ == SymbolValue.__annotations__["Number"]:
                self_.Number = kvargs["Number"]
            else:
                self_.Number = kvargs["Number"]
        if "Text" in kvargs and kvargs["Text"] is not None:
            if type(kvargs["Text"]).__name__ == SymbolValue.__annotations__["Text"]:
                self_.Text = kvargs["Text"]
            else:
                self_.Text = kvargs["Text"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableMetadata:
    """

    Attributes
    ----------
    byte_size: int
      Static RAM memory used in bytes.
    comment: str
      Table comment.
    is_loose: bool
      If set to true, the table is loose due to circular connection.
      The default value is false.
    is_semantic: bool
      If set to true, the table is semantic.
      The default value is false.
    is_system: bool
      If set to true, the table is a system table.
      The default value is false.
    name: str
      Name of the table.
    no_of_fields: int
      Number of fields.
    no_of_key_fields: int
      Number of key fields.
    no_of_rows: int
      Number of rows.
    """

    byte_size: int = None
    comment: str = None
    is_loose: bool = None
    is_semantic: bool = None
    is_system: bool = None
    name: str = None
    no_of_fields: int = None
    no_of_key_fields: int = None
    no_of_rows: int = None

    def __init__(self_, **kvargs):

        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            if (
                type(kvargs["byte_size"]).__name__
                == TableMetadata.__annotations__["byte_size"]
            ):
                self_.byte_size = kvargs["byte_size"]
            else:
                self_.byte_size = kvargs["byte_size"]
        if "comment" in kvargs and kvargs["comment"] is not None:
            if (
                type(kvargs["comment"]).__name__
                == TableMetadata.__annotations__["comment"]
            ):
                self_.comment = kvargs["comment"]
            else:
                self_.comment = kvargs["comment"]
        if "is_loose" in kvargs and kvargs["is_loose"] is not None:
            if (
                type(kvargs["is_loose"]).__name__
                == TableMetadata.__annotations__["is_loose"]
            ):
                self_.is_loose = kvargs["is_loose"]
            else:
                self_.is_loose = kvargs["is_loose"]
        if "is_semantic" in kvargs and kvargs["is_semantic"] is not None:
            if (
                type(kvargs["is_semantic"]).__name__
                == TableMetadata.__annotations__["is_semantic"]
            ):
                self_.is_semantic = kvargs["is_semantic"]
            else:
                self_.is_semantic = kvargs["is_semantic"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            if (
                type(kvargs["is_system"]).__name__
                == TableMetadata.__annotations__["is_system"]
            ):
                self_.is_system = kvargs["is_system"]
            else:
                self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == TableMetadata.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "no_of_fields" in kvargs and kvargs["no_of_fields"] is not None:
            if (
                type(kvargs["no_of_fields"]).__name__
                == TableMetadata.__annotations__["no_of_fields"]
            ):
                self_.no_of_fields = kvargs["no_of_fields"]
            else:
                self_.no_of_fields = kvargs["no_of_fields"]
        if "no_of_key_fields" in kvargs and kvargs["no_of_key_fields"] is not None:
            if (
                type(kvargs["no_of_key_fields"]).__name__
                == TableMetadata.__annotations__["no_of_key_fields"]
            ):
                self_.no_of_key_fields = kvargs["no_of_key_fields"]
            else:
                self_.no_of_key_fields = kvargs["no_of_key_fields"]
        if "no_of_rows" in kvargs and kvargs["no_of_rows"] is not None:
            if (
                type(kvargs["no_of_rows"]).__name__
                == TableMetadata.__annotations__["no_of_rows"]
            ):
                self_.no_of_rows = kvargs["no_of_rows"]
            else:
                self_.no_of_rows = kvargs["no_of_rows"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableProfilingData:
    """

    Attributes
    ----------
    FieldProfiling: list[FieldInTableProfilingData]
      Field values profiling info
    NoOfRows: int
      Number of rows in the table.
    """

    FieldProfiling: list[FieldInTableProfilingData] = None
    NoOfRows: int = None

    def __init__(self_, **kvargs):

        if "FieldProfiling" in kvargs and kvargs["FieldProfiling"] is not None:
            if (
                len(kvargs["FieldProfiling"]) > 0
                and f"list[{type(kvargs['FieldProfiling'][0]).__name__}]"
                == TableProfilingData.__annotations__["FieldProfiling"]
            ):
                self_.FieldProfiling = kvargs["FieldProfiling"]
            else:
                self_.FieldProfiling = [
                    FieldInTableProfilingData(**e) for e in kvargs["FieldProfiling"]
                ]
        if "NoOfRows" in kvargs and kvargs["NoOfRows"] is not None:
            if (
                type(kvargs["NoOfRows"]).__name__
                == TableProfilingData.__annotations__["NoOfRows"]
            ):
                self_.NoOfRows = kvargs["NoOfRows"]
            else:
                self_.NoOfRows = kvargs["NoOfRows"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    """

    attributes: AppUpdateAttributes = None

    def __init__(self_, **kvargs):

        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == UpdateApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateOwner:
    """

    Attributes
    ----------
    ownerId: str
    """

    ownerId: str = None

    def __init__(self_, **kvargs):

        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            if (
                type(kvargs["ownerId"]).__name__
                == UpdateOwner.__annotations__["ownerId"]
            ):
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateSpace:
    """

    Attributes
    ----------
    spaceId: str
    """

    spaceId: str = None

    def __init__(self_, **kvargs):

        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            if (
                type(kvargs["spaceId"]).__name__
                == UpdateSpace.__annotations__["spaceId"]
            ):
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Cmpbool:
    """

    Attributes
    ----------
    absoluteDiff: float
    diff: float
    trend: str
    baseline: bool
    comparison: bool
    """

    absoluteDiff: float = None
    diff: float = None
    trend: str = None
    baseline: bool = None
    comparison: bool = None

    def __init__(self_, **kvargs):

        if "absoluteDiff" in kvargs and kvargs["absoluteDiff"] is not None:
            if (
                type(kvargs["absoluteDiff"]).__name__
                == Cmpbool.__annotations__["absoluteDiff"]
            ):
                self_.absoluteDiff = kvargs["absoluteDiff"]
            else:
                self_.absoluteDiff = kvargs["absoluteDiff"]
        if "diff" in kvargs and kvargs["diff"] is not None:
            if type(kvargs["diff"]).__name__ == Cmpbool.__annotations__["diff"]:
                self_.diff = kvargs["diff"]
            else:
                self_.diff = kvargs["diff"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            if type(kvargs["trend"]).__name__ == Cmpbool.__annotations__["trend"]:
                self_.trend = kvargs["trend"]
            else:
                self_.trend = kvargs["trend"]
        if "baseline" in kvargs and kvargs["baseline"] is not None:
            if type(kvargs["baseline"]).__name__ == Cmpbool.__annotations__["baseline"]:
                self_.baseline = kvargs["baseline"]
            else:
                self_.baseline = kvargs["baseline"]
        if "comparison" in kvargs and kvargs["comparison"] is not None:
            if (
                type(kvargs["comparison"]).__name__
                == Cmpbool.__annotations__["comparison"]
            ):
                self_.comparison = kvargs["comparison"]
            else:
                self_.comparison = kvargs["comparison"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Cmpfloat:
    """

    Attributes
    ----------
    absoluteDiff: float
    diff: float
    trend: str
    baseline: float
    comparison: float
    """

    absoluteDiff: float = None
    diff: float = None
    trend: str = None
    baseline: float = None
    comparison: float = None

    def __init__(self_, **kvargs):

        if "absoluteDiff" in kvargs and kvargs["absoluteDiff"] is not None:
            if (
                type(kvargs["absoluteDiff"]).__name__
                == Cmpfloat.__annotations__["absoluteDiff"]
            ):
                self_.absoluteDiff = kvargs["absoluteDiff"]
            else:
                self_.absoluteDiff = kvargs["absoluteDiff"]
        if "diff" in kvargs and kvargs["diff"] is not None:
            if type(kvargs["diff"]).__name__ == Cmpfloat.__annotations__["diff"]:
                self_.diff = kvargs["diff"]
            else:
                self_.diff = kvargs["diff"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            if type(kvargs["trend"]).__name__ == Cmpfloat.__annotations__["trend"]:
                self_.trend = kvargs["trend"]
            else:
                self_.trend = kvargs["trend"]
        if "baseline" in kvargs and kvargs["baseline"] is not None:
            if (
                type(kvargs["baseline"]).__name__
                == Cmpfloat.__annotations__["baseline"]
            ):
                self_.baseline = kvargs["baseline"]
            else:
                self_.baseline = kvargs["baseline"]
        if "comparison" in kvargs and kvargs["comparison"] is not None:
            if (
                type(kvargs["comparison"]).__name__
                == Cmpfloat.__annotations__["comparison"]
            ):
                self_.comparison = kvargs["comparison"]
            else:
                self_.comparison = kvargs["comparison"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Cmpint:
    """

    Attributes
    ----------
    absoluteDiff: float
    diff: float
    trend: str
    baseline: float
    comparison: float
    """

    absoluteDiff: float = None
    diff: float = None
    trend: str = None
    baseline: float = None
    comparison: float = None

    def __init__(self_, **kvargs):

        if "absoluteDiff" in kvargs and kvargs["absoluteDiff"] is not None:
            if (
                type(kvargs["absoluteDiff"]).__name__
                == Cmpint.__annotations__["absoluteDiff"]
            ):
                self_.absoluteDiff = kvargs["absoluteDiff"]
            else:
                self_.absoluteDiff = kvargs["absoluteDiff"]
        if "diff" in kvargs and kvargs["diff"] is not None:
            if type(kvargs["diff"]).__name__ == Cmpint.__annotations__["diff"]:
                self_.diff = kvargs["diff"]
            else:
                self_.diff = kvargs["diff"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            if type(kvargs["trend"]).__name__ == Cmpint.__annotations__["trend"]:
                self_.trend = kvargs["trend"]
            else:
                self_.trend = kvargs["trend"]
        if "baseline" in kvargs and kvargs["baseline"] is not None:
            if type(kvargs["baseline"]).__name__ == Cmpint.__annotations__["baseline"]:
                self_.baseline = kvargs["baseline"]
            else:
                self_.baseline = kvargs["baseline"]
        if "comparison" in kvargs and kvargs["comparison"] is not None:
            if (
                type(kvargs["comparison"]).__name__
                == Cmpint.__annotations__["comparison"]
            ):
                self_.comparison = kvargs["comparison"]
            else:
                self_.comparison = kvargs["comparison"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Comparison:
    """

    Attributes
    ----------
    appOpenTimeSeconds: Cmpfloat
    dataModelSizeMib: Cmpfloat
    documentSizeMib: Cmpfloat
    fileSizeMib: Cmpfloat
    hasSectionAccess: Cmpbool
    maxMemoryMib: Cmpfloat
    objHeavy: Sortedcomparisonoobjheavy
    objNoCache: Sortedcomparisonobjresponsetime
    objSingleThreaded: Sortedcomparisonobjresponsetime
    objSlowCached: Sortedcomparisonobjresponsetime
    objSlowUncached: Sortedcomparisonobjresponsetime
    objectCount: Cmpint
    rowCount: Cmpint
    sheetCount: Cmpint
    sheetsCached: Sortedcomparisonobjresponsetime
    sheetsUncached: Sortedcomparisonobjresponsetime
    topFieldsByBytes: Sortedcomparisonfields
    topTablesByBytes: Sortedcomparisontables
    """

    appOpenTimeSeconds: Cmpfloat = None
    dataModelSizeMib: Cmpfloat = None
    documentSizeMib: Cmpfloat = None
    fileSizeMib: Cmpfloat = None
    hasSectionAccess: Cmpbool = None
    maxMemoryMib: Cmpfloat = None
    objHeavy: Sortedcomparisonoobjheavy = None
    objNoCache: Sortedcomparisonobjresponsetime = None
    objSingleThreaded: Sortedcomparisonobjresponsetime = None
    objSlowCached: Sortedcomparisonobjresponsetime = None
    objSlowUncached: Sortedcomparisonobjresponsetime = None
    objectCount: Cmpint = None
    rowCount: Cmpint = None
    sheetCount: Cmpint = None
    sheetsCached: Sortedcomparisonobjresponsetime = None
    sheetsUncached: Sortedcomparisonobjresponsetime = None
    topFieldsByBytes: Sortedcomparisonfields = None
    topTablesByBytes: Sortedcomparisontables = None

    def __init__(self_, **kvargs):

        if "appOpenTimeSeconds" in kvargs and kvargs["appOpenTimeSeconds"] is not None:
            if (
                type(kvargs["appOpenTimeSeconds"]).__name__
                == Comparison.__annotations__["appOpenTimeSeconds"]
            ):
                self_.appOpenTimeSeconds = kvargs["appOpenTimeSeconds"]
            else:
                self_.appOpenTimeSeconds = Cmpfloat(**kvargs["appOpenTimeSeconds"])
        if "dataModelSizeMib" in kvargs and kvargs["dataModelSizeMib"] is not None:
            if (
                type(kvargs["dataModelSizeMib"]).__name__
                == Comparison.__annotations__["dataModelSizeMib"]
            ):
                self_.dataModelSizeMib = kvargs["dataModelSizeMib"]
            else:
                self_.dataModelSizeMib = Cmpfloat(**kvargs["dataModelSizeMib"])
        if "documentSizeMib" in kvargs and kvargs["documentSizeMib"] is not None:
            if (
                type(kvargs["documentSizeMib"]).__name__
                == Comparison.__annotations__["documentSizeMib"]
            ):
                self_.documentSizeMib = kvargs["documentSizeMib"]
            else:
                self_.documentSizeMib = Cmpfloat(**kvargs["documentSizeMib"])
        if "fileSizeMib" in kvargs and kvargs["fileSizeMib"] is not None:
            if (
                type(kvargs["fileSizeMib"]).__name__
                == Comparison.__annotations__["fileSizeMib"]
            ):
                self_.fileSizeMib = kvargs["fileSizeMib"]
            else:
                self_.fileSizeMib = Cmpfloat(**kvargs["fileSizeMib"])
        if "hasSectionAccess" in kvargs and kvargs["hasSectionAccess"] is not None:
            if (
                type(kvargs["hasSectionAccess"]).__name__
                == Comparison.__annotations__["hasSectionAccess"]
            ):
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
            else:
                self_.hasSectionAccess = Cmpbool(**kvargs["hasSectionAccess"])
        if "maxMemoryMib" in kvargs and kvargs["maxMemoryMib"] is not None:
            if (
                type(kvargs["maxMemoryMib"]).__name__
                == Comparison.__annotations__["maxMemoryMib"]
            ):
                self_.maxMemoryMib = kvargs["maxMemoryMib"]
            else:
                self_.maxMemoryMib = Cmpfloat(**kvargs["maxMemoryMib"])
        if "objHeavy" in kvargs and kvargs["objHeavy"] is not None:
            if (
                type(kvargs["objHeavy"]).__name__
                == Comparison.__annotations__["objHeavy"]
            ):
                self_.objHeavy = kvargs["objHeavy"]
            else:
                self_.objHeavy = Sortedcomparisonoobjheavy(**kvargs["objHeavy"])
        if "objNoCache" in kvargs and kvargs["objNoCache"] is not None:
            if (
                type(kvargs["objNoCache"]).__name__
                == Comparison.__annotations__["objNoCache"]
            ):
                self_.objNoCache = kvargs["objNoCache"]
            else:
                self_.objNoCache = Sortedcomparisonobjresponsetime(
                    **kvargs["objNoCache"]
                )
        if "objSingleThreaded" in kvargs and kvargs["objSingleThreaded"] is not None:
            if (
                type(kvargs["objSingleThreaded"]).__name__
                == Comparison.__annotations__["objSingleThreaded"]
            ):
                self_.objSingleThreaded = kvargs["objSingleThreaded"]
            else:
                self_.objSingleThreaded = Sortedcomparisonobjresponsetime(
                    **kvargs["objSingleThreaded"]
                )
        if "objSlowCached" in kvargs and kvargs["objSlowCached"] is not None:
            if (
                type(kvargs["objSlowCached"]).__name__
                == Comparison.__annotations__["objSlowCached"]
            ):
                self_.objSlowCached = kvargs["objSlowCached"]
            else:
                self_.objSlowCached = Sortedcomparisonobjresponsetime(
                    **kvargs["objSlowCached"]
                )
        if "objSlowUncached" in kvargs and kvargs["objSlowUncached"] is not None:
            if (
                type(kvargs["objSlowUncached"]).__name__
                == Comparison.__annotations__["objSlowUncached"]
            ):
                self_.objSlowUncached = kvargs["objSlowUncached"]
            else:
                self_.objSlowUncached = Sortedcomparisonobjresponsetime(
                    **kvargs["objSlowUncached"]
                )
        if "objectCount" in kvargs and kvargs["objectCount"] is not None:
            if (
                type(kvargs["objectCount"]).__name__
                == Comparison.__annotations__["objectCount"]
            ):
                self_.objectCount = kvargs["objectCount"]
            else:
                self_.objectCount = Cmpint(**kvargs["objectCount"])
        if "rowCount" in kvargs and kvargs["rowCount"] is not None:
            if (
                type(kvargs["rowCount"]).__name__
                == Comparison.__annotations__["rowCount"]
            ):
                self_.rowCount = kvargs["rowCount"]
            else:
                self_.rowCount = Cmpint(**kvargs["rowCount"])
        if "sheetCount" in kvargs and kvargs["sheetCount"] is not None:
            if (
                type(kvargs["sheetCount"]).__name__
                == Comparison.__annotations__["sheetCount"]
            ):
                self_.sheetCount = kvargs["sheetCount"]
            else:
                self_.sheetCount = Cmpint(**kvargs["sheetCount"])
        if "sheetsCached" in kvargs and kvargs["sheetsCached"] is not None:
            if (
                type(kvargs["sheetsCached"]).__name__
                == Comparison.__annotations__["sheetsCached"]
            ):
                self_.sheetsCached = kvargs["sheetsCached"]
            else:
                self_.sheetsCached = Sortedcomparisonobjresponsetime(
                    **kvargs["sheetsCached"]
                )
        if "sheetsUncached" in kvargs and kvargs["sheetsUncached"] is not None:
            if (
                type(kvargs["sheetsUncached"]).__name__
                == Comparison.__annotations__["sheetsUncached"]
            ):
                self_.sheetsUncached = kvargs["sheetsUncached"]
            else:
                self_.sheetsUncached = Sortedcomparisonobjresponsetime(
                    **kvargs["sheetsUncached"]
                )
        if "topFieldsByBytes" in kvargs and kvargs["topFieldsByBytes"] is not None:
            if (
                type(kvargs["topFieldsByBytes"]).__name__
                == Comparison.__annotations__["topFieldsByBytes"]
            ):
                self_.topFieldsByBytes = kvargs["topFieldsByBytes"]
            else:
                self_.topFieldsByBytes = Sortedcomparisonfields(
                    **kvargs["topFieldsByBytes"]
                )
        if "topTablesByBytes" in kvargs and kvargs["topTablesByBytes"] is not None:
            if (
                type(kvargs["topTablesByBytes"]).__name__
                == Comparison.__annotations__["topTablesByBytes"]
            ):
                self_.topTablesByBytes = kvargs["topTablesByBytes"]
            else:
                self_.topTablesByBytes = Sortedcomparisontables(
                    **kvargs["topTablesByBytes"]
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Evaluation:
    """

    Attributes
    ----------
    appId: str
    appItemId: str
    appName: str
    details: EvaluationDetails
    ended: str
    events: list[Event]
    id: str
    metadata: Metadata
    result: Result
    sheetId: str
    sheetTitle: str
    started: str
    status: str
    tenantId: str
    timestamp: str
    version: float
    """

    appId: str = None
    appItemId: str = None
    appName: str = None
    details: EvaluationDetails = None
    ended: str = None
    events: list[Event] = None
    id: str = None
    metadata: Metadata = None
    result: Result = None
    sheetId: str = None
    sheetTitle: str = None
    started: str = None
    status: str = None
    tenantId: str = None
    timestamp: str = None
    version: float = None

    def __init__(self_, **kvargs):

        if "appId" in kvargs and kvargs["appId"] is not None:
            if type(kvargs["appId"]).__name__ == Evaluation.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "appItemId" in kvargs and kvargs["appItemId"] is not None:
            if (
                type(kvargs["appItemId"]).__name__
                == Evaluation.__annotations__["appItemId"]
            ):
                self_.appItemId = kvargs["appItemId"]
            else:
                self_.appItemId = kvargs["appItemId"]
        if "appName" in kvargs and kvargs["appName"] is not None:
            if (
                type(kvargs["appName"]).__name__
                == Evaluation.__annotations__["appName"]
            ):
                self_.appName = kvargs["appName"]
            else:
                self_.appName = kvargs["appName"]
        if "details" in kvargs and kvargs["details"] is not None:
            if (
                type(kvargs["details"]).__name__
                == Evaluation.__annotations__["details"]
            ):
                self_.details = kvargs["details"]
            else:
                self_.details = EvaluationDetails(**kvargs["details"])
        if "ended" in kvargs and kvargs["ended"] is not None:
            if type(kvargs["ended"]).__name__ == Evaluation.__annotations__["ended"]:
                self_.ended = kvargs["ended"]
            else:
                self_.ended = kvargs["ended"]
        if "events" in kvargs and kvargs["events"] is not None:
            if (
                len(kvargs["events"]) > 0
                and f"list[{type(kvargs['events'][0]).__name__}]"
                == Evaluation.__annotations__["events"]
            ):
                self_.events = kvargs["events"]
            else:
                self_.events = [Event(**e) for e in kvargs["events"]]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == Evaluation.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "metadata" in kvargs and kvargs["metadata"] is not None:
            if (
                type(kvargs["metadata"]).__name__
                == Evaluation.__annotations__["metadata"]
            ):
                self_.metadata = kvargs["metadata"]
            else:
                self_.metadata = Metadata(**kvargs["metadata"])
        if "result" in kvargs and kvargs["result"] is not None:
            if type(kvargs["result"]).__name__ == Evaluation.__annotations__["result"]:
                self_.result = kvargs["result"]
            else:
                self_.result = Result(**kvargs["result"])
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            if (
                type(kvargs["sheetId"]).__name__
                == Evaluation.__annotations__["sheetId"]
            ):
                self_.sheetId = kvargs["sheetId"]
            else:
                self_.sheetId = kvargs["sheetId"]
        if "sheetTitle" in kvargs and kvargs["sheetTitle"] is not None:
            if (
                type(kvargs["sheetTitle"]).__name__
                == Evaluation.__annotations__["sheetTitle"]
            ):
                self_.sheetTitle = kvargs["sheetTitle"]
            else:
                self_.sheetTitle = kvargs["sheetTitle"]
        if "started" in kvargs and kvargs["started"] is not None:
            if (
                type(kvargs["started"]).__name__
                == Evaluation.__annotations__["started"]
            ):
                self_.started = kvargs["started"]
            else:
                self_.started = kvargs["started"]
        if "status" in kvargs and kvargs["status"] is not None:
            if type(kvargs["status"]).__name__ == Evaluation.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if (
                type(kvargs["tenantId"]).__name__
                == Evaluation.__annotations__["tenantId"]
            ):
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "timestamp" in kvargs and kvargs["timestamp"] is not None:
            if (
                type(kvargs["timestamp"]).__name__
                == Evaluation.__annotations__["timestamp"]
            ):
                self_.timestamp = kvargs["timestamp"]
            else:
                self_.timestamp = kvargs["timestamp"]
        if "version" in kvargs and kvargs["version"] is not None:
            if (
                type(kvargs["version"]).__name__
                == Evaluation.__annotations__["version"]
            ):
                self_.version = kvargs["version"]
            else:
                self_.version = kvargs["version"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def download(self) -> Evaluation:
        """
        Download a detailed XML log of a specific evaluation
        Find and download an evaluation log by a specific evaluation id.


        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/evaluations/{id}/actions/download".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )
        obj = Evaluation(**response.json())
        obj.auth = self.auth
        return obj


@dataclass
class EvaluationDetails:
    """

    Attributes
    ----------
    concurrentReload: bool
    dedicated: bool
    engineHasCache: bool
    errors: list[str]
    objectMetrics: object
    warnings: list[str]
    """

    concurrentReload: bool = None
    dedicated: bool = None
    engineHasCache: bool = None
    errors: list[str] = None
    objectMetrics: object = None
    warnings: list[str] = None

    def __init__(self_, **kvargs):

        if "concurrentReload" in kvargs and kvargs["concurrentReload"] is not None:
            if (
                type(kvargs["concurrentReload"]).__name__
                == EvaluationDetails.__annotations__["concurrentReload"]
            ):
                self_.concurrentReload = kvargs["concurrentReload"]
            else:
                self_.concurrentReload = kvargs["concurrentReload"]
        if "dedicated" in kvargs and kvargs["dedicated"] is not None:
            if (
                type(kvargs["dedicated"]).__name__
                == EvaluationDetails.__annotations__["dedicated"]
            ):
                self_.dedicated = kvargs["dedicated"]
            else:
                self_.dedicated = kvargs["dedicated"]
        if "engineHasCache" in kvargs and kvargs["engineHasCache"] is not None:
            if (
                type(kvargs["engineHasCache"]).__name__
                == EvaluationDetails.__annotations__["engineHasCache"]
            ):
                self_.engineHasCache = kvargs["engineHasCache"]
            else:
                self_.engineHasCache = kvargs["engineHasCache"]
        if "errors" in kvargs and kvargs["errors"] is not None:
            if (
                type(kvargs["errors"]).__name__
                == EvaluationDetails.__annotations__["errors"]
            ):
                self_.errors = kvargs["errors"]
            else:
                self_.errors = kvargs["errors"]
        if "objectMetrics" in kvargs and kvargs["objectMetrics"] is not None:
            if (
                type(kvargs["objectMetrics"]).__name__
                == EvaluationDetails.__annotations__["objectMetrics"]
            ):
                self_.objectMetrics = kvargs["objectMetrics"]
            else:
                self_.objectMetrics = kvargs["objectMetrics"]
        if "warnings" in kvargs and kvargs["warnings"] is not None:
            if (
                type(kvargs["warnings"]).__name__
                == EvaluationDetails.__annotations__["warnings"]
            ):
                self_.warnings = kvargs["warnings"]
            else:
                self_.warnings = kvargs["warnings"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Evaluations:
    """

    Attributes
    ----------
    data: list[Evaluation]
    links: EvaluationsLinks
    """

    data: list[Evaluation] = None
    links: EvaluationsLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == Evaluations.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Evaluation(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Evaluations.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = EvaluationsLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EvaluationsLinks:
    """

    Attributes
    ----------
    next: EvaluationsLinksNext
    prev: EvaluationsLinksPrev
    """

    next: EvaluationsLinksNext = None
    prev: EvaluationsLinksPrev = None

    def __init__(self_, **kvargs):

        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == EvaluationsLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = EvaluationsLinksNext(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == EvaluationsLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = EvaluationsLinksPrev(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EvaluationsLinksNext:
    """

    Attributes
    ----------
    href: str
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if (
                type(kvargs["href"]).__name__
                == EvaluationsLinksNext.__annotations__["href"]
            ):
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EvaluationsLinksPrev:
    """

    Attributes
    ----------
    href: str
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if (
                type(kvargs["href"]).__name__
                == EvaluationsLinksPrev.__annotations__["href"]
            ):
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Event:
    """

    Attributes
    ----------
    details: str
    errorCode: str
    objectId: str
    objectTitle: str
    objectType: str
    objectVisualization: str
    severity: str
    sheetId: str
    sheetTitle: str
    """

    details: str = None
    errorCode: str = None
    objectId: str = None
    objectTitle: str = None
    objectType: str = None
    objectVisualization: str = None
    severity: str = None
    sheetId: str = None
    sheetTitle: str = None

    def __init__(self_, **kvargs):

        if "details" in kvargs and kvargs["details"] is not None:
            if type(kvargs["details"]).__name__ == Event.__annotations__["details"]:
                self_.details = kvargs["details"]
            else:
                self_.details = kvargs["details"]
        if "errorCode" in kvargs and kvargs["errorCode"] is not None:
            if type(kvargs["errorCode"]).__name__ == Event.__annotations__["errorCode"]:
                self_.errorCode = kvargs["errorCode"]
            else:
                self_.errorCode = kvargs["errorCode"]
        if "objectId" in kvargs and kvargs["objectId"] is not None:
            if type(kvargs["objectId"]).__name__ == Event.__annotations__["objectId"]:
                self_.objectId = kvargs["objectId"]
            else:
                self_.objectId = kvargs["objectId"]
        if "objectTitle" in kvargs and kvargs["objectTitle"] is not None:
            if (
                type(kvargs["objectTitle"]).__name__
                == Event.__annotations__["objectTitle"]
            ):
                self_.objectTitle = kvargs["objectTitle"]
            else:
                self_.objectTitle = kvargs["objectTitle"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            if (
                type(kvargs["objectType"]).__name__
                == Event.__annotations__["objectType"]
            ):
                self_.objectType = kvargs["objectType"]
            else:
                self_.objectType = kvargs["objectType"]
        if (
            "objectVisualization" in kvargs
            and kvargs["objectVisualization"] is not None
        ):
            if (
                type(kvargs["objectVisualization"]).__name__
                == Event.__annotations__["objectVisualization"]
            ):
                self_.objectVisualization = kvargs["objectVisualization"]
            else:
                self_.objectVisualization = kvargs["objectVisualization"]
        if "severity" in kvargs and kvargs["severity"] is not None:
            if type(kvargs["severity"]).__name__ == Event.__annotations__["severity"]:
                self_.severity = kvargs["severity"]
            else:
                self_.severity = kvargs["severity"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            if type(kvargs["sheetId"]).__name__ == Event.__annotations__["sheetId"]:
                self_.sheetId = kvargs["sheetId"]
            else:
                self_.sheetId = kvargs["sheetId"]
        if "sheetTitle" in kvargs and kvargs["sheetTitle"] is not None:
            if (
                type(kvargs["sheetTitle"]).__name__
                == Event.__annotations__["sheetTitle"]
            ):
                self_.sheetTitle = kvargs["sheetTitle"]
            else:
                self_.sheetTitle = kvargs["sheetTitle"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Metadata:
    """

    Attributes
    ----------
    amountofcardinalfieldvalues: float
    amountoffields: float
    amountoffieldvalues: float
    amountofrows: float
    amountoftables: float
    hassectionaccess: bool
    reloadmeta: MetadataReloadmeta
    staticbytesize: float
    """

    amountofcardinalfieldvalues: float = None
    amountoffields: float = None
    amountoffieldvalues: float = None
    amountofrows: float = None
    amountoftables: float = None
    hassectionaccess: bool = None
    reloadmeta: MetadataReloadmeta = None
    staticbytesize: float = None

    def __init__(self_, **kvargs):

        if (
            "amountofcardinalfieldvalues" in kvargs
            and kvargs["amountofcardinalfieldvalues"] is not None
        ):
            if (
                type(kvargs["amountofcardinalfieldvalues"]).__name__
                == Metadata.__annotations__["amountofcardinalfieldvalues"]
            ):
                self_.amountofcardinalfieldvalues = kvargs[
                    "amountofcardinalfieldvalues"
                ]
            else:
                self_.amountofcardinalfieldvalues = kvargs[
                    "amountofcardinalfieldvalues"
                ]
        if "amountoffields" in kvargs and kvargs["amountoffields"] is not None:
            if (
                type(kvargs["amountoffields"]).__name__
                == Metadata.__annotations__["amountoffields"]
            ):
                self_.amountoffields = kvargs["amountoffields"]
            else:
                self_.amountoffields = kvargs["amountoffields"]
        if (
            "amountoffieldvalues" in kvargs
            and kvargs["amountoffieldvalues"] is not None
        ):
            if (
                type(kvargs["amountoffieldvalues"]).__name__
                == Metadata.__annotations__["amountoffieldvalues"]
            ):
                self_.amountoffieldvalues = kvargs["amountoffieldvalues"]
            else:
                self_.amountoffieldvalues = kvargs["amountoffieldvalues"]
        if "amountofrows" in kvargs and kvargs["amountofrows"] is not None:
            if (
                type(kvargs["amountofrows"]).__name__
                == Metadata.__annotations__["amountofrows"]
            ):
                self_.amountofrows = kvargs["amountofrows"]
            else:
                self_.amountofrows = kvargs["amountofrows"]
        if "amountoftables" in kvargs and kvargs["amountoftables"] is not None:
            if (
                type(kvargs["amountoftables"]).__name__
                == Metadata.__annotations__["amountoftables"]
            ):
                self_.amountoftables = kvargs["amountoftables"]
            else:
                self_.amountoftables = kvargs["amountoftables"]
        if "hassectionaccess" in kvargs and kvargs["hassectionaccess"] is not None:
            if (
                type(kvargs["hassectionaccess"]).__name__
                == Metadata.__annotations__["hassectionaccess"]
            ):
                self_.hassectionaccess = kvargs["hassectionaccess"]
            else:
                self_.hassectionaccess = kvargs["hassectionaccess"]
        if "reloadmeta" in kvargs and kvargs["reloadmeta"] is not None:
            if (
                type(kvargs["reloadmeta"]).__name__
                == Metadata.__annotations__["reloadmeta"]
            ):
                self_.reloadmeta = kvargs["reloadmeta"]
            else:
                self_.reloadmeta = MetadataReloadmeta(**kvargs["reloadmeta"])
        if "staticbytesize" in kvargs and kvargs["staticbytesize"] is not None:
            if (
                type(kvargs["staticbytesize"]).__name__
                == Metadata.__annotations__["staticbytesize"]
            ):
                self_.staticbytesize = kvargs["staticbytesize"]
            else:
                self_.staticbytesize = kvargs["staticbytesize"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MetadataReloadmeta:
    """

    Attributes
    ----------
    cpuspent: float
    peakmemorybytes: float
    """

    cpuspent: float = None
    peakmemorybytes: float = None

    def __init__(self_, **kvargs):

        if "cpuspent" in kvargs and kvargs["cpuspent"] is not None:
            if (
                type(kvargs["cpuspent"]).__name__
                == MetadataReloadmeta.__annotations__["cpuspent"]
            ):
                self_.cpuspent = kvargs["cpuspent"]
            else:
                self_.cpuspent = kvargs["cpuspent"]
        if "peakmemorybytes" in kvargs and kvargs["peakmemorybytes"] is not None:
            if (
                type(kvargs["peakmemorybytes"]).__name__
                == MetadataReloadmeta.__annotations__["peakmemorybytes"]
            ):
                self_.peakmemorybytes = kvargs["peakmemorybytes"]
            else:
                self_.peakmemorybytes = kvargs["peakmemorybytes"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Objectspec:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == Objectspec.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            if (
                type(kvargs["objectType"]).__name__
                == Objectspec.__annotations__["objectType"]
            ):
                self_.objectType = kvargs["objectType"]
            else:
                self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            if (
                type(kvargs["sheetId"]).__name__
                == Objectspec.__annotations__["sheetId"]
            ):
                self_.sheetId = kvargs["sheetId"]
            else:
                self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            if type(kvargs["title"]).__name__ == Objectspec.__annotations__["title"]:
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Result:
    """

    Attributes
    ----------
    documentSizeMiB: float
    hasSectionAccess: bool
    objNoCache: list[Resultobjresponsetime]
    objSingleThreaded: list[Resultsingle]
    objSlowCached: list[Resultobjsinglethreaded]
    objSlowUncached: list[Resultobjresponsetime]
    objectCount: float
    rowCount: float
    sheetCount: float
    sheets: list[Resultobjsheet]
    topFieldsByBytes: list[Resultmetadatatopfields]
    topTablesByBytes: list[Resultmetadatatoptables]
    """

    documentSizeMiB: float = None
    hasSectionAccess: bool = None
    objNoCache: list[Resultobjresponsetime] = None
    objSingleThreaded: list[Resultsingle] = None
    objSlowCached: list[Resultobjsinglethreaded] = None
    objSlowUncached: list[Resultobjresponsetime] = None
    objectCount: float = None
    rowCount: float = None
    sheetCount: float = None
    sheets: list[Resultobjsheet] = None
    topFieldsByBytes: list[Resultmetadatatopfields] = None
    topTablesByBytes: list[Resultmetadatatoptables] = None

    def __init__(self_, **kvargs):

        if "documentSizeMiB" in kvargs and kvargs["documentSizeMiB"] is not None:
            if (
                type(kvargs["documentSizeMiB"]).__name__
                == Result.__annotations__["documentSizeMiB"]
            ):
                self_.documentSizeMiB = kvargs["documentSizeMiB"]
            else:
                self_.documentSizeMiB = kvargs["documentSizeMiB"]
        if "hasSectionAccess" in kvargs and kvargs["hasSectionAccess"] is not None:
            if (
                type(kvargs["hasSectionAccess"]).__name__
                == Result.__annotations__["hasSectionAccess"]
            ):
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
            else:
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
        if "objNoCache" in kvargs and kvargs["objNoCache"] is not None:
            if (
                len(kvargs["objNoCache"]) > 0
                and f"list[{type(kvargs['objNoCache'][0]).__name__}]"
                == Result.__annotations__["objNoCache"]
            ):
                self_.objNoCache = kvargs["objNoCache"]
            else:
                self_.objNoCache = [
                    Resultobjresponsetime(**e) for e in kvargs["objNoCache"]
                ]
        if "objSingleThreaded" in kvargs and kvargs["objSingleThreaded"] is not None:
            if (
                len(kvargs["objSingleThreaded"]) > 0
                and f"list[{type(kvargs['objSingleThreaded'][0]).__name__}]"
                == Result.__annotations__["objSingleThreaded"]
            ):
                self_.objSingleThreaded = kvargs["objSingleThreaded"]
            else:
                self_.objSingleThreaded = [
                    Resultsingle(**e) for e in kvargs["objSingleThreaded"]
                ]
        if "objSlowCached" in kvargs and kvargs["objSlowCached"] is not None:
            if (
                len(kvargs["objSlowCached"]) > 0
                and f"list[{type(kvargs['objSlowCached'][0]).__name__}]"
                == Result.__annotations__["objSlowCached"]
            ):
                self_.objSlowCached = kvargs["objSlowCached"]
            else:
                self_.objSlowCached = [
                    Resultobjsinglethreaded(**e) for e in kvargs["objSlowCached"]
                ]
        if "objSlowUncached" in kvargs and kvargs["objSlowUncached"] is not None:
            if (
                len(kvargs["objSlowUncached"]) > 0
                and f"list[{type(kvargs['objSlowUncached'][0]).__name__}]"
                == Result.__annotations__["objSlowUncached"]
            ):
                self_.objSlowUncached = kvargs["objSlowUncached"]
            else:
                self_.objSlowUncached = [
                    Resultobjresponsetime(**e) for e in kvargs["objSlowUncached"]
                ]
        if "objectCount" in kvargs and kvargs["objectCount"] is not None:
            if (
                type(kvargs["objectCount"]).__name__
                == Result.__annotations__["objectCount"]
            ):
                self_.objectCount = kvargs["objectCount"]
            else:
                self_.objectCount = kvargs["objectCount"]
        if "rowCount" in kvargs and kvargs["rowCount"] is not None:
            if type(kvargs["rowCount"]).__name__ == Result.__annotations__["rowCount"]:
                self_.rowCount = kvargs["rowCount"]
            else:
                self_.rowCount = kvargs["rowCount"]
        if "sheetCount" in kvargs and kvargs["sheetCount"] is not None:
            if (
                type(kvargs["sheetCount"]).__name__
                == Result.__annotations__["sheetCount"]
            ):
                self_.sheetCount = kvargs["sheetCount"]
            else:
                self_.sheetCount = kvargs["sheetCount"]
        if "sheets" in kvargs and kvargs["sheets"] is not None:
            if (
                len(kvargs["sheets"]) > 0
                and f"list[{type(kvargs['sheets'][0]).__name__}]"
                == Result.__annotations__["sheets"]
            ):
                self_.sheets = kvargs["sheets"]
            else:
                self_.sheets = [Resultobjsheet(**e) for e in kvargs["sheets"]]
        if "topFieldsByBytes" in kvargs and kvargs["topFieldsByBytes"] is not None:
            if (
                len(kvargs["topFieldsByBytes"]) > 0
                and f"list[{type(kvargs['topFieldsByBytes'][0]).__name__}]"
                == Result.__annotations__["topFieldsByBytes"]
            ):
                self_.topFieldsByBytes = kvargs["topFieldsByBytes"]
            else:
                self_.topFieldsByBytes = [
                    Resultmetadatatopfields(**e) for e in kvargs["topFieldsByBytes"]
                ]
        if "topTablesByBytes" in kvargs and kvargs["topTablesByBytes"] is not None:
            if (
                len(kvargs["topTablesByBytes"]) > 0
                and f"list[{type(kvargs['topTablesByBytes'][0]).__name__}]"
                == Result.__annotations__["topTablesByBytes"]
            ):
                self_.topTablesByBytes = kvargs["topTablesByBytes"]
            else:
                self_.topTablesByBytes = [
                    Resultmetadatatoptables(**e) for e in kvargs["topTablesByBytes"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultmetadatatopfields:
    """

    Attributes
    ----------
    byte_size: float
    is_system: bool
    name: str
    """

    byte_size: float = None
    is_system: bool = None
    name: str = None

    def __init__(self_, **kvargs):

        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            if (
                type(kvargs["byte_size"]).__name__
                == Resultmetadatatopfields.__annotations__["byte_size"]
            ):
                self_.byte_size = kvargs["byte_size"]
            else:
                self_.byte_size = kvargs["byte_size"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            if (
                type(kvargs["is_system"]).__name__
                == Resultmetadatatopfields.__annotations__["is_system"]
            ):
                self_.is_system = kvargs["is_system"]
            else:
                self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == Resultmetadatatopfields.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultmetadatatoptables:
    """

    Attributes
    ----------
    byte_size: float
    is_system: bool
    name: str
    """

    byte_size: float = None
    is_system: bool = None
    name: str = None

    def __init__(self_, **kvargs):

        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            if (
                type(kvargs["byte_size"]).__name__
                == Resultmetadatatoptables.__annotations__["byte_size"]
            ):
                self_.byte_size = kvargs["byte_size"]
            else:
                self_.byte_size = kvargs["byte_size"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            if (
                type(kvargs["is_system"]).__name__
                == Resultmetadatatoptables.__annotations__["is_system"]
            ):
                self_.is_system = kvargs["is_system"]
            else:
                self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == Resultmetadatatoptables.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultobjresponsetime:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    responseTimeSeconds: float
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None
    responseTimeSeconds: float = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if (
                type(kvargs["id"]).__name__
                == Resultobjresponsetime.__annotations__["id"]
            ):
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            if (
                type(kvargs["objectType"]).__name__
                == Resultobjresponsetime.__annotations__["objectType"]
            ):
                self_.objectType = kvargs["objectType"]
            else:
                self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            if (
                type(kvargs["sheetId"]).__name__
                == Resultobjresponsetime.__annotations__["sheetId"]
            ):
                self_.sheetId = kvargs["sheetId"]
            else:
                self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            if (
                type(kvargs["title"]).__name__
                == Resultobjresponsetime.__annotations__["title"]
            ):
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        if (
            "responseTimeSeconds" in kvargs
            and kvargs["responseTimeSeconds"] is not None
        ):
            if (
                type(kvargs["responseTimeSeconds"]).__name__
                == Resultobjresponsetime.__annotations__["responseTimeSeconds"]
            ):
                self_.responseTimeSeconds = kvargs["responseTimeSeconds"]
            else:
                self_.responseTimeSeconds = kvargs["responseTimeSeconds"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultobjsheet:
    """

    Attributes
    ----------
    objectCount: float
    sheet: Resultobjresponsetime
    sheetObjects: list[Resultobjresponsetime]
    """

    objectCount: float = None
    sheet: Resultobjresponsetime = None
    sheetObjects: list[Resultobjresponsetime] = None

    def __init__(self_, **kvargs):

        if "objectCount" in kvargs and kvargs["objectCount"] is not None:
            if (
                type(kvargs["objectCount"]).__name__
                == Resultobjsheet.__annotations__["objectCount"]
            ):
                self_.objectCount = kvargs["objectCount"]
            else:
                self_.objectCount = kvargs["objectCount"]
        if "sheet" in kvargs and kvargs["sheet"] is not None:
            if (
                type(kvargs["sheet"]).__name__
                == Resultobjsheet.__annotations__["sheet"]
            ):
                self_.sheet = kvargs["sheet"]
            else:
                self_.sheet = Resultobjresponsetime(**kvargs["sheet"])
        if "sheetObjects" in kvargs and kvargs["sheetObjects"] is not None:
            if (
                len(kvargs["sheetObjects"]) > 0
                and f"list[{type(kvargs['sheetObjects'][0]).__name__}]"
                == Resultobjsheet.__annotations__["sheetObjects"]
            ):
                self_.sheetObjects = kvargs["sheetObjects"]
            else:
                self_.sheetObjects = [
                    Resultobjresponsetime(**e) for e in kvargs["sheetObjects"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultobjsinglethreaded:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    cpuQuotients: list[float]
    responseTimeSeconds: float
    schema: Objectspec
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None
    cpuQuotients: list[float] = None
    responseTimeSeconds: float = None
    schema: Objectspec = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if (
                type(kvargs["id"]).__name__
                == Resultobjsinglethreaded.__annotations__["id"]
            ):
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            if (
                type(kvargs["objectType"]).__name__
                == Resultobjsinglethreaded.__annotations__["objectType"]
            ):
                self_.objectType = kvargs["objectType"]
            else:
                self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            if (
                type(kvargs["sheetId"]).__name__
                == Resultobjsinglethreaded.__annotations__["sheetId"]
            ):
                self_.sheetId = kvargs["sheetId"]
            else:
                self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            if (
                type(kvargs["title"]).__name__
                == Resultobjsinglethreaded.__annotations__["title"]
            ):
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        if "cpuQuotients" in kvargs and kvargs["cpuQuotients"] is not None:
            if (
                type(kvargs["cpuQuotients"]).__name__
                == Resultobjsinglethreaded.__annotations__["cpuQuotients"]
            ):
                self_.cpuQuotients = kvargs["cpuQuotients"]
            else:
                self_.cpuQuotients = kvargs["cpuQuotients"]
        if (
            "responseTimeSeconds" in kvargs
            and kvargs["responseTimeSeconds"] is not None
        ):
            if (
                type(kvargs["responseTimeSeconds"]).__name__
                == Resultobjsinglethreaded.__annotations__["responseTimeSeconds"]
            ):
                self_.responseTimeSeconds = kvargs["responseTimeSeconds"]
            else:
                self_.responseTimeSeconds = kvargs["responseTimeSeconds"]
        if "schema" in kvargs and kvargs["schema"] is not None:
            if (
                type(kvargs["schema"]).__name__
                == Resultobjsinglethreaded.__annotations__["schema"]
            ):
                self_.schema = kvargs["schema"]
            else:
                self_.schema = Objectspec(**kvargs["schema"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultsingle:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    cpuQuotient1: float
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None
    cpuQuotient1: float = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == Resultsingle.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            if (
                type(kvargs["objectType"]).__name__
                == Resultsingle.__annotations__["objectType"]
            ):
                self_.objectType = kvargs["objectType"]
            else:
                self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            if (
                type(kvargs["sheetId"]).__name__
                == Resultsingle.__annotations__["sheetId"]
            ):
                self_.sheetId = kvargs["sheetId"]
            else:
                self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            if type(kvargs["title"]).__name__ == Resultsingle.__annotations__["title"]:
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        if "cpuQuotient1" in kvargs and kvargs["cpuQuotient1"] is not None:
            if (
                type(kvargs["cpuQuotient1"]).__name__
                == Resultsingle.__annotations__["cpuQuotient1"]
            ):
                self_.cpuQuotient1 = kvargs["cpuQuotient1"]
            else:
                self_.cpuQuotient1 = kvargs["cpuQuotient1"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisonfields:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: str
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: str = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):

        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            if (
                type(kvargs["absoluteDiffAsc"]).__name__
                == Sortedcomparisonfields.__annotations__["absoluteDiffAsc"]
            ):
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
            else:
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            if (
                type(kvargs["absoluteDiffDesc"]).__name__
                == Sortedcomparisonfields.__annotations__["absoluteDiffDesc"]
            ):
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
            else:
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            if (
                type(kvargs["dataSourceStatus"]).__name__
                == Sortedcomparisonfields.__annotations__["dataSourceStatus"]
            ):
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
            else:
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            if (
                type(kvargs["list"]).__name__
                == Sortedcomparisonfields.__annotations__["list"]
            ):
                self_.list = kvargs["list"]
            else:
                self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            if (
                type(kvargs["relativeDiffAsc"]).__name__
                == Sortedcomparisonfields.__annotations__["relativeDiffAsc"]
            ):
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
            else:
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            if (
                type(kvargs["relativeDiffDesc"]).__name__
                == Sortedcomparisonfields.__annotations__["relativeDiffDesc"]
            ):
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
            else:
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisonobjresponsetime:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: str
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: str = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):

        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            if (
                type(kvargs["absoluteDiffAsc"]).__name__
                == Sortedcomparisonobjresponsetime.__annotations__["absoluteDiffAsc"]
            ):
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
            else:
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            if (
                type(kvargs["absoluteDiffDesc"]).__name__
                == Sortedcomparisonobjresponsetime.__annotations__["absoluteDiffDesc"]
            ):
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
            else:
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            if (
                type(kvargs["dataSourceStatus"]).__name__
                == Sortedcomparisonobjresponsetime.__annotations__["dataSourceStatus"]
            ):
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
            else:
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            if (
                type(kvargs["list"]).__name__
                == Sortedcomparisonobjresponsetime.__annotations__["list"]
            ):
                self_.list = kvargs["list"]
            else:
                self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            if (
                type(kvargs["relativeDiffAsc"]).__name__
                == Sortedcomparisonobjresponsetime.__annotations__["relativeDiffAsc"]
            ):
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
            else:
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            if (
                type(kvargs["relativeDiffDesc"]).__name__
                == Sortedcomparisonobjresponsetime.__annotations__["relativeDiffDesc"]
            ):
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
            else:
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisonoobjheavy:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: str
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: str = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):

        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            if (
                type(kvargs["absoluteDiffAsc"]).__name__
                == Sortedcomparisonoobjheavy.__annotations__["absoluteDiffAsc"]
            ):
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
            else:
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            if (
                type(kvargs["absoluteDiffDesc"]).__name__
                == Sortedcomparisonoobjheavy.__annotations__["absoluteDiffDesc"]
            ):
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
            else:
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            if (
                type(kvargs["dataSourceStatus"]).__name__
                == Sortedcomparisonoobjheavy.__annotations__["dataSourceStatus"]
            ):
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
            else:
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            if (
                type(kvargs["list"]).__name__
                == Sortedcomparisonoobjheavy.__annotations__["list"]
            ):
                self_.list = kvargs["list"]
            else:
                self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            if (
                type(kvargs["relativeDiffAsc"]).__name__
                == Sortedcomparisonoobjheavy.__annotations__["relativeDiffAsc"]
            ):
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
            else:
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            if (
                type(kvargs["relativeDiffDesc"]).__name__
                == Sortedcomparisonoobjheavy.__annotations__["relativeDiffDesc"]
            ):
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
            else:
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisontables:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: str
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: str = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):

        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            if (
                type(kvargs["absoluteDiffAsc"]).__name__
                == Sortedcomparisontables.__annotations__["absoluteDiffAsc"]
            ):
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
            else:
                self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            if (
                type(kvargs["absoluteDiffDesc"]).__name__
                == Sortedcomparisontables.__annotations__["absoluteDiffDesc"]
            ):
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
            else:
                self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            if (
                type(kvargs["dataSourceStatus"]).__name__
                == Sortedcomparisontables.__annotations__["dataSourceStatus"]
            ):
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
            else:
                self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            if (
                type(kvargs["list"]).__name__
                == Sortedcomparisontables.__annotations__["list"]
            ):
                self_.list = kvargs["list"]
            else:
                self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            if (
                type(kvargs["relativeDiffAsc"]).__name__
                == Sortedcomparisontables.__annotations__["relativeDiffAsc"]
            ):
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
            else:
                self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            if (
                type(kvargs["relativeDiffDesc"]).__name__
                == Sortedcomparisontables.__annotations__["relativeDiffDesc"]
            ):
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
            else:
                self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Apps:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def download_apps_evaluations_compare(
        self, baseid: str, comparisonid: str
    ) -> Comparison:
        """
        Download a comparison log of two evaluations
        Accepts two evaluation ids and downloads a log, in XML format, denoting the differences between the two.


        Parameters
        ----------
        baseid: str
          Id of the baseline evaluation
        comparisonid: str
          Id of the comparison evaluation
        """
        response = self.auth.rest(
            path="/apps/evaluations/{baseid}/actions/compare/{comparisonid}/actions/download".replace(
                "{baseid}", baseid
            ).replace(
                "{comparisonid}", comparisonid
            ),
            method="GET",
            params={},
            data=None,
        )
        obj = Comparison(**response.json())
        obj.auth = self.auth
        return obj

    def compare_apps_evaluations(
        self, baseid: str, comparisonid: str, all: bool = None, format: str = None
    ) -> Comparison:
        """
        Compare two evaluations
        Accepts two evaluation ids and returns a comparison denoting the differences between the two.


        Parameters
        ----------
        baseid: str
          Id of the baseline evaluation
        comparisonid: str
          Id of the comparison evaluation
        all: bool = None
          Get the full list of comparisons including non-significant diffs
        format: str = None
          Specify output format, currently supported are 'json' and 'xml'
        """
        query_params = {}
        if all is not None:
            query_params["all"] = all
        if format is not None:
            query_params["format"] = format
        response = self.auth.rest(
            path="/apps/evaluations/{baseid}/actions/compare/{comparisonid}".replace(
                "{baseid}", baseid
            ).replace("{comparisonid}", comparisonid),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = Comparison(**response.json())
        obj.auth = self.auth
        return obj

    def get_evaluation(
        self, id: str, all: bool = None, format: str = None
    ) -> Evaluation:
        """
        Retrieve a specific evaluation
        Find an evaluation by a specific id.


        Parameters
        ----------
        id: str
          Id of the desired evaluation.
        all: bool = None
          Get the full data of the evaluation
        format: str = None
          Specify output format, currently supported are 'json' and 'xml'
        """
        query_params = {}
        if all is not None:
            query_params["all"] = all
        if format is not None:
            query_params["format"] = format
        response = self.auth.rest(
            path="/apps/evaluations/{id}".replace("{id}", id),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = Evaluation(**response.json())
        obj.auth = self.auth
        return obj

    def import_app(
        self,
        data: FileData = None,
        appId: str = None,
        fallbackName: str = None,
        fileId: str = None,
        mode: str = None,
        name: str = None,
        NoData: bool = None,
        spaceId: str = None,
    ) -> NxApp:
        """
        Imports an app into the system.

        Parameters
        ----------
        appId: str = None
          The app ID of the target app when source is qvw file.
        fallbackName: str = None
          The name of the target app when source does not have a specified name, applicable if source is qvw file.
        fileId: str = None
          The file ID to be downloaded from Temporary Content Service (TCS) and used during import.
        mode: str = None
          The import mode. In `new` mode (default), the source app will be imported as a new app.The `autoreplace` mode is an internal mode only and is not permitted for external use.

          One of:

          • NEW

          • AUTOREPLACE
        name: str = None
          The name of the target app.
        NoData: bool = None
          If NoData is true, the data of the existing app will be kept as is, otherwise it will be replaced by the new incoming data.
        spaceId: str = None
          The space ID of the target app.
        data: FileData = None
          Path of the source app.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if fallbackName is not None:
            query_params["fallbackName"] = fallbackName
        if fileId is not None:
            query_params["fileId"] = fileId
        if mode is not None:
            query_params["mode"] = mode
        if name is not None:
            query_params["name"] = name
        if NoData is not None:
            query_params["NoData"] = NoData
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        response = self.auth.rest(
            path="/apps/import",
            method="POST",
            params=query_params,
            data=data,
            headers={"Content-Type": "application/octet-stream"},
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_privileges(self) -> list[str]:
        """
        Gets the app privileges for the current user, such as create app and import app. Empty means that the current user has no app privileges.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/privileges",
            method="GET",
            params={},
            data=None,
        )
        return response.json()

    def delete_media_file(self, appId: str, path: str) -> None:
        """
        Deletes a media content file or complete directory.
        Returns OK if the bytes containing the media file (or the complete content of a directory) were successfully deleted, or error in case of failure or lack of permission.

        Parameters
        ----------
        appId: str
          Unique application identifier.
        path: str
          Path to file content.
        """
        self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="DELETE",
            params={},
            data=None,
        )

    def get_media_file(self, appId: str, path: str) -> str:
        """
        Gets media content from file.
        Returns a stream of bytes containing the media file content on success, or error if file is not found.

        Parameters
        ----------
        appId: str
          Unique application identifier.
        path: str
          Path to file content.
        """
        response = self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def set_media_file(self, appId: str, path: str, data: FileData) -> None:
        """
        Stores the media content file.
        Returns OK if the bytes containing the media file content were successfully stored, or error in case of failure, lack of permission or file already exists on the supplied path.

        Parameters
        ----------
        appId: str
          Unique application identifier.
        path: str
          Path to file content.
        data: FileData

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="PUT",
            params={},
            data=data,
            headers={"Content-Type": "application/octet-stream"},
        )

    def get_media_lists(
        self, appId: str, path: str, show: str = None
    ) -> AppContentList:
        """
        Lists media content.
        Returns a JSON formatted array of strings describing the available media content or error if the optional path supplied is not found.

        Parameters
        ----------
        appId: str
          Unique application identifier.
        path: str
          The path to sub folder with static content relative to the root folder. Use empty path to access the root folder.
        show: str = None
          Optional. List output can include files and folders in different ways:

          • Not recursive, default if show option is not supplied or incorrectly specified, results in output with files and empty directories for the path specified only.

          • Recursive(r), use ?show=r or ?show=recursive, results in a recursive output with files, all empty folders are excluded.

          • All(a), use ?show=a or ?show=all, results in a recursive output with files and empty directories.
        """
        query_params = {}
        if show is not None:
            query_params["show"] = show
        response = self.auth.rest(
            path="/apps/{appId}/media/list/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = AppContentList(**response.json())
        obj.auth = self.auth
        return obj

    def get_reloads_log(self, appId: str, reloadId: str) -> str:
        """
        Retrieves the log of a specific reload.
        Returns the log as "text/plain; charset=UTF-8".

        Parameters
        ----------
        appId: str
          Identifier of the app.
        reloadId: str
          Identifier of the reload.
        """
        response = self.auth.rest(
            path="/apps/{appId}/reloads/logs/{reloadId}".replace(
                "{appId}", appId
            ).replace("{reloadId}", reloadId),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def get(self, appId: str) -> NxApp:
        """
        Retrieves information for a specific app.

        Parameters
        ----------
        appId: str
          Identifier of the app.
        """
        response = self.auth.rest(
            path="/apps/{appId}".replace("{appId}", appId),
            method="GET",
            params={},
            data=None,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_evaluations(
        self,
        guid: str,
        all: bool = None,
        fileMode: bool = None,
        format: str = None,
        limit: int = 20,
        next: str = None,
        prev: str = None,
        sort: str = None,
        max_items: int = 20,
    ) -> ListableResource[Evaluation]:
        """
        Retrieve a list of all historic evaluations for an app GUID
        Find all evaluations for an app GUID.
        Supports paging via next, prev which are sent in the response body


        Parameters
        ----------
        guid: str
          The app guid.
        all: bool = None
          Get the full data of the evaluation
        fileMode: bool = None
          Add file transfer headers to response
        format: str = None
          Specify output format, currently supported are 'json' and 'xml'
        limit: int = 20
          Number of results to return per page.
        next: str = None
          The app evaluation id to get next page from
        prev: str = None
          The app evaluation id to get previous page from
        sort: str = None
          Property to sort list on
        """
        query_params = {}
        if all is not None:
            query_params["all"] = all
        if fileMode is not None:
            query_params["fileMode"] = fileMode
        if format is not None:
            query_params["format"] = format
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/apps/{guid}/evaluations".replace("{guid}", guid),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Evaluation,
            auth=self.auth,
            path="/apps/{guid}/evaluations",
            max_items=max_items,
            query_params=query_params,
        )

    def create_evaluation(self, guid: str) -> Evaluation:
        """
        Queue an app evaluation
        Queue an app evaluation by its app guid.


        Parameters
        ----------
        guid: str
          Guid of the app.
        """
        response = self.auth.rest(
            path="/apps/{guid}/evaluations".replace("{guid}", guid),
            method="POST",
            params={},
            data=None,
        )
        obj = Evaluation(**response.json())
        obj.auth = self.auth
        return obj

    def create(self, data: CreateApp) -> NxApp:
        """
        Creates a new app.

        Parameters
        ----------
        data: CreateApp
          Attributes that the user wants to set in new app.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps",
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def create_session_app(self, session_app_id: str) -> NxApp:
        """
        creates an empty session app

        Parameters
        ----------
        session_app_id: string the a self generated "app_id" prefixed with SessionApp_

        Examples
        ----------
        >>> session_app_id = "SessionApp_" + str(uuid.uuid2())
        ... session_app = apps.create_session_app(session_app_id)
        ... with session_app.open():
        ...     script = "Load RecNo() as N autogenerate(200);"
        ...     session_app.set_script(script)
        ...     session_app.do_reload()
        """
        obj = NxApp(attributes={"id": session_app_id})
        obj.auth = self.auth
        return obj
