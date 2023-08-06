import random
import json

import numpy as np
import pandas as pd

from lmfit import models
from lmfit.model import save_modelresult, load_modelresult, save_model
from scipy import signal

class Analyzer():


    def put_data_into_dict(self):

        spec_dict = {
            'data': {
                'x': self.x,
                'y': self.y
            }
        }
        return spec_dict


    def create_specifications_manually(self):

        spec_dict = self.put_data_into_dict()
        models_list = []
        for model in self.models:
            model_dict = {
                'type': model[0],
                'params': {
                    'center': model[1][0],
                    'height': model[1][1],
                    'sigma': model[1][2]
                },
                'help': {
                    'center': {
                        'min':model[2][0],
                        'max':model[2][1]
                    }
                }
            }
            models_list.append(model_dict)
        spec_dict.update({'models': models_list})
        json_models_dict = json.dumps(spec_dict, indent=4)
        with open("models_dict.json", "w") as outfile:
            outfile.write(json_models_dict)


    def create_specifications_automatically(self, tolerance, peak_widths=(20,)):

        t = tolerance
        w = peak_widths
        peak_indices = signal.find_peaks_cwt(self.y, w)
        x_range = np.max(self.x) - np.min(self.x)
        x_val_peak = [self.x[peak_index] for peak_index in peak_indices]
        y_val_peak = [self.y[peak_index] for peak_index in peak_indices]
        peak_dict = {}
        for i in range(len(x_val_peak)):
            peak_dict[x_val_peak[i]] = y_val_peak[i]
        spec_dict =self.put_data_into_dict()
        models_list = []
        for x_val, y_val in zip(x_val_peak, y_val_peak):
            model_dict = {
                'type': self.model_type,
                'params': {
                    'center': x_val,
                    'height': y_val,
                    'sigma': x_range / len(x_val_peak) * np.min(w)
                },
                'help': {
                    'center': {
                        'min': (x_val-t),
                        'max': (x_val+t)
                    }
                }
            }
            models_list.append(model_dict)
        spec_dict.update({'models':models_list})
        json_models_dict = json.dumps(spec_dict, indent=4)
        with open("models_dict.json", "w") as outfile:
            outfile.write(json_models_dict)


    def generate_model(self, speci):

        composite_model = None
        params = None
        x_min = np.min(speci['data']['x'])
        x_max = np.max(speci['data']['x'])
        x_range = x_max - x_min
        y_max = np.max(speci['data']['y'])
        for i, basis_func in enumerate(speci['models']):
            prefix = f'model{i}_'
            model = getattr(models, basis_func['type'])(prefix=prefix)
            if basis_func['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel']: # for VoigtModel gamma is constrained to sigma
                model.set_param_hint('sigma', min=1e-6, max=x_range)
                model.set_param_hint('center', min=x_min, max=x_max)
                model.set_param_hint('height', min=1e-6, max=1.1*y_max)
                model.set_param_hint('amplitude', min=1e-6)
                default_params = {
                    prefix+'center': x_min + x_range * random.random(),
                    prefix+'height': y_max * random.random(),
                    prefix+'sigma': x_range * random.random()
                }
            else:
                raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
            if 'help' in basis_func:  # allow override of settings in parameter
                for param, options in basis_func['help'].items():
                    model.set_param_hint(param, **options)
            model_params = model.make_params(**default_params, **basis_func.get('params', {}))
            if params is None:
                params = model_params
            else:
                params.update(model_params)
            if composite_model is None:
                composite_model = model
            else:
                composite_model = composite_model + model
        return composite_model, params


    def initialize(
        self, experimental_data : pd.DataFrame,
        only_load_model_result_and_plot : bool = False,
        start_from_json_file : bool = False,
        automatic_peak_finding : bool = True,
        **kwargs
        ):
        if only_load_model_result_and_plot == False:
            if start_from_json_file == False:
                self.exp_data = experimental_data
                self.x = self.exp_data.iloc[:,0].values.tolist()
                self.y = self.exp_data.iloc[:,0].values.tolist()

                # for manual set specifications only
                self.n_models= kwargs['number_of_models']
                self.models = kwargs['model_specifications']

                # for automatically generated specifications only
                if kwargs.get('peak_widths') == None:
                    peak_widths = (2.5,)
                else:
                    peak_widths=kwargs['peak_widths']
                if kwargs.get('tolerance') == None:
                    tolerance = 0.5
                else:
                    tolerance=kwargs['tolerance']
                if automatic_peak_finding == True:        
                    self.model_type = kwargs['model_type']
                if automatic_peak_finding == False:
                    self.create_specifications_manually()
                else :
                    self.create_specifications_automatically(tolerance, peak_widths)
            else:
                pass
            with open('models_dict.json', 'r') as outfile:
                speci = json.load(outfile)
            model, params = self.generate_model(speci)
            save_model(model, 'model.sav')
            model_result = model.fit(speci['data']['y'], params, x = speci['data']['x'])
            save_modelresult(model_result, 'model_result.sav')
        else:
            pass
        model_result = load_modelresult('model_result.sav')
        print(model_result.fit_report())
        fig = model_result.plot(data_kws={'markersize': 1})
        fig.axes[0].set_title('')
