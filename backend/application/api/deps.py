from datetime import datetime
from pathlib import Path


from ..connections import (
    RedisDependency,
)  # noqa


class BaseQueryDependency:
    PATH_TO_SQL_QUERY = "sql"

    def read_sql_query(self, file_name: str) -> str:
        with open(
            Path(__file__).parent.parent
            / f"{self.PATH_TO_SQL_QUERY}/query_{file_name}.sql",
            "r",
        ) as file:
            return file.read()


class PaginatedQueryDependency(BaseQueryDependency):
    def __init__(
        self,
        page_number: int = 1,
        page_size: int = 100,
        use_cache: bool = True,
    ) -> None:
        self.limit = page_size
        self.skip = (page_number - 1) * page_size
        self.use_cache = use_cache

    def end_sql_statement(self) -> str:
        """
        end_sql_statement method is used to return the end SQL statement for the query.

        Returns:
            str: The end SQL statement for the query with the skip and limit values.
        """
        return "LIMIT :skip, :limit"

    def assemble_query_without_limit_params(
        self, sql_statement: str, sql_params: dict | None = None
    ) -> tuple[str, dict]:
        sql_statement = f"""{sql_statement}"""

        sql_params = {} if sql_params is None else sql_params

        return sql_statement, sql_params

    def assemble_query_with_limit_params(
        self,
        sql_statement: str,
        sql_params: dict | None = None,
    ) -> tuple[str, dict]:
        """
        combine_sql_statement method is used to combine the common query parameters with the SQL statement.

        Args:
            sql_statement (str): The SQL statement to be combined with the common query parameters.

        Returns:
            str: The combined SQL statement.
        """
        sql_statement = f"""{sql_statement} 
        {self.end_sql_statement()}"""

        sql_params = {
            **({} if sql_params is None else sql_params),
            "skip": self.skip,
            "limit": self.limit,
        }

        return sql_statement, sql_params


class DeliveryFromToQueryDependency(BaseQueryDependency):
    """
    CommonQueryDependency class is used to define the common query parameters,
    which can be used in any API endpoint.

    """

    __slots__ = (
        "delivery_from",
        "delivery_to",
        "use_cache",
    )

    def __init__(
        self,
        delivery_from: datetime | None = None,
        delivery_to: datetime | None = None,
        use_cache: bool = True,
    ) -> None:
        self.delivery_from = delivery_from if delivery_from else datetime.now()
        self.delivery_to = delivery_to if delivery_to else datetime.now()
        self.use_cache = use_cache


# Redis dependency
redis_dependency: RedisDependency = RedisDependency()

# # Database dependency
# database_dependency: DatabaseDependency = DatabaseDependency()


# sipx_imb_api_client: APIClientDependency = APIClientDependency(
#     hostname=settings.SIPX_API_ENDPOINT
# )

# metering_data_api_client: APIClientDependency = APIClientDependency(
#     hostname=settings.METERING_SERVICE_ENDPOINT
# )
