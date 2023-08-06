from typing import Dict


class ProxyMixin:
    """Site wise proxy handler."""

    _proxies: Dict[str, str] = {}

    def with_proxy(self, proxy):
        """set the proxy url."""
        if proxy != '':
            self._proxies = {'https': proxy}
        return self
