from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Scheme (Enum):
    STRATUM_V1 = "stratum+tcp"
    STRATUM_V2 = "stratum2+tcp"

@dataclass
class PoolUrl:
    scheme: Scheme
    host: str
    port: int
    pubKey: Optional[str] = None

    def __str__(self) -> str:
        if self.scheme == Scheme.STRATUM_V2 and self.pubKey:
            return f"{self.scheme.value}://{self.host}:{self.port}/{self.pubKey}"
        else:
            return f"{self.scheme.value}://{self.host}:{self.port}"


@dataclass
class PoolMetrics:
    """A dataclass to standardize pool metrics returned from miners.
    Attributes:

    accepted: Number of accepted shares.
    rejected: Number of rejected shares.
    get_failures: Number of failures in obtaining work from the pool.
    remote_failures: Number of failures communicating with the pool server.
    active: Indicates if the miner is connected to the stratum server.
    Alive : Indicates if a pool is alive.
    url: URL of the pool.
    index: Index of the pool.
    user: Username for the pool.
    pool_rejected_percent: Percentage of rejected shares by the pool.
    pool_stale_percent: Percentage of stale shares by the pool.
    """

    accepted: int
    rejected: int
    get_failures: int
    remote_failures: int
    active: bool
    alive: bool
    url: PoolUrl
    index: int
    user: str
    pool_rejected_percent: float = field(init=False)
    pool_stale_percent: float = field(init=False)

    @property
    def pool_rejected_percent(self) -> float:  # noqa - Skip PyCharm inspection
        """Calculate and return the percentage of rejected shares"""
        return self._calculate_percentage(self.rejected, self.accepted + self.rejected)

    @pool_rejected_percent.setter
    def pool_rejected_percent(self, val):
        pass

    @property
    def pool_stale_percent(self) -> float:  # noqa - Skip PyCharm inspection
        """Calculate and return the percentage of stale shares."""
        return self._calculate_percentage(
            self.get_failures, self.accepted + self.rejected
        )

    @pool_stale_percent.setter
    def pool_stale_percent(self, val):
        pass

    @staticmethod
    def _calculate_percentage(value: int, total: int) -> float:
        """Calculate the percentage."""
        if total == 0:
            return 0
        return (value / total) * 100
