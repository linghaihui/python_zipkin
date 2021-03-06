import requests
import datetime
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.config import Configurator
from py_zipkin.zipkin import create_http_headers_for_new_span
from wsgiref.simple_server import make_server

class ZipkinNode(object):
    connect_url='http://localhost:9001/api'
    zipkin_url='http://localhost:9411'
    zipkin_span_api=zipkin_url+'/api/v1/spans'
    zipkin_service_name='default_service_name'
    config=None

    def zipkin_handler(self,stream_name, encoded_span):
      requests.post(
          self.zipkin_span_api,
          data=encoded_span,
          headers={'Content-Type': 'application/x-thrift'},
      )

    def init_zipkin_settings(self,service_name): 
      settings = {}
      settings['service_name'] = service_name
      self.zipkin_service_name=service_name
      settings['zipkin.transport_handler'] = self.zipkin_handler
      settings['zipkin.tracing_percent'] = 100.0
      self.config = Configurator(settings=settings)
      self.config.include('pyramid_zipkin')

    def add_router(self,router_type,router_url):
      self.config.add_route(router_type, router_url)
      self.config.scan()
 
    def invoke_wsgi_service(self,host_port):
      app = self.config.make_wsgi_app()
      server = make_server('0.0.0.0', host_port, app)
      print('service '+self.zipkin_service_name+' listening : http://localhost:'+str(host_port))
      server.serve_forever()


@view_config(route_name='invoke_service')
def invoke_service(request):
    headers = {}
    headers.update(create_http_headers_for_new_span())
    response_fromb = requests.get(
        'http://localhost:9002/apib',
        headers=headers,
    )
    headers = {}
    headers.update(create_http_headers_for_new_span())
    response_fromc = requests.get(
        'http://localhost:9003/apic',
        headers=headers,
    )
    return Response(str(response_fromb.text) + "\t" + str(response_fromc.text))

node=ZipkinNode()
node.init_zipkin_settings('Service_A')
node.add_router('invoke_service','/api')
node.invoke_wsgi_service(9001)
