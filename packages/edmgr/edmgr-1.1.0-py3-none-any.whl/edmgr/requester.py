from logging import getLogger
from typing import Optional
from urllib.parse import urljoin

from requests import RequestException, Session, Response


logger = getLogger(__name__)


class Requester:
    """
    An instance of this class communicates with service Mulesoft API.
    """

    def __init__(
        self, base_url: Optional[str] = None, token: Optional[str] = None, **kwargs
    ) -> None:
        """
        Create a edm_client instance with the provided options.

        :param base_url: string
        :param token: token for making api calls
        :param timeout: requests timeout
        :param raise_request_exc: re-raise RequestException(s) after logging them
        """
        self.base_url = base_url or ""
        self.__token = token
        self._session = Session()
        if token is not None:
            self._session.headers.update({"Authorization": f"Bearer {token}"})
        self.__kwargs = kwargs

    def send(
        self,
        method: str,
        endpoint: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[str] = None,
        headers: Optional[dict] = None,
        **kwargs,
    ) -> Optional[Response]:
        """
        Helper function to call the API

        :param endpoint: URL to the service
        :param method: HTTP verb
        :param payload: payload for the request
        :param headers: request headers
        :param timeout: request timeout
        :param raise_request_exc: re-raise RequestException(s) after logging them
        :return: API response
        """
        kwargs = {**self.__kwargs, **kwargs}
        timeout = kwargs.get("timeout")

        if endpoint:
            if not self.base_url.endswith("/"):
                base_url = self.base_url + "/"
            url = urljoin(base_url, endpoint)
        else:
            url = self.base_url

        try:
            return self._session.request(
                method=method,
                url=url,
                params=params,
                data=payload,
                headers=headers,
                timeout=timeout,
            )
        except RequestException as e:
            logger.error(str(e))
            if kwargs.get("raise_request_exc"):
                raise

    def get(
        self, endpoint: Optional[str] = None, params: Optional[dict] = None, **kwargs
    ) -> Optional[Response]:
        """Shortcut for invoking send() with method GET"""
        return self.send("GET", endpoint, params, **kwargs)

    @property
    def token(self) -> Optional[str]:
        return self.__token

    @token.setter
    def token(self, token: str) -> None:
        """
        Set the token for the request
        """
        logger.debug("Updating token in requester")
        self.__token = token
        self._session.headers.update({"Authorization": f"Bearer {token}"})
