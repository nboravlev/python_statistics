# python_statistics
Статистика в Python. Примеры работы в ГС и выборками, сравнение параметров, статистические тесты. 

### [Очистка данных](https://github.com/nboravlev/python_statistics/blob/main/HW_base_statistic.ipynb)

Подготовка датасета к работе на примере [датасета про лошадей](https://raw.githubusercontent.com/obulygin/pyda_homeworks/master/statistics_basics/horse_data.csv)

- заполнение отсутствующих значений с помощью методов groupby/transform;
- работа с выбросами;
- работа с нечисловыми типами данных;

Библиотеки pandas, numpy

-------

### [Статистические методы](https://github.com/nboravlev/python_statistics/blob/main/HW_casestudy.ipynb)

На примере исторических данных о продажах и оценках [видеоигр](https://raw.githubusercontent.com/obulygin/pyda_homeworks/master/stat_case_study/vgsales.csv) проводятся статистические исследования.

- сэмплирование;
- сравнение выборок между собой по различным параметрам;
- оценка нормальности распределения признака;
- выдвижение гипотез;
- применение параметрических и непараметрических тестов;
- выводы.

Использованные библиотеки: pandas, scipy, seaborn, matplotlib

------

### [Аналитика на тему того, почему я до сих пор не нашел работу аналитиком](https://github.com/nboravlev/python_statistics/blob/main/About_job.ipynb)

Вопрос, который я бы хотел исследовать вот какой: моя цель найти удаленную работу в сфере Gambling в аналитике не в РФ. Я начал рассылать резюме в декабре, меня расстраивала обратная связь со стороны компаний, и я решил заказать английское резюме у экспертов. Хорошее, со всеми буллитами, настроенное на все хитрые алгоритмы. В марте эксперт из компании #TopCV сочинил резюме и сопроводительное письмо. Я стал использовать новые современные эффективные технологии. Уже май, я веду [статистику](https://github.com/nboravlev/python_statistics/blob/main/job_s.csv), накопилось примерно по 100 наблюдений до события и после, и это повод провести аналитику.

- загрузил данные, сформировал датафрейм, наложил на временную шкалу, чтобы убрать пропуски и посмотреть корректную линейную историю;
- посчитал метрик, построил графики;
- разбил датафрейм на до нового резюме и после;
- сделал группировку и агрегацию по названиям вакансий, источникам вакансий и регионам, куда я подавал;
- получилось 3 пары связанных выборок, где я могу проверить, как себя ведут метрики;
- проверил на нормальность распределения признаков непараметриским тестом Шапиро-Уилка;
- померил конверсии тестом Вилкоксона для связанных выборок с ненормальным распределением;
- тест изменений не детектировал.

Использованные библиотеки: pandas, scipy, seaborn, matplotlib
