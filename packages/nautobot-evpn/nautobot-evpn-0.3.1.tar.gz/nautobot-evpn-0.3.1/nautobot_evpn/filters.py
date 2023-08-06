from nautobot.extras.filters import NautobotFilterSet
from nautobot.utilities.filters import SearchFilter
from nautobot_evpn.models import EthernetSegment


class EthernetSegmentFilterSet(
    NautobotFilterSet,
):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "segment_id": "icontains",
        },
    )

    class Meta:
        model = EthernetSegment
        fields = [
            "id",
            "name",
            "segment_id"
        ]
