from typing import Any, List, Optional, Union

from chalk.features.dataframe import DataFrame
from chalk.features.feature_field import Feature, feature, feature_time, has_many, has_one
from chalk.features.feature_set import Features, FeatureSetBase, is_features_cls
from chalk.features.feature_set_decorator import features
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.filter import Filter, TimeDelta, after, before
from chalk.features.hooks import after_all, before_all
from chalk.features.resolver import Cron, ScheduleOptions, offline, online, sink
from chalk.features.tag import Environments, Tags
from chalk.utils import MachineType

__all__ = [
    "Cron",
    "DataFrame",
    "Environments",
    "Feature",
    "Features",
    "ScheduleOptions",
    "Tags",
    "after",
    "after_all",
    "before",
    "before_all",
    "description",
    "feature",
    "feature_time",
    "features",
    "has_many",
    "has_one",
    "is_primary",
    "offline",
    "online",
    "owner",
    "sink",
    "tags",
    "FeatureSetBase",
    "FeatureWrapper",
    "Filter",
    "TimeDelta",
    "unwrap_feature",
    "ensure_feature",
    "MachineType",
]


def is_primary(f: Any) -> bool:
    """
    Determine whether a feature is a primary key
    :param f: A feature (ie. User.email)
    :return: True if the feature is primary and False otherwise
    """
    # Typing f as Any as feature annotations will have the type of the feature, not the FeatureWrapper or Feature type
    return unwrap_feature(f).primary


def owner(f: Any) -> Optional[str]:
    """
    Get the owner for a feature or feature class
    :param f: A feature (ie. User.email or User)
    :return: The owner for a feature or feature class, if it exists.
    Note that the owner could be inherited from the feature class.
    """
    # Typing f as Any as feature annotations will have the type of the feature, not the FeatureWrapper or Feature type
    if is_features_cls(f):
        return f.__chalk_owner__
    if isinstance(f, (Feature, FeatureWrapper)):
        feature = unwrap_feature(f)
        return feature.owner
    raise TypeError(f"Could not determine the owner of {f} as it is neither a Feature or Feature Set")


def description(f: Any) -> Optional[str]:
    """
    Get the description of a feature or feature class
    :param f: A feature or feature class (ie. User.email or User)
    :return: The description given for the feature or feature class.
    """
    # Typing f as Any as feature annotations will have the type of the feature, not the FeatureWrapper or Feature type
    if is_features_cls(f):
        return f.__doc__
    if isinstance(f, (Feature, FeatureWrapper)):
        feature = unwrap_feature(f)
        return feature.description
    raise TypeError(f"Could not determine the description of {f} as it is neither a Feature or Feature Set")


def tags(f: Any) -> Optional[List[str]]:
    """
    Get the tags for a feature or feature class
    :param f: A feature or feature class (ie. User.email or User)
    :return: The tags given for the feature or feature class
    Note that the owner can be inherited from the feature class.
    """
    # Typing f as Any as feature annotations will have the type of the feature, not the FeatureWrapper or Feature type
    if is_features_cls(f):
        return f.__chalk_tags__
    if isinstance(f, (Feature, FeatureWrapper)):
        feature = unwrap_feature(f)
        return feature.tags
    raise TypeError(f"Could not determine the tags of {f} as it is neither a Feature or Feature Set")


def ensure_feature(feature: Union[str, Feature, FeatureWrapper, Any]) -> Feature:
    if isinstance(feature, str):
        return Feature.from_root_fqn(feature)
    if isinstance(feature, FeatureWrapper):
        return unwrap_feature(feature)
    if isinstance(feature, Feature):
        return feature
    raise TypeError(f"Feature identifier {feature} of type {type(feature).__name__} is not supported.")
