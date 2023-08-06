import logging
from typing import Dict

from deepdriver.sdk.config import Config
from deepdriver.sdk.data_types.run import set_run, Run

from deepdriver.sdk.interface import interface

from deepdriver import logger
from deepdriver import util
import deepdriver
from urllib.parse import urljoin


# 실행과 실험환경을 만드는 함수
@util.login_required
def init(exp_name: str="", team_name: str="", run_name: str="", config: Dict=None) -> Run:
    rsp = interface.init(exp_name, team_name, run_name, config)
    run_url = urljoin(f"http://{interface.get_http_host_ip()}:9111", rsp['runUrl'])
    run = Run(rsp["teamName"], rsp["expName"], rsp["runName"], rsp["runId"], run_url)
    logger.info("DeepDriver initialized\n"
        f"Team Name={rsp['teamName']}\n"
        f"Exp Name={rsp['expName']}\n"
        f"Run Name={rsp['runName']}\n"
        f"Run URL={run_url}"
    )
    set_run(run)

    # init config
    deepdriver.config = Config()
    if config:
        for key, value in config.items():
            setattr(deepdriver.config, key, value)

    return run
