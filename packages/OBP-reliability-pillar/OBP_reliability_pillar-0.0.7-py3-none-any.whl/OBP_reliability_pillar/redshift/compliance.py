import logging
from OBP_reliability_pillar.redshift.redshift_backup_enabled import redshift_backup_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def  redshift_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside redshift :: redshift_compliance()")

    response = [
        redshift_backup_enabled(self)
    ]

    return response