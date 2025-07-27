export PYTHONDONTWRITEBYTECODE=1

criar_ambiente:
	python3 -m venv .venv

salvar_bibliotecas:
	@. .venv/bin/activate && pip freeze > requirements.txt

instalar_bibliotecas:
	@. .venv/bin/activate && pip install -r requirements.txt
	@. .venv/bin/activate && python3 -m pip install --upgrade pip

run:
	@echo "Iniciando Jogo da Velha"
	@. .venv/bin/activate && python3 Jogo/interface.py

executavel_windows:
	@. .venv/bin/activate && pyinstaller --name JogoDaVelha ^
	            --onefile ^
	            --windowed ^
	            --icon=Images/jogo-da-velha.ico ^
	            --add-data "Images;Images" ^
	            Jogo/interface.py

executavel_linux:
	@. .venv/bin/activate && pyinstaller --name JogoDaVelha \
	            --onefile \
	            --windowed \
	            --icon=Images/jogo-da-velha.ico \
	            --add-data "Images:Images" \
	            Jogo/interface.py


