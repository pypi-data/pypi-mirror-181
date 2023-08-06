from __future__ import print_function

import logging

import grpc
import sahale_pb2
import sahale_pb2_grpc
import json
import sys

# TODO: need to re-enable TLS for the handlers in the fly.toml file. Try these settings: https://community.fly.io/t/urgent-grpc-server-unreachable-via-grpcurl/2694/12 for alpn
# TODO figure out how to configure the settings for fly.toml for grpc!
# TODO also need to make sure different runs don't interfere with each other
# TODO add a parameter for an entry point into the system (currently, assume that using sahale_app.py)
class Client:
    def __init__(self, user_id, app, local=False): # TODO: infer user id
        self.app = app
        self.user_id = user_id
        self.local = local

    def start_new_activity(self, name, request):
        # with grpc.insecure_channel('localhost:50051') as channel:
        if self.local:
            endpoint = 'localhost:50051'
        else:
            endpoint = self.user_id + '-' + self.app + '-' + name + ".fly.dev" + ":443" # TODO convert to all lower case and dashes only

        print("Connecting to endpoint: " + endpoint) # TODO remove this later so customer can't see this
        with grpc.insecure_channel(endpoint) as channel:
            stub = sahale_pb2_grpc.SahaleStub(channel)
            response = stub.RunActivity(sahale_pb2.Request(parameters=json.dumps(request)))
            return response
