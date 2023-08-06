# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_tea_util import models as util_models
from alibabacloud_edsofficeservice20221125 import models as eds_office_service_20221125_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('edsofficeservice', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def create_desktop_pool_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> eds_office_service_20221125_models.CreateDesktopPoolResponse:
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='CreateDesktopPool',
            version='2022-11-25',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            eds_office_service_20221125_models.CreateDesktopPoolResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_desktop_pool_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> eds_office_service_20221125_models.CreateDesktopPoolResponse:
        req = open_api_models.OpenApiRequest()
        params = open_api_models.Params(
            action='CreateDesktopPool',
            version='2022-11-25',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            eds_office_service_20221125_models.CreateDesktopPoolResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_desktop_pool(self) -> eds_office_service_20221125_models.CreateDesktopPoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_desktop_pool_with_options(runtime)

    async def create_desktop_pool_async(self) -> eds_office_service_20221125_models.CreateDesktopPoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_desktop_pool_with_options_async(runtime)
