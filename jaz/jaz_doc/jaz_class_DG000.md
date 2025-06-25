# __Class PlotWin__

## __Schéma 1__
Définition de 2 classes

__Class JazMainBoard__
* * *
sock  
module_info  
num_jaz	 # number of jaz modules
* * *
+ init_connection()
+ close_connection()
+ get_module_info()


__Class JazModule__  
* * *
serial_number  
wave_cal_pol  
non_linearity_pol  
dark_level  
saturation_level  
wavelength_axis  
* * *
+ get_module_info()
+ get_wavelength_axis()
+ set_integration_time()
+ get_spectrum()


## __Schéma 2__
Définition d'une classes

Class Jaz
* * *
dark_level : list  
serial_number : list  
wave_cal_pol : list  
saturation_level : list  
* * *
+ init_jaz_DPU(
+ init_jaz_modules()
+ _set_integration_time()
+ set_all_integration_time()
+ _get_spectrum()
+ get_all_spectrum()
+ get_serial_number()
+ _get_wavelength_axis()
+ get_all_wavelength_axis()
