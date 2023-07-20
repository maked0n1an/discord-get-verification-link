from urllib.parse import urlparse

class ProxyInfo:
    def __init__(self, username, password, hostname, port):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port

    @staticmethod
    def parse_proxy_url(proxy_url):
        parsed_proxy = urlparse(proxy_url)

        username = parsed_proxy.username
        password = parsed_proxy.password
        hostname = parsed_proxy.hostname
        port = parsed_proxy.port

        return ProxyInfo(username, password, hostname, port)