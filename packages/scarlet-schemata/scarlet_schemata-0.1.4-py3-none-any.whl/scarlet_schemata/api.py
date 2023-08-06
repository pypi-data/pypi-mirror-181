import orjson
from datetime import datetime
from pydantic import UUID4, BaseModel, IPvAnyAddress, IPvAnyNetwork, validator, Field
from enum import Enum
from uuid import uuid4


class BaseSchema(BaseModel):
    def show(self):
        j = orjson.loads(self.json())

        try:
            j["_id"] = j.pop("id")
        except KeyError:
            pass

        return j


class ID(BaseSchema):
    id: UUID4 = Field(default="", alias="_id")
    created: datetime = datetime.now()
    updated: datetime = datetime.now()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = uuid4()
        
        if not self.created:
            self.created = datetime.now()

        if not self.updated:
            self.updated = self.created
        


class Scope(BaseSchema):
    ip_blocks: list[IPvAnyNetwork] = []
    names: list[str] = []


# Users ------------------------------------------------------------------
 
class BaseUser(BaseSchema):
    fullname: str  # John Doe
    name: str  # johndoe


class User(BaseUser, ID):
    """
    An application user, i.e. a hacker. Authenticates using a digital certificate, therefore, only the name is necessary
    """

# Campaigns --------------------------------------------------------------

class CampaignType(str, Enum):
    Pentest = "pentest"
    RedTeaming = "redteaming"
    PurpleTeaming = "purpleteaming"
    VulnerabilityAssessment = "vulnerabilityassessment"


class BaseCampaign(BaseSchema):
    name: str
    description: str = ""
    type: CampaignType = CampaignType.Pentest
    start: datetime 
    end: datetime
    scope: Scope
    users: list[UUID4] = []

    @property 
    def stealth(self):
        if self.type == CampaignType.RedTeaming:
            return True 
        else: 
            return False


class Campaign(BaseCampaign, ID):
    """A hacking campaign"""


# Engagements -----------------------------------------------------------

class BaseEngagement(BaseSchema):
    name: str 
    campaign_id: UUID4 
    description: str | None
    scope: Scope
    start: datetime = datetime.now() 
    end: datetime | None
    users: list[UUID4] = []


class Engagement(BaseEngagement, ID):
    """
    A series of actions within a campaign
    """




# Nodes -----------------------------------------------------------------

class BaseNode(BaseSchema):
    campaign_id: UUID4
    ip: IPvAnyAddress
    gateway: UUID4 | None

class Node(BaseNode, ID):
    """
    An IP address, optionally linking to another node as a gateway. Used for creating visualizations. Filled using traceroute scans and Services.
    """


# Services --------------------------------------------------------------

class NetworkProtocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    SCTP = "SCTP"



class BaseService(BaseSchema):
    campaign_id: UUID4
    labels: list[str] = []
    notes: list[dict] = []
    hostname: str = ""
    protocol: NetworkProtocol = NetworkProtocol.ICMP
    port: int = 0

    @validator("port")
    def port_checks(cls, v, values):
        assert v < 65536, f"Invalid port number"
        if values["protocol"] != NetworkProtocol.ICMP:
            assert v > 0, f"Invalid port number for protocol {values['protocol']}"
        
        return v

class Service(BaseService, ID):
    node_id: UUID4




# Resources --------------------------------------

# class HttpMethod(str, Enum):
#     GET = "GET"
#     POST = "POST"
#     CONNECT = "CONNECT"
#     PUT = "PUT"
#     DELETE = "DELETE"
#     PATCH = "PATCH"
#     HEAD = "HEAD"
#     OPTIONS = "OPTIONS"
#     TRACE = "TRACE"
#     LOCK = "LOCK"
#     MKCOL = "MKCOL"
#     MOVE = "MOVE"
#     PROPFIND = "PROPFIND"
#     PROPPATCH = "PROPPATCH"
#     UNLOCK = "UNLOCK"
#     NONE = "NONE"


# OPENAPI STUFF --------------------------------------------

# class ParameterType(str, Enum):
#     Url = "url"
#     Query = "query"
#     Cookie = "cookie"
#     Header = "Header"


# class DataType(str, Enum):
#     string = "string"
#     integer = "integer"
#     number = "number"
#     boolean = "boolean"
#     array = "array"
#     object = "object"


# class Discriminator(BaseModel):
#     propertyName: str


# class Schema(BaseModel):
#     type: DataType
#     enum: list
#     # additionalProperties: 'Schema' | bool 
#     # pattern: str | None 
#     # items: list['Schema'] | None 
#     # properties: dict[str, 'Schema'] | None
#     # required: bool = False
#     # anyOf: list['Schema'] | None 
#     # oneOf: list['Schema'] | None
#     # allOf: list['Schema'] | None
#     # Not: 'Schema' | None = Field(alias='not')
#     descriminator: Discriminator


# class Parameter(BaseSchema):
#     name: str 
#     description: str 
#     type: ParameterType
#     required: list[str] | bool = False
#     # schema: Schema


# class TopSchema(BaseModel):
#     # schema: Schema
#     pass

# class RequestContent(BaseSchema):
#     application_json: TopSchema | None = Field(alias="application/json")
#     application_xml: TopSchema | None = Field(alias="application/xml")


# class RequestBody(BaseSchema):
#     description: str 
#     required: list[str] | bool = False 
#     content: RequestContent


# class OpenAPIInfo(BaseModel):
#     title: str 
#     description: str 
#     version: str


# class OpenAPIPath(BaseModel):
#     tags: list[str] = []
#     summary: str | None
#     description: str | None
#     operationId: str 
#     parameters: list[Parameter] | None 
#     requestBody: RequestBody | None 
#     responses: dict # not interesting to our use-case
#     externalDocs: dict  # not interesting to our use-case


# class OpenAPI(BaseModel):
#     openapi: str 
#     info: OpenAPIInfo
#     servers: list[dict[str, str]]
#     paths: dict[str, OpenAPIPath]


# class BaseResource(BaseSchema):
#     path: str
#     service_id: UUID4
#     engagement_id: UUID4 | None
#     method: HttpMethod = HttpMethod.GET
#     parameters: list[Parameter]
#     body = RequestBody
#     labels: list[str] = []
#     notes: list[dict] = []
    

# class Resource(BaseResource, ID):
#     campaign_id: UUID4




# # class User(ID):
# #     username: str
# #     campaign: UUID4
# #     name: Optional[str]
# #     email: Optional[str]
# #     password: Optional[str]


# class Severity(str, Enum):
#     CRITICAL = "CRITICAL"
#     HIGH = "HIGH"
#     MEDIUM = "MEDIUM"
#     LOW = "LOW"
#     INFO = "INFO"


# class CWE(ID):
#     pass


# class CVE(ID):
#     identifier: str
#     year: int = 2000
#     summary: str = ""
#     # cvss: CVSS3 = None
#     cwe: CWE = None

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.year = int(self.identifier.split("-")[1])

#     @validator("identifier")
#     def check_type(cls, v):
#         assert v.startswith("CVE-"), f"{v} does not start with CVE-"
#         assert v.count("-") == 2
#         assert datetime.now().year >= int(v.split("-")[1]) > 1970, f"Invalid year"
#         return v

# class BaseFinding(BaseSchema):
#     service_id: UUID4
#     engagement_id: UUID4    
#     title: str 
#     severity: Severity = Severity.INFO    
#     cvss: str = None
#     score: float = 0.0
#     description: str = ""
#     cve: list[CVE] = []

#     # class Config:
#     #     arbitrary_types_allowed = True

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         if self.score == 0.0:
#             self.severity = Severity.INFO
#         elif self.score < 4.0:
#             self.severity = Severity.LOW
#         elif self.score < 7.0:
#             self.severity = Severity.MEDIUM
#         elif self.score < 9.0:
#             self.severity = Severity.HIGH
#         else:
#             self.severity = Severity.CRITICAL

#     @validator("score")
#     def check_range(cls, v):
#         assert 0.0 <= v <= 10.0, f"Value not between 0 and 10"
#         return v

# class Finding(BaseFinding, ID):
#     campaign_id: UUID4
