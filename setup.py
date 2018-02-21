import cx_Freeze

executables = [cx_Freeze.Executable("invade.py")]

cx_Freeze.setup(name="PSI!",options={"build_exe" : {"packages" : ["pygame"], \
				"include_files" : ["media/", "sprites/", "spritesheets/", "sentiments/"  ], "includes" : ["idna.idnadata"]}}, \
				executables = executables
				)	