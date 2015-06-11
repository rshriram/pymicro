#!/usr/bin/python
import simplejson as json
import urllib
import bottle # Web server
from urllib import urlopen
from bottle import run, route, request, template
import sys
import random, time
import os
from discovery import ServiceDiscovery
import socket
from json2html import *

stderr = sys.stderr.write
myip = socket.gethostbyname(socket.gethostname())
zookeeper=""
sd = None
culprit = False
my_instance_id = None
myname = None
##schema for microservice
##{name : service_name
##path : node_path_in_zookeeper (and also the URL sub path)
##children: array of microservices}

###############DB###########################
serviceDB1 = {
    "name" : "serviceDB1",
    "path" : "/bottle/all/view/DB/serviceDB1",
    "children" : []
}
serviceDB2 = {
    "name" : "serviceDB2",
    "path" : "/bottle/all/view/DB/serviceDB2",
    "children" : []
}
serviceDB3 = {
    "name" : "serviceDB3",
    "path" : "/bottle/all/view/DB/serviceDB3",
    "children" : []
}

################ASYNC##########################
serviceAsync1 = {
    "name" : "serviceAsync1",
    "path" : "/bottle/all/view/async/serviceAsync1",
    "children" : [serviceDB1]
}
serviceAsync2 = {
    "name" : "serviceAsync2",
    "path" : "/bottle/all/view/async/serviceAsync2",
    "children" : [serviceDB2]
}
serviceAsync3 = {
    "name" : "serviceAsync3",
    "path" : "/bottle/all/view/async/serviceAsync3",
    "children" : [serviceDB3]
}

##############serviceA's children##################
serviceA1 = {
    "name" : "serviceA1",
    "path" : "/bottle/all/view/serviceA/serviceA1",
    "children" : [serviceDB1]
}
serviceA2 = {
    "name" : "serviceA2",
    "path" : "/bottle/all/view/serviceA/serviceA2",
    "children" : [serviceDB2]
}
serviceA3 = {
    "name" : "serviceA3",
    "path" : "/bottle/all/view/serviceA/serviceA3",
    "children" : [serviceDB3]
}

############serviceB's children####################
serviceB1 = {
    "name" : "serviceB1",
    "path" : "/bottle/all/view/serviceB/serviceB1",
    "children" : [serviceDB1]
}
serviceB2 = {
    "name" : "serviceB2",
    "path" : "/bottle/all/view/serviceB/serviceB2",
    "children" : [serviceDB2]
}
serviceB3 = {
    "name" : "serviceB3",
    "path" : "/bottle/all/view/serviceB/serviceB3",
    "children" : [serviceDB3]
}

###########serviceC's children#####################
serviceC1 = {
    "name" : "serviceC1",
    "path" : "/bottle/all/view/serviceC/serviceC1",
    "children" : [serviceDB1]
}
serviceC2 = {
    "name" : "serviceC2",
    "path" : "/bottle/all/view/serviceC/serviceC2",
    "children" : [serviceDB2]
}
serviceC3 = {
    "name" : "serviceC3",
    "path" : "/bottle/all/view/serviceC/serviceC3",
    "children" : [serviceDB3]
}

###########serviceD's children#####################
serviceD1 = {
    "name" : "serviceD1",
    "path" : "/bottle/all/auth/serviceD/serviceD1",
    "children" : []
}
serviceD2 = {
    "name" : "serviceD2",
    "path" : "/bottle/all/auth/serviceD/serviceD2",
    "children" : []
}
serviceD3 = {
    "name" : "serviceD3",
    "path" : "/bottle/all/auth/serviceD/serviceD3",
    "children" : []
}
##################################################
serviceA = {
    "name" : "serviceA",
    "path" : "/bottle/all/view/serviceA",
    "children" : [serviceA1, serviceA2, serviceA3]
}

serviceB = {
    "name" : "serviceB",
    "path" : "/bottle/all/view/serviceB",
    "children" : [serviceB1, serviceB2, serviceB3]
}

serviceC = {
    "name" : "serviceC",
    "path" : "/bottle/all/view/serviceC",
    "children" : [serviceC1, serviceC2, serviceC3]
}

serviceD = {
    "name" : "serviceD",
    "path" : "/bottle/all/auth/serviceD",
    "children" : [serviceD1, serviceD2, serviceD3]
}
################################################
view_services = {
    "name" : "view",
    "path" : "/bottle/all/view",
    "children" : [serviceA, serviceB, serviceC]
}

auth_services = {
    "name" : "auth",
    "path" : "/bottle/all/auth",
    "children" : [serviceD]
}

all_services = {
    "name" : "master",
    "path" : "/bottle/all",
    "children" : [view_services, auth_services]
}
##################################################
service_dict = {
    "master" : all_services,
    "auth" : auth_services,
    "view" : view_services,
    "serviceA" : serviceA,
    "serviceB" : serviceB,
    "serviceC" : serviceC,
    "serviceD" : serviceD,
    "serviceA1" : serviceA1,
    "serviceA2" : serviceA2,
    "serviceA3" : serviceA3,
    "serviceB1" : serviceB1,
    "serviceB2" : serviceB2,
    "serviceB3" : serviceB3,
    "serviceC1" : serviceC1,
    "serviceC2" : serviceC2,
    "serviceC3" : serviceC3,
    "serviceD1" : serviceD1,
    "serviceD2" : serviceD2,
    "serviceD3" : serviceD3,
    "serviceDB1" : serviceDB1,
    "serviceDB2" : serviceDB2,
    "serviceDB3" : serviceDB3,
    "serviceAsync1" : serviceAsync1,
    "serviceAsync2" : serviceAsync2,
    "serviceAsync3" : serviceAsync3
}

class InvalidConfigurationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

@route('/')
@route('/bottle')
def index():
    """ Display welcome & instruction messages """
    global all_services

    top = """
    <html>
    <head>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    </head>
    <title>Synthetic Microservice-based Application</title>
    <body>
    <p><h2>Hello! This is a simple synthetic microservice-based app!</h2></p>
    <p><h4>The table below shows the current configuration of various services in the application</h4></p>
    """

    middle = json2html.convert(json = json.dumps(all_services),
                               table_attributes="class=\"table table-condensed table-bordered table-hover\"")
    bottom = """
    </body>
    </html>
    """
    return top+middle+bottom

def raw_service_output(snode, nodescend=False):
    _output = []
    if nodescend == True or (len(snode['children']) == 0):
        _output.append({'name': snode['name'], 'message': "Hello World!"})
        return json.dumps(_output)

    for s in snode["children"]:
        name = s['name']
        try:
            inst = sd.get_instance(s['name'])
            url = inst+s['path']
            res = json.loads(urlopen(url).read())
        except Exception as e:
            res = str(e)
        _output.append({'name': name, 'message': res})
    if len(_output) == 0:
        _output.append({'name' : snode['name'], 'message': "Error:All child services are inaccessible!"})
    return json.dumps(_output)

def html_response(snode):
    top = """
    <html>
    <head>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    </head>
    <title>Synthetic Microservice-based Application</title>
    <body>
    <p><h2>Hello! This is the <b>%s</b> service that is powered by the following microservices:</h2></p>
    """ % (snode['name'])

    _output = raw_service_output(snode)
    middle = json2html.convert(json = json.dumps(_output),
                               table_attributes="class=\"table table-condensed table-bordered table-hover\"")
    bottom = """
    </body>
    </html>
    """
    return top+middle+bottom

@route('/bottle/all/<name>')
def level0(name='view'):
    global service_dict
    #stderr("level0:received %s\n" % name)
    snode = service_dict[name]
    return raw_service_output(snode)

@route('/bottle/all/view/<name>')
@route('/bottle/all/auth/<name>')
def level1(name='serviceA'):
    global service_dict
    #stderr("level1:received %s\n" % name)
    snode = service_dict[name]
    return raw_service_output(snode)

@route('/bottle/all/view/serviceA/<name>')
@route('/bottle/all/view/serviceB/<name>')
@route('/bottle/all/view/serviceC/<name>')
@route('/bottle/all/view/DB/<name>')
@route('/bottle/all/view/async/<name>')
@route('/bottle/all/auth/serviceD/<name>')
def level2(name='serviceA1'):
    global service_dict
    #stderr("level2:received %s\n" % name)
    snode = service_dict[name]
    return raw_service_output(snode)

if __name__ == '__main__':
    # To run the server, type-in $ python server.py
    bottle.debug(True) # display traceback
    p = int(sys.argv[1])
    zookeeper=os.environ.get('ZOOKEEPER')
    myname = os.environ.get('SERVICE_NAME')
    if (myname is None) or (zookeeper is None):
        raise InvalidConfigurationError("SERVICE_NAME and ZOOKEEPER env vars are needed")
    if myname not in service_dict:
        raise InvalidConfigurationError("Invalid service name %s" % myname)
    c = os.environ.get('SLOW_SERVICE')
    if c is not None and (c.lower() == 'true' or c.lower() == 1):
        culprit = True
    else:
        culprit = False

    stderr("registering with zookeeper at %s under %s\n" % (zookeeper, myname))
    sd = ServiceDiscovery('/bottle', zookeeper)
    my_instance_id = sd.register(myname, myip, p)
    run(host='0.0.0.0', port=p, reloader=True)
