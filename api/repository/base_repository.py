from typing import Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from uuid import UUID

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, entity_class: Optional[type[T]] = None):
        self.db = db
        self.entity_class = entity_class

    def get_by_id(self, entity_id: str) -> Optional[T]:
        if isinstance(entity_id, UUID):
            entity_id = str(entity_id)
        return self.db.query(self.entity_class).filter(self.entity_class.id == entity_id).first()

    def create(self, **kwargs) -> Optional[T]:
        try:
            entity = self.entity_class(**kwargs)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            print(f"Error in create: {e}")
            return None

    def get_all(self) -> list[T]:
        return self.db.query(self.entity_class).all()

    def delete(self, entity_id: str) -> bool:
        try:
            entity = self.get_by_id(entity_id)
            if entity:
                self.db.delete(entity)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            print(f"Error in delete: {e}")
            return False
