# -*- coding: utf-8 -*-
"""ANOVA_Kruskal_

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XH0bM6eV6joDKw-qobrUoFW5GlIi4fhr
"""

import random
from matplotlib.pyplot import hist, show
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import shapiro

n = 4        # sample size
m = 200000   # number of samples

means = []
stds = []

for j in range(m):
    sample = [random.gauss(0,1) for i in range(n)]
    mean = sum(sample) / n
    disp = sum([(x-mean)**2 for x in sample]) / (n-1)
    means.append(mean)
    stds.append(disp ** 0.5)

z = [n**0.5 * means[i] for i in range(m)]
t = [n**0.5 * means[i]/stds[i] for i in range(m)]

hist(z, bins = 50, alpha = 0.5, color='r', density=True, range=[-4, 4])
hist(t, bins = 50, alpha = 0.5, color='b', density=True, range=[-4, 4])
show()

URL = 'https://stepik.org/media/attachments/lesson/8083/genetherapy.csv'
df = pd.read_csv(URL)
df.head()

df.info()

# Проверка нормальности распределения (например, тест Шапиро-Уилка)


groups = df.groupby('Therapy')['expr']
normality = {group: shapiro(values)[1] for group, values in groups}

print("Нормальность распределения (p-value):")
for group, p in normality.items():
    print(f"{group}: {p:.4f}")

"""Шапиро-Уилк говорит, что распределено в принципе нормально. Особенно D)
Посмотрим на графики.

"""

sns.histplot(data=df, x="expr", hue="Therapy", bins = 15, kde = True)

# Настройка стиля графиков
sns.set(style="whitegrid", palette="pastel")

# Боксплот
plt.figure(figsize=(10, 6))
sns.boxplot(x='expr', y='Therapy', data=df)
plt.title('Распределение экспрессии гена по группам')
plt.xlabel('Группа')
plt.ylabel('Уровень экспрессии')
plt.show()

plt.figure(figsize=(10, 6))
sns.pointplot(x='expr', y='Therapy', data=df,
              ci=95,  # 95% доверительный интервал
              capsize=0.1,  # "Шляпки" на интервалах
              color='red')
plt.title('Средняя экспрессия гена с 95% доверительным интервалом')
plt.xlabel('Группа')
plt.ylabel('Уровень экспрессии')
plt.show()

plt.figure(figsize=(12, 7))
sns.boxplot(x='expr', y='Therapy', data=df, width=0.4)
sns.pointplot(x='expr', y='Therapy', data=df,
              ci=95, color='red', capsize=0.1, scale=0.7)
plt.title('Экспрессия гена: распределение и доверительные интервалы')
plt.xlabel('Группа')
plt.ylabel('Уровень экспрессии')
plt.show()

# Проверка гомогенности дисперсий (тест Левена)
from scipy.stats import levene

levene_stat, levene_p = levene(*[group.values for name, group in groups])
print(f"\nТест Левена (p-value): {levene_p:.4f}")

# Однофакторный ANOVA
model = ols(f'expr ~ Therapy', data=df).fit() #зависимая и независимая переменная. Лучше в виде variables оформить
anova_table = sm.stats.anova_lm(model, typ=2)
print("\nРезультаты ANOVA:")
print(anova_table)

# Пост-хок тест (Тьюки) для парных сравнений
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(df['expr'], df['Therapy'])
print("\nТест Тьюки:")
print(tukey.summary())

# Визуализация
plt.figure(figsize=(10, 6))
sns.boxplot(hue='Therapy', y='expr', data=df, palette='viridis')
plt.title(f'Экспрессия гена по группам')
plt.show()

"""##Представим, что данные не нормальные. (тест Краскела-Уоллеса)"""

!pip install scikit-posthocs

from scipy.stats import kruskal
import scikit_posthocs as sp  # Для пост-хок тестов



# 1. Подготовка данных: разделяем значения по группам
groups = df.groupby('Therapy')['expr'].apply(list)

# 2. Тест Крускала-Уоллиса
stat, p_value = kruskal(*groups)
print(f"Результат теста Крускала-Уоллиса:")
print(f"Статистика = {stat:.3f}, p-value = {p_value:.4f}")

# 3. Пост-хок тест Данна для парных сравнений (если p-value < 0.05)
if p_value < 0.05:
    print("\nПроводим пост-хок анализ:")
    dunn_result = sp.posthoc_dunn(df, val_col='expr', group_col='Therapy', p_adjust='holm')
    print("Матрица p-values:")
    print(dunn_result)
else:
    print("\nНет значимых различий между группами.")

# 4. Визуализация
plt.figure(figsize=(10, 6))
sns.boxplot(x='Therapy', y='expr', data=df, palette='Set2')
plt.title('Распределение экспрессии гена по группам (Крускал-Уоллис)')
plt.show()

"""#Попробуем воспроизвести многофакторный анализ.

"""

import pandas as pd
from statsmodels.graphics.factorplots import interaction_plot
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene
from statsmodels.stats.multicomp import pairwise_tukeyhsd

URL = 'https://stepik.org/media/attachments/lesson/9250/atherosclerosis.csv'
data_1 = pd.read_csv(URL)
# Проверка структуры данных
print(data_1.head())
print(data_1.describe())
print(data_1["age"].unique())
print(data_1["dose"].unique())

"""##Проверка предположений ANOVA
* нормальность распределения остатков

"""

# Построение модели
model = ols('expr ~ C(age) + C(dose) + C(age):C(dose)', data=data_1).fit()

# Тест Шапиро-Уилка для остатков
shapiro_stat, shapiro_p = shapiro(model.resid)
print(f"Shapiro-Wilk p-value: {shapiro_p:.4f}")
# Если p < 0.05 → данные не нормальны → используйте непараметрические тесты.

"""* гомогенность дисперсий (тест Левена)"""

# Группируем данные по комбинациям факторов
groups = data_1.groupby(["age", "dose"])["expr"].apply(list).values

# Тест Левена
levene_stat, levene_p = levene(*groups)
print(f"Levene's p-value: {levene_p:.4f}")
# Если p < 0.05 → дисперсии неоднородны → используйте поправки (Welch ANOVA).

"""* визуализируем данные"""

# Боксплот для взаимодействия факторов
plt.figure(figsize=(12, 6))
sns.boxplot(x="age", y="expr", hue="dose", data=data_1, palette="viridis")
plt.title("Распределение экспрессии гена по группам")
plt.show()

plt.figure(figsize=(10, 6))
#x="age", y="expr", hue="dose", data=data_1, palette="viridis"
sns.pointplot(x='dose', y='expr', hue = 'age',data=data_1,
              ci=95,  # 95% доверительный интервал
              capsize=0.1,  # "Шляпки" на интервалах
              color='red')
plt.title('Средняя экспрессия гена с 95% доверительным интервалом')
plt.xlabel('Группа')
plt.ylabel('Уровень экспрессии')
plt.show()

"""* двухфакторный ANOVA"""

# Построение модели с взаимодействием факторов
model = ols('expr ~ C(age) + C(dose) + C(age):C(dose)', data=data_1).fit()
anova_table = sm.stats.anova_lm(model, typ=2)  # Тип 2 для несбалансированных данных

print("Результаты ANOVA:")
print(anova_table)

"""* Интерпретация результатов
Основные эффекты:

C(age_group): Влияние возраста на экспрессию гена.

C(dose): Влияние дозировки на экспрессию гена.

* Эффект взаимодействия:

C(age_group):C(dose): Взаимодействие возраста и дозировки.

* Критерий значимости:

PR(>F) < 0.05 → эффект статистически значим.

* пост-хок анализ
"""

# Для возраста
tukey_age = pairwise_tukeyhsd(data_1["expr"], data_1["age"])
print("Попарные сравнения (возраст):")
print(tukey_age.summary())

# Для дозировки
tukey_dose = pairwise_tukeyhsd(data_1["expr"], data_1["dose"])
print("Попарные сравнения (дозировка):")
print(tukey_dose.summary())

# Для взаимодействия (пример для группы "young")
young_data = data_1[data_1["age"] == 1]
tukey_young = pairwise_tukeyhsd(young_data["expr"], young_data["dose"])
print("Попарные сравнения (дозировка для молодых):")
print(tukey_young.summary())

URL = 'https://stepik.org/media/attachments/lesson/9250/birds.csv'
data = pd.read_csv(URL)

#data=pd.read_csv('birds.csv', sep=',')
#Картинка
fig=interaction_plot(data.sex,data.hormone,data.var4,colors=['green','red'], markers=['D','^'], ms=10)

#Степени свободы
N = len(data.var4)
m1 = len(data.hormone.unique())
m2 = len(data.sex.unique())
df_a = m1 - 1
df_b = m2 - 1
df_axb = df_a*df_b
df_w = N - m1*m2

#Общее среднее
grand_mean = data['var4'].mean()

#Суммы квадратов
ssq_a = sum([(data[data.hormone ==i].var4.mean()-grand_mean)**2 for i in data.hormone])
ssq_b = sum([(data[data.sex ==i].var4.mean()-grand_mean)**2 for i in data.sex])
ssq_t = sum((data.var4 - grand_mean)**2)
spl_age=[data[data.hormone == i] for i in data.hormone.unique()]
age_means=[[x_age[x_age.sex == d].var4.mean() for d in x_age.sex] for x_age in spl_age]
ssq_w = sum([sum((spl_age[i].var4-age_means[i])**2) for i in range(len(data.hormone.unique()))])
ssq_axb = ssq_t-ssq_a-ssq_b-ssq_w

#Средние квадраты
ms_a = ssq_a/df_a
ms_b = ssq_b/df_b
ms_axb = ssq_axb/df_axb
ms_w = ssq_w/df_w

#F-значения
f_a = ms_a/ms_w
f_b = ms_b/ms_w
f_axb = ms_axb/ms_w

#P-значения
p_a = stats.f.sf(f_a, df_a, df_w)
p_b = stats.f.sf(f_b, df_b, df_w)
p_axb = stats.f.sf(f_axb, df_axb, df_w)

#результаты
results = {'sum_sq':[ssq_a, ssq_b, ssq_axb, ssq_w], 'df':[df_a, df_b, df_axb, df_w],'F':[f_a, f_b, f_axb, 'NaN']\
          ,'PR(>F)':[p_a, p_b, p_axb, 'NaN']}
columns=['sum_sq', 'df', 'F', 'PR(>F)']
aov_table1 = pd.DataFrame(results, columns=columns, index=['hormone', 'sex','hormone : sex', 'Residual'])

print(aov_table1)