import logging
import botocore
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# checks compliance.py for rds automatic minor version enabled
def rds_automatic_minor_version_upgrade_enabled(self) -> dict:
    """
    :param self:
    :return dict: AWS RDS automatic minor version enabled compliance.py
    """
    logger.info(" ---Inside rds :: rds_automatic_minor_version_upgrade_enabled()")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "RDS instance automatic minor version upgrade enabled"
    description = "Checks if automatic minor version upgrade is enabled for RDS instances."
    resource_type = "RDS Instance"

    regions = self.session.get_available_regions('rds')

    for region in regions:
        try:
            client = self.session.client('rds', region_name=region)
            marker = ''
            while True:
                response = client.describe_db_instances(
                    MaxRecords=100,
                    Marker=marker
                )
                for instance in response['DBInstances']:
                    minor_version = instance['AutoMinorVersionUpgrade']
                    if not minor_version:
                        result = False
                        failReason = "Automatic minor version upgrade is not enabled"
                        offenders.append(region+': '+instance['DBInstanceIdentifier'])

                try:
                    marker = response['Marker']
                    if marker == '':
                        break
                except KeyError:
                    break
        except botocore.exceptions.ClientError as e:
            logger.error('Something went wrong with region {}: {}'.format(region, e))

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description
    }