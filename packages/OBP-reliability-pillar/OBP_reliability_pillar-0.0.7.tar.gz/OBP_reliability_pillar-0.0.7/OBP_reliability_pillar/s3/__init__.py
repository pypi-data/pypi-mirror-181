
class s3:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import s3_compliance