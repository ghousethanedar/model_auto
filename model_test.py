from model import Modelnew

a=Modelnew()

ws=a.createworkspace()
cpu_cluster=a.compute(ws)

model1 = a.register_model(ws)

a.conda_dependence()

webservice=a.deploy_aci(ws,model1)

a.testing(ws)

# model_path_scaler = os.path.join(os.getcwd(),"outputs","scaler.pkl")
#
# model_name_scaler="scaler"
# model_name_used="usedcarsmodel"
#
# model_path_usedcars = os.path.join(os.getcwd(),"outputs","usedcarsmodel.pkl")
#
# files = os.listdir(path)
# print(path)
#
# print(files)