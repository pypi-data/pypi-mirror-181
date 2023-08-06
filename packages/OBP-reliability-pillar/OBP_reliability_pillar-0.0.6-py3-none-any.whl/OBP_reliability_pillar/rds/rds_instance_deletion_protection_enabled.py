import logging
import botocore
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# checks compliance.py for rds automatic minor version enabled
def rds_instance_deletion_protection_enabled(self) -> dict:
    """

    @param self:
    @return dict: AWS RDS instance deletion protection enabled compliance.py
    """
    logger.info(" ---Inside rds :: rds_instance_deletion_protection_enabled()")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "RDS instance deletion protection enabled"
    description = "Checks if deletion protection is enabled for RDS instances."
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
                    deletion_protection = instance['DeletionProtection']
                    if not deletion_protection:
                        result = False
                        failReason = "Deletion protection is not enabled is not enabled"
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