# ai-sims

# Installation

## Backend

### Docker

1. Go to `ai` directory

2. Build image and run

```sh
make build && make run
```

### Local

1. Go to `ai` directory
2. Install requirements

```sh
cd ai
pip install -r requirements.txt
```

3. Run

```sh
python3 run main.py
```

## Game

1. Download [Unity Hub](https://learn.unity.com/tutorial/install-the-unity-hub-and-editor#)
2. Select `2022.3` Unity Editor version
3. Inside Unity Hub > Projects > Add > Select `game` directory

## LLM's API

### Connecting to KASK

Make sure to run the LLM's API in kask and run in on port `8888`. See: Local hosting

1. SSH bind to kask. Backend will connect to localhost:8888

```sh
ssh -L 8888:sanna.kask:PORT -N account@kask.eti.pg.gda.pl
```



### Local hosting

1. Go to `api` directory
2. Install requirements

```sh
cd api
pip install -r requirements.txt
```

3. Change model (Optional)

In main.py change Generational Model and Embedding model to preferences. By default LLama2 and MxbaiModel will be set

```py
# main.py:12
model: GenerationModel = Llama2()
embedding_model: EmbeddingModel = MxbaiModel()
```

4. Run

```sh
python3 run run.py
```
