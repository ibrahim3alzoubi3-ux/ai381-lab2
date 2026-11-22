# Model selection

Fill this in after you have trained your candidates in MLflow. Short sentences are fine. Use numbers from your runs.

## The question
The model predicts whether a customer is likely to leave the service. A wrong prediction could cause the company to miss an at-risk customer or waste resources on a customer who was not going to leave.

## Candidates

| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---|---|---|---|---|---|
| Logistic Regression | Simple and fast baseline | 0.798 | 0.495 | 0.250 | 4.035 | 4 | a58d7048 |
| Random Forest | To test a nonlinear ensemble | 0.759 | 0.454 | 0.222 | 13.500 | 3160 | 4e54443c |
| Gradient Boosting | To test boosted decision trees | 0.748 | 0.417 | 0.222 | 7.226 | 142 | caaaabfa |


## The champion
I selected Logistic Regression as the champion because it achieved the highest overall F1 score (0.495) and AUC (0.798), with the lowest p95 latency (4.035 ms) and a small model size (4 KB). However, I accepted lower F1 scores for one-year and two-year contract customers, where other models performed better.
## My promotion rules
- Latency budget (p95): 20 ms, because it allows some performance variation while keeping predictions fast.
- Minimum gain to replace the champion (F1 points): 0.01, because a new model should provide a meaningful improvement.

## What I would check next
I would monitor changes in customer behavior and evaluate the model regularly on each contract type. If the customer data changes over time, the model's predictions may become less accurate, especially for one-year and two-year contract customers.
