import json
import os
import numpy as np
import pandas as pd
from sklearn import linear_model 
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from azureml.core import Run
from azureml.core import Workspace
from azureml.core.run import Run
from azureml.core.experiment import Experiment
import pickle
from sklearn.externals import joblib
from azureml.core.model import Model
from sklearn.externals import joblib


def run(input_json):
    columns = ['patient_nbr', 'number_diagnoses', 'admission_type_id',
               'discharge_disposition_id', 'admission_source_id', 'time_in_hospital',
               'encounter_id', 'race', 'gender', 'age', 'num_lab_procedures',
               'num_procedures', 'num_medications', 'number_outpatient',
               'number_emergency', 'number_inpatient', 'change', 'readmitted',
               'Total_drugs', 'diagnosis']
    try:
        model_name = "soloinsulin01"
        model_path = Model.get_model_path(model_name)
        print('Looking for models in: ', model_path)
        newmodel = joblib.load(model_path)
        inputs = json.loads(input_json)
        data_df = pd.DataFrame(np.array(inputs).reshape(-1, len(columns)), columns = columns)
        # Get the predictions...
        prediction = newmodel.predict(data_df).tolist()
        prediction = json.dumps(prediction)
    except Exception as e:
        prediction = str(e)
    return prediction