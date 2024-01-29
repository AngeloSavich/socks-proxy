import requests
import socks
import socket

class Socks5ProxyHTTPSClient:
    """
    A class to make HTTPS requests through a SOCKS5 proxy.
    """

    def __init__(self, proxy_host, proxy_port):
        """
        Initializes the client with the given proxy settings.

        :param proxy_host: The hostname or IP address of the SOCKS5 proxy.
        :param proxy_port: The port number of the SOCKS5 proxy.
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.setup_proxy()

    def setup_proxy(self):
        """
        Configures the SOCKS5 proxy for domain resolution.
        """
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, self.proxy_host, self.proxy_port)
        socket.socket = socks.socksocket

    def make_request(self, url, method='GET', **kwargs):
        """
        Makes an HTTPS request through the SOCKS5 proxy.

        :param url: The URL for the request.
        :param method: The HTTP method to use ('GET', 'POST', etc.).
        :param kwargs: Additional arguments to pass to requests.request.
        :return: A requests.Response object.
        """
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
proxy_client = Socks5ProxyHTTPSClient('localhost', 49000)
response = proxy_client.make_request('https://api.example.com/data')
if response:
    print(response.text)


class Socks5ProxyHTTPSClientTemporary:
    """
    A class to make HTTPS requests through a SOCKS5 proxy.
    """

    def __init__(self, proxy_host, proxy_port):
        """
        Initializes the client with the given proxy settings.
        """
        self.session = requests.Session()
        self.session.proxies = {
            'http': f'socks5://{proxy_host}:{proxy_port}',
            'https': f'socks5://{proxy_host}:{proxy_port}'
        }

    def make_request(self, url, method='GET', **kwargs):
        """
        Makes an HTTPS request through the SOCKS5 proxy.
        """
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
