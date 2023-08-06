import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def redshift_backup_enabled(self) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside redshift :: redshift_backup_enabled()")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "Redshift Backup Enabled"
    description = "Checks if backup is enabled on redshift cluster or not"
    resource_type = "Redshift"

    regions = self.session.get_available_regions('redshift')

    for region in regions:
        try:
            client = self.session.client('redshift', region_name=region)
            marker = ''
            while True:
                if marker == '' or marker is None:
                    response = client.describe_clusters()
                else:
                    response = client.describe_clusters(
                        Marker=marker
                    )
                for cluster in response['Clusters']:
                    retention_period = cluster['AutomatedSnapshotRetentionPeriod']
                    if retention_period <= 0:
                        result = False
                        failReason = "Redshift backup is not enabled"
                        offenders.append(region + ': ' + cluster['ClusterIdentifier'])

                try:
                    marker = response['Marker']
                    if marker == '':
                        break
                except KeyError:
                    break
        except ClientError as e:
            logger.error("Something went wrong with region {}: {}".format(region, e))

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description
    }