import yaml
from ..utils import config_path


def config(cfg):
    cfg_output = {}
    cfg = config_path(f"base/{cfg}")
    with open(cfg) as f:
        cfg_output.update(yaml.load(f, Loader=yaml.FullLoader))

    with open(config_path(cfg_output["data"])) as f:
        cfg_output.update(yaml.load(f, Loader=yaml.FullLoader))
    del cfg_output['data']

    with open(config_path(cfg_output["model"])) as f:
        cfg_output.update(yaml.load(f, Loader=yaml.FullLoader))
    del cfg_output['model']

    return cfg_output
