
class rds:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import rds_compliance
