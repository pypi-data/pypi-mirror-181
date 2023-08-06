import importlib
import logging
from os import getenv
from typing import List, Optional

from .abstract_metric import Counter, Distribution, Gauge
from .metric_client import MetricClient

__all__ = ["Metrics"]

LOG = logging.getLogger(__name__)

DEFAULT_METRIC_CLIENT_CLS = "odp.compute.metrics.client.MetricMockClient"


class Metrics:

    METRICS_CLIENT: MetricClient = None

    @staticmethod
    def _load_metric_client() -> MetricClient:
        """Load a metrics client based on environment.

        Metrics client is determined by the environment variable
        `ODP__METRIC_CLIENT_CLS`, which should be a valid class path.

        Returns:
            `MetricClient` intance based on `ODP__METRIC_CLIENT_CLS` env-variable
        """
        try:
            metric_client_packagename = getenv("ODP__METRIC_CLIENT_CLS", DEFAULT_METRIC_CLIENT_CLS)
            client_args = [x.strip() for x in getenv("ODP__METRIC_CLIENT_ARGS", "").split(",")]
            client_args = [x for x in client_args if x]

            parts = metric_client_packagename.split(".")

            if parts[-1][0].islower():
                client_packagename, client_clsname = ".".join(parts[:-2]), parts[-2]
                client_funcname = parts[-1]
            else:
                client_packagename, client_clsname = ".".join(parts[:-1]), parts[-1]
                client_funcname = None

            client_module = importlib.import_module(client_packagename)
            client_cls = getattr(client_module, client_clsname)

            if client_funcname:
                return getattr(client_cls, client_funcname)(*client_args)
            else:
                return client_cls(*client_args)
        except KeyError:
            LOG.exception(f"Failed to load metrics class `{client_cls}'")
            from odp.compute.metrics.client.metric_mock_client import MetricMockClient

            return MetricMockClient()

    @staticmethod
    def _get_metric_client() -> MetricClient:
        """Get metrics client.

        Similar to `_load_metric_client`, but will cache the `MetricClient` on first
        run and return the cached instance on every subsequent run.

        Returns:
            Cached `MetricClient` instance
        """
        if Metrics.METRICS_CLIENT is None:
            Metrics.METRICS_CLIENT = Metrics._load_metric_client()
            LOG.info("Using metrics client: {}".format(Metrics.METRICS_CLIENT.__class__))
        return Metrics.METRICS_CLIENT

    @staticmethod
    def counter(
        namespace: str,
        name: str,
        labels: Optional[List] = None,
        description: Optional[str] = None,
    ) -> Counter:
        """Create a new counter

        Counters are metrics which only hold integer values and can only be incremented.

        Args:
            namespace: Counter namespace
            name: Counter name
            labels: Counter labels
            description: Counter description

        Returns:
            A new counter instance
        """
        client = Metrics._get_metric_client()
        return client.create_counter(namespace, name, labels, description)

    @staticmethod
    def gauge(
        namespace: str,
        name: str,
        labels: Optional[List] = None,
        description: Optional[str] = None,
    ) -> Gauge:
        """Create a new gauge.

        A gauge is a metrics that can hold floating-point values and can be set to
        arbitrarily.

        Args:
            namespace: Gauge namespace
            name: Gauge name
            labels: Gauge labels
            description: Gauge description

        Returns:
            A new gauge instance
        """
        client = Metrics._get_metric_client()
        return client.create_gauge(namespace, name, labels, description)

    @staticmethod
    def distribution(
        namespace: str,
        name: str,
        labels: Optional[List] = None,
        description: Optional[str] = None,
    ) -> Distribution:
        """Create a new distribution

        Distributions are metrics that hold floating-point values and can be set
        arbitrarily. In addition, they will track min and max values, means and
        standard deviations.

        Args:
            namespace: Distribution namespace
            name: Distribution name
            labels: Distribution labels
            description: Distribution description

        Returns:
            A new distribution instance
        """
        client = Metrics._get_metric_client()
        return client.create_distribution(namespace, name, labels, description)

    @staticmethod
    def push(raise_on_error=True):
        """Push metrics, optionally ignore errors.

        Metrics must periodically be pushed to the metrics-collector.

        Args:
            raise_on_error: If set to `False`, errors will be caught and ignored.
        """
        client = Metrics._get_metric_client()

        try:
            client.push()
        except Exception as e:
            if raise_on_error:
                raise e
            else:
                LOG.warning(
                    f"An exception occurred when attempting to push metrics: {e}",
                    exc_info=True,
                )
