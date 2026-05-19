
# Tech Challenge 4

## Autores
- Adryen Simões de Oliveira

## Descrição

Este projeto representa o Tech Challenge 4 da FIAP para o curso de Machine Learning Engineering.

O objetivo do projeto é implementar um modelo de deep-learning Long Short
Term Memory (LSTM), cujo objetivo é prever o preço de fechamento de um ativo na bolsa de valores (empresa escolhida: Disney).

## Link do vídeo descritivo
https://youtu.be/eDoxAatL7g8

## Como usar
Para utilizar o projeto, será necessário ter o docker e o python instalado. Com isso, você poderá rodar o projeto localmente e acessar as apis em: http://localhost:8000.

Para instalar e rodar localmente, vá para a sessão de instalação.

### Documentação do Modelo LSTM
O projeto monta um LSTM utilizando PyTorch. No diretório Model/app/ está localizado os fontes do modelo, sendo divididos em 3 arquivos:

- model.py: Onde se encontra o coração do modelo e a implementação do LSTM, juntamente com a função Linear para a transformação dos dados;

- train.py: Onde se encontra os métodos de treino e teste do modelo. O treino aplicando as funções de ativação e atualização dos pesos do modelo e o teste com a aplicação das métricas para avaliação do modelo (MAPE, MAE e RMSE);

- main.py: O orquestrador, onde ocorre a coleta e preparação dos dados para o treino do modelo (separando em períodos de 90 dias), instanciação do modelo passando os argumentos input_size = 5, output_size=1, num_layers = 10, hidden_size = 64, o treino e teste do modelo, e por fim, o salvamento dos pesos do modelo para inferência na API, juntamente com os scalers de normalização.

Para poder gerar o modelo, vá a sessão de instalação e uso.

O repositório já vem com o modelo e os scalers gerados para já ver o funcionamento via api.

#### Diretório com o Modelo e os Scalers:
SavedModels/

### Documentação da API

O projeto disponibiliza das seguintes rotas de api (Essas informações podem ser encontradas na rota /docs, onde é montado um swagger para as mesmas):

#### /metrics
Verbo http: GET

Response Body (retorna 200):
```json
string
```
Descrição: Essa rota é gerada pelo prometheus para análise de métricas sobre a API (usamos o prometheus com o grafana para monitoramento da API).

---

#### /predict
Verbo http: POST

Request Body:
```json
{
  "how_many_days": 0,
  "historic_data": [
    {
      "date_time": "yyyy-MM-dd",
      "close": 0,
      "high": 0,
      "low": 0,
      "open": 0,
      "volume": 0
    }
  ]
}
```

Response Body:
```json
{
    "used_manual_history": true,
    "warn": "",
    "result": [
        {
            "close": 0,
            "date_time": "yyyy-MM-dd"
        }
    ]
}
```
Descrição: Essa rota serve para realizar uma predição passando o Histórico (ou não) de preços do ativo (Disney). O atributo "how_many_days" serve para indicar quantos dias teremos previsão. O atributo "historic_data" serve para passarmos o histórico do ativo (para usar o histórico, devemos passar no mínimo 90 dias de histórico). Na resposta, o "used_manual_history" serve para indicar se foi passado ou não o histórico, "warn" serve para dar algum aviso sobre a resposta e "result" serve para mostrar a lista de previsões de acordo com o número de dias passado (quanto maior o número de dias, menor a precisão).

No projeto, tem um arquivo chamado example_with_history.json, ele é um exemplo com 90 dias de histórico para teste.

## Funcionamento

Este projeto é dividido em 2, uma parte para a implementação, treinamento, avaliação e salvamento de um modelo LSTM, e a segunda parte uma API implementada em FastAPI para servir o modelo que foi gerado.

Na parte da geração do modelo, é coletado os dados da bolsa de valores da Disney e o modelo é treinado com base nesses dados com um base em históricos de 90 dias, ou seja, o modelo é treinado para analisar um histórico de 90 dias e então dar uma previsão aproximada do preço de fechamento do ativo do próximo dia.

Na parte de api, foi utilizado o framework do FastAPI. Sempre que o projeto inicia, caso seja optado o uso do REDIS, o projeto irá coletar os últimos 95 dias do ativo da Disney com a biblioteca do yfinance e salva no banco de dados em memória REDIS. Ele só faz essa busca também caso o REDIS esteja vazio, caso contrário, ele deixa o histórico lá. Com isso, caso o uso do REDIS tenha sido habilitado, não tem a necessidade de sempre enviar o histórico nas requisições.

Além disso, é carregado o modelo LSTM e os scalers usados para normalização dos dados. E então é feito a predição de acordo com as requisições, caso haja histórico passado, ele o utiliza, caso contrário e o REDIS esteja ativo, ele busca no próprio REDIS, e caso não tenha habilitado o REDIS e não tenha passado o histórico, ele não realiza predição.

Todas as requisições são monitoradas pelo Prometheus, permitindo a configuração do Grafana para acompanhamento de métricas da api.

### Métricas do modelo LSTM gerado:
- MAPE: 2.14%;
- MAE: 2.38
- RMSE: 2.78


### Escolhas do projeto
Foi escolhido o framework do FastApi pela sua velocidade e praticidade em disponibilizar endpoints.

Foi escolhido o PyTorch por ser bem didático e prático para criação de modelos de deep learning.

Foi escolhido o Adam pela sua alta qualidade em atualização dos pesos no treinamento do modelo.

Foi escolhido o Prometheus por sua praticidade de implementação e acoplamento com outras ferramentas (como o próprio Grafana).

## Instalação e Uso
Caso queira instalar e utilizar o projeto localmente, nessa sessão vamos ensinar a instalar e rodar o projeto.

### Requisitos
- docker
- python

### Como gerar um Modelo novo

Vá até o diretório do projeto onde foi salvo em sua máquina e inicialize um ambiente virtual com:

```bash
  python -m venv venv
  source venv/bin/activate
```

E instale os requerimentos com:

```bash
  pip install -r requirements.txt 
``` 

Depois disso, rode o main no diretório Model/app/ com:

```bash
  python main.py
```

Com isso, o modelo será treinado, avaliado e salvado em SavedModels junto com os scalers.

### Como rodar a api

Vá até o diretório do projeto onde foi salvo em sua máquina. Lá teremos um arquivo chamado docker-compose.yml. Você poderá alterar ele para seu agrado, com a configuração mais importante sendo o volume da api (./SavedModels:/app/SavedModels), aqui você precisa indicar onde os modelos estão em sua máquina. Caso não mova os modelos, o diretório já estará correto.

Além disso, é possível configurar mais algumas variáveis de ambiente:

- USE_REDIS: Essa variável recebe True ou False, sendo True indicando que o projeto utilizará Redis e False indicando que não usará;
- REDIS_HOST: Essa variável serve para indicar o host do REDIS;
- REDIS_PORT: Essa variável serve para indicar a porta do REDIS;
- REDIS_USER: Essa variável serve para dizer qual o nome de usuário do REDIS (se tiver);
- REDIS_PASS: Essa variável serve para indicar a senha do REDIS (se tiver)
- MODEL_PATH: Essa variável serve para indicar o path do modelo caso você tenha mexido no volume;
- X_SCALER_PATH: Essa variável serve para indicar o path do scaler das features caso você tenha mexido no volume;
- Y_SCALER_PATH: Essa variável serve para indicar o path do scaler do resultado caso você tenha mexido no volume.

Por fim, nesse docker compose também já se encontra o redis, prometheus e grafana.
Após configurar o docker compose a sua necessidade, basta rodar ele com:

```bash
  docker compose up -d
```

Dessa forma, os containers serão gerados e rodaram em sua maquina em segundo plano (caso queira acompanhar os logs, retire o -d), com a api ficando disponível em http://localhost:8000, o prometheus em http://localhost:9090 e o grafana em http://localhost:3000.
