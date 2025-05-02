import numpy as np
import matplotlib.pyplot as plt

def strategy_utility_and_winrate(num_trials=10000):
    # товары
    k = 5
    #множители ставок исследуемого игрока
    multipliers = [0.7, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.3]
    stats = {m: {"utility": [], "wins": 0, "total": 0} for m in multipliers}

    for _ in range(num_trials):
        v_i = np.random.randint(10, 51)
        other_bids = np.random.randint(1, 51, size=np.random.randint(9, 25))

        for m in multipliers:
            b_i = int(round(m * v_i))
            bids = np.append(other_bids, b_i)
            bidder_index = len(bids) - 1

            sorted_indices = np.argsort(bids)[::-1]
            allocation = np.zeros(len(bids), dtype=int)
            winners = sorted_indices[:k]
            allocation[winners] = 1

            price = bids[sorted_indices[k]] if len(bids) > k else 0
            got_item = allocation[bidder_index] == 1
            utility = v_i - price if got_item else 0

            stats[m]["utility"].append(utility)
            stats[m]["wins"] += int(got_item)
            stats[m]["total"] += 1

    avg_util = [np.mean(stats[m]["utility"]) for m in multipliers]
    win_prob = [stats[m]["wins"] / stats[m]["total"] for m in multipliers]
    print(f"было воспроизведено {num_trials} значений участника i, было произведено {num_trials*9} аукционов")
    print("ожидается, что максимальная полезность будет при значении множителя равном 1")
    return multipliers, avg_util, win_prob

#Выполнение симуляции
multipliers, avg_util, win_prob = strategy_utility_and_winrate()

#Средняя полезность
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(multipliers, avg_util, marker='o', color='teal')
plt.title('Средняя полезность vs коэффициент ставки')
plt.xlabel('Коэффициент (ставка = коэффициент * vᵢ)')
plt.ylabel('Средняя полезность uᵢ')
plt.grid(True)

#Вероятность выигрыша
plt.subplot(1, 2, 2)
plt.plot(multipliers, win_prob, marker='s', color='orange')
plt.title('Вероятность выигрыша vs коэффициент ставки')
plt.xlabel('Коэффициент (ставка = коэффициент * vᵢ)')
plt.ylabel('Вероятность выигрыша')
plt.grid(True)

plt.tight_layout()
plt.show()
