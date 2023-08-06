from abc import ABC, abstractmethod
from typing import List, Optional

from .abstract_metric import Counter, Distribution, Gauge

__all__ = ["MetricClient"]


class MetricClient(ABC):
    @abstractmethod
    def create_counter(
        self,
        namespace: str,
        name: str,
        labels: Optional[List] = None,
        description: Optional[str] = None,
    ) -> Counter:
        """Create a counter

        Args:
            namespace: Counter namespace
            name: Counter name
            labels: Counter labels
            description: Counter description

        Returns:
            New counter instance
        """

    @abstractmethod
    def create_gauge(
        self,
        namespace: str,
        name: str,
        labels: Optional[List] = None,
        description: Optional[str] = None,
    ) -> Gauge:
        """Create a gauge

        Args:
            namespace: Gauge namespace
            name: Gauge name
            labels: Gauge labels
            description: Gauge description

        Returns:
            New gauge instance
        """

    @abstractmethod
    def create_distribution(
        self,
        namespace: str,
        name: str,
        labels: Optional[List] = None,
        description: Optional[str] = None,
    ) -> Distribution:
        """Create a distribution

        Args:
            namespace: Distribution namespace
            name: Distribution name
            labels: Distribution labels
            description: Distribution description

        Returns:
            A new distribution
        """

    @abstractmethod
    def push(self):
        """Push metrics to metrics-collector"""
