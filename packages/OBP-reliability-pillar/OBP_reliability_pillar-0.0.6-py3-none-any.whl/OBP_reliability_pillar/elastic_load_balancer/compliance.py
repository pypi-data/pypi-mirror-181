import logging
from OBP_reliability_pillar.elastic_load_balancer.cross_zone_load_balancing_enabled import \
    cross_zone_load_balancing_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def elb_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_load_balancer :: elb_compliance()")

    response = [
        cross_zone_load_balancing_enabled(self),
    ]

    return response