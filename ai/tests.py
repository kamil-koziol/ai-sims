from agents.memory.memory_node import MemoryNode, MemoryNodeAttributes
from datetime import datetime, timedelta
from llm_model.model import MockedEmbeddingModel, MockedGenerationModel, GenerationModel, EmbeddingModel
from colorama import Fore, Style
from llm_model.model_service import ModelService
import traceback


DEBUG_MODE = False

# TEST models

try:
    MOCKED = True

    embed_url = 'http://localhost:8888'
    generation_url = 'http://localhost:8888'

    if MOCKED:
        embed_model = MockedEmbeddingModel(embed_url)
    else:
        embed_model = EmbeddingModel(embed_url)

    if MOCKED:
        generation_model = MockedGenerationModel(generation_url)
    else:
        generation_model = GenerationModel(generation_url)

    generation_prompt = 'something'
    generated_text = generation_model.generate_text(generation_prompt)

    text_to_embed = 'something'
    embedded_text = embed_model.embed(text_to_embed)
    if DEBUG_MODE:
        print(generated_text)
        print(embedded_text)
except Exception:
    print('Model test: ' + Fore.RED + 'x')
    if DEBUG_MODE: print(traceback.format_exc()) # noqa
    print(Style.RESET_ALL)
else:
    print('Model test: ' + Fore.GREEN + '\u2713')
    print(Style.RESET_ALL)


# TEST memory_node

try:
    embed_model = MockedEmbeddingModel('')
    attributes = MemoryNodeAttributes(
        importance=4,
        created=datetime.now(),
        description='desc',
        node_type='chat',
        embeddings=embed_model.embed('something')
    )
    memory_node = MemoryNode(attributes)

    relevance_score = memory_node.calculate_relevance_score('something')

    date = datetime.now() + timedelta(days=1)
    recency_score = memory_node.calculate_recency_score(date)

    overall_score = memory_node.calculate_overall_compare_score('something')

    if DEBUG_MODE:
        print(relevance_score)
        print(recency_score)
        print(overall_score)
except Exception:
    print('Memory node test: ' + Fore.RED + '\u2717')
    if DEBUG_MODE: print(traceback.format_exc()) # noqa
    print(Style.RESET_ALL)
else:
    print('Memory node test: ' + Fore.GREEN + '\u2713')
    print(Style.RESET_ALL)


# TEST Model Manager
try:
    importance_score = ModelService().calculate_importance_score('', 'description')
    prompt = ModelService().prepare_prompt(['this is a convo', 'name1', 'name2'], "summarize_conversation.txt")

    if DEBUG_MODE:
        print(importance_score)
        print(prompt)

except Exception:
    print('Model manager test: ' + Fore.RED + '\u2717')
    if DEBUG_MODE: print(traceback.format_exc()) # noqa
    print(Style.RESET_ALL)
else:
    print('Model manager test: ' + Fore.GREEN + '\u2713')
    print(Style.RESET_ALL)
