from typing import Iterable

from benchling_api_client.v2.alpha.api.apps import (
    archive_canvases,
    create_canvas,
    get_benchling_app_manifest,
    get_canvas,
    put_benchling_app_manifest,
    unarchive_canvases,
    update_canvas,
)
from benchling_api_client.v2.alpha.models.benchling_app_manifest_alpha import BenchlingAppManifestAlpha
from benchling_api_client.v2.alpha.models.canvas import Canvas
from benchling_api_client.v2.alpha.models.canvas_create import CanvasCreate
from benchling_api_client.v2.alpha.models.canvas_update import CanvasUpdate
from benchling_api_client.v2.alpha.models.canvases_archival_change import CanvasesArchivalChange
from benchling_api_client.v2.alpha.models.canvases_archive import CanvasesArchive
from benchling_api_client.v2.alpha.models.canvases_archive_reason import CanvasesArchiveReason
from benchling_api_client.v2.alpha.models.canvases_unarchive import CanvasesUnarchive

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.v2.base_service import BaseService


class V2AlphaAppService(BaseService):
    """
    V2-Alpha Apps.

    Create and manage Apps on your tenant.

    https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps
    """

    @api_method
    def get_manifest(self, app_id: str) -> BenchlingAppManifestAlpha:
        """
        Get app manifest.

        See https://benchling.com/api/v2-alpha/reference?stability=la/Apps/getBenchlingAppManifest
        """
        response = get_benchling_app_manifest.sync_detailed(client=self.client, app_id=app_id)
        return model_from_detailed(response)

    @api_method
    def update_manifest(self, app_id: str, manifest: BenchlingAppManifestAlpha) -> BenchlingAppManifestAlpha:
        """
        Update an app manifest.

        See https://benchling.com/api/v2-alpha/reference?stability=la#/Apps/putBenchlingAppManifest
        """
        response = put_benchling_app_manifest.sync_detailed(
            client=self.client, app_id=app_id, yaml_body=manifest
        )
        return model_from_detailed(response)

    @api_method
    def create_canvas(self, canvas: CanvasCreate) -> Canvas:
        """
        Create an App Canvas that a Benchling App can write to and read user interaction from.

        See https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps/createCanvas
        """
        response = create_canvas.sync_detailed(
            client=self.client,
            json_body=canvas,
        )
        return model_from_detailed(response)

    @api_method
    def get_canvas(self, canvas_id: str) -> Canvas:
        """
        Get the current state of the App Canvas, including user input elements.

        See https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps/getCanvas
        """
        response = get_canvas.sync_detailed(
            client=self.client,
            canvas_id=canvas_id,
        )
        return model_from_detailed(response)

    @api_method
    def update_canvas(self, canvas_id: str, canvas: CanvasUpdate) -> Canvas:
        """
        Update App Canvas.

        See https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps/updateCanvas
        """
        response = update_canvas.sync_detailed(
            client=self.client,
            canvas_id=canvas_id,
            json_body=canvas,
        )
        return model_from_detailed(response)

    @api_method
    def archive_canvases(
        self, canvas_ids: Iterable[str], reason: CanvasesArchiveReason
    ) -> CanvasesArchivalChange:
        """
        Archive App Canvases.

        See https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps/archiveCanvases
        """
        archive_request = CanvasesArchive(reason=reason, canvas_ids=list(canvas_ids))
        response = archive_canvases.sync_detailed(
            client=self.client,
            json_body=archive_request,
        )
        return model_from_detailed(response)

    @api_method
    def unarchive_canvases(self, canvas_ids: Iterable[str]) -> CanvasesArchivalChange:
        """
        Unarchive App Canvases.

        See https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps/unarchiveCanvases
        """
        unarchive_request = CanvasesUnarchive(canvas_ids=list(canvas_ids))
        response = unarchive_canvases.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)
