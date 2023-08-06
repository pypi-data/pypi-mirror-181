from .core import BaseClient
from .resources.alerts import AsyncAlertsResource, SyncAlertsResource
from .resources.balances import AsyncBalancesResource, SyncBalancesResource
from .resources.institutions import AsyncInstitutionsResource, SyncInstitutionsResource
from .resources.transactions import AsyncTransactionsResource, SyncTransactionsResource
from .resources.users import AsyncUsersResource, SyncUsersResource


class AsyncClient(BaseClient):
    def __init__(
        self,
        access_token: str,
        concurrency_limit: int = 50,
        base_url: str = "https://api.pngme.com/beta",
    ):
        super().__init__(
            access_token=access_token,
            concurrency_limit=concurrency_limit,
            base_url=base_url,
        )

        self.alerts = AsyncAlertsResource(self)
        self.balances = AsyncBalancesResource(self)
        self.institutions = AsyncInstitutionsResource(self)
        self.transactions = AsyncTransactionsResource(self)
        self.users = AsyncUsersResource(self)


class Client(BaseClient):
    def __init__(
        self,
        access_token: str,
        concurrency_limit: int = 50,
        base_url: str = "https://api.pngme.com/beta",
    ):
        super().__init__(
            access_token=access_token,
            concurrency_limit=concurrency_limit,
            base_url=base_url,
        )

        self.alerts = SyncAlertsResource(self)
        self.balances = SyncBalancesResource(self)
        self.institutions = SyncInstitutionsResource(self)
        self.transactions = SyncTransactionsResource(self)
        self.users = SyncUsersResource(self)
