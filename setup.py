import cx_Freeze

executables = [cx_Freeze.Executable("invade.py")]

cx_Freeze.setup(name="PSI!",options={"build_exe" : {"packages" : ["pygame", "requests"], \
				"include_files" : ["alien.py", "bullets.py", "buttons.py", \
				"game_function.py", "media/", "networking.py", \
				"pygame_textinput.py", "reticle.py", "scoreboard.py", \
				"settings.py", "ship.py", \
				"sprites/", "spritesheet.py", \
				"spritesheets/", "statistic.py"], "includes" : ["idna.idnadata"]}}, \
				executables = executables
				)	