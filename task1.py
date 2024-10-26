from time import time
from typing import Dict
import matplotlib.pyplot as plt

def find_coins_greedy(amount: int, coins:list, verbose:bool=False) -> Dict[int, int]:
    """
    Жадібний алгоритм для знаходження кількості монет для видачі решти.
    
    Args:
        amount (int): Сума для розміну
        coins (list): Список номіналів монет, cортований за спаданням
        
    Returns:
        Dict[int, int]: Словник, де ключ - номінал монети, значення - кількість монет
    """
    result = {}
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            result[coin] = count
            amount -= coin * count
            print(f"Монета: {coin}, Кількість: {count}, Залишок: {amount}") if verbose else None
            
        if amount == 0:
            break
            
    return result

def find_min_coins(amount: int, coins:list, verbose: bool=False) -> Dict[int, int]:
    """
    Алгоритм динамічного програмування для знаходження мінімальної кількості монет.
    
    Args:
        amount (int): Сума для розміну
        coins (list): Список номіналів монет, cортований за спаданням
        verbose (bool): Виведення додаткової інформації

    Returns:
        Dict[int, int]: Словник, де ключ - номінал монети, значення - кількість монет
    """
    # Масив для зберігання мінімальної кількості монет для кожної суми
    MAX_VAL = amount + 1
    coins_amount = [MAX_VAL] * (MAX_VAL)
    
    
    # Масив для зберігання останньої використаної монети
    last_coin = [0] * MAX_VAL
    coins_amount[0] = 0
    
    if verbose:
        print(f"Масив кількості монет: {coins_amount}", end="\n\n")
        print(f"Масив останньої монети: {last_coin}", end="\n\n")

    # Заповнюємо масиви coins_amount та last_coin
    for i in range(1, MAX_VAL):
        for coin in coins:
            if coin <= i and coins_amount[i - coin] + 1 < coins_amount[i]:
                coins_amount[i] = coins_amount[i - coin] + 1
                last_coin[i] = coin
                print(f"Сума: {i}, Монета: {coin}, Кількість: {coins_amount[i]}") if verbose else None
    if verbose:
        print(f"Масив кількості монет: {coins_amount}", end="\n\n")
        print(f"Масив останньої монети: {last_coin}", end="\n\n")

    result = {}
    current_amount = amount
    
    while current_amount > 0:
        coin = last_coin[current_amount]
        result[coin] = result.get(coin, 0) + 1
        current_amount -= coin
        print(f"Сума: {current_amount}, Монета: {coin}, Кількість: {result[coin]}") if verbose else None

    return result

def compare_algorithms(amount: int, coins:list) -> tuple:
    """
    Порівнює час виконання обох алгоритмів.
    
    Args:
        amount (int): Сума для розміну
        coins (list): Список номіналів монет, cортований за спаданням
        
    Returns:
        tuple: (результат жадібного алгоритму, час жадібного алгоритму,
               результат динамічного програмування, час динамічного програмування)
    """

    # Тестуємо жадібний алгоритм
    start_time = time()
    greedy_result = find_coins_greedy(amount, coins, verbose=False)
    greedy_time = time() - start_time
    
    # Тестуємо алгоритм динамічного програмування
    start_time = time()
    dp_result = find_min_coins(amount, coins, verbose=False)
    dp_time = time() - start_time
    
    return greedy_result, greedy_time, dp_result, dp_time

def testing()->None:
    """ Тестування алгоритмів """
    amount = 113
    coins = [1, 2, 5, 10, 25, 50]
    print(f"Сума: {amount}, {coins} ", end="\n\n")
    greedy_result, greedy_time, dp_result, dp_time = compare_algorithms(amount, coins)
    print(f"Жадібний алгоритм: {greedy_result}, Час: {greedy_time}")
    print(f"Алгоритм динамічного програмування: {dp_result}, Час: {dp_time}")

def main()->None:
    """ Головна функція """
    # Генерація тестових даних
    test_amounts = [113, 1113, 10113, 111307, 1113113, 11131137]
    test_coins_unsorted = [1, 2, 5, 10, 25, 50]
    test_coins_sorted = sorted(test_coins_unsorted, reverse=True)

    results = {
        "amount": [],
        "greedy_time_sorted": [],
        "dp_time_sorted": [],
        "greedy_time_unsorted": [],
        "dp_time_unsorted": []
    }

    for amount in test_amounts:
        # Тест з відсортованими монетами
        print(f"Сума: {amount}, {test_coins_sorted} ")
        greedy_result, greedy_time, dp_result, dp_time = compare_algorithms(amount, test_coins_sorted)
        results["amount"].append(amount)
        results["greedy_time_sorted"].append(greedy_time)
        results["dp_time_sorted"].append(dp_time)
        print(f"Жадібний алгоритм: {greedy_result}, Час: {greedy_time:0.6f}")   
        print(f"Алгоритм динамічного програмування: {dp_result}, Час: {dp_time:0.6f}")

        # Тест з не відсортованими монетами
        print(f"Сума: {amount}, {test_coins_unsorted} ")
        greedy_result, greedy_time, dp_result, dp_time = compare_algorithms(amount, test_coins_unsorted)
        results["greedy_time_unsorted"].append(greedy_time)
        results["dp_time_unsorted"].append(dp_time)
        print(f"Жадібний алгоритм: {greedy_result}, Час: {greedy_time:0.6f}")
        print(f"Алгоритм динамічного програмування: {dp_result}, Час: {dp_time:0.6f}", end="\n\n")

    plt.figure("Графік порівняння", figsize=(12, 6))
    plt.plot(
        results["amount"],
        results["greedy_time_sorted"],
        label="Жадібний (відсортовані монети)",
        marker="o",
    )
    plt.plot(
        results["amount"], 
        results["dp_time_sorted"], 
        label="Динамічний (відсортовані монети)", marker='o')
    plt.plot(
        results["amount"],
        results["greedy_time_unsorted"],
        label="Жадібний (не відсортовані монети)",
        marker="o",
    )
    plt.plot(
        results["amount"],
        results["dp_time_unsorted"],
        label="Динамічний (не відсортовані монети)",
        marker="o",
    )

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Сума')
    plt.ylabel('Час (секунди)')
    plt.title('Порівняння алгоритмів')
    plt.legend()
    plt.grid(True, which="both", ls="--")

    # Висновки про ефективність алгоритмів
    greedy_efficiency = "O(n)"  # Жадібний алгоритм має лінійну складність
    dp_efficiency = "O(n * m)"  # Алгоритм динамічного програмування має складність O(n * m), де n - сума, m - кількість монет

    plt.annotate(greedy_efficiency, xy=(test_amounts[0], results["greedy_time_sorted"][0]), xytext=(test_amounts[1], results["greedy_time_sorted"][1]),
                 arrowprops=dict(facecolor='blue', shrink=0.05))
    plt.annotate(dp_efficiency, xy=(test_amounts[0], results["dp_time_sorted"][0]), xytext=(test_amounts[1], results["dp_time_sorted"][1]),
                 arrowprops=dict(facecolor='red', shrink=0.05))
    plt.savefig('algorithm_efficiency_comparison.png')
    plt.show()    

if __name__ == "__main__":
    main()
    #testing()