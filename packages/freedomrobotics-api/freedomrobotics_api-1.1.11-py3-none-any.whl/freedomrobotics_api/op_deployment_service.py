from .entity import Entity


class OPDeploymentService(Entity):
    pk = 'id'

    @property
    def url_base(self):
        return '/accounts/{}/op-deployment-services'.format(self.account_id)

    @property
    def url_id(self):
        return '{}/{}'.format(self.url_base, self._id)

    @property
    def account_id(self):
        """str: Account id.
        """
        return self._data.get("account_id")

    @property
    def name(self):
        """str: Deployment name.
        """
        return self._data.get("name")

    @property
    def configuration(self):
        """dict: Deployment-service configuration.
        """
        return self._data.get("configuration")
