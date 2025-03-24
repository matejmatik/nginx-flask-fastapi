from datetime import datetime, timedelta
from collections import defaultdict
from logging import getLogger
from pathlib import Path
from typing import Any, Literal

from ..core import settings
from ..connections import AsyncMySQL, AsyncRedis


logger = getLogger(__name__)


async def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def get_dates(days_offset: int = 0, as_str: bool = False) -> Any:
    """Get date in format YYYY-MM-DD."""

    calculated_date = datetime.today() + timedelta(days=days_offset)
    return calculated_date.strftime("%Y-%m-%d") if as_str else calculated_date


def read_sql_statement(
    file_name: str, mode: Literal["query", "insert", "update", "delete"] = "query"
) -> str:
    """
    read_sql_query reads the SQL query from the file and returns it.



    Args:
        file_name (str): file name to read the SQL query from

    Returns:
        str: SQL query from the file
    """

    with open(
        Path(__file__).parent.parent
        / f"{settings.PATH_TO_SQL_QUERY}/{mode}_{file_name}.sql",
        "r",
    ) as file:
        return file.read()


def prepare_sql_query(
    file_name: str,
    sql_params: dict = {},
):
    return (
        f"{read_sql_statement(file_name)} LIMIT :skip, :limit"
        if sql_params.get("limit") is not None and sql_params.get("skip") is not None
        else read_sql_statement(file_name)
    )


async def __fetch_from_redis(key: str, redis: AsyncRedis) -> Any:
    try:
        if await redis.exists(key):
            return await redis.get(key)
        return None
    except Exception as e:
        logger.error(f"Error fetching data from Redis: {e}")
        return None


async def __fetch_timeseries_from_redis_by_daterange(
    key: str,
    # delivery_from: Y-M-D, delivery_to: Y-M-D
    delivery_from: str,
    delivery_to: str,
    redis: AsyncRedis,
) -> list[dict]:
    from_date = datetime.strptime(delivery_from, "%Y-%m-%d")
    to_date = datetime.strptime(delivery_to, "%Y-%m-%d")

    try:
        if await redis.exists_many(
            keys=[
                f"{key}:{delivery_from}",
                f"{key}:{delivery_to}",
            ]
        ):
            # Initialize an empty list to store all results
            collected_timeseries = []

            # Generate the date range from delivery_from to delivery_to (inclusive)
            current_iteration_date = from_date
            while current_iteration_date <= to_date:
                daily_data = await redis.get(
                    f"{key}:{current_iteration_date.strftime('%Y-%m-%d')}"
                )
                if daily_data:
                    collected_timeseries.extend(daily_data)

                # Move to the next day
                current_iteration_date += timedelta(days=1)

            return collected_timeseries
        return []
    except Exception as e:
        logger.error(f"Error fetching data from Redis: {e}")
        return []


async def __save_timeseries_to_redis_per_day(
    key: str,
    redis: AsyncRedis,
    data: list[dict],
    expire: int = 3600,  # 1 hour
) -> None:
    if len(data) == 0:
        return
    # group by day in timestamp column
    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item.get("timestamp").strftime("%Y-%m-%d")].append(item)

    for datetime_day, value in grouped_data.items():
        await redis.save(key=f"{key}:{datetime_day}", value=value, expire=expire)


async def fetch_data(
    db: AsyncMySQL,
    redis: AsyncRedis,
    key: str,
    sql_statement: str,
    sql_params: dict = {},
    expire: int = 3600,  # 1 hour
    use_cache: bool = False,
    save_to_cache: bool = True,
    return_data: bool = True,
    is_timeseries: bool = False,
    **kwargs,
) -> Any:
    """
    Fetch data from the database or Redis cache.
    """

    # ========================
    # If the data is timeseries, fetch it from the cache or database by date range
    # ========================
    if is_timeseries:
        data = (
            await __fetch_timeseries_from_redis_by_daterange(
                key=key,
                delivery_from=kwargs.get("delivery_from").strftime("%Y-%m-%d"),
                delivery_to=kwargs.get("delivery_to").strftime("%Y-%m-%d"),
                redis=redis,
            )
            if use_cache
            else []
        )

        # In case the data is not found in the cache, fetch it from the database
        if len(data) == 0:
            data = await db.exec(statement=sql_statement, params=sql_params)
            if save_to_cache and len(data) > 0:
                await __save_timeseries_to_redis_per_day(
                    key=key, redis=redis, data=data, expire=expire
                )
    # ========================
    # If the data is not timeseries, fetch it from the cache or database
    # ========================
    else:
        data = await __fetch_from_redis(key=key, redis=redis) if use_cache else None

        if data is None or not use_cache:
            data = await db.exec(statement=sql_statement, params=sql_params)
            if save_to_cache and data:
                await redis.save(key=key, value=data, expire=expire)

    if return_data:
        return data
