# Классификатор набора параметров
## Состав репозитория

Репозиторий включает в себя 6 основных каталогов:

* `step_ini` - этап генерации конфигурационных файлов;
* `step_genout` - этап генерации запросов;
* `step_caches` - этап запуска симуляторов кэшей;
* `step_final` - финальный этап со сравнением и предсказаниями;
* `stats` - каталог со статистикой частоты появления атрибутов;
* `scache` - каталог с модифицированными генератором и симуляторами кэшей;
* `scache_copy` - ссылка на исходный репозиторий с генератором.

В корневом каталоге репозитория также находится таблица атрибутов `table.json`, полученная парсингом реальных данных. К сожалению, ввиду системного ограничения, в репозитории представлена неполная таблица.

Кроме того, там же расположен парсер реальных данных `parse.py`. С его помощью была получена вышеуказанная таблица.

В качестве подмодуля используется репозиторий `scache`, который размещён в каталоге `scache_copy`.

### Состав каталога `stats`

В каталоге содержится программа `stats.py`, которая по построенной таблице атрибутов выводит частоту встречаемости всех атрибутов в таблице. 

Кроме того, в каталоге имеются два текстовых файла: `res.txt` и `hash_res.txt`. В них находятся результаты выполнения программы для обычной и захэшированной таблицы атрибутов соответственно.

### Состав каталога `step_ini`

Каталог содержит генератор конфигурационных файлов `ini_gen.py` и подкаталог `gen_ini`.

Программа `ini_gen.py` принимает 3 необязательных аргумента командной строки (указываются в том же порядке, что ниже): 

* левая граница интервала генерации _конфигурационных файлов_ (по умолчанию 1);
* левая граница интервала генерации конфигурационных файлов (по умолчанию 1000);
* _seed_ для повторения экспериментов (если не введён - генерируется случайным образом и выводится на экран).

Кроме того, требуется, чтобы в этом каталоге лежал файл `motives.txt`, целиком определяющий структуру генерируемых конфигурационных файлов. Каждая строка должна представлять собой набор атрибутов, отвечающий секции с соответствующим номером. Таким образом, количество строк соответствует количеству секций.

Все сгенерированные конфигурационные файлы помещаются в каталог `gen_ini`, а их название имеет вид "_test`i`.ini_", где `i` - порядковый номер сгенерированного ini-файла.


### Состав каталога `step_genout`

Здесь находятся скрипт `generation.sh` и подкаталог `gen_out`. 

Скрипт `generation.sh` осуществляет запуск генератора запросов, а сами сгенерированные запросы помещаются в каталог `gen_out`.

На вход ему подаются три _обязательных_ аргумента командной строки: левая и правая граница интервала генерации трасс, а также количество запросов в каждой из них (указываются в таком же порядке)

Сам скрипт использует конфигурационные файлы с названием вида "_test`i`.ini_", а генерируемые запросы помещает в подкаталог `gen_out`.
Название генерируемых запросов имеет вид  _"out_test`i`.txt"_, где `i` - порядковый номер сгенерированного запроса.

***Важно!*** Для корректной работы модифицированный генератор должен быть расположен в подкаталоге `scache` корневого каталога репозитория.

### Состав каталога `step_caches`

В директории имеется ряд скриптов (`to_lru.sh`, `to_lru2.sh`, `to_snlru.sh`, а также `to_scache.sh`) с соответствующими им подкаталогами `lru_out`, `lru2_out`, `snlru_out` и `scache_out`, а также подкаталог `log`. Кроме того, в директории же находятся и программы с симуляторами кэшей (`LRU.cpp`, `LRU_2.cpp`, `SNLRU.cpp`). 

Каждый из скриптов подаёт сгенерированную трассу соответствующему кэшу и помещает результат работы в соответствующий подкаталог.

Все скрипты принимают на вход четыре _обязательных_ параметра: левая и правая граница интервала, "делитель" (число M такое, что каждые M запросов происходит "замер" BHR) и размер кэша (в Кб). Кроме того, скрипт `to_lru2.sh` принимает пятый _обязательный_ параметр: вещественное число от 0 до 1, выражающее объём дополнительного сегмента от общего объёма в долях.

Кроме того, каждую из программ можно скомпилировать и запускать в отдельности. Программы принимают на вход в качестве аргументов командной строки имя файла с трассой, "делитель" и размер кэша. Для сегментированных кэшей также принимаются на вход размеры сегментов, выраженные в долях.

Каталог `log` содержит файлы с логом работы кэшей.

### Состав каталога `step_final`

Подкаталог содержит в себе два других подкаталога: `2_caches` и `3_caches`, которые соответствуют случаям двух и трёх алгоритмов кэширования.
Все программы в данном каталоге можно запускать без аргументов на предложенном тестовом наборе. Кроме того, здесь же располагаются скрипты `put_ini.sh` и `put_gen.sh`. Они принимают _три_ обязательных аргумента командной строки: первый и второй - граница интервала для создания конфигурационных файлов/генерации запросов. Третий аргумент для `put_ini.sh` - описанный для `step_ini` seed, а для `put_gen.sh` - количество запросов.

В обоих подкаталогах имеются каталоги подкаталоги `dec_tree`, `KNN`, `graphs`, `tables`. Кроме того, в `2_caches` присутствует директория `lin_reg`, а в `3_caches` - `matrix`. Каталог `tables` носит технический характер: в нём содержатся таблицы со сравнением алгоритмов на разном количестве запросов. Директория `graphs` содержит визуализацию для соответствующих алгоритмов.

#### Получение сравнительной таблицы

В каталогах имеются скрипты `put_lru.sh`, `put_lru2.sh` и `put_snlru.sh` (последний присутствует только в `3_caches`), осуществляющих запуск симуляторов кэшей, `put_cmpr.py`, создающий сравнительную таблицу для алгоритмов, а также `puttghr.sh`, который осуществляет последовательное выполнение всех шагов генерации сравнительных таблиц. Все указанные скрипты (кроме `put_lru2.sh`) принимают 4 параметра: левая и правая граница интервала предсказания алгоритмов, количество запросов и "делитель" (описан в `step_caches`). Кроме того, скрипт `put_lru2.sh` принимает на вход пятый _обязательный_ параметр, соответствующий объёму дополнительного сегмента, выраженного в долях, т. е. число от 0 до 1 (аналогично скрипту `to_lru2.sh`).

В каждом из каталогов также содержатся программы `2_caches.py` и `3_caches.py` соответственно, которые создают сравнительные таблицы для разного количества запросов. Обе они принимают на вход три необязательных параметра: первые два - границы интервала для создания таблиц, третий - идентификатор для указанных таблиц (фигурирует лишь в названии самих таблиц). Такие же параметры на вход принимает программа `compare.py`, которая осуществляет анализ таблиц из `tables` и формирует итоговую сравнительную таблицу `final_table.txt` для алгоритмов кэширования.

Кроме вышеуказанного, каталоги содержат программу `subtable.py`. С её помощью из полной таблицы можно получать "подтаблицы", т.е. таблицу с номерами строк от N до M, которые подаются в качестве параметров, которые затем подаются на вход методам для выбора наилучшего алгоритма кэширования.

Таблица `final_table.txt` содержит итоговую информацию о результате работы кэшей.

В данной таблице имеется несколько столбцов (зависит от количества алгоритмов кэширования):

* список всех мотивов для данного эксперимента;
* показатели качества BHR для каждого из алгоритмов кэширования (каждый - в отдельном столбце);
* если алгоритмов кэширования всего два - отдельный столбец под их разность;
* сравнение BHR (номер класса).

#### Выбор наилучшего алгоритма кэширования

Каталог `lin_reg` состоит из каталогов `dim_2` и `dim_5`. Для корректной работы программ в них (`pol_reg.py` и `lin_reg.py`) достаточно нахождения файлов с именами `res_table.txt` и `true_table.txt`, где `res_table.txt` содержит в себе данные точек с известными, уже полученными данными, а `true_table.txt` - данные точек, для которых необходимо предсказать алгоритм кэширования.

Директория `matrix` содержит две программы: `matrix.py` и `TensorFlow.py`. Для корректной работы этих программ необходимо, чтобы в каталоге с ними лежал файл `full_table.txt`, содержащий таблицу с данными для точек в случае трёх алгоритмов кэширования. Программа `matrix.py` раскладывает исходную таблицу на подматрицы с понижением размерности, а `TensorFlow.py` визуализирует "реальные данные" в случае трёх алгоритмов.

Каталог `dec_tree` содержит две программы - `decision_tree.py` и `decision_PCA.py`. Обе программы для корректной работы требуют нахождения в каталоге с ними файлов `res_table.txt` и `true_table.txt` с данными такого же формата, что был описан выше. Кроме того, опционально программы могут принимать на вход два параметра: _CHECK_DOTS_FROM_ и _CHECK_DOTS_TO_, которые должны соответствовать левой и правой границе интервала точек из `true_table.txt`.

Каталог `KNN` содержит в себе две программы - `table_analyzer.py` и `cmpr_pred.py`, а также два подкаталога - `dim 2` и `preds`.  Программа `table_analyzer.py` осуществляет анализ исходной таблицы `res_table.txt` и выбор наилучшего алгоритма кэширования (данные об этом выборе помещаются в каталог `preds`). На вход ей опционально подаются параметры _CHECK_DOTS_FROM_ и _CHECK_DOTS_TO_, соответствующие левой и правой границе интервала предсказываемых точек (как и выше), а также _K_ - количество "соседей" для k-NN. Программа `cmpr_pred.py` анализирует предсказания и фактические данные для точек из `true_table.txt`, выводя итоговый результат в зависимости от количества соседей. Каталог `dim 2` содержит аналогичные файлы, но при этом осуществляется понижение размерности точек с 5 до 2.
