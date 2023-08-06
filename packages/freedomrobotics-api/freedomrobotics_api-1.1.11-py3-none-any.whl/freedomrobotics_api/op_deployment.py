import json

from .entity import Entity
from .op_deployment_service import OPDeploymentService


class OPDeployment(Entity):
    pk = 'id'

    @property
    def url_base(self):
        return '/accounts/{}/op-deployments'.format(self.account_id)

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
        """str: Service name.
        """
        return self._data.get("name")

    def get_op_deployment_services(self, attributes=None, params=None, raw=False, api_call_kwargs={}):
        """:obj:`list` : Fetch a list of deployment-services for this deployment.

        Args:
            attributes (list): Optional list of deployment-service attributes to return.
            params (dict): Optional query parameters.
            raw (bool): Will return the raw JSON if True. False by default.
            api_call_kwargs (dict): Optional keyword arguments for api call.
        """
        if params is None:
            params = {}
        if attributes is not None:
            params["attributes"] = json.dumps(attributes)
        params['op_deployment_id'] = self._id

        deployment_services_data = self.api.call(
            "GET",
            OPDeploymentService(None, _data={'account_id': self.account_id}).url_base,
            params=params, **api_call_kwargs)
        if not deployment_services_data:
            return []
        if raw:
            deployment_services = deployment_services_data
        else:
            deployment_services = [
                OPDeploymentService(ds_data["id"], ds_data) for ds_data in deployment_services_data
            ]
        return deployment_services
