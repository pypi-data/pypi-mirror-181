from enum import Enum
from pydantic import Field, BaseModel
from typing import Dict, Any, Union, List, Literal, Optional
from rath.scalars import ID
from datetime import datetime
from fluss.funcs import aexecute, execute
from fluss.traits import Graph, MockableTrait
from fluss.rath import FlussRath
from fluss.scalars import EventValue


class StreamKind(str, Enum):
    INT = "INT"
    STRING = "STRING"
    STRUCTURE = "STRUCTURE"
    LIST = "LIST"
    BOOL = "BOOL"
    ENUM = "ENUM"
    DICT = "DICT"
    UNSET = "UNSET"


class RunEventType(str, Enum):
    """An enumeration."""

    NEXT = "NEXT"
    "NEXT (Value represent Labels)"
    ERROR = "ERROR"
    "Error (Value represent Intensity)"
    COMPLETE = "COMPLETE"
    "COMPLETE (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "UNKNOWN (Value represent Intensity)"


class ReactiveImplementationModelInput(str, Enum):
    """An enumeration."""

    ZIP = "ZIP"
    "ZIP (Zip the data)"
    COMBINELATEST = "COMBINELATEST"
    "COMBINELATEST (Combine values with latest value from each stream)"
    WITHLATEST = "WITHLATEST"
    "WITHLATEST (Combine a leading value with the latest value)"
    BUFFER_COMPLETE = "BUFFER_COMPLETE"
    "BUFFER_COMPLETE (Buffer values until complete is retrieved)"
    BUFFER_UNTIL = "BUFFER_UNTIL"
    "BUFFER_UNTIL (Buffer values until signal is send)"
    CHUNK = "CHUNK"
    "CHUNK (Chunk the data)"
    SPLIT = "SPLIT"
    "SPLIT (Split the data)"
    OMIT = "OMIT"
    "OMIT (Omit the data)"
    TO_LIST = "TO_LIST"
    "TO_LIST (Convert to list)"
    FOREACH = "FOREACH"
    "FOREACH (Foreach element in list)"
    IF = "IF"
    "IF (If condition is met)"
    AND = "AND"
    "AND (AND condition)"


class ConstantKind(str, Enum):
    STRING = "STRING"
    INT = "INT"
    BOOL = "BOOL"
    FLOAT = "FLOAT"


class MapStrategy(str, Enum):
    """Variety expresses the Type of Representation we are dealing with"""

    MAP = "MAP"
    MERGEMAP = "MERGEMAP"
    SWITCHMAP = "SWITCHMAP"
    CONCATMAP = "CONCATMAP"


class EventTypeInput(str, Enum):
    """Variety expresses the Type of Representation we are dealing with"""

    NEXT = "NEXT"
    "NEXT (Value represent Labels)"
    ERROR = "ERROR"
    "Error (Value represent Intensity)"
    COMPLETE = "COMPLETE"
    "COMPLETE (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "UNKNOWN (Value represent Intensity)"


class GraphInput(BaseModel):
    zoom: Optional[float]
    nodes: List[Optional["NodeInput"]]
    edges: List[Optional["EdgeInput"]]
    args: List[Optional["ArgPortInput"]]
    returns: List[Optional["ReturnPortInput"]]
    globals: List[Optional["GlobalInput"]]


class NodeInput(BaseModel):
    id: str
    typename: str
    hash: Optional[str]
    interface: Optional[str]
    name: Optional[str]
    description: Optional[str]
    kind: Optional[str]
    implementation: Optional[ReactiveImplementationModelInput]
    documentation: Optional[str]
    position: "PositionInput"
    defaults: Optional[Dict]
    extra: Optional[Dict]
    instream: List[Optional[List[Optional["StreamItemInput"]]]]
    outstream: List[Optional[List[Optional["StreamItemInput"]]]]
    constream: List[Optional[List[Optional["StreamItemInput"]]]]
    map_strategy: Optional[MapStrategy] = Field(alias="mapStrategy")
    allow_local: Optional[bool] = Field(alias="allowLocal")
    reserve_params: Optional["ReserveParamsInput"] = Field(alias="reserveParams")


class PositionInput(BaseModel):
    x: float
    y: float


class StreamItemInput(BaseModel):
    key: str
    kind: StreamKind
    identifier: Optional[str]
    nullable: bool
    child: Optional["StreamItemChildInput"]


class StreamItemChildInput(BaseModel):
    kind: StreamKind
    identifier: Optional[str]
    child: Optional["StreamItemChildInput"]


class ReserveParamsInput(BaseModel):
    agents: Optional[List[Optional[str]]]


class EdgeInput(BaseModel):
    id: str
    typename: str
    source: str
    target: str
    source_handle: str = Field(alias="sourceHandle")
    target_handle: str = Field(alias="targetHandle")
    stream: Optional[List[Optional[StreamItemInput]]]

    class Config:
        allow_population_by_field_name = True


class ArgPortInput(BaseModel):
    identifier: Optional[str]
    "The identifier"
    key: str
    "The key of the arg"
    name: Optional[str]
    "The name of this argument"
    label: Optional[str]
    "The name of this argument"
    kind: StreamKind
    "The type of this argument"
    description: Optional[str]
    "The description of this argument"
    child: Optional["ChildPortInput"]
    "The child of this argument"
    widget: Optional["WidgetInput"]
    "The child of this argument"
    default: Optional[Any]
    "The key of the arg"
    nullable: bool
    "Is this argument nullable"


class ChildPortInput(BaseModel):
    nullable: Optional[bool]
    identifier: Optional[str]
    "The identifier"
    kind: StreamKind
    "The type of this argument"
    child: Optional["ChildPortInput"]


class WidgetInput(BaseModel):
    kind: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    dependencies: Optional[List[Optional[str]]]
    "The dependencies of this port"
    choices: Optional[List[Optional["ChoiceInput"]]]
    "The dependencies of this port"
    max: Optional[int]
    "Max value for int widget"
    min: Optional[int]
    "Max value for int widget"
    placeholder: Optional[str]
    "Placeholder for any widget"
    as_paragraph: Optional[bool] = Field(alias="asParagraph")
    "Is this a paragraph"
    hook: Optional[str]
    "A hook for the app to call"
    ward: Optional[str]
    "A ward for the app to call"


class ChoiceInput(BaseModel):
    value: Any
    label: str


class ReturnPortInput(BaseModel):
    identifier: Optional[str]
    "The identifier"
    key: str
    "The key of the arg"
    name: Optional[str]
    "The name of this argument"
    label: Optional[str]
    "The name of this argument"
    kind: StreamKind
    "The type of this argument"
    description: Optional[str]
    "The description of this argument"
    child: Optional[ChildPortInput]
    "The child of this argument"
    widget: Optional["ReturnWidgetInput"]
    "The child of this argument"
    nullable: bool
    "Is this argument nullable"


class ReturnWidgetInput(BaseModel):
    kind: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    hook: Optional[str]
    "A hook for the app to call"
    ward: Optional[str]
    "A ward for the app to call"


class GlobalInput(BaseModel):
    key: str
    value: Optional[Dict]


class GlobalFragment(BaseModel):
    typename: Optional[Literal["Global"]] = Field(alias="__typename")
    locked: Optional[bool]
    key: str
    value: Optional[Dict]
    mapped: Optional[List[Optional[str]]]
    identifier: Optional[str]
    typename: str
    widget: Optional[Dict]


class StreamItemChildFragmentChild(MockableTrait, BaseModel):
    typename: Optional[Literal["StreamItemChild"]] = Field(alias="__typename")
    kind: StreamKind
    identifier: Optional[str]


class StreamItemChildFragment(MockableTrait, BaseModel):
    typename: Optional[Literal["StreamItemChild"]] = Field(alias="__typename")
    kind: StreamKind
    identifier: Optional[str]
    child: Optional[StreamItemChildFragmentChild]


class StreamItemFragment(MockableTrait, BaseModel):
    typename: Optional[Literal["StreamItem"]] = Field(alias="__typename")
    key: str
    kind: StreamKind
    identifier: Optional[str]
    nullable: bool
    child: Optional[StreamItemChildFragment]


class FlowNodeCommonsFragmentBase(BaseModel):
    instream: List[Optional[List[Optional[StreamItemFragment]]]]
    outstream: List[Optional[List[Optional[StreamItemFragment]]]]
    constream: List[Optional[List[Optional[StreamItemFragment]]]]
    constants: Optional[Dict]


class ArkitektNodeFragmentReserveparams(BaseModel):
    typename: Optional[Literal["ReserveParams"]] = Field(alias="__typename")
    agents: Optional[List[Optional[str]]]


class ArkitektNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ArkitektNode"]] = Field(alias="__typename")
    name: Optional[str]
    description: Optional[str]
    hash: str
    kind: str
    defaults: Optional[Dict]
    reserve_params: ArkitektNodeFragmentReserveparams = Field(alias="reserveParams")
    allow_local: bool = Field(alias="allowLocal")
    map_strategy: MapStrategy = Field(alias="mapStrategy")


class ReactiveNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ReactiveNode"]] = Field(alias="__typename")
    implementation: ReactiveImplementationModelInput
    defaults: Optional[Dict]


class ArgNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ArgNode"]] = Field(alias="__typename")


class KwargNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["KwargNode"]] = Field(alias="__typename")


class ReturnNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ReturnNode"]] = Field(alias="__typename")


class FlowNodeFragmentBasePosition(BaseModel):
    typename: Optional[Literal["Position"]] = Field(alias="__typename")
    x: int
    y: int


class FlowNodeFragmentBase(BaseModel):
    id: str
    position: FlowNodeFragmentBasePosition
    typename: str


class FlowNodeFragmentBaseArkitektNode(ArkitektNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseReactiveNode(ReactiveNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseArgNode(ArgNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseKwargNode(KwargNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseReturnNode(ReturnNodeFragment, FlowNodeFragmentBase):
    pass


FlowNodeFragment = Union[
    FlowNodeFragmentBaseArkitektNode,
    FlowNodeFragmentBaseReactiveNode,
    FlowNodeFragmentBaseArgNode,
    FlowNodeFragmentBaseKwargNode,
    FlowNodeFragmentBaseReturnNode,
    FlowNodeFragmentBase,
]


class FlowEdgeCommonsFragmentBase(BaseModel):
    stream: List[Optional[StreamItemFragment]]


class LabeledEdgeFragment(FlowEdgeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["LabeledEdge"]] = Field(alias="__typename")


class FancyEdgeFragment(FlowEdgeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["FancyEdge"]] = Field(alias="__typename")


class FlowEdgeFragmentBase(BaseModel):
    id: str
    source: str
    source_handle: str = Field(alias="sourceHandle")
    target: str
    target_handle: str = Field(alias="targetHandle")
    typename: str


class FlowEdgeFragmentBaseLabeledEdge(LabeledEdgeFragment, FlowEdgeFragmentBase):
    pass


class FlowEdgeFragmentBaseFancyEdge(FancyEdgeFragment, FlowEdgeFragmentBase):
    pass


FlowEdgeFragment = Union[
    FlowEdgeFragmentBaseLabeledEdge, FlowEdgeFragmentBaseFancyEdge, FlowEdgeFragmentBase
]


class WidgetFragmentChoices(BaseModel):
    typename: Optional[Literal["Choice"]] = Field(alias="__typename")
    label: str
    value: Any


class WidgetFragment(BaseModel):
    typename: Optional[Literal["Widget"]] = Field(alias="__typename")
    kind: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    hook: Optional[str]
    "A hook for the app to call"
    placeholder: Optional[str]
    "Placeholder for any widget"
    choices: Optional[List[Optional[WidgetFragmentChoices]]]
    "The dependencies of this port"
    ward: Optional[str]
    "A hook for the app to call"


class ReturnWidgetFragmentChoices(BaseModel):
    typename: Optional[Literal["Choice"]] = Field(alias="__typename")
    label: str
    value: Any


class ReturnWidgetFragment(BaseModel):
    typename: Optional[Literal["ReturnWidget"]] = Field(alias="__typename")
    kind: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    hook: Optional[str]
    "A hook for the app to call"
    placeholder: Optional[str]
    "Placeholder for any widget"
    choices: Optional[List[Optional[ReturnWidgetFragmentChoices]]]
    "The dependencies of this port"
    ward: Optional[str]
    "A hook for the app to call"


class ArgPortChildFragmentChild(BaseModel):
    typename: Optional[Literal["ArgPortChild"]] = Field(alias="__typename")
    kind: StreamKind
    identifier: Optional[str]


class ArgPortChildFragment(BaseModel):
    typename: Optional[Literal["ArgPortChild"]] = Field(alias="__typename")
    kind: StreamKind
    identifier: Optional[str]
    nullable: Optional[bool]
    child: Optional[ArgPortChildFragmentChild]


class ReturnPortChildFragmentChild(BaseModel):
    typename: Optional[Literal["ArgPortChild"]] = Field(alias="__typename")
    kind: StreamKind
    identifier: Optional[str]


class ReturnPortChildFragment(BaseModel):
    typename: Optional[Literal["ReturnPortChild"]] = Field(alias="__typename")
    kind: StreamKind
    identifier: Optional[str]
    nullable: Optional[bool]
    child: Optional[ReturnPortChildFragmentChild]


class ArgPortFragment(BaseModel):
    typename: Optional[Literal["ArgPort"]] = Field(alias="__typename")
    key: str
    label: Optional[str]
    identifier: Optional[str]
    kind: StreamKind
    name: Optional[str]
    description: Optional[str]
    widget: Optional[WidgetFragment]
    child: Optional[ArgPortChildFragment]
    nullable: bool
    "The key of the arg"


class ReturnPortFragment(BaseModel):
    typename: Optional[Literal["ReturnPort"]] = Field(alias="__typename")
    key: str
    label: Optional[str]
    identifier: Optional[str]
    kind: StreamKind
    name: Optional[str]
    description: Optional[str]
    widget: Optional[ReturnWidgetFragment]
    child: Optional[ReturnPortChildFragment]
    nullable: bool
    "The key of the arg"


class FlowFragmentGraph(Graph, BaseModel):
    typename: Optional[Literal["FlowGraph"]] = Field(alias="__typename")
    nodes: List[Optional[FlowNodeFragment]]
    edges: List[Optional[FlowEdgeFragment]]
    globals: List[Optional[GlobalFragment]]
    args: List[Optional[ArgPortFragment]]
    returns: List[Optional[ReturnPortFragment]]


class FlowFragmentWorkspace(BaseModel):
    typename: Optional[Literal["Workspace"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]


class FlowFragment(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename")
    id: ID
    name: str
    graph: FlowFragmentGraph
    brittle: bool
    "Is this a brittle flow? aka. should the flow fail on any exception?"
    created_at: datetime = Field(alias="createdAt")
    workspace: Optional[FlowFragmentWorkspace]
    hash: str


class ListFlowFragment(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename")
    id: ID
    name: str
    hash: str


class WorkspaceFragment(BaseModel):
    typename: Optional[Literal["Workspace"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    latest_flow: Optional[FlowFragment] = Field(alias="latestFlow")
    "The latest flow"


class ListWorkspaceFragmentFlows(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename")
    id: ID


class ListWorkspaceFragment(BaseModel):
    typename: Optional[Literal["Workspace"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    flows: List[ListWorkspaceFragmentFlows]


class RunMutationStart(BaseModel):
    typename: Optional[Literal["Run"]] = Field(alias="__typename")
    id: ID


class RunMutation(BaseModel):
    """Start a run on fluss"""

    start: Optional[RunMutationStart]

    class Arguments(BaseModel):
        assignation: ID
        flow: ID

    class Meta:
        document = "mutation run($assignation: ID!, $flow: ID!) {\n  start(assignation: $assignation, flow: $flow) {\n    id\n  }\n}"


class RunlogMutationAlog(BaseModel):
    typename: Optional[Literal["RunLog"]] = Field(alias="__typename")
    id: ID


class RunlogMutation(BaseModel):
    """Start a run on fluss"""

    alog: Optional[RunlogMutationAlog]

    class Arguments(BaseModel):
        run: ID
        message: str

    class Meta:
        document = "mutation runlog($run: ID!, $message: String!) {\n  alog(run: $run, message: $message) {\n    id\n  }\n}"


class SnapshotMutationSnapshot(BaseModel):
    typename: Optional[Literal["Snapshot"]] = Field(alias="__typename")
    id: ID


class SnapshotMutation(BaseModel):
    """Snapshot the current state on the fluss platform"""

    snapshot: Optional[SnapshotMutationSnapshot]

    class Arguments(BaseModel):
        run: ID
        events: List[Optional[ID]]
        t: int

    class Meta:
        document = "mutation snapshot($run: ID!, $events: [ID]!, $t: Int!) {\n  snapshot(run: $run, events: $events, t: $t) {\n    id\n  }\n}"


class TrackMutationTrack(BaseModel):
    typename: Optional[Literal["RunEvent"]] = Field(alias="__typename")
    id: ID
    source: str
    handle: str
    type: RunEventType
    value: Optional[EventValue]


class TrackMutation(BaseModel):
    """Track a new event on the fluss platform"""

    track: Optional[TrackMutationTrack]

    class Arguments(BaseModel):
        run: ID
        source: str
        handle: str
        type: EventTypeInput
        value: Optional[EventValue] = None
        t: int

    class Meta:
        document = "mutation track($run: ID!, $source: String!, $handle: String!, $type: EventTypeInput!, $value: EventValue, $t: Int!) {\n  track(\n    run: $run\n    source: $source\n    handle: $handle\n    type: $type\n    value: $value\n    t: $t\n  ) {\n    id\n    source\n    handle\n    type\n    value\n  }\n}"


class Get_flowQuery(BaseModel):
    flow: Optional[FlowFragment]

    class Arguments(BaseModel):
        id: Optional[ID] = None

    class Meta:
        document = "fragment StreamItemChild on StreamItemChild {\n  kind\n  identifier\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment StreamItem on StreamItem {\n  key\n  kind\n  identifier\n  nullable\n  child {\n    ...StreamItemChild\n  }\n}\n\nfragment FlowEdgeCommons on FlowEdgeCommons {\n  stream {\n    ...StreamItem\n  }\n}\n\nfragment FlowNodeCommons on FlowNodeCommons {\n  instream {\n    ...StreamItem\n  }\n  outstream {\n    ...StreamItem\n  }\n  constream {\n    ...StreamItem\n  }\n  constants\n}\n\nfragment KwargNode on KwargNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment Widget on Widget {\n  kind\n  query\n  hook\n  placeholder\n  choices {\n    label\n    value\n  }\n  ward\n}\n\nfragment ReturnPortChild on ReturnPortChild {\n  kind\n  identifier\n  nullable\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment FancyEdge on FancyEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment ArkitektNode on ArkitektNode {\n  ...FlowNodeCommons\n  __typename\n  name\n  description\n  hash\n  kind\n  defaults\n  reserveParams {\n    agents\n  }\n  allowLocal\n  mapStrategy\n}\n\nfragment ReturnNode on ReturnNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment ArgPortChild on ArgPortChild {\n  kind\n  identifier\n  nullable\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment ReturnWidget on ReturnWidget {\n  kind\n  query\n  hook\n  placeholder\n  choices {\n    label\n    value\n  }\n  ward\n}\n\nfragment ReactiveNode on ReactiveNode {\n  ...FlowNodeCommons\n  __typename\n  implementation\n  defaults\n}\n\nfragment LabeledEdge on LabeledEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment ArgNode on ArgNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment FlowEdge on FlowEdge {\n  id\n  source\n  sourceHandle\n  target\n  targetHandle\n  typename\n  ...LabeledEdge\n  ...FancyEdge\n}\n\nfragment ReturnPort on ReturnPort {\n  key\n  label\n  identifier\n  kind\n  name\n  description\n  widget {\n    ...ReturnWidget\n  }\n  child {\n    ...ReturnPortChild\n  }\n  nullable\n}\n\nfragment ArgPort on ArgPort {\n  key\n  label\n  identifier\n  kind\n  name\n  description\n  widget {\n    ...Widget\n  }\n  child {\n    ...ArgPortChild\n  }\n  nullable\n}\n\nfragment Global on Global {\n  locked\n  key\n  value\n  mapped\n  identifier\n  typename\n  widget\n}\n\nfragment FlowNode on FlowNode {\n  id\n  position {\n    x\n    y\n  }\n  typename\n  ...ArkitektNode\n  ...ReactiveNode\n  ...ArgNode\n  ...KwargNode\n  ...ReturnNode\n}\n\nfragment Flow on Flow {\n  __typename\n  id\n  name\n  graph {\n    nodes {\n      ...FlowNode\n    }\n    edges {\n      ...FlowEdge\n    }\n    globals {\n      ...Global\n    }\n    args {\n      ...ArgPort\n    }\n    returns {\n      ...ReturnPort\n    }\n  }\n  brittle\n  createdAt\n  workspace {\n    id\n    name\n  }\n  hash\n}\n\nquery get_flow($id: ID) {\n  flow(id: $id) {\n    ...Flow\n  }\n}"


class Search_flowsQueryOptions(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename")
    value: ID
    label: str


class Search_flowsQuery(BaseModel):
    options: Optional[List[Optional[Search_flowsQueryOptions]]]

    class Arguments(BaseModel):
        search: Optional[str] = None

    class Meta:
        document = "query search_flows($search: String) {\n  options: flows(name: $search) {\n    value: id\n    label: name\n  }\n}"


class List_flowsQuery(BaseModel):
    flows: Optional[List[Optional[ListFlowFragment]]]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListFlow on Flow {\n  id\n  name\n  hash\n}\n\nquery list_flows {\n  flows {\n    ...ListFlow\n  }\n}"


class WorkspaceQuery(BaseModel):
    workspace: Optional[WorkspaceFragment]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment StreamItemChild on StreamItemChild {\n  kind\n  identifier\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment StreamItem on StreamItem {\n  key\n  kind\n  identifier\n  nullable\n  child {\n    ...StreamItemChild\n  }\n}\n\nfragment FlowEdgeCommons on FlowEdgeCommons {\n  stream {\n    ...StreamItem\n  }\n}\n\nfragment FlowNodeCommons on FlowNodeCommons {\n  instream {\n    ...StreamItem\n  }\n  outstream {\n    ...StreamItem\n  }\n  constream {\n    ...StreamItem\n  }\n  constants\n}\n\nfragment KwargNode on KwargNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment Widget on Widget {\n  kind\n  query\n  hook\n  placeholder\n  choices {\n    label\n    value\n  }\n  ward\n}\n\nfragment ReturnPortChild on ReturnPortChild {\n  kind\n  identifier\n  nullable\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment FancyEdge on FancyEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment ArkitektNode on ArkitektNode {\n  ...FlowNodeCommons\n  __typename\n  name\n  description\n  hash\n  kind\n  defaults\n  reserveParams {\n    agents\n  }\n  allowLocal\n  mapStrategy\n}\n\nfragment ReturnNode on ReturnNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment ArgPortChild on ArgPortChild {\n  kind\n  identifier\n  nullable\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment ReturnWidget on ReturnWidget {\n  kind\n  query\n  hook\n  placeholder\n  choices {\n    label\n    value\n  }\n  ward\n}\n\nfragment ReactiveNode on ReactiveNode {\n  ...FlowNodeCommons\n  __typename\n  implementation\n  defaults\n}\n\nfragment LabeledEdge on LabeledEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment ArgNode on ArgNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment FlowEdge on FlowEdge {\n  id\n  source\n  sourceHandle\n  target\n  targetHandle\n  typename\n  ...LabeledEdge\n  ...FancyEdge\n}\n\nfragment ReturnPort on ReturnPort {\n  key\n  label\n  identifier\n  kind\n  name\n  description\n  widget {\n    ...ReturnWidget\n  }\n  child {\n    ...ReturnPortChild\n  }\n  nullable\n}\n\nfragment ArgPort on ArgPort {\n  key\n  label\n  identifier\n  kind\n  name\n  description\n  widget {\n    ...Widget\n  }\n  child {\n    ...ArgPortChild\n  }\n  nullable\n}\n\nfragment Global on Global {\n  locked\n  key\n  value\n  mapped\n  identifier\n  typename\n  widget\n}\n\nfragment FlowNode on FlowNode {\n  id\n  position {\n    x\n    y\n  }\n  typename\n  ...ArkitektNode\n  ...ReactiveNode\n  ...ArgNode\n  ...KwargNode\n  ...ReturnNode\n}\n\nfragment Flow on Flow {\n  __typename\n  id\n  name\n  graph {\n    nodes {\n      ...FlowNode\n    }\n    edges {\n      ...FlowEdge\n    }\n    globals {\n      ...Global\n    }\n    args {\n      ...ArgPort\n    }\n    returns {\n      ...ReturnPort\n    }\n  }\n  brittle\n  createdAt\n  workspace {\n    id\n    name\n  }\n  hash\n}\n\nfragment Workspace on Workspace {\n  id\n  name\n  latestFlow {\n    ...Flow\n  }\n}\n\nquery Workspace($id: ID!) {\n  workspace(id: $id) {\n    ...Workspace\n  }\n}"


class MyWorkspacesQuery(BaseModel):
    myworkspaces: Optional[List[Optional[ListWorkspaceFragment]]]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListWorkspace on Workspace {\n  id\n  name\n  flows {\n    id\n  }\n}\n\nquery MyWorkspaces {\n  myworkspaces {\n    ...ListWorkspace\n  }\n}"


async def arun(
    assignation: ID, flow: ID, rath: FlussRath = None
) -> Optional[RunMutationStart]:
    """run

     Start a run on fluss

    Arguments:
        assignation (ID): assignation
        flow (ID): flow
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunMutationStart]"""
    return (
        await aexecute(
            RunMutation, {"assignation": assignation, "flow": flow}, rath=rath
        )
    ).start


def run(
    assignation: ID, flow: ID, rath: FlussRath = None
) -> Optional[RunMutationStart]:
    """run

     Start a run on fluss

    Arguments:
        assignation (ID): assignation
        flow (ID): flow
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunMutationStart]"""
    return execute(
        RunMutation, {"assignation": assignation, "flow": flow}, rath=rath
    ).start


async def arunlog(
    run: ID, message: str, rath: FlussRath = None
) -> Optional[RunlogMutationAlog]:
    """runlog

     Start a run on fluss

    Arguments:
        run (ID): run
        message (str): message
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunlogMutationAlog]"""
    return (
        await aexecute(RunlogMutation, {"run": run, "message": message}, rath=rath)
    ).alog


def runlog(
    run: ID, message: str, rath: FlussRath = None
) -> Optional[RunlogMutationAlog]:
    """runlog

     Start a run on fluss

    Arguments:
        run (ID): run
        message (str): message
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunlogMutationAlog]"""
    return execute(RunlogMutation, {"run": run, "message": message}, rath=rath).alog


async def asnapshot(
    run: ID, events: List[Optional[ID]], t: int, rath: FlussRath = None
) -> Optional[SnapshotMutationSnapshot]:
    """snapshot

     Snapshot the current state on the fluss platform

    Arguments:
        run (ID): run
        events (List[Optional[ID]]): events
        t (int): t
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[SnapshotMutationSnapshot]"""
    return (
        await aexecute(
            SnapshotMutation, {"run": run, "events": events, "t": t}, rath=rath
        )
    ).snapshot


def snapshot(
    run: ID, events: List[Optional[ID]], t: int, rath: FlussRath = None
) -> Optional[SnapshotMutationSnapshot]:
    """snapshot

     Snapshot the current state on the fluss platform

    Arguments:
        run (ID): run
        events (List[Optional[ID]]): events
        t (int): t
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[SnapshotMutationSnapshot]"""
    return execute(
        SnapshotMutation, {"run": run, "events": events, "t": t}, rath=rath
    ).snapshot


async def atrack(
    run: ID,
    source: str,
    handle: str,
    type: EventTypeInput,
    t: int,
    value: Optional[EventValue] = None,
    rath: FlussRath = None,
) -> Optional[TrackMutationTrack]:
    """track

     Track a new event on the fluss platform

    Arguments:
        run (ID): run
        source (str): source
        handle (str): handle
        type (EventTypeInput): type
        t (int): t
        value (Optional[EventValue], optional): value.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[TrackMutationTrack]"""
    return (
        await aexecute(
            TrackMutation,
            {
                "run": run,
                "source": source,
                "handle": handle,
                "type": type,
                "value": value,
                "t": t,
            },
            rath=rath,
        )
    ).track


def track(
    run: ID,
    source: str,
    handle: str,
    type: EventTypeInput,
    t: int,
    value: Optional[EventValue] = None,
    rath: FlussRath = None,
) -> Optional[TrackMutationTrack]:
    """track

     Track a new event on the fluss platform

    Arguments:
        run (ID): run
        source (str): source
        handle (str): handle
        type (EventTypeInput): type
        t (int): t
        value (Optional[EventValue], optional): value.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[TrackMutationTrack]"""
    return execute(
        TrackMutation,
        {
            "run": run,
            "source": source,
            "handle": handle,
            "type": type,
            "value": value,
            "t": t,
        },
        rath=rath,
    ).track


async def aget_flow(
    id: Optional[ID] = None, rath: FlussRath = None
) -> Optional[FlowFragment]:
    """get_flow



    Arguments:
        id (Optional[ID], optional): id.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[FlowFragment]"""
    return (await aexecute(Get_flowQuery, {"id": id}, rath=rath)).flow


def get_flow(id: Optional[ID] = None, rath: FlussRath = None) -> Optional[FlowFragment]:
    """get_flow



    Arguments:
        id (Optional[ID], optional): id.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[FlowFragment]"""
    return execute(Get_flowQuery, {"id": id}, rath=rath).flow


async def asearch_flows(
    search: Optional[str] = None, rath: FlussRath = None
) -> Optional[List[Optional[Search_flowsQueryOptions]]]:
    """search_flows



    Arguments:
        search (Optional[str], optional): search.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_flowsQueryFlows]]]"""
    return (await aexecute(Search_flowsQuery, {"search": search}, rath=rath)).flows


def search_flows(
    search: Optional[str] = None, rath: FlussRath = None
) -> Optional[List[Optional[Search_flowsQueryOptions]]]:
    """search_flows



    Arguments:
        search (Optional[str], optional): search.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_flowsQueryFlows]]]"""
    return execute(Search_flowsQuery, {"search": search}, rath=rath).flows


async def alist_flows(
    rath: FlussRath = None,
) -> Optional[List[Optional[ListFlowFragment]]]:
    """list_flows



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListFlowFragment]]]"""
    return (await aexecute(List_flowsQuery, {}, rath=rath)).flows


def list_flows(rath: FlussRath = None) -> Optional[List[Optional[ListFlowFragment]]]:
    """list_flows



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListFlowFragment]]]"""
    return execute(List_flowsQuery, {}, rath=rath).flows


async def aworkspace(id: ID, rath: FlussRath = None) -> Optional[WorkspaceFragment]:
    """Workspace



    Arguments:
        id (ID): id
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[WorkspaceFragment]"""
    return (await aexecute(WorkspaceQuery, {"id": id}, rath=rath)).workspace


def workspace(id: ID, rath: FlussRath = None) -> Optional[WorkspaceFragment]:
    """Workspace



    Arguments:
        id (ID): id
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[WorkspaceFragment]"""
    return execute(WorkspaceQuery, {"id": id}, rath=rath).workspace


async def amy_workspaces(
    rath: FlussRath = None,
) -> Optional[List[Optional[ListWorkspaceFragment]]]:
    """MyWorkspaces



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListWorkspaceFragment]]]"""
    return (await aexecute(MyWorkspacesQuery, {}, rath=rath)).myworkspaces


def my_workspaces(
    rath: FlussRath = None,
) -> Optional[List[Optional[ListWorkspaceFragment]]]:
    """MyWorkspaces



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListWorkspaceFragment]]]"""
    return execute(MyWorkspacesQuery, {}, rath=rath).myworkspaces


ArgPortInput.update_forward_refs()
ChildPortInput.update_forward_refs()
GraphInput.update_forward_refs()
NodeInput.update_forward_refs()
ReturnPortInput.update_forward_refs()
StreamItemChildInput.update_forward_refs()
StreamItemInput.update_forward_refs()
WidgetInput.update_forward_refs()
