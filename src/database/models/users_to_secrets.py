from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.ids import SecretId, UserId
from database.models import SecretModel, UserModel
from database.models._mixins import CreatedAtMixin
from database.models.base import BaseAlchemyModel


class UsersToSecretsModel(CreatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users_to_secrets"

    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    secret_id: Mapped[SecretId] = mapped_column(
        ForeignKey("secrets.id"),
        primary_key=True,
    )

    user: Mapped[UserModel] = relationship(
        "UserModel",
        cascade="all,delete",
    )
    secret: Mapped[SecretModel] = relationship(
        "SecretModel",
        cascade="all,delete",
    )
