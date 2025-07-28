export PYTHONDONTWRITEBYTECODE=1

criar_ambiente:
	python3 -m venv .venv

salvar_bibliotecas:
	@. .venv/bin/activate && pip freeze > requirements.txt

instalar_bibliotecas:
	@. .venv/bin/activate && pip install -r requirements.txt
	@. .venv/bin/activate && python3 -m pip install --upgrade pip

run:
	@echo "Iniciando Campo Minado..."
	@. .venv/bin/activate && python3 Jogo/interface.py

executavel_windows:
	@. .venv/bin/activate && pyinstaller --name CampoMinado ^
	            --onefile ^
	            --windowed ^
	            --icon=Images/campo-minado.ico ^
	            --add-data "Images;Images" ^
	            Jogo/interface.py

executavel_linux:
	@. .venv/bin/activate && pyinstaller --name CampoMinado \
	            --onefile \
	            --windowed \
	            --icon=Images/campo-minado.ico \
	            --add-data "Images:Images" \
	            Jogo/interface.py


