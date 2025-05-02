import numpy as np
import matplotlib.pyplot as plt

def strategy_utility_and_winrate(num_trials=10000):
    # товары
    k = 5
    #множители ставок исследуемого игрока
    multipliers = [0.7, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.3]

    #словарь, хранящий статистику
    dictionary_of_stats = {m: {"usefullness": [], "wins": 0, "total": 0} for m in multipliers}

    #win_counts_by_bid = defaultdict(int)
    win_counts_by_bid={i:0 for i in range(1,51)}
    total_counts_by_bid = {i:0 for i in range(1,51)}

    for _ in range(num_trials):
        #50/1.3=38.5
        #также прибавление 1 на 25 строке - сделано, чтобы все значения участника i были ограничены 50.
        v_i = np.random.randint(1, 39)
        other_other = np.random.randint(1, 51, size=np.random.randint(9, 24))
        #итерация по множителям ставок
        for m in multipliers:
            bid = int(m * v_i)+1

            #массив значений
            other = np.append(other_other, bid)

            bidder_index = len(other) - 1
            #массив индексов в порядке убывания стоимости
            sorted_indices = np.argsort(other)[::-1]

            #соответствие значения результату аукциона
            allocation = np.zeros(len(other), dtype=int)

            winners = sorted_indices[:k]
            allocation[winners] = 1
            win = int(allocation[bidder_index] == 1)

            #правдивая цена на товар находится под индексом 5.
            price = other[sorted_indices[k]] # if len(other) > k else 0

            #проверка на получение товара участником i
            got_item = allocation[bidder_index]

            utility = v_i - price if got_item else 0
            
            dictionary_of_stats[m]["usefullness"].append(utility)
            dictionary_of_stats[m]["wins"] += int(got_item)
            dictionary_of_stats[m]["total"] += 1

            #заполнение статистики побед
            win_counts_by_bid[bid] += win
            total_counts_by_bid[bid] += 1

    array_of_usefullness = [np.mean(dictionary_of_stats[m]["usefullness"]) for m in multipliers]
    array_of_win_probabilities = [dictionary_of_stats[m]["wins"] / dictionary_of_stats[m]["total"] for m in multipliers]
    array_of_bid_vals = sorted(total_counts_by_bid.keys())

    #округлениями число 48 не получить, на подтверждение гипотезы это не влияет.
    array_of_bid_vals.remove(48)
    bid_array_of_win_probabilities = [win_counts_by_bid[b] / total_counts_by_bid[b] for b in array_of_bid_vals]

    print(f"было воспроизведено {num_trials} значений участника i, было произведено {num_trials*9} аукционов")
    print("ожидается, что максимальная полезность будет при значении множителя равном 1")
    return multipliers, array_of_usefullness, array_of_win_probabilities, array_of_bid_vals, bid_array_of_win_probabilities

#Выполнение симуляции
multipliers, array_of_usefullness, array_of_win_probabilities, array_of_bid_vals, bid_array_of_win_probabilities = strategy_utility_and_winrate()

#Средняя полезность
plt.figure(figsize=(14, 4))
plt.subplot(1, 3, 1)
plt.plot(multipliers, array_of_usefullness, marker='o', color='teal')
plt.title('Средняя полезность от коэффициента ставки')
plt.xlabel('Коэффициент (ставка = коэффициент * vᵢ)')
plt.ylabel('Средняя полезность uᵢ')
plt.grid(True)

#Вероятность выигрыша от множителя
plt.subplot(1, 3, 2)
plt.plot(multipliers, array_of_win_probabilities, marker='s', color='orange')
plt.title('Вероятность выигрыша от коэффициента ставки')
plt.xlabel('Коэффициент (ставка = коэффициент * vᵢ)')
plt.ylabel('Вероятность выигрыша')
plt.grid(True)

#Вероятность выигрыша от абсолютного значения
plt.subplot(1, 3, 3)
plt.plot(array_of_bid_vals, bid_array_of_win_probabilities, marker='d', color='darkred')
plt.title('Вероятность выигрыша от ставки bᵢ')
plt.xlabel('Ставка bᵢ')
plt.ylabel('Вероятность выигрыша')
plt.grid(True)

plt.tight_layout()
plt.show()
