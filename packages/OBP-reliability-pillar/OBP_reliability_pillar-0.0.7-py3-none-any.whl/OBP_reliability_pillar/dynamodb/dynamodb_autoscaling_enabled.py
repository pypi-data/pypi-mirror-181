import botocore
import logging

from OBP_reliability_pillar.dynamodb.utils import list_dynamodb_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance.py for dynamodb auto-scaling is enabled
def dynamodb_autoscaling_enabled(self) -> dict:
    """

    :param self:
    :return:
    """
    logger.info(" ---Inside dynamodb :: dynamodb_autoscaling_enabled()")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "Dynamodb autoscaling enabled"
    description = "Checks if Auto Scaling or On-Demand is enabled on your DynamoDB tables"
    resource_type = "Dynamodb"

    regions = self.session.get_available_regions('dynamodb')

    for region in regions:
        try:
            client = self.session.client('dynamodb',region_name=region)

            dynamodb_tables = list_dynamodb_tables(client)
            for table in dynamodb_tables:
                response = client.describe_table(
                    TableName=table
                )
                global_secondary_index = [index_name['IndexName'] for index_name in response['table']['GlobalSecondaryIndexes']]
                response_scalable_targets = client.describe_scalable_targets(
                    ServiceNamespace='dynamodb',
                    ResourceIds= [table].extend(global_secondary_index)
                )
                if len(response_scalable_targets['ScalableTargets']) == 0:
                    result = False
                    failReason = 'AWS DynamoDB Auto Scaling is not enabled for the table and/or its global secondary index.'
                    offenders.append(table)
        except botocore.exceptions.ClientError as e:
            logger.error("Something went wrong with region {}: {}".format(region, e))

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description
    }
