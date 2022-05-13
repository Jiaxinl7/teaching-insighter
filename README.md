# teaching-insighter

## Usage

### 2. Question Categorization

Run `grouping.py` to get the `grouping_output.csv`,`Distribution of Question Topics.svg` and `counter_topics.csv`.

`grouping_output.csv`: Result of question labelling.

`Distribution of Question Topics.svg`: Pie chart of distribution of the number of topics.

`counter_topics.csv`: Frequency statistics of topics

```
python grouping.py PATH
```
### 3. Answer Locating

Run `answer_locating.py` to get the answer to each question in `grouping_output.csv`, and append a column `answer` to it.

```
python answer_locating.py PATH
```

### 4. Report Generating

ReportLab will be installed using:

```
pip install reportlab
```

Then run the following command to generate the report:

```
python report_generator.py
```
