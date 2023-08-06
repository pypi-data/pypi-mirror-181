from OBP_reliability_pillar.rds.rds_automatic_minor_version_upgrade_enabled import *
from OBP_reliability_pillar.rds.rds_enhanced_monitoring_enabled import *
from OBP_reliability_pillar.rds.rds_multi_az_support_enabled import *
from OBP_reliability_pillar.rds.rds_instance_deletion_protection_enabled import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def rds_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside rds :: rds_compliance()")

    response = [
        rds_multi_az_support_enabled(self),
        rds_instance_deletion_protection_enabled(self),
        rds_enhanced_monitoring_enabled(self),
        rds_automatic_minor_version_upgrade_enabled(self)
    ]

    return response