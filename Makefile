all: spawner.py ui_spawner.py
	./spawner.py

ui_spawner.py: ui_spawner.ui
	pyuic5 ui_spawner.ui -o ui_spawner.py
