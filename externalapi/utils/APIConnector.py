from aiohttp import ClientSession, TCPConnector

from types import TracebackType
from typing import Optional, Type


class APIConnector:
    @property
    def session(self) -> ClientSession:
        """Session creation is enclosed here."""
        if not hasattr(self, '_session'):
            self._session = None
        if not hasattr(self, '_session_headers'):
            raise AttributeError('_session_headers MUST be defined in child class')

        if self._session is None:
            self._session = ClientSession(
                headers=self._session_headers,
                connector=TCPConnector(verify_ssl=False)
            )
        return self._session

    async def close(self) -> None:
        """Do not forget to close session if methods with arg auto_close_session equal to False called."""
        session = self.session
        if session is not None:
            await session.close()

    async def __aenter__(self):
        """Enable async context manager use of APIConnector."""
        return self

    async def __aexit__(self,
                        exc_type: Optional[Type[Exception]],
                        exc: Optional[Exception],
                        exc_tb: Optional[TracebackType]) -> None:
        """Enable async context manager use of APIConnector."""
        await self.close()
