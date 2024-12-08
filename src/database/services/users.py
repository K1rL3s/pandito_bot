from database.repos.logs import LogsRepo
from database.repos.users import UsersRepo


class UsersService:
    def __init__(
        self,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
    ) -> None:
        self.users_repo = users_repo
        self.logs_repo = logs_repo

    async def admin_update_balance(
        self,
        slave_id: int,
        master_id: int,
        amount: int,
    ) -> int:
        user = await self.users_repo.get_user(slave_id)
        if user is None:
            raise Exception  # TODO: сделать ошибку

        admin = await self.users_repo.get_user(master_id)
        if admin is None:
            raise Exception  # TODO: сделать ошибку

        if user.balance + amount < 0:  # если отнимаем
            raise Exception  # TODO: сделать ошибку

        new_balance = user.balance + amount
        await self.users_repo.set_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            master_id,
            f"Added money {amount} to user {slave_id}",
        )

        return new_balance

    async def admin_set_balance(
        self,
        slave_id: int,
        master_id: int,
        new_balance: int,
    ) -> int:
        if new_balance < 0:
            raise Exception  # TODO: сделать ошибку

        user = await self.users_repo.get_user(slave_id)
        if user is None:
            raise Exception  # TODO: сделать ошибку

        admin = await self.users_repo.get_user(master_id)
        if admin is None:
            raise Exception  # TODO: сделать ошибку

        await self.users_repo.set_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            master_id,
            f"Set {new_balance} money to user {slave_id}",
        )
        await self.logs_repo.log_action(
            slave_id,
            f"Set {new_balance} money from user {master_id}",
        )

        return new_balance

    async def transfer_funds(
        self,
        sender_id: int,
        receiver_id: int,
        amount: int,
    ) -> int:
        if amount <= 0:
            raise Exception  # TODO сделать ошибку

        sender = await self.users_repo.get_user(sender_id)
        if sender is None:
            raise Exception  # TODO сделать ошибку

        receiver = await self.users_repo.get_user(receiver_id)
        if receiver is None:
            raise Exception  # TODO сделать ошибку

        if sender.balance < amount:
            raise Exception  # TODO сделать ошибку

        new_sender_balance = sender.balance - amount
        await self.users_repo.set_balance(sender_id, new_sender_balance)

        new_receiver_balance = receiver.balance + amount
        await self.users_repo.set_balance(receiver_id, new_receiver_balance)

        await self.logs_repo.log_action(
            sender_id,
            f"Transferred {amount} to user {sender_id}",
        )
        await self.logs_repo.log_action(
            receiver_id,
            f"Received {amount} from user {sender_id}",
        )

        return new_sender_balance
