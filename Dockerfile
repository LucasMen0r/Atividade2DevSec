# 1) Imagem base leve com Python 3.9
FROM python:3.9-slim                             

# 2) Diretório de trabalho dentro do container
WORKDIR /app                                     

# 3) Atualiza pip e instala dependências
COPY requirements.txt .                          
RUN pip install --no-cache-dir -r requirements.txt 

# 4) Copia todo o código da aplicação
COPY . .                                          

# 5) Expõe a porta padrão do Flask
EXPOSE 5000                                      

# 6) Comando para iniciar a aplicação
CMD ["python", "app.py"]                         
