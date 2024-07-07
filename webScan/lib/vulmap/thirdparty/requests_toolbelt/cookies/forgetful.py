"""The module containing the code for ForgetfulCookieJar."""
from lib.vulmap.thirdparty.requests.cookies from lib.vulmap.thirdparty import requestsCookieJar


class ForgetfulCookieJar(RequestsCookieJar):
    def set_cookie(self, *args, **kwargs):
        return
