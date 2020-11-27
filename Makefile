# Automatically updates dependencies before running a program

A = Constants
C = Computed_Files
E = Extra
O = OUTPUT

# generates all outputs specified in Navigating Clean_2015
all : plot_ms plot_hess plot_uvj plot_T_vs_Z_quiescent plot_T_vs_Z_star-forming plot_slopes plot_intercepts slope_equation intercept_equation equation

# prints out the equation of the best-fit star-forming main sequence
equation :
	make $(C)/slopes_z_fit
	make $(C)/intercepts_9_z_fit
	make $(C)/slopes_z_20K
	make $(C)/intercepts_9_z_20K
	python3 z_equation.py

# prints out the best-fit intercept as a function of the age of the universe
intercept_equation :
	make $(C)/intercepts_9_z_fit
	python3 z_intercept_equation.py

# prints out the best-fit slope as a function of the age of the universe
slope_equation :
	make $(C)/slopes_z_fit
	python3 z_slope_equation.py

# plots the intercepts of the best fit star-forming main sequence vs age of the universe
plot_intercepts :
	make $(C)/intercepts_9_z
	python3 plot_intercepts_z.py

# plots the slopes of the best fit star-forming main sequence vs age of the universe
plot_slopes :
	make $(C)/slopes_z
	python3 plot_slopes_z.py

# plots temperature vs redshift only for quiescent galaxies
plot_T_vs_Z_quiescent :
	make $(C)/galaxy_properties.npy
	python3 plot_T_vs_z_quiescent.py

# plots temperature vs redshift only for star-forming galaxies
plot_T_vs_Z_star-forming :
	make $(C)/galaxy_properties.npy
	python3 plot_T_vs_z_star-forming.py

# plots UVJ diagram
plot_uvj :
	make $(C)/galaxy_properties.npy
	python3 plot_uvj.py

# plots the star-forming main sequence as a Hess diagram (colored by density of points)
plot_hess :
	make $(C)/galaxy_properties.npy
	python3 plot_hess.py

# plots the star-forming main sequence colored by temperature
plot_ms :
	make $(C)/galaxy_properties.npy
	python3 plot_ms.py

$(C)/slopes_z_fit : $(C)/slopes_z
	python3 plot_slopes_z.py

$(C)/intercepts_9_z_fit : $(C)/intercepts_9_z
	python3 plot_intercepts_z.py

$(C)/intercepts_9_z_20K : $(C)/galaxy_properties_20K.npy
	python3 plot_hess_20K.py

$(C)/intercepts_9_z : $(C)/galaxy_properties.npy
	python3 plot_hess.py

$(C)/slopes_z_20K : $(C)/galaxy_properties_20K.npy
	python3 plot_hess_20K.py

$(C)/slopes_z : $(C)/galaxy_properties.npy
	python3 plot_hess.py

$(C)/galaxy_properties_20K.npy : $(C)/galaxy_properties_pure_uvj_20K.npy apply_sSFR_cut_20K.py
	python3 apply_sSFR_cut_20K.py

$(C)/galaxy_properties.npy : $(C)/galaxy_properties_pure_uvj.npy apply_sSFR_cut.py
	python3 apply_sSFR_cut.py

$(C)/galaxy_properties_pure_uvj_20K.npy : $(C)/galaxy_uvj.npy $(E)/idtempz.txt $(A)/constants.py Auxiliary_Files $(C)/Basis_Props glxy_props_pure_uvj_20K.py
	python3 glxy_props_pure_uvj_20K.py

$(C)/galaxy_properties_pure_uvj.npy : $(C)/galaxy_uvj.npy $(E)/idtempz.txt $(A)/constants.py Auxiliary_Files $(C)/Basis_Props glxy_props_pure_uvj.py
	python3 glxy_props_pure_uvj.py

Auxiliary_Files : $(O) aux_file_writer.py
	python3 aux_file_writer.py
	@touch Auxiliary_Files

$(C)/galaxy_uvj.npy : $(C)/UVJ_By_Temp glxy_uvj.py
	python3 glxy_uvj.py

$(C)/UVJ_By_Temp : $(E)/idtempz.txt $(C)/Catalogs_By_Temp $(E)/Param_Files $(E)/fspstemplates eazy_uvj.py
	python3 eazy_uvj.py
	@touch $(C)/UVJ_By_Temp

$(E)/fspstemplates : template_files.py
	python3 template_files.py
	@touch $(E)/fspstemplates

$(C)/Catalogs_By_Temp : $(E)/idtempz.txt $(E)/2015catalog.cat temp_catalog.py
	python3 temp_catalog.py
	@touch $(C)/Catalogs_By_Temp

$(E)/Param_Files : $(E)/param param_files.py
	python3 param_files.py
	@touch $(E)/Param_Files

$(A)/constants.py : $(E)/idtempz.txt update_constants.py
	python3 update_constants.py

$(E)/idtempz.txt : $(O) generate_idtempz.py
	python3 generate_idtempz.py

.PHONY = equation intercept_equation slope_equation plot_intercepts plot_slopes plot_T_vs_Z_quiescent plot_T_vs_Z_star-forming plot_uvj plot_hess plot_ms
