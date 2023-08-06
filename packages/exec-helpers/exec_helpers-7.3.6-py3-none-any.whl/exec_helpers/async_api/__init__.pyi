#    Copyright 2018 - 2021 Alexey Stepanov aka penguinolog.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at

#         http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Execution helpers for simplified usage of subprocess. Async version.

.. versionadded:: 3.0.0
"""

# noinspection PyUnresolvedReferences
__all__ = (
    # pylint: disable=undefined-all-variable
    # lazy load
    # API
    "ExecHelper",
    "ExecResult",
    # Expensive
    "Subprocess",
)

# Standard Library
import typing

# Local Implementation
from .api import ExecHelper
from .exec_result import ExecResult
from .subprocess import Subprocess  # nosec  # Expected

_deprecated: typing.Dict[str, str] = ...

def __getattr__(name: str) -> typing.Any:
    """Get attributes lazy.

    :return: attribute by name
    :raises AttributeError: attribute is not defined for lazy load
    """
