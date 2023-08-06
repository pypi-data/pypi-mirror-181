import logging
import botocore
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# checks compliance.py for rds automatic minor version enabled
def rds_multi_az_support_enabled(self) -> dict:
    """

    @param self:
    @return dict: AWS RDS multi az support enabled compliance.py
    """
    logger.info(" ---Inside rds :: rds_multi_az_support_enabled()")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "RDS multi az support enabled"
    description = "Checks if multi az support is enabled for RDS instances."
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
                    multi_az = instance['MultiAZ']
                    if not multi_az:
                        result = False
                        failReason = "Multi az support is not enabled"
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