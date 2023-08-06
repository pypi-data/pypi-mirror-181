import numpy as np
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil


IP = '54.226.28.103:8000'
#IP = '127.0.0.1:8000'

def login(username, key):
  print("Logging in...")
  credentials = {'username':username, 'key':key, 'task':'login'}
  response = requests.post('http://'+IP+'/api/python_login', data=credentials)
  if response.text == '1':
    os.environ["username"] = username
    os.environ["key"] = key
    os.environ["prev_file"] = ''
    os.environ["prev_func"] = ''
    os.environ['prev_node'] = "-999"
    print("Successfully connected to tunerml!")
  else:
    print("Credentials could not be verified.")


def project(project_name):

  os.environ['project_name'] = project_name
    
  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  project_info_list = ['Codebase Python ' + platform.python_version()]
  
  project_info_list.append("    GPU    ")
  gpus = GPUtil.getGPUs()
  if len(gpus) == 0:
    project_info_list.append("No NVIDIA GPU found")
  else:
    for gpu in gpus:
      gpu_id = gpu.id
      gpu_name = gpu.name
      gpu_memory = gpu.memoryTotal
      project_info_list.append("GPU ID " + str(gpu_id))
      project_info_list.append(gpu_name)
      project_info_list.append(str(gpu_memory) + " MB")

  project_info_list.append("    CPU    ")
  project_info_list.append(platform.processor())
  project_info_list.append(platform.platform())
  project_info_list.append(platform.machine())
  project_info_list.append("    MEMORY    ")
  project_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'project_name': project_name, 'installed_packages': str(installed_packages_list),
          'username': os.environ['username'], 'key': os.environ['key'], 'project_information': str(project_info_list)}
  
  response = requests.post('http://'+IP+'/api/create_project', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    response_dict = ast.literal_eval(response.text)
    
    if response_dict['exists'] == 0:
      print("Created a new project.")
    else:
      print("Project exists. Created a new run")
      
  os.environ['project_id'] = str(response_dict['project_id'])
  os.environ["prev_file"] = ''
  os.environ["prev_func"] = ''
  os.environ['prev_node'] = "-999"      
  
def node(node_name = "", filename = "", lineno = 0, node_description=""):

  if os.environ['prev_node'] == "-999":
    data = {'current_node_name': node_name, 'node_description': node_description,
            'username': os.environ['username'], 'key': os.environ['key'], 'project_id': os.environ['project_id'],
            'filepath': filename, 'line_number': lineno}
  else:
    data = {'current_node_name': node_name, 'connect_with':  os.environ['prev_node'], 'node_description': node_description,
            'username': os.environ['username'], 'key': os.environ['key'], 'project_id': os.environ['project_id'],
            'filepath': filename, 'line_number': lineno}

  response = requests.post('http://'+IP+'/api/create_node', data=data)

  if response.text == '-1':
    print("Authentication failed")
  elif response.text == '-3':
    print("Node repeated")
  else:
    print(response.text)

      
    os.environ['prev_node'] = response.text #Store previous node
    os.environ["prev_func"] = node_name
    os.environ["prev_file"] = filename  


def node_log(variables):
  if len(variables) == 0:
    return 0

  data = {'_id': os.environ['prev_node'], 'type':'node', 'variables': str(variables), 'username': os.environ['username'], 'key': os.environ['key']}
  response = requests.post('http://'+IP+'/api/set_variables', data=data)




def tracefunc(frame, event, arg, indent=[0]):
    save_function = False
    
    allowed_commands_function = False
    current_command = ""
    allowed_commands = ['optimizer.py', 'lr_scheduler.py', 'dataset.py', 'dataloader.py', 'transforms.py']
    #if 'torch' in frame.f_code.co_name or 'torch' in frame.f_code.co_filename:
    #  print(frame.f_code.co_name, frame.f_code.co_filename)

    for command in allowed_commands:
        if command in frame.f_code.co_filename or command in frame.f_code.co_name:
            save_function = True
            allowed_commands_function = True
            current_command = command
            break;
    
    if 'Attributes' in frame.f_code.co_filename or 'Attributes' in frame.f_code.co_name:
        pass
    elif "Python" in frame.f_code.co_filename:
        pass
    elif "<module" in frame.f_code.co_name:
        pass
    elif ("<" in frame.f_code.co_name or "<" in frame.f_code.co_filename) and ("<ipython-input" not in frame.f_code.co_filename):
        pass
    elif "site-packages" in frame.f_code.co_filename:
        pass
    elif "dist-packages" in frame.f_code.co_filename:
        pass
    elif "lib/python" in frame.f_code.co_filename:
        pass
    else:
        save_function = True
        
    if save_function:
        
        if event == "call":
            print(frame.f_code.co_name, frame.f_code.co_filename)
            
            if allowed_commands_function:
                node(command, frame.f_code.co_filename, frame.f_code.co_firstlineno)
            elif 'ipykernel' not in frame.f_code.co_filename:
                node(frame.f_code.co_name, frame.f_code.co_filename, frame.f_code.co_firstlineno)
            else:
                node(frame.f_code.co_name, 'Jupyter notebook', 0)

        if event == "return": # or repeat_func == 1: #update variables of existing node if repeated instead of creating multiple nodes
            variables_to_log = {}
          
            exclusion_variables = inclusion_variables = include_variable = None
            for key in frame.f_globals:
                f = str(frame.f_globals[key])
                if 'exclusion_variables' in key:
                    exclusion_variables = ast.literal_eval(f)
                    for key in frame.f_locals:
                      if key not in exclusion_variables:
                        variables_to_log[key] = frame.f_locals[key]
                        
                elif 'inclusion_variables' in key:
                    inclusion_variables = ast.literal_eval(f)
                    for key in frame.f_locals:
                      if key in inclusion_variables:
                        variables_to_log[key] = frame.f_locals[key]
                        
                elif 'include_variables' in key:
                    include_variables = ast.literal_eval(f)
                    if include_variables:
                      variables_to_log = frame.f_locals
                else:
                    pass

            node_log(variables_to_log)

        return tracefunc
   
def settrace():
  sys.setprofile(tracefunc)


