# Bayesian Text Classification

## Introduction
In this Task, we built a Bayesian model to determine whether a piece of text belongs to a particular Shakespear play. The goal is to construct a naïve Bayes classifier in Python that predicts, given a piece of text, which of ten Shakespeare plays it most likely belongs to.

## Data
We used ten Shakespeare plays provided as text files:
1. The Merchant of Venice (merchant.txt)
2. Romeo and Juliet (romeo.txt)
3. The Tempest (tempest.txt)
4. Twelfth Night (twelfth.txt)
5. Othello (othello.txt)
6. King Lear (lear.txt)
7. Much Ado About Nothing (ado.txt)
8. Midsummer Night’s Dream (midsummer.txt)
9. Macbeth (macbeth.txt)
10. Hamlet (hamlet.txt)

## Tasks Accompolished

### Task 1: Word Cleaning
Here, we Write a Python program that accepts a string, extracts the words, and outputs them in lowercase, with all non-alphabetical characters removed.

**Input**
A single line of text.

**Output**
Words in lowercase, separated by a single space.

**Example**
```python
Input: "Your Grace hath ta'en great pains to qualify"
Output: "your grace hath taen great pains to qualify"
```

### Task 2: Bag-of-words
Here, we Write a Python program that reads a text file, extracts all the words, and builds a frequency count of how often each word appears.

**Input**
A single line indicating the filename.

**Output**
Top three most common words in the file.

**Example**
```python
Input: "merchant.txt"
Output: "the i and"
```

### Task 3: Classifying Sentences
Here, we built a classifier to determine which play is more likely to contain a given sentence. Used the bag-of-words model for each play and apply the naïve Bayes formula.

**Input**
A single line of text.

**Output**
The most likely play.

**Example**
```python
Input: "Men, heaven and devils confess'd"
Output: "Othello"
```

### Task 4: Full Estimates
And then we computed the full posterior probabilities for each play, given a sentence. Output the probabilities, rounded to the nearest whole number.

**Input**
A single line of text.

**Output**
Probabilities for each play, ordered from most likely to least likely.

**Example**
```python
Input: "You shall be king."
Output:
Macbeth: 88%
Hamlet: 6%
The Tempest: 4%
...
```

## Running the Code
To run the code, you ensure that all the ten play text files are in the same directory as your Python script. Execute the script with the necessary input as described in each Task.

---
