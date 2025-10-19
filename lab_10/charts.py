import pandas as pd
import matplotlib.pyplot as plt

# 1. Загрузка данных из CSV
df = pd.read_csv('./time.csv', sep=';')

print(df.tail())
# 2. Группировка по 'exp_name' и вычисление среднего
means = df.groupby('exp_name')[['DB', 'Redis']].mean()
print(means)

# 3. Построение графика
ax = means.plot(
    kind='bar',
    figsize=(10, 6),
    color=['#FF6347', '#4CAF50'],  # зелёный для DB, томатный для Redis
    width=0.8
)

# 4. Настройка графика
plt.title('Среднее время выполнения: DB vs Redis', fontsize=14)
plt.xlabel('Тип операции', fontsize=12)
plt.ylabel('Время (секунды)', fontsize=12)
plt.xticks(rotation=0)
plt.legend(['DB', 'Redis'])
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 5. Добавление значений над столбцами
for container in ax.containers:
    ax.bar_label(container, fmt='%.4f', padding=3)

# 6. Отображение
plt.tight_layout()
plt.show()