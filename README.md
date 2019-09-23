# Neural-Code-Search

Neural-Code-Search presents an evaluation dataset consisting of natural language query and code snippet pairs, with the hope that future work in this area can use this dataset as a common benchmark. We also provide the results of two code search models ([NCS](https://dl.acm.org/citation.cfm?id=3211353), [UNIF](https://arxiv.org/abs/1905.03813)) from recent work. 

The full paper is available at [Neural Code Search Evaluation Dataset](https://arxiv.org/abs/1908.09804).

## Dataset contents

All the dataset contents are in the `data` directory. 

### GitHub Repositories
The most popular Android repositories on GitHub (ranked by the number of stars) is used to create the search corpus. For each repository that we indexed, we provide the link, specific to the commit that was used. In total, there are 24,549 repositories. This is located in `data/android_repositories_download_links.txt`.

Example: 

    https://github.com/00-00-00/ably-chat/archive/9bb2e36acc24f1cd684ef5d1b98d837055ba9cc8.zip
    https://github.com/01sadra/Detoxiom/archive/c3fffd36989b0cd93bd09cbaa35123b9d605f989.zip
    https://github.com/0411ameya/MPG_update/archive/27ac5531ca2c2f123e0cb854ebcb4d0441e2bc98.zip
    ...

---
### Search Corpus
The search corpus is indexed using all method bodies parsed from the 24,549 GitHub repositories. In total, there are 4,716,814
methods in this corpus. The code search model will find relevant code snippets (i.e. method bodies) from this corpus given a natural language query. In this data release, we will provide the following information for each method in the corpus:

* **id:** Each method in the corpus has a unique numeric identifier. This ID number will also be referenced in our evaluation
dataset.
* **filepath:** The file path is in the format of `:owner/:repo/relative-file-path-to-the-repo`
* **method_name**
* **start_line:** Starting line number of the method in the file.
* **end_line:** Ending line number of the method in the file.
* **url:** GitHub link to the method body with commit ID and line numbers encoded.

This is located in two parts (due to GitHub file size constraints): `data/search_corpus_1.tar.gz` and `data/search_corpus_2.tar.gz`.

Example: 
```
{
  "id": 4716813,
  "filepath": "Mindgames/VideoStreamServer/playersdk/src/main/java/com/kaltura/playersdk/PlayerViewController.java",
  "method_name": "notifyKPlayerEvent",
  "start_line": 506,
  "end_line": 566,
  "url":  "https://github.com/Mindgames/VideoStreamServer/blob/b7c73d2bcd296b3a24f83cf67d6a5998c7a1af6b/playersdk/src/main/java/com/kaltura/playersdk/PlayerViewController.java\#L506-L566"
}
```
---
### Evaluation Dataset
The evaluation dataset is composed of 287 Stack Overflow question and answer pairs, for which we release the following information: 
* **stackoverflow_id:** Stack Overflow post ID.
* **question:** Title fo the Stack Overflow post.
* **question_url:** URL of the Stack Overflow post.
* **answer:** Code snippet answer to the question.

This is located in `data/287_android_questions.json`.

Example:
```
{
  "stackoverflow_id": 1109022,
  "question": "Close/hide the Android Soft Keyboard",
  "question_url": "https://stackoverflow.com/questions/1109022/close-hide-the-android-soft-keyboard",
  "question_author": "Vidar Vestnes",
  "question_author_url": "https://stackoverflow.com/users/133858",
  "answer": "// Check if no view has focus:\nView 
        view = this.getCurrentFocus(); \nif view != null) {InputMethodManager 
        imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);       
        imm.hideSoftInputFromWindow(view.getWindowToken(), 0);}",
  "answer_url": "https://stackoverflow.com/a/1109108",
  "answer_author": "Reto Meier",
  "answer_author_url": "https://stackoverflow.com/users/822",
  "examples": [1841045, 1800067, 1271795],
  "examples_url": [
    "https://github.com/alextselegidis/easyappointmentsandroid-client/blob/39f1e8...",
    "https://github.com/zelloptt/zello-android-clientsdk/blob/87b45b6...",
    "https://github.com/systers/conference-android/blob/a67982abf54e0...",
  ]
}
```
---
### NCS / UNIF Score Sheet
We provide the evaluation results for two code search models of our creation, each with two variations:
* **NCS:** NCS: an unsupervised model which uses word embedding derived directly from the [search corpus](https://dl.acm.org/citation.cfm?id=3211353).
* **NCS<sub>postrank</sub>:**  an extension of the base NCS model that performs a post-pass ranking, as explained in [here](https://dl.acm.org/citation.cfm?id=3211353).
* **UNIF<sub>android</sub>**, **UNIF<sub>stackoverflow</sub>**: a supervised extension of the NCS model that uses a bag-of-words-based neural network with attention. The supervision is learned using GitHub-Android-Train and StackOverflow-AndroidTrain datasets, respectively, as described here [UNIF](https://arxiv.org/abs/1905.03813).

We provide the rank of the first correct answer (FRank) for each question in our evaluation dataset. The score sheet is
saved in a comma-delimited csv file in `data/score_sheet.csv`.

Example: 
```
No.,StackOverflow ID,NCS FRank,NCS_postrank FRank, UNIF_android FRank,UNIF_stackoverflow FRank
1,1109022,NF,1,1,1
2,4616095,17,1,31,19
3,3004515,2,1,5,2
4,1560788,1,4,5,1
5,3423754,5,1,22,10
6,1397361,NF,3,2,1
```

## Full documentation

See the [CONTRIBUTING](CONTRIBUTING.md) file for how to help out.

## License
Neural-Code-Search is CC-BY-NC 4.0 (Attr Non-Commercial Inter.) (e.g., FAIR) licensed, as found in the LICENSE file.
