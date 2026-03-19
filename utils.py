import pymorphy3
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

morph = pymorphy3.MorphAnalyzer()

def lemmatize_text(text):
    # print(text)
    text_prepared = text.split(" ")
    # print(text_prepared)
    lemmas = [morph.parse(token)[0].normal_form for token in text_prepared]
    lemmas = " ".join(lemmas)
    # print("lemmas", lemmas)
    return lemmas




# Исходные данные
# data = {
#     'img1': [['кот', 'рама', 'мыть'], ['мама', 'кот', 'гладить']],
#     'img2': [['мальчик1', 'мяч', 'бьет'], ['мяч', 'ворота', 'летит']],
#     'img3': [['мальчик2', 'мальчик1', 'бьет']],
#     'img3 ааа.jpg': [['мальчик2', 'мальчик1', 'бьет']]
# }

# Функция для построения и отображения графа
def build_and_show_graph(image_name, triples):
    # Создаем направленный граф
    G = nx.DiGraph()
    
    # Добавляем ребра: (субъект, объект, действие)
    for subj, obj, action in triples:
        G.add_edge(subj, obj, label=action)
    
    # Проверка на пустой граф
    if len(G.nodes()) == 0:
        print(f"Для {image_name} нет данных для построения графа.")
        return
    
    # Создаем рисунок
    plt.figure(figsize=(16, 12))
    
    # Определяем расположение узлов (для красоты)
    pos = nx.spring_layout(G, seed=42, k=1.5)  # k регулирует расстояние между узлами
    
    # Рисуем узлы и ребра
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Рисуем стрелки (ребра)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, 
                           connectionstyle='arc3,rad=0.1')  # rad для изогнутых линий
    
    # Добавляем подписи к ребрам (действия)
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    
    # Настраиваем отображение
    plt.title(f"Граф для {image_name}")
    plt.axis('off')  # Убираем оси координат
    plt.tight_layout()
    plt.show()

