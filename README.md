# teaching-insighter

## Usage

### 1. Automatic labeling

Run 'auto_label/label_topic.py' to get the automatic labeling. You can customize the label generation, for example:

python auto_label/label_topic.py --line_corpus_path cs510.dat  --label_min_df 2 --n_cand_labels 5 --n_topics 5

Please see https://github.com/xiaohan2012/chowmein for more information.

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
