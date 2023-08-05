from . import crawler_data_processor_pb2_grpc as importStub

class DataProcessorService(object):

    def __init__(self, router):
        self.connector = router.get_connection(DataProcessorService, importStub.DataProcessorStub)

    def CrawlerConnect(self, request, timeout=None, properties=None):
        return self.connector.create_request('CrawlerConnect', request, timeout, properties)

    def IntervalStart(self, request, timeout=None, properties=None):
        return self.connector.create_request('IntervalStart', request, timeout, properties)

    def SendEvent(self, request, timeout=None, properties=None):
        return self.connector.create_request('SendEvent', request, timeout, properties)

    def SendMessage(self, request, timeout=None, properties=None):
        return self.connector.create_request('SendMessage', request, timeout, properties)