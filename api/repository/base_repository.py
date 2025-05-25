from shared.db_connections import get_db_session
from typing import Any, Optional, TypeVar, Generic

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, table_name: str, entity_class: Optional[type[T]] = None):
        self.table_name = table_name
        self.entity_class = entity_class

    def _to_entity(self, data: dict) -> T:
        if self.entity_class and data:
            return self.entity_class(**data)
        return data

    def _to_entities(self, data_list: list[dict]) -> list[T]:
        return [self._to_entity(data) for data in data_list]

    def find_by_id(self, id: int) -> Optional[T]:
        try:
            with get_db_session() as session:
                response = session.table(self.table_name).select("*").eq("id", id).execute()
                if response.data and len(response.data) > 0:
                    print("The response.data[0] is", response.data[0])
                    return self._to_entity(response.data[0])
                return None
        except Exception as e:
            print(f"Error in find_by_id: {e}")
            return None

    def create(self, data: dict[str, Any]) -> Optional[T]:
        try:
            with get_db_session() as session:
                response = session.table(self.table_name).insert(data).execute()
                if response.data and len(response.data) > 0:
                    return self._to_entity(response.data[0])
                return None
        except Exception as e:
            print(f"Error in create: {e}")
            return None
