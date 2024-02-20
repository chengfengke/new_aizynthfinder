""" Module containing a class for encapsulating the settings of the tree search
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import yaml
from aizynthfinder.context.policy import ExpansionPolicy, FilterPolicy
from aizynthfinder.context.scoring import ScorerCollection
from aizynthfinder.context.stock import Stock
from aizynthfinder.utils.logging import logger

if TYPE_CHECKING:
    from aizynthfinder.utils.type_utils import Any, Dict, List, Optional, StrDict, Union


@dataclass
class _PostprocessingConfiguration:
    min_routes: int = 5
    max_routes: int = 25
    all_routes: bool = False
    route_distance_model: Optional[str] = None
    route_scorer: str = "state score"


@dataclass
class _SearchConfiguration:
    algorithm: str = "mcts"
    algorithm_config: Dict[str, Any] = field(
        default_factory=lambda: {
            "C": 1.4,
            "default_prior": 0.5,
            "use_prior": True,
            "prune_cycles_in_search": True,
            "search_reward": "state score",
            "immediate_instantiation": (),
            "mcts_grouping": None,
        }
    )
    max_transforms: int = 6
    iteration_limit: int = 100
    time_limit: int = 120
    return_first: bool = False
    exclude_target_from_stock: bool = True
    break_bonds: List[List[int]] = field(default_factory=list)
    freeze_bonds: List[List[int]] = field(default_factory=list)
    break_bonds_operator: str = "and"


@dataclass
class Configuration:
    """
    Encapsulating the settings of the tree search, including the policy,
    the stock, the loaded scorers and various parameters.
    """

    search: _SearchConfiguration = field(default_factory=_SearchConfiguration)
    post_processing: _PostprocessingConfiguration = field(
        default_factory=_PostprocessingConfiguration
    )
    stock: Stock = field(init=False)
    expansion_policy: ExpansionPolicy = field(init=False)
    filter_policy: FilterPolicy = field(init=False)
    scorers: ScorerCollection = field(init=False)

    def __post_init__(self) -> None:
        self.stock = Stock()
        self.expansion_policy = ExpansionPolicy(self)
        self.filter_policy = FilterPolicy(self)
        self.scorers = ScorerCollection(self)
        self._logger = logger()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Configuration):
            return False
        for key, setting in vars(self).items():
            if isinstance(setting, (int, float, str, bool, list)):
                if (
                        vars(self)[key] != vars(other)[key]
                        or self.search != other.search
                        or self.post_processing != other.post_processing
                ):
                    return False
        return True

    @classmethod
    def from_dict(cls, source: StrDict) -> "Configuration":
        """
        Loads a configuration from a dictionary structure.
        The parameters not set in the dictionary are taken from the default values.
        The policies and stocks specified are directly loaded.

        :param source: the dictionary source
        :return: a Configuration object with settings from the source
        """
        expansion_config = source.pop("expansion", {})
        filter_config = source.pop("filter", {})
        stock_config = source.pop("stock", {})
        scorer_config = source.pop("scorer", {})

        config_obj = Configuration()
        config_obj._update_from_config(dict(source))

        config_obj.expansion_policy.load_from_config(**expansion_config)
        config_obj.filter_policy.load_from_config(**filter_config)
        config_obj.stock.load_from_config(**stock_config)
        config_obj.scorers.create_default_scorers()
        config_obj.scorers.load_from_config(**scorer_config)

        return config_obj

    @classmethod
    def from_file(cls, filename: str) -> "Configuration":
        """
        Loads a configuration from a yaml file.
        The parameters not set in the yaml file are taken from the default values.
        The policies and stocks specified in the yaml file are directly loaded.
        The parameters in the yaml file may also contain environment variables as
        values.

        :param filename: the path to a yaml file
        :return: a Configuration object with settings from the yaml file
        :raises:
            ValueError: if parameter's value expects an environment variable that
                does not exist in the current environment
        """
        with open(filename, "r") as fileobj:
            txt = fileobj.read()
        environ_var = re.findall(r"\$\{.+?\}", txt)
        for item in environ_var:
            if item[2:-1] not in os.environ:
                raise ValueError(f"'{item[2:-1]}' not in environment variables")
            txt = txt.replace(item, os.environ[item[2:-1]])
        _config = yaml.load(txt, Loader=yaml.SafeLoader)

        start_dir = os.getcwd()
        current_dir = start_dir
        while True:
            git_dir = os.path.join(current_dir, '.git')
            if os.path.exists(git_dir) and os.path.isdir(git_dir):
                break
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                print('请使用git进行项目管理')
            current_dir = parent_dir

        # 拼接绝对路径
        Configuration._update_paths(_config, current_dir)
        return Configuration.from_dict(_config)

    # 拼接工作路径
    @staticmethod
    def _update_paths(config, path_prefix):
        if isinstance(config, dict):
            for key, value in config.items():
                if isinstance(value, list):
                    config[key] = [os.path.join(path_prefix, item.lstrip('\\')) for item in value]
                elif isinstance(value, str) and value.startswith('\\'):
                    config[key] = os.path.join(path_prefix, value.lstrip('\\'))
                else:
                    Configuration._update_paths(value, path_prefix)
        elif isinstance(config, list):
            for i, item in enumerate(config):
                if isinstance(item, str) and item.startswith('\\'):
                    config[i] = os.path.join(path_prefix, item.lstrip('\\'))
                else:
                    Configuration._update_paths(item, path_prefix)

    def _update_from_config(self, config: StrDict) -> None:
        self.post_processing = _PostprocessingConfiguration(
            **config.pop("post_processing", {})
        )

        search_config = config.pop("search", {})
        for setting, value in search_config.items():
            if value is None:
                continue
            if not hasattr(self.search, setting):
                raise AttributeError(f"Could not find attribute to set: {setting}")
            if setting.endswith("_bonds"):
                if not isinstance(value, list):
                    raise ValueError("Bond settings need to be lists")
                value = _handle_bond_pair_tuples(value) if value else []
            if setting == "algorithm_config":
                if not isinstance(value, dict):
                    raise ValueError("algorithm_config settings need to be dictionary")
                self.search.algorithm_config.update(value)
            else:
                setattr(self.search, setting, value)


def _handle_bond_pair_tuples(bonds: List[List[int]]) -> List[List[int]]:
    if not all(len(bond_pair) == 2 for bond_pair in bonds):
        raise ValueError("Lists of bond pairs to break/freeze should be of length 2")
    return [bond_pair[:2] for bond_pair in bonds]
