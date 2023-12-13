# Sports GPT2

## Fine Tune Space
1. Generate Tags, Questions and Respones from GPT-3.5-turbo

*python FineTuneDataGeneration.py api_key Numtag NumQuestion NumParaphrase NumAnswer*

* api_key: Your Api Key
* Numtag: number of tags, default 200, optional
* NumQuestion: number of questions, default 2, optional
* NumParaphrase: number of question paraphrases, default 1, optional
* NumAnswer: number of answers, default 3, optional

2. Convert Json to TXT for fine-tune

*python Json2Txt.py*