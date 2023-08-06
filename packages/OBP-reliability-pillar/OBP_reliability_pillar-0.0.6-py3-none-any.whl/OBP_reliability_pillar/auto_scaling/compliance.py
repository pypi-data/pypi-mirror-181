from OBP_reliability_pillar.auto_scaling.launch_config_public_ip_disabled import *
from OBP_reliability_pillar.auto_scaling.asg_elb_healthcheck_required import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# checks compliance.py for cloudwatch
def auto_scaling_compliance(self) -> dict:
    logger.info(" ---Inside auto_scaling_compliance()")
    response = [
        launch_config_public_ip_disabled(self),
        asg_elb_healthcheck_required(self)
    ]

    return response