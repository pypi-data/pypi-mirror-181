import logging

from OBP_reliability_pillar.ec2.ec2_instance_detailed_monitoring_enabled import ec2_instance_detailed_monitoring_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def ec2_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_compliance()")

    response = [
        ec2_instance_detailed_monitoring_enabled(self),
    ]

    return response