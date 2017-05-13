from scrapy.dupefilter import RFPDupeFilter

class CookieRFPDupeFilter(RFPDupeFilter):
    name = "CookieRFPDupeFilter"
    def __init__(self, path=None, debug=False):
        super(CookieRFPDupeFilter, self).__init__(path, debug)

    def request_fingerprint(self, request):
        return request_fingerprint(request, include_headers=['Cookie'])
