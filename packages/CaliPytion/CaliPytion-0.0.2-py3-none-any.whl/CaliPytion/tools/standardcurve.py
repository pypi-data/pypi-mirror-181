from typing import Dict, List, Callable
from CaliPytion.core.calibration import Calibration
from CaliPytion.tools.calibrationmodel import CalibrationModel
from CaliPytion.core.device import Device
from CaliPytion.core.spectrum import Spectrum
from CaliPytion.core.standard import Standard
from CaliPytion.core.series import Series

from CaliPytion.tools.calibrationmodel import linear1, quadratic, poly3, poly_e, rational, root_linear1, root_poly3, root_poly_e, root_quadratic, root_rational, equation_dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from pandas import DataFrame
from pyenzyme import EnzymeMLDocument
from scipy.optimize import fsolve

# TODO calcualte method to abso --> conc

class StandardCurve:
    def __init__(self, calibration_data: Calibration, wavelength: int = None, blanc_data: bool = True, cutoff_absorption: float = None, show_output: bool = True):
        self.blank_data = blanc_data
        self.cutoff = cutoff_absorption
        self.calibration_data = calibration_data
        self.wavelength = wavelength
        self.standard = self._get_Standard()
        self.concentration_unit = self.standard.concentration_unit
        self.substance_name = calibration_data.reactant_id
        self._initialize_measurement_arrays(show_output)
        self.models = self._initialize_models()
        self._fit_models(show_output)

    def _initialize_measurement_arrays(self, show_output: bool):
        absorption = [measurement.values for measurement in self.standard.absorption]
        n_replicates = len(absorption)

        self.concentration = np.tile(self.standard.concentration, n_replicates)
        if self.blank_data and np.any(self.concentration == 0):
            pos = int(np.where(np.array(self.standard.concentration) == 0)[0])
            absorption = np.array([])
            for repeat in self.standard.absorption:
                absorption = np.append(absorption, [x - repeat.values[pos] for x in repeat.values])
            if show_output:
                print("Calibration data was automatically blanked.")
            self.absorption = absorption
        else:
            self.absorption = np.array([measurement.values for measurement in self.standard.absorption]).flatten()
        
        if self.cutoff != None:
            self._cutoff_absorption()

    def _get_Standard(self):
        if self.wavelength != None:
            try:
                return next(standard for standard in self.calibration_data.standard if standard.wavelength == self.wavelength)
            except:
                raise StopIteration(
                    f"No calibration data found for calibration at {self.wavelength} nm. Calibration data exists for following wavelengths: {[x.wavelength for x in self.calibration_data.standard]}")
        else:
            standard = self.calibration_data.standard[0]
            print(f"Found calibration data at {int(standard.wavelength)} nm")
            self.wavelength = standard.wavelength
            return standard

    def _cutoff_absorption(self):
        pos = np.where(self.absorption < self.cutoff)
        self.concentration = self.concentration[pos]
        self.absorption = self.absorption[pos]


    def _initialize_models(self) -> Dict[str, CalibrationModel]:
        linear_model = CalibrationModel(
            name="Linear",
            equation=linear1,
            parameters={"a": 0.0}
        )
        quadratic_model = CalibrationModel(
            name="Quadratic",
            equation=quadratic,
            parameters={"a": 0.0, "b": 0.0}
        )
        poly3_model = CalibrationModel(
            name="3rd polynominal",
            equation=poly3,
            parameters={"a": 0.0, "b": 0.0, "c": 0.0}
        )
        polye_model = CalibrationModel(
            name="Exponential",
            equation=poly_e,
            parameters={"a": 0.0, "b": 0.0}
        )
        rational_model = CalibrationModel(
            name="Rational",
            equation=rational,
            parameters={"a": 0.0, "b": 0.0}
        )
        return {
            linear_model.name: linear_model,
            quadratic_model.name: quadratic_model,
            poly3_model.name: poly3_model,
            polye_model.name: polye_model,
            rational_model.name: rational_model}


    def _fit_models(self, show_output: bool = True):
        for model in self.models.values():
            model.fit(self.absorption, self.concentration)

        self.result_dict = self._evaluate_aic()
        if show_output:
            display(DataFrame.from_dict(self.result_dict, orient='index', columns=["AIC"]).rename(columns={0: "AIC"}).round().astype("int").style.set_table_attributes('style="font-size: 12px"'))

    def _evaluate_aic(self):
        names = []
        aic = []
        for model in self.models.values():
            names.append(model.name)
            aic.append(model.result.aic)

        result_dict = dict(zip(names, aic))
        result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]))

        return result_dict


    def visualize(self, model_name: str = None, ax: plt.Axes = None, title: str = None, y_label: str = None):
        ax
        if ax is None:
            ax_provided = False
            ax = plt.gca()
        else:
            ax_provided = True

        if model_name is None:
            model = self.models[next(iter(self.result_dict.keys()))]
        else:
            model = self.models[model_name]

        smooth_x = np.linspace(
            self.concentration[0], self.concentration[-1], len(self.concentration)*2)

        equation = model.equation
        params = model.result.params.valuesdict()

        ax.scatter(self.concentration, self.absorption)
        ax.plot(smooth_x, equation(smooth_x, **params))
        if ax_provided == False:
            ax.set_ylabel(f"absorption at {int(self.wavelength)} nm")
            ax.set_xlabel(f"{self.substance_name} [{self.concentration_unit}]")
            ax.set_title(f"calibration curve of {self.substance_name}")
        if title:
            ax.set_title(title)
        if y_label:
            print(f"{y_label}")
            ax.set_ylabel(y_label)


    def get_concentration(self, absorption: List[float], model_name: str = None) -> List[float]:
        
        # Convert to ndarray for performance
        if not isinstance(absorption, np.ndarray):
            absorption = np.array(absorption)

        # Select model equation
        if model_name == None:
            model = self.models[next(iter(self.result_dict))]
        else:
            model = self.models[model_name]
        equation: Callable = equation_dict[model.name]

        # Avoide extrapolation
        if np.any(absorption > max(self.absorption)):
            absorption = [float("nan") if x > max(self.absorption) else x for x in absorption]
            print("Absorption values out of calibration bonds. Respective values were replaced with \'nan\'.")

        # Calculate concentration through roots
        concentration = []
        for value in absorption:
            params = model.parameters
            params["absorption"] = value
            concentration.append(float(fsolve(equation, 0, params)))

        concentration = [float("nan") if x == 0 else x for x in concentration]
        return concentration

    def apply_to_EnzymeML(
        self,
        enzmldoc: EnzymeMLDocument,
        species_id: str,
        model_name: str = None,
        ommit_nan_measurements: bool = False
        ) -> EnzymeMLDocument:

        max_absorption_standard_curve = max(self.absorption)

        delete_measurements = []

        for id, measurement in enzmldoc.measurement_dict.items():
            del_meas = False
            for rep, replicates in enumerate(measurement.getReactant(species_id).replicates):
                data = [x if x < max_absorption_standard_curve else float("nan") for x in replicates.data] # TODO add info if values are removed
                
                # Check if nan values are in measurement data
                if np.isnan(np.min(data)) and ommit_nan_measurements == True:
                    del_meas = True
                else:
                    conc = self.get_concentration(absorption=data, model_name=model_name)
                    conc = [float(x) if x != 0 else float("nan") for x in conc] #retrieves nans from 'to_concentration', since fsolve outputs 0 if input is nan

                    enzmldoc.measurement_dict[id].species_dict["reactants"][species_id].replicates[rep].data = conc
                    enzmldoc.measurement_dict[id].species_dict["reactants"][species_id].replicates[rep].data_unit = self.concentration_unit
                    enzmldoc.measurement_dict[id].species_dict["reactants"][species_id].replicates[rep].data_type = "conc"
            if del_meas:
                delete_measurements.append(id)
        for id in delete_measurements:
            del enzmldoc.measurement_dict[id]
        
        if len(delete_measurements) != 0:
            print(f"Measurements '{delete_measurements}' removed from document, since respective measurement values are out of calibration range.")

        return enzmldoc

    @classmethod
    def from_excel(
        cls,
        path: str,
        reactant_id: str,
        wavelength: float,
        concentration_unit: str,
        temperature: float = None,
        temperature_unit: str = None,
        pH: float = None,
        device_name: str = None,
        device_model: str = None,
        blanc_data: bool = True,
        cutoff_absorption: float = None,
        sheet_name: str = None):

        df = pd.read_excel(path, sheet_name=sheet_name)
        concentration = df.iloc[:,0].values
        absorptions = df.iloc[:,1:]
        absorption_list = absorptions.values.T

        device = Device(
            manufacturer=device_name,
            model=device_model)

        absorption = []
        for abso in absorption_list:
            absorption.append(Series(values=list(abso)))


        standard = Standard(
            wavelength=wavelength,
            concentration=list(concentration),
            concentration_unit=concentration_unit,
            absorption=absorption)

        calibration = Calibration(
            reactant_id=reactant_id,
            pH=pH,
            temperature=temperature,
            temmperature_unit=temperature_unit,
            device=device,
            standard=[standard]
        )

        return cls(
            calibration_data=calibration,
            blanc_data=blanc_data, 
            cutoff_absorption=cutoff_absorption,
            wavelength=wavelength
        )