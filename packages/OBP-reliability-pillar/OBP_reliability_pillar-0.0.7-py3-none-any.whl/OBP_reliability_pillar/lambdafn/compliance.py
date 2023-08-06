from OBP_reliability_pillar.lambdafn.lambda_dlq_check import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks aws lambda compliance
def lambda_compliance(self) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside lambdafn :: lambda_compliance()")
    response = [
        lambda_dlq_check(self)
    ]

    return response