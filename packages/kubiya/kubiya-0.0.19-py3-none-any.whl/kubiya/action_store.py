from typing import List, Dict, NoReturn, Any, Iterable, Optional
import inspect
from logging import getLogger


logger = getLogger(__name__)

class ActionStore:
    """handles kubiya actions and exeution"""

    _instances = list()

    @classmethod
    def register_action_store(cls, action_store: "ActionStore") -> NoReturn:
        cls._instances.append(action_store)
    
    def __init__(self, store_name: str, version: str = "testing") -> None:
        assert store_name != "", "store_name cannot be empty"
        self._registered_actions = {}
        self._registered_secrets = []
        self._name = store_name
        self._version = version
        self.__class__.register_action_store(self)

    @classmethod
    def validate_action(cls, action: callable) -> NoReturn:
        cls._validate_action_is_callable(action)
        cls._validate_action_signature(action)

    @classmethod
    def _validate_action_is_callable(cls, action: callable) -> NoReturn:
        assert callable(
            action
        ), f"{action} must be callable in order to be registered as an action"

    @classmethod
    def _validate_action_signature(cls, action: callable) -> NoReturn:
        sig = inspect.signature(action)
        mandatory_args = [
            nm
            for nm, par in sig.parameters.items()
            if par.default == inspect.Signature.empty
            and par.kind not in (par.VAR_KEYWORD, par.VAR_POSITIONAL)
        ]
        if len(mandatory_args) > 1:
            raise AssertionError(
                f"{action} must have at most 1 mandatory argument ({mandatory_args})"
            )

    def register_action(self, action_name: str, action: callable) -> NoReturn:
        self.validate_action(action)
        self._registered_actions[action_name] = action

    def uses_secrets(self, secret_names: Iterable[str]) -> NoReturn:
        self._registered_secrets.extend(secret_names)

    def get_registered_actions(self) -> List[str]:
        return list(self._registered_actions.keys())

    def get_registered_action_info(self, action_name: str) -> callable:
        assert (
            action_name in self._registered_actions
        ), f"`{action_name}` is not a registered action"
        return self._registered_actions[action_name]

    def get_registered_actions_info(self) -> List[callable]:
        return self._registered_actions.values()

    def get_registered_secrets(self) -> List[str]:
        return self._registered_secrets

    def execute_action(self, action_name: str, input: Optional[Dict]) -> Any:
        assert (
            action_name in self._registered_actions
        ), f"`{action_name}` is not a registered action"
        action = self._registered_actions[action_name]
        if input is None:
            return action()
        else:
            return action(input)

    def get_version(self) -> str:
        return self._version

    def get_name(self) -> str:
        return self._name
