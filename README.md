# generic-datagen

## Goal
* a generic frame work to generate data into various format

## Components
* Model Definition through simple config file
  1. Allow user to specify the relationship of the columes
  2. A set of handy relationship could be selected. e.g. random, linear, non-linear
  3. Support Timestamp as a column. User could specify the granularity of interval. e.g. milliseconds, second, 5 secons. 
  4. Support trend, seasonality and white-noise into data.
  5. Support continuous or categorical data

* Data output
  1. csv
  2. json
  3. yaml
  4. Events 
  5. DB friendly format
  6. Column oriented format

## Sample config file (Let's become yaml engineer)
### Example YAML of a icecream example
```yaml
- name: icecream
  columns:
  - name: timestamp
    data_source: timestamp
  - name: temperature
    type: continuous
    depends_on_columns: null
    depends_on_others:
    - variable_name: x
      source: 
        type: white_noice
        scale: 4
        mean: 25
    relationship:
      input: x
      formula_steps:
      - name: scale
        value: 1
  - name: icecream_melt_speed
    type: continuous
    depends_on_columns: 
    - variable_name: x
      column_source: temperature
    depends_on_others:
    - variable_name: n
      source: 
        type: white_noice
        scale: 0.1
    relationship: 
      input: x
      formula_steps: 
      - name: scale
        value: 0.5
      - name: add
        value: 20
      - name: add
        value_from:
          name: n
      # equal to "0.5 * x + 20 + n"
  - name: icecream_sold
    type: continuous
    depends_on_others:
    - variable_name: n
      source:  
        type: white_noice
        scale: 1
        mean: 0.1
    relationship:
      input: n
      function_steps: 
      - name: sigmoid
      - name: scale
        value: 30
      - name: to_int
  - name: icecream_finished_before_melt
    type: categorical
    depends_on_columns:
    - variable_name: x
      column_source: icecream_melt_speed
    relationship:
      input: x
      function_steps:
      - name: categorical
        candidates: 
        - false
        - true
        rules:
        - output: false
          method: larger_than
          threshold: 32
  row: 
    related_column: timestamp
    format: timerange
    interval: 
      format: second
      value: 3600
    range_start: 01-01-2020:00:00:00
    range_end: 07-01-2020:00:00:00 
  outputs:
  - format: file
    style:
      format: csv
      with_timestamp: true
      prefix: icecream 
  - format: stdout
```
### Semantic meaning of the icecream example
1. 5 columns: timestamp, temperature, icecream_melt_speed, icecream_sold and icecream_finished_before_melt
2. row is bounded in a time range
3. output is in csv format and also stdout
4. ***temperature*** is from white_noice
5. ***icecream_melt_speed equal*** = "0.5 * ***temperature*** + 20 + ***noise***"
6. ***icecream_sold*** = int ( 30 * sigmoid ( ***noise*** ) ), with noise has mean 0.1, std 1
7. ***icecream_finished_before_melt*** = ***icecream_melt_speed*** > 32 ? false : true
