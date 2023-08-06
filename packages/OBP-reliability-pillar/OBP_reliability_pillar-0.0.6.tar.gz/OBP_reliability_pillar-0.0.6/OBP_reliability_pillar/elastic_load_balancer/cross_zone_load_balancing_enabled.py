from botocore.exceptions import ClientError
import logging

from OBP_reliability_pillar.elastic_load_balancer.utils import list_elb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def cross_zone_load_balancing_enabled(self) -> dict:
    """

    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_load_balancer :: cross_zone_load_balancing_enabled()")

    result = True
    failReason = ''
    offenders = []
    compliance_type = "Cross Zone Load Balancing Enabled"
    description = "Checks if cross zone load balancing is enabled or not"
    resource_type = "Elastic Load Balancer"

    regions = self.session.get_available_regions('elb')

    for region in regions:
        try:
            client = self.session.client('elb', region_name=region)
            elb_list = list_elb(self, region)

            for elb in elb_list:
                response = client.describe_load_balancer_attributes(
                    LoadBalancerName=elb
                )
                if not response['LoadBalancerAttributes']['CrossZoneLoadBalancing']['Enabled']:
                    result = False
                    failReason = 'AWS ELB cross zone load balancing is not enabled'
                    offenders.append(elb)

        except ClientError as e:
            logger.error("Something went wrong with the regions {}: {}".format(region, e))

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description
    }