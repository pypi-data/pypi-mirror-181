import logging
from OBP_reliability_pillar.s3.s3_bucket_replication_enabled import s3_bucket_replication_enabled
from OBP_reliability_pillar.s3.s3_bucket_versioning_enabled import s3_bucket_versioning_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def s3_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside s3 :: s3_compliance()")

    response = [
        s3_bucket_replication_enabled(self),
        s3_bucket_versioning_enabled(self)
    ]

    return response