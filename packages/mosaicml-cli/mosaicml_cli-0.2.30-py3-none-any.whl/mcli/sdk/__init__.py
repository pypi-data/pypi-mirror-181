"""Primary import target for the Python API"""

from mcli.config import FeatureFlag, MCLIConfig

if MCLIConfig.load_config(safe=True).feature_enabled(FeatureFlag.USE_MCLOUD):
    from mcli.api.runs import *
    from mcli.api.secrets import *
else:
    from mcli.api.kube.runs import *
