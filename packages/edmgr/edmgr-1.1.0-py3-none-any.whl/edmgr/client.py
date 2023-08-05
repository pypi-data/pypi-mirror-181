from logging import getLogger
import json
from typing import BinaryIO, Optional, Union
from urllib.parse import urljoin

from msal import TokenCache
import requests

from edmgr.auth import (
    msal_login,
    msal_logout,
    decode_jwt_token,
)
from edmgr.config import settings
from edmgr.download import HTTPDownload, FASPSpec
from edmgr.exceptions import EdmAuthError, EdmAPIError, EdmTokenNotFound, EdmEulaError
from edmgr.requester import Requester


logger = getLogger(__name__)


def _handle_response(response: Optional[requests.Response]) -> Optional[dict]:
    if response is not None:
        try:
            response.raise_for_status()
        except requests.HTTPError as http_err:
            logger.debug(str(http_err))
            if response.status_code == 401:
                raise EdmAuthError("Unauthorized.")
            try:
                response_body = response.json()
            except json.JSONDecodeError as e:
                raise EdmAPIError(f"Cannot decode response body: {e}") from e
            if response_body.get("errorName"):
                return response_body
            raise
        try:
            response_body = response.json()
            if response_body:
                return response_body
        except json.JSONDecodeError as e:
            raise EdmAPIError(f"Invalid response body: {e}") from e


def _handle_eula_error(payload: dict) -> Optional[dict]:
    if payload and payload.get("errorName") == "download-error-eula-required":
        return {
            "name": "eula-error",
            "description": payload.get("errorDescription"),
            "url": payload.get("agreementUrl"),
        }


class Client:
    """
    client = Client()
    client = Client(token='token')
    client = Client(username='username', password='password')
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        msal_cache: Optional[TokenCache] = None,
        check_jwt_signature: bool = True,
        **kwargs,
    ) -> None:
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.__init_token: Optional[str] = token
        self.__token: Optional[str] = None
        self.__msal_cache: Optional[TokenCache] = msal_cache
        self._check_jwt_signature = check_jwt_signature
        self.__kwargs = kwargs
        entitlements_endpoint = urljoin(
            settings.get("base_url"), settings.get("entitlement_endpoint")
        )
        self.entitlements_api = Requester(
            base_url=entitlements_endpoint,
            timeout=kwargs.get("timeout"),
            raise_request_exc=kwargs.get("raise_request_exc"),
        )
        self._acquire_token(timeout=kwargs.get("timeout"), allow_null=True)

    @property
    def token(self) -> Optional[str]:
        return self.__token

    @token.setter
    def token(self, token: str) -> None:
        self._set_token(token, check_signature=self._check_jwt_signature)

    def _set_token(self, token: str, check_signature: bool = True) -> dict:
        logger.debug(f"Verify token: check_signature={check_signature}")
        payload = decode_jwt_token(token, check_signature=check_signature)
        self.__token = token
        self.entitlements_api.token = token
        return payload

    def _acquire_token(
        self, timeout: Optional[Union[float, tuple]] = None, allow_null: bool = False
    ) -> None:
        logger.debug(f"Acquiring token: allow_null={allow_null}")
        # If the current instance has a valid token already, do nothing
        if self.__token is not None:
            logger.debug("Using instance token")
            try:
                self._set_token(self.__token, check_signature=False)
                return
            except EdmAuthError:
                pass
        # otherwise, if the current instance was instanciated with a token, use it
        if self.__init_token is not None:
            logger.debug("Using init token")
            self._set_token(
                self.__init_token, check_signature=self._check_jwt_signature
            )
        # otherwise, if an access token is set in the config module, use it
        elif settings.get("access_token") is not None:
            logger.debug("Using settings token")
            self._set_token(
                settings["access_token"], check_signature=self._check_jwt_signature
            )
        # otherwise, get an access token from msal:
        #   - if username and password are provided and the token is expired, a
        #     new one will be acquired
        #   - if no username and password are provided, self.__msal_cache will
        #     be used to acquire the token
        #   - if no user/password or msal_cache is empty/invalid, raise EdmAuthError
        elif (self.username is not None and self.password is not None) or (
            self.__msal_cache is not None
        ):
            logger.debug("Acquiring token from MSAL")
            access_token = msal_login(
                username=self.username,
                password=self.password,
                timeout=timeout,
                cache=self.__msal_cache,
            )
            self._set_token(access_token, check_signature=False)
        elif not allow_null:
            raise EdmTokenNotFound("Access token not found.")

    def logout(self):
        """Sign out, remove accout from MSAL cache and remove access token from Client"""
        if self.__msal_cache is not None:
            msal_logout(self.__msal_cache)
            self.__msal_cache = TokenCache()
        self.__token = None

    def get_entitlements(
        self,
        entitlement_id: Optional[str] = None,
        params: Optional[dict] = None,
        **kwargs,
    ) -> list:
        """
        Call the entitlements API and get a list of entitlements

        :param entitlement_id: Entitlement ID
        :param params: Query params
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: a list of entitlements
        """
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))
        if entitlement_id is not None:
            url = str(entitlement_id)
        else:
            url = ""
        response: Optional[requests.Response] = self.entitlements_api.get(
            url, params, **kwargs
        )

        data: Optional[dict] = _handle_response(response)

        if data:
            if entitlement_id is not None:
                return [data]
            return data.get("items", [])
        return []

    def find_entitlements(
        self,
        search_query: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs,
    ) -> list:
        """
        Call the entitlements API and get a list of entitlements that match the
        query.

        :param query: dict containing search parameters
        :param params: extra request parameters
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: a list of entitlements
        """
        if search_query is None:
            search_query = {}
        if params is None:
            params = {}
        search: str = json.dumps(search_query, separators=(",", ":"))
        return self.get_entitlements(params={"search": search, **params}, **kwargs)

    def get_releases(
        self,
        entitlement_id: str,
        release_id: Optional[str] = None,
        params: Optional[dict] = None,
        **kwargs,
    ) -> list:
        """
        Call the entitlements API with the entitlement ID to get a list of product releases

        :param entitlement_id: Entitlement ID
        :param release_id: Release ID
        :param params: Query params
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: a list of product releases
        """
        logger.debug(f"get_releases {kwargs}")
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))

        parts = [f"{entitlement_id}/rights/download/releases"]
        if release_id is not None:
            parts.append(release_id)
        url = "/".join(parts)
        response: Optional[requests.Response] = self.entitlements_api.get(
            url, params, **kwargs
        )

        data: Optional[dict] = _handle_response(response)

        if data:
            if release_id is not None:
                return [data]
            return data.get("items", [])
        return []

    def get_artifacts(
        self,
        entitlement_id: str,
        release_id: str,
        artifact_id: Optional[str] = None,
        **kwargs,
    ) -> list:
        """
        Call the entitlements API with the entitlement ID and release ID to get a list of artifacts

        :param entitlement_id: entitlement ID
        :param release_id: release ID
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: a list of artifacts
        """
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))

        parts = [f"{entitlement_id}/rights/download/releases/{release_id}"]
        if artifact_id is not None:
            parts.append(f"artifact/{artifact_id}")
        url = "/".join(parts)
        response: Optional[requests.Response] = self.entitlements_api.get(url, **kwargs)
        data: Optional[dict] = _handle_response(response)

        if data:
            if artifact_id is not None:
                return [data]
            return data.get("artifacts", [])
        return []

    def get_artifact_download_url(
        self, entitlement_id: str, release_id: str, artifact_id: str, **kwargs
    ) -> dict:
        """
        Call the entitlements API with the entitlement ID, release ID, and artifact_id to get an artifact's HTTP
        download url.
        Then filters based on Artifact ID

        :param artifact_id: artifact ID
        :param entitlement_id: entitlement ID
        :param release_id: release ID
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: None or a list of artifacts
        """
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))
        response: Optional[requests.Response] = self.entitlements_api.get(
            f"{entitlement_id}/rights/download/releases/{release_id}/artifact/{artifact_id}/http",
            **kwargs,
        )
        data: Optional[dict] = _handle_response(response)
        if not data:
            raise EdmAPIError(
                "Couldn't find download URL for"
                f" Entitlement ID: {entitlement_id}, Release ID: {release_id} and Artifact ID: {artifact_id}"
            )
        return data

    def get_artifact_fasp_spec(
        self, entitlement_id: str, release_id: str, artifact_id: str, **kwargs
    ) -> dict:
        """
        Call the entitlements API with the entitlement ID, release ID, and artifact_id to get the FASP Specs for
        downloading an artifact using IBM Aspera FASP protocol.
        Then filters based on Artifact ID

        :param artifact_id: artifact ID
        :param entitlement_id: entitlement ID
        :param release_id: release ID
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: None or a list of artifacts
        """
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))
        response: Optional[requests.Response] = self.entitlements_api.get(
            f"{entitlement_id}/rights/download/releases/{release_id}/artifact/{artifact_id}/fasp",
            **kwargs,
        )
        data: Optional[dict] = _handle_response(response)
        if not data:
            raise EdmAPIError(
                "Couldn't find FASP spec for"
                f" Entitlement ID: {entitlement_id}, Release ID: {release_id} and Artifact ID: {artifact_id}"
            )
        return data

    def get_artifact_download_http(
        self, entitlement_id: str, release_id: str, artifact_id: str, **kwargs
    ) -> HTTPDownload:
        """
        Call the entitlements API with the entitlement ID, release ID, and artifact_id,
        (filter results based on Artifact ID) and use the obtained download URL
        to construct a HTTPDownload stream object.

        :param artifact_id: artifact ID
        :param entitlement_id: entitlement ID
        :param release_id: release ID
        :raises EdmAPIError: If the response body is invalid or the dowload URL is not found
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: HTTPDownload stream object
        """
        download_response: dict = self.get_artifact_download_url(
            entitlement_id=entitlement_id,
            release_id=release_id,
            artifact_id=artifact_id,
            **kwargs,
        )
        error = _handle_eula_error(download_response)
        if error:
            return HTTPDownload(error=error)
        download_url = download_response.get("downloadUrl")
        if not download_url:
            raise EdmAPIError("Invalid download URL")
        file_response = requests.get(download_url, stream=True)
        return HTTPDownload(content=file_response)

    def _get_artifact_download_fasp(
        self, entitlement_id: str, release_id: str, artifact_id: str, **kwargs
    ) -> FASPSpec:
        spec_response: dict = self.get_artifact_fasp_spec(
            entitlement_id=entitlement_id,
            release_id=release_id,
            artifact_id=artifact_id,
            **kwargs,
        )
        error = _handle_eula_error(spec_response)
        if error:
            return FASPSpec(error=error)
        spec = (
            spec_response.get("data", {})
            .get("transfer_specs", [{}])[0]
            .get("transfer_spec")
        )
        return FASPSpec(spec=spec)

    def download_artifact(
        self,
        fp: BinaryIO,
        entitlement_id: str,
        release_id: str,
        artifact_id: str,
        chunk_size: int = 1024,
        **kwargs,
    ) -> int:
        """
        Attemp to download and write an artifact based on entitlement ID, release ID, and artifact ID
        parameters.

        :param fp: A binary file-like object
        :param artifact_id: artifact ID
        :param entitlement_id: entitlement ID
        :param release_id: release ID
        :param chunk_size: The artifact will be downloaded and written in chunks of chunk_size
        :raises EdmAPIError: If the response body is invalid or the dowload URL is not found
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :raises EdmEulaError: If EULA was not signed for the artifact
        :return: The number of bytes written
        """
        download_stream: HTTPDownload = self.get_artifact_download_http(
            entitlement_id=entitlement_id,
            release_id=release_id,
            artifact_id=artifact_id,
            **kwargs,
        )
        if download_stream.error.get("name") == "eula-error":
            raise EdmEulaError(
                "EULA not signed",
                description=download_stream.error["description"],
                eula_url=download_stream.error["url"],
            )
        bytes_written = 0
        with download_stream as stream:
            for chunk in stream.iter_content(chunk_size=chunk_size):
                data_size = fp.write(chunk)
                bytes_written += data_size
        return bytes_written
