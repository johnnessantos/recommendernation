## Ambiente
A preparação do ambiente se dá com os comandos abaixo, por recomendação é preferivel utilizar ambientes virtuais. [Ler mais...](https://docs.python.org/3/library/venv.html)
```bash
$ python -m venv "codenationvenv"
$ source codenationvenv/bin/activate
$ pip install -r requirements.txt
```

Com o modelo baixado `output/modelo.pkl` basta rodar o comando:
```bash
$ streamlit run app.py
```

Caso contrario:
```bash
$ python src/main.py
$ streamlit run app.py
```