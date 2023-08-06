import logging

from typing import Any
from typing import Callable
from typing import Dict
from typing import ItemsView
from typing import Iterator
from typing import KeysView
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union
from typing import ValuesView

from .prometheus_metrics import decider_client_counter
from .rust_decider import Decider as PyDecider
from .rust_decider import DeciderException
from .rust_decider import DeciderInitException
from .rust_decider import FeatureNotFoundException
from .rust_decider import init
from .rust_decider import make_ctx
from .rust_decider import PartialLoadException
from .rust_decider import ValueTypeMismatchException
from .rust_decider import version

logger = logging.getLogger(__name__)

DEFAULT_DECISIONMAKERS = (
    "darkmode overrides targeting holdout mutex_group fractional_availability value"
)

JsonValue = Union[
    None, int, float, str, bool, List["JsonValue"], Mapping[str, "JsonValue"]
]


class Decision(Mapping[str, Any]):
    def __init__(
        self,
        variant: Optional[str],
        value: Optional[JsonValue],
        feature_id: int,
        feature_name: str,
        feature_version: int,
        events: List[str],
    ):
        self.variant = variant
        self.value = value
        self.feature_id = feature_id
        self.feature_name = feature_name
        self.feature_version = feature_version
        self.events = events

    def keys(self) -> KeysView[str]:
        return self.__dict__.keys()

    def items(self) -> ItemsView[str, Any]:
        return self.__dict__.items()

    def values(self) -> ValuesView[Any]:
        return self.__dict__.values()

    def get(self, key: str, default=None) -> Optional[Any]:
        return self.__dict__.get(key, default)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)


class Decider:
    """Decider class wraps python bindings for Rust decider crate."""

    def __init__(self, path: str):
        self._pkg_version = version()

        try:
            self._decider = PyDecider(path)
        except PartialLoadException as e:
            decider_client_counter.labels(
                operation="init",
                success="false",
                error_type="partial_init_exception",
                pkg_version=self._pkg_version,
            ).inc()

            # log errors of misconfigured features
            logger.error(f"{e.args[0]}: {e.args[2]}")

            # set _decider to partially initialized PyDecider instance
            self._decider = e.args[1]

            # FIXME
            # remove py_decider in favor of _decider
            # once `get_decider()` can be deprecated in Experiments.py
            py_decider = init(DEFAULT_DECISIONMAKERS, path)
            # do not validate since it will raise an exception
            # and the partially loaded _decider will not be leveraged

            # self._validate_decider(py_decider)
            self.py_decider = py_decider

            return
        except DeciderInitException as e:
            decider_client_counter.labels(
                operation="init",
                success="false",
                error_type="init_exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise e

        # FIXME
        # remove py_decider in favor of _decider
        # once `get_decider()` can be deprecated in Experiments.py
        py_decider = init(DEFAULT_DECISIONMAKERS, path)
        self._validate_decider(py_decider)
        self.py_decider = py_decider

        decider_client_counter.labels(
            operation="init",
            success="true",
            error_type="",
            pkg_version=self._pkg_version,
        ).inc()

    # FIXME
    # Remove me once Experiments.py has no further dependencies on
    # accessing internal `self.py_decider` instance directly
    def _validate_decider(self, decider: Optional[Any]) -> None:
        if decider is None:
            decider_client_counter.labels(
                operation="init",
                success="false",
                error_type="missing_decider",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderInitException(
                "rust_decider.init() returned `None` and did not initialize."
            )

        decider_err = decider.err()
        if decider_err:
            decider_client_counter.labels(
                operation="init",
                success="false",
                error_type="init_exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderInitException(f"rust_decider.init() has error: {decider_err}")

    # FIXME
    # Remove me once Experiments.py has no further dependencies on
    # accessing internal `self.py_decider` instance directly
    def get_decider(self):
        return self.py_decider

    def choose(
        self,
        feature_name: str,
        context: Mapping[str, JsonValue],
    ) -> Decision:
        """Return a :code:`Decision` for a given :code:`feature_name` and :code:`context`.

        If dict() is called on the Decision instance, the following fields are returned:
            .. code-block:: python
            {
                "variant": Optional[str],
                "value": Optional[JsonValue],
                "feature_id": int,
                "feature_name": str,
                "feature_version": int,
                "events": [str]
            }

        Raises :code:`DeciderException` if an error occurs when fetching the Decision.

        :param feature_name: Name of feature you want a variant or value for.

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides, targeting, & bucketing.

        :return: A :code:`Decision` instance if feature is active/exists,
            raises an :code:`FeatureNotFoundException` otherwise.
        """
        if context is None:
            decider_client_counter.labels(
                operation="choose",
                success="false",
                error_type="missing_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException(
                f"Missing `context` param for feature_name: {feature_name}"
            )

        ctx = make_ctx(context)
        ctx_err = ctx.err()
        if ctx_err:
            decider_client_counter.labels(
                operation="choose",
                success="false",
                error_type="invalid_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException(
                f"Encountered error from rust_decider.make_ctx() for context: {ctx_err}"
            )

        try:
            decision = self._decider.choose(feature_name, ctx)
        except FeatureNotFoundException as e:
            decider_client_counter.labels(
                operation="choose",
                success="false",
                error_type="feature_not_found",
                pkg_version=self._pkg_version,
            ).inc()
            raise e
        except DeciderException as e:
            decider_client_counter.labels(
                operation="choose",
                success="false",
                error_type="decider_exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise e
        except Exception as e:
            decider_client_counter.labels(
                operation="choose",
                success="false",
                error_type="exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise e

        decider_client_counter.labels(
            operation="choose",
            success="true",
            error_type="",
            pkg_version=self._pkg_version,
        ).inc()

        return Decision(
            variant=decision.variant_name,
            feature_id=decision.feature_id,
            feature_name=decision.feature_name,
            feature_version=decision.feature_version,
            value=decision.value,
            events=decision.event_data,
        )

    def choose_all(
        self,
        context: Mapping[str, JsonValue],
        bucketing_field_filter: Optional[str] = None,
    ) -> Dict[str, Decision]:
        """Return a :code:`Dict[str, Decision]` for all active features (with the key as the feature_name)...

        (not including features of :code:`"type": "dynamic_config"`) using the :code:`context` for bucketing.

        If dict() is called on a Decision instance, the following fields are returned:
            .. code-block:: python
            {
                "variant": Optional[str],
                "value": Optional[JsonValue],
                "feature_id": int,
                "feature_name": str,
                "feature_version": int,
                "events": [str]
            }

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides, targeting, & bucketing.

        :param bucketing_field_filter: An optional string used to filter out features to be bucketed.
            Features with a "bucket_val" field that does not match the
            :code:`bucketing_field_filter` param will be excluded from bucketing.

        :return: A dict of Decision instances as the values and the corresponding :code:`feature_name` as the key.
        """
        if context is None:
            decider_client_counter.labels(
                operation="choose_all",
                success="false",
                error_type="missing_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException("Missing `context` param")

        ctx = make_ctx(context)
        ctx_err = ctx.err()
        if ctx_err:
            decider_client_counter.labels(
                operation="choose_all",
                success="false",
                error_type="invalid_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException(
                f"Encountered error from rust_decider.make_ctx() for context: {ctx_err}"
            )

        try:
            all_decisions = self._decider.choose_all(ctx, bucketing_field_filter)
        except Exception as e:
            decider_client_counter.labels(
                operation="choose_all",
                success="false",
                error_type="exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise e

        output_decisions = {}

        for feature_name, decision in all_decisions.items():
            output_decisions[feature_name] = Decision(
                variant=decision.variant_name,
                feature_id=decision.feature_id,
                feature_name=decision.feature_name,
                feature_version=decision.feature_version,
                value=decision.value,
                events=decision.event_data,
            )

        decider_client_counter.labels(
            operation="choose_all",
            success="true",
            error_type="",
            pkg_version=self._pkg_version,
        ).inc()

        return output_decisions

    def get_bool(self, feature_name: str, context: Mapping[str, JsonValue]) -> bool:
        """Fetch a Dynamic Configuration of boolean type.

        Raises :code:`DeciderException` if an error occurs when fetching DC.

        Raises :code:`ValueTypeMismatchException` if requested feature is not of type boolean.

        :param feature_name: Name of the dynamic config you want a value for.

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides & targeting.

        :return: the boolean value of the dyanimc config if it is active/exists,
            raises an :code:`FeatureNotFoundException` otherwise.
        """
        return self._get_dynamic_config_value(
            feature_name, context, self._decider.get_bool
        )

    def get_int(self, feature_name: str, context: Mapping[str, JsonValue]) -> int:
        """Fetch a Dynamic Configuration of int type.

        Raises :code:`DeciderException` if an error occurs when fetching DC.

        Raises :code:`ValueTypeMismatchException` if requested feature is not of type integer.

        :param feature_name: Name of the dynamic config you want a value for.

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides & targeting.

        :return: the int value of the dyanimc config if it is active/exists,
            raises an :code:`FeatureNotFoundException` otherwise.
        """
        return self._get_dynamic_config_value(
            feature_name, context, self._decider.get_int
        )

    def get_float(self, feature_name: str, context: Mapping[str, JsonValue]) -> float:
        """Fetch a Dynamic Configuration of float type.

        Raises :code:`DeciderException` if an error occurs when fetching DC.

        Raises :code:`ValueTypeMismatchException` if requested feature is not of type float.

        :param feature_name: Name of the dynamic config you want a value for.

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides & targeting.

        :return: the float value of the dyanimc config if it is active/exists,
            raises an :code:`FeatureNotFoundException` otherwise.
        """
        return self._get_dynamic_config_value(
            feature_name, context, self._decider.get_float
        )

    def get_string(self, feature_name: str, context: Mapping[str, JsonValue]) -> str:
        """Fetch a Dynamic Configuration of string type.

        Raises :code:`DeciderException` if an error occurs when fetching DC.

        Raises :code:`ValueTypeMismatchException` if requested feature is not of type string.

        :param feature_name: Name of the dynamic config you want a value for.

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides & targeting.

        :return: the string value of the dyanimc config if it is active/exists,
            raises an :code:`FeatureNotFoundException` otherwise.
        """
        return self._get_dynamic_config_value(
            feature_name, context, self._decider.get_string
        )

    def get_map(
        self, feature_name: str, context: Mapping[str, JsonValue]
    ) -> Optional[dict]:
        """Fetch a Dynamic Configuration of map type.

        Raises :code:`DeciderException` if an error occurs when fetching DC.

        Raises :code:`ValueTypeMismatchException` if requested feature is not of type map.

        :param feature_name: Name of the dynamic config you want a value for.

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides & targeting.

        :return: the map value of the dyanimc config if it is active/exists,
            raises an :code:`FeatureNotFoundException` otherwise.
        """
        return self._get_dynamic_config_value(
            feature_name, context, self._decider.get_map
        )

    def _get_dynamic_config_value(
        self,
        feature_name: str,
        context: Mapping[str, JsonValue],
        get_fn: Callable,
    ) -> Optional[Any]:
        dc_type = get_fn.__name__

        if context is None:
            decider_client_counter.labels(
                operation=f"{dc_type}",
                success="false",
                error_type="missing_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException(
                f"Missing `context` param for feature_name: {feature_name}"
            )

        ctx = make_ctx(context)
        ctx_err = ctx.err()
        if ctx_err:
            decider_client_counter.labels(
                operation=f"{dc_type}",
                success="false",
                error_type="invalid_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException(
                f"Encountered error from rust_decider.make_ctx(): {ctx_err}"
            )

        try:
            dc = get_fn(feature_name, ctx)
        except FeatureNotFoundException as e:
            decider_client_counter.labels(
                operation=f"{dc_type}",
                success="false",
                error_type="feature_not_found",
                pkg_version=self._pkg_version,
            ).inc()
            raise e
        except ValueTypeMismatchException as e:
            decider_client_counter.labels(
                operation=f"{dc_type}",
                success="false",
                error_type="type_mismatch",
                pkg_version=self._pkg_version,
            ).inc()
            raise e
        except DeciderException as e:
            decider_client_counter.labels(
                operation=f"{dc_type}",
                success="false",
                error_type="decider_exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise e
        except Exception as e:
            decider_client_counter.labels(
                operation=f"{dc_type}",
                success="false",
                error_type="exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise e

        decider_client_counter.labels(
            operation=f"{dc_type}",
            success="true",
            error_type="",
            pkg_version=self._pkg_version,
        ).inc()

        return dc

    def all_values(
        self,
        context: Mapping[str, JsonValue],
    ) -> Dict[str, JsonValue]:
        """Return a :code:`Dict[str, JsonValue]` for all active Dynamic Configurations (with the key as the feature_name)...

        using the :code:`context` for overrides/targeting.

        The value of the return dict contains the Dynamic Config value.

        Dynamic Configurations that are malformed, fail parsing, or otherwise
        error for any reason are included in the response and have their respective default
        values set:

        .. code-block:: python

            boolean -> False
            integer -> 0
            float   -> 0.0
            string  -> ""
            map     -> {}

        :param context: A required :code:`Mapping[str, JsonValue]` of context fields used for
            feature overrides & targeting.

        :return: A dict of Dynamic Config :code:`JsonValue`s as the dict values and the corresponding :code:`feature_name` as the key.
        """
        if context is None:
            decider_client_counter.labels(
                operation="all_values",
                success="false",
                error_type="missing_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException("Missing `context` param")

        ctx = make_ctx(context)
        ctx_err = ctx.err()
        if ctx_err:
            decider_client_counter.labels(
                operation="all_values",
                success="false",
                error_type="invalid_context",
                pkg_version=self._pkg_version,
            ).inc()
            raise DeciderException(
                f"Encountered error from rust_decider.make_ctx() for context: {ctx_err}"
            )

        try:
            all_decisions = self._decider.all_values(ctx)
        except Exception as e:
            decider_client_counter.labels(
                operation="all_values",
                success="false",
                error_type="exception",
                pkg_version=self._pkg_version,
            ).inc()
            raise e

        values = {}

        for feature_name, decision in all_decisions.items():
            values[feature_name] = decision.value

        decider_client_counter.labels(
            operation="all_values",
            success="true",
            error_type="",
            pkg_version=self._pkg_version,
        ).inc()

        return values
