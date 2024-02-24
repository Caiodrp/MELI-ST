# Especifica a imagem base e a tag
FROM python:3.10.9

# Especifica o diretório na imagem em que instruções posteriores são executadas.
WORKDIR /app

# Instala pacotes adicionais
RUN pip install scikit-learn==1.2.1 joblib==1.3.2

# Copia o código do aplicativo de treinamento para a imagem.
COPY predictions.py /app/predictions.py

# Copia o modelo para a imagem.
COPY model.joblib /app/model.joblib

# Configura o ponto de entrada para chamar o código de treinamento a ser executado.
ENTRYPOINT ["python", "predictions.py"]