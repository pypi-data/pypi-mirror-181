import subprocess
import os
import shutil
import sys
import inspect
import json

from concurrent import futures
from cakework import cakework_pb2
from cakework import cakework_pb2_grpc
from .activity_server import ActivityServer
import importlib

# TODO: trim this requirements.txt file and remove extraneous stuff
# need to copy over the requirements.txt?
# grpciotools - only needed for compiling the protobuf files. don't need to package this with the pypi distribution
# cakework_files = ["activity_server.py", "cakework_pb2_grpc.py", "cakework_pb2.py", "cakework_pb2.pyi"]

class App:
	# do we actually need the url? 
	# TODO figure out how to allow people to specify the version of python to use
	# TODO infer user id automatically
	def __init__(self, app, user_id="shared"): # TODO change app to name
		# TODO sanitize the user id and app name
		self.user_id = user_id # TODO once we have auth will no longer have this be shared
		self.app = app

		# create a build directory 
		self.current_dir = os.getcwd()
		self.build_dir = self.current_dir
		# self.build_dir = os.path.join(self.current_dir, "build") // for now, omit creating a separate build directory
		# self.files_to_copy = []
		
		self.config = { "user_id": self.user_id, "app": self.app }
		# if os.path.exists(self.build_dir):
		# 	shutil.rmtree(self.build_dir)
		# os.mkdir(self.build_dir)

		# print("current working directory: " + os.getcwd())
		print("Created app for user id: " + user_id + ", app name: " + app)
		# print("app build directory: " + self.build_dir)

		# for f in cakework_files:
		# 	f_copy = os.path.join(os.path.dirname(__file__), f)
		# 	print("will copy file: " + f_copy)
		# 	self.files_to_copy.append(f_copy)

	# create a new sub-directory in the build directory with the activity_name
	# copy protobuf files over
	# copy the cakework_server file over and modify it

	def register_activity(self, activity):
		print("Registering activity")
		activity_server = ActivityServer(activity) # Q: this gets shut down?
		activity_server.start()
		# start the activity server



		# inspect the activity to get the module
		# self.config['module'] = inspect.getmodule(activity).__name__
		# self.config['activity'] = activity_name # currently only supports one activity at a time
		# # verify that we wrote to the right place
		# print("registered module: " + self.config['module'] + " and activity: " + self.config['activity'])

		# # activity_build_dir = os.path.join(self.build_dir, activity_name)
		# # print("activity build directory: ")

		# config_path = os.path.join(self.build_dir, 'cakework.json')
		# with open(config_path, 'w') as outfile:
		# 	outfile.write(json.dumps(self.config, indent=4))
		
		# return config_path

		# # copy entire current directory containing the script to a new build directory
		# print("activity build directory: " + activity_build_dir)
		# shutil.copytree(self.current_dir, activity_build_dir, ignore=shutil.ignore_patterns("build"))
		
		# # get the import line as well as the activity invocation line
		# # replace it in the activity_server.py file
		# # look for entry point file in current directory titled register_activity.py
		# # entry_point = os.path.join(self.current_dir, "register_activity.py")
		# # TODO make it so that it's not hard coded!
		# import_line = None
		# with open("register_activity.py", 'r') as f:
		# 	for line in f:
		# 		if activity_name in line and "import" in line:
		# 			import_line = line
		# 			break

		# if import_line is not None:
		# 	print("found import line: " + import_line)
		# else:
		# 	sys.exit("Couldn't find import line in register_activity.py")

		# for file in self.files_to_copy:
		# 	shutil.copy(file, os.path.join(activity_build_dir, os.path.basename(file)))
		
		# lines = None	
		# # open the file to write to, i.e. the activity_server.py in the build directory
		# with open(os.path.join(activity_build_dir, "activity_server.py")) as f:
		# 	lines = f.readlines()
		# 	for i, line in enumerate(lines):
		# 		if 'REPLACE_ME_ACTIVITY_IMPORT' in line:
		# 			lines[i] = import_line + "\n"
		# 			# print("replaced import: " + line)
		# 		if 'REPLACE_ME_ACTIVITY_INVOCATION' in line:
		# 			lines[i] = "        res = " + activity_name + "(**parameters)\n"
		# 			# print("replaced invocation " + line)
		
		# f = open(os.path.join(activity_build_dir, "activity_server.py"), 'w')
		# f.writelines(lines)
		# f.close()

		# # f.writelines(lines)
		
		
		# # # for now, just create a single Docker file
		# # # when we have to deploy multiple activities, 
		# # dir_path = os.path.dirname(os.path.dirname(__file__))
		# # print("this script's path: " + dir_path)
		# # # create empty __init__.py
		# # init = open(os.path.join(self.build_dir, "__init__.py"), 'x')
		# # init.close()

		# # os.mkdir(os.path.join(self.build_dir, "cakework"))


		# return activity_build_dir # is this the right thing to return? 

		# # # copy the app definition file. required to be called cakework.py
		# # shutil.copy(os.path.join(self.current_dir, "cakework.py"), self.build_dir)

		# # # need to copy sub-folders too. skip copying the build directory.
		# # for root, dirs, files in os.walk(self.current_dir):
		# # 	for file in files:
		# # 		path_file = os.path.join(root, file)
		# # 		shutil.copy(path_file, self.build_dir)

		# # # for now just copy files with python extension. 
		# # # we also need to copy the user's requirements.txt and join that with our server's
		# # # need to make sure that versions of python is compatible!
		
		# # # TODO also need to make sure the user's app.py file doesn't overwrite the cakework one
		# # # TODO copy the user's requirements.txt file
		# # # sanitize the activity name		
		
def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1)) # what should the default be?
    cakework_pb2_grpc.add_CakeworkServicer_to_server(Cakework(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()