import uuid
from typing import Generator, List, Optional

from structlog import get_logger

from data_point_client import AuthenticatedClient
from data_point_client.api.data_point import data_point_get_data_points
from data_point_client.models import DataPointResponseBase, EnDataPointExistenceDTO, ProblemDetails
from nista_library.nista_connetion import NistaConnection
from nista_library.nista_data_point import NistaDataPoint

log = get_logger()


class NistaDataPoints:
    def __init__(self, connection: NistaConnection):
        self.connection = connection

    def get_data_point_list(self) -> Generator[NistaDataPoint, None, None]:
        token = self.connection.get_access_token()
        client = AuthenticatedClient(
            base_url=self.connection.datapoint_base_url, token=token, verify_ssl=self.connection.verify_ssl
        )

        data_point_list = data_point_get_data_points.sync(
            workspace_id=self.connection.workspace_id, client=client, existence=[EnDataPointExistenceDTO.FULL]
        )
        if isinstance(data_point_list, ProblemDetails):
            problems: ProblemDetails = data_point_list
            raise Exception(problems)

        if isinstance(data_point_list, list):
            list_of_data_points: List[DataPointResponseBase] = data_point_list

        for data_point in list_of_data_points:
            name: Optional[str] = None
            if isinstance(data_point.name, str):
                name = data_point.name

            nista_data_point = NistaDataPoint(
                connection=self.connection, data_point_id=uuid.UUID(data_point.data_point_id), name=name
            )
            yield nista_data_point
