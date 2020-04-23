## function to create the worksspace
from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.model import Model
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.image import ContainerImage
from azureml.core.webservice import AciWebservice, Webservice
import json

import os
import json


class Modelnew():
    def __init__(self):
        self.config=self.get_json_file()
        self.model_path = os.path.join(os.getcwd(),self.config['folder'],self.config['model_file'])


    def get_json_file(self):
        with open("config.json","rb") as json_file:
            config=json.load(json_file)
        return config


    def createworkspace(self):
        print("creating the workspace name:{} using subscription id {} in the region {}".format(self.config['workspace']['workspace_name'],self.config['workspace']['subscription_id'],self.config['workspace']['region']))
        ws = Workspace.create(name=self.config['workspace']['workspace_name'],
                              subscription_id=self.config['workspace']['subscription_id'],
                              resource_group=self.config['workspace']['resource_group'],
                              create_resource_group=True,
                              location=self.config['workspace']['region'],
                              exist_ok=True)
        print('workspace created successfully')

        print("workspace details",ws)

        return ws



    def compute(self, ws):

        # Verify that cluster does not exist already
        try:
            cpu_cluster = ComputeTarget(workspace=ws, name=self.config['compute']['cpu_cluster_name'])
            print('Found existing cluster, use it.')

        except ComputeTargetException:
            compute_config = AmlCompute.provisioning_configuration(vm_size=self.config['compute']['vmsize'],
                                                                   max_nodes=self.config['compute']['max_nodes'])
            cpu_cluster = ComputeTarget.create(ws, self.config['compute']['cpu_cluster_name'], compute_config)
            print("creating new compute target")
        cpu_cluster.wait_for_completion(show_output=True)
        return cpu_cluster

    def register_model(self, ws):

        model = Model.register(model_path=self.model_path, model_name=self.config['model_register']['model_name'],
                               # this is the name the model is registered as
                               tags={"type": self.config['model_register']['type_a'], "Score": self.config['model_register']['score']},
                               description=self.config['model_register']['model_description'],
                               workspace=ws
                               )

        print("Model registered: {} \nModel Description: {} \nModel Version: {}".format(model.name,
                                                                                        model.description,
                                                                                        model.version))
        return model

    def conda_dependence(self):
        mycondaenv = CondaDependencies.create(conda_packages=['scikit-learn', 'numpy', 'pandas'])
        filename=self.config['dependencies']['filename']
        with open(filename, "w") as f:
            f.write(mycondaenv.serialize_to_string())

    def deploy_aci(self, ws, model):
        # Create the scoring script
        # See the scoring script available in ./score.py

        # Build the ContainerImage
        image_config = ContainerImage.image_configuration(execution_script=self.config['deploy_image']['driver_file'],
                                                          runtime=self.config['deploy_image']['runtime'],
                                                          conda_file=self.config['deploy_image']['conda_file'])
        aci_config = AciWebservice.deploy_configuration(cpu_cores=self.config['deploy_image']['cpu_cores'],
                                                        memory_gb=self.config['deploy_image']['memory_gb'],
                                                        tags=self.config['deploy_image']['tags'],
                                                        description=self.config['deploy_image']['description'])
        webservice = Webservice.deploy_from_model(workspace=ws, name=self.config['deploy_image']['servicename'], deployment_config=aci_config,
                                                  models=[model],
                                                  image_config=image_config)
        webservice.wait_for_deployment(show_output=True)
        print(webservice.state)

        return webservice

    def testing(self,ws):
        lis1 = self.config['test_data']

        test_data = json.dumps(lis1)
        print(test_data)
        webservice = Webservice(workspace=ws, name=self.servicename)
        # If the webservice is not ready, run this cell again...
        result = webservice.run(input_data=test_data)
        print(result)




