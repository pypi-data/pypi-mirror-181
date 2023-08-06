import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns the list of load balancers
def list_elb(self, region: str)-> list:
    logger.info(" ---Inside list_elb()")
    res = []
    client = self.session.client('elb', region_name= region)

    marker = ''
    while True:
        if marker == '' or marker is None:
            response = client.describe_load_balancers()
        else:
            response = client.describe_load_balancers(
                Marker=marker
            )
        for lb in response['LoadBalancerDescriptions']:
            res.append(lb['LoadBalancerName'])

        try:
            marker = response['NextMarker']
            if marker == '':
                break
        except KeyError:
            break

    return res
