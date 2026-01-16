from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseScene(ABC):
    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
