**DoS Attack (Denial of Service)**
A DoS attack is a cyberattack in which a single system or source sends a large number of requests to a server, making it slow or unavailable to legitimate users.
Example: One computer continuously sends requests to an online shopping website, making it unavailable to other customers.


**2. DDoS Attack (Distributed Denial of Service)**
A DDoS attack is a cyberattack in which multiple compromised computers or devices send huge amounts of traffic to a target server simultaneously, making the service unavailable.
Example: Thousands of infected computers simultaneously send requests to a banking website, causing it to crash or become unavailable.

**Port Scanning**
Port scanning is a technique used to check the ports of a computer or server to identify which ports are open, closed, or filtered.
A port is a logical communication endpoint used by applications to send and receive network data.

**Nmap (Network Mapper)**
Nmap is a tool used by network administrators and cybersecurity professionals to:
1. Discover devices on a network.
2. Identify open ports.
3. Detect running services.
4. Identify service versions.
5. Perform operating system detection.
6. Audit network security.


**Brute Force Attack**
A brute force attack is a type of cyberattack in which an attacker tries different combinations of usernames and passwords repeatedly until the correct credentials are found.

In simple words, the attacker keeps guessing passwords until one works.

**Web ATTACK**
A web attack is a type of cyberattack in which an attacker targets a website, web application, or web server to steal information, gain unauthorized access, modify data, or disrupt services.

In simple words, a web attack happens when someone tries to exploit weaknesses in a website or web application.

Example: An attacker exploits a weakness in an online shopping website to steal customers' personal information or payment details.

Web attacks are generally harder to detect than DDoS attacks because they often use normal-looking web requests and exploit vulnerabilities in applications. They may generate very little traffic and can hide malicious code inside legitimate-looking requests. HTTPS encryption and stolen user credentials can make detection even more difficult.

In contrast, DDoS attacks generally generate unusually large amounts of traffic, making abnormal network activity easier to identify.

# CIC-IDS2017 – Attack Notes

## 1. FTP-Patator
A brute force attack that repeatedly tries different username-password combinations to access an FTP server.
Its main objective is to gain unauthorized access to files.

## 2. SSH-Patator
A brute force attack that attempts to guess SSH login credentials.
Its objective is to gain unauthorized remote access to a computer or server.

## 3. DoS Hulk
An HTTP-based Denial of Service attack that sends excessive requests to a web server.
Its objective is to overload server resources and make the website unavailable.

## 4. DoS GoldenEye
An HTTP-based DoS attack that repeatedly sends requests and keeps connections active.
It attempts to exhaust web server resources and disrupt normal access.

## 5. DoS Slowloris
A slow HTTP attack that keeps multiple connections open using incomplete requests.
It consumes server connection resources and prevents legitimate users from connecting.

## 6. DoS Slowhttptest
A slow HTTP denial-of-service attack that uses slow or incomplete HTTP communication.
It attempts to exhaust server resources and reduce website availability.

## 7. Heartbleed
A vulnerability in certain OpenSSL versions that allows attackers to read unintended data from server memory.
It may expose sensitive information such as passwords and private keys.

## 8. Web Attack – Brute Force
An attack that repeatedly tries different passwords to access a website or web application.
Its objective is to gain unauthorized access to user or administrator accounts.

## 9. Web Attack – XSS
Cross-Site Scripting involves injecting malicious scripts into a vulnerable website.
These scripts execute in another user's browser and may steal session information.

## 10. Web Attack – SQL Injection
An attack that inserts malicious SQL commands into vulnerable website inputs.
It can allow attackers to access, modify or delete database information.

## 11. Infiltration
An attack in which an attacker gains unauthorized access to a computer or network.
It may lead to data theft, system compromise and further malicious activities.

## 12. Bot
Malicious automated software or compromised devices perform unwanted network activities.
Bots may steal information, send spam or participate in coordinated attacks.

## 13. PortScan
A technique used to discover open, closed or filtered ports on a computer or server.
It helps identify available services and potential security weaknesses.

## 14. DDoS
A Distributed Denial of Service attack uses multiple compromised devices to send excessive traffic to a target.
It overloads server resources and makes services unavailable to legitimate users.

## 15. Benign
BENIGN represents normal network traffic that does not contain any detected attack.


## Day 2: Data understanding (EDA)
- Dataset: CIC-IDS2017, 8 CSV files, 2,830,743 rows x 79 columns
- Benign is about 80% of the data; the smallest class (Heartbleed) has 11 rows
- Raw problems: 4,376 infinite values, 1,358 missing values, 330,995 duplicate rows
- Web attack labels had garbled characters (encoding problem)
- Why I capped big classes at 60,000. The data was extremely imbalanced (Benign was about 80% of the rows, Heartbleed had 11). I capped each large class at 60,000 rows to reduce the imbalance and speed up training, and kept all rows of the small classes.

## Day 3: Cleaning
- Removed 332,558 rows (about 12%): 2,830,743 -> 2,498,185
- Fixed infinite and missing values, duplicates, and label names
- Duplicates were uneven: SSH-Patator lost about 45%, PortScan about 43%, DoS Hulk about 25%
- Why: (attack tools send many near-identical connections)
- Why I removed duplicates before the split: (so identical rows can't be in both train and test)
- Sample after cleaning: 274,187 rows


## Day 4: Label grouping, split, feature selection

**Label grouping**
- Merged 15 labels into 8 classes: Benign, DoS, DDoS, Port Scan, Brute Force, Web Attack, Bot, Other
- Why: (some classes were too small to learn, e.g. Heartbleed 11 rows, SQL Injection 21 rows)
- "Other" (Infiltration + Heartbleed) has only 47 rows in total, 9 in the test set, so its scores can't be trusted
- Kept the original label in `Label_fine`, so I can check later which specific attack the model confuses

**Feature engineering**
- Created 5 features: total_packets, total_bytes, fwd_bwd_packet_ratio, fwd_bwd_bytes_ratio, bytes_per_packet
- Only 2 survived feature selection (the two ratios). The other 3 were highly correlated with existing columns.
- Why the `+ 1` in the ratios: (to avoid dividing by zero)

**Train/test split**
- 80/20 stratified split: 219,349 train rows, 54,838 test rows
- Why stratified: (so each class, even tiny ones, appears in train and test in the same proportion)
- random_state=42 so the split is repeatable

**Feature selection (train set only)**
- 83 features -> dropped 8 constant + 30 highly correlated (> 0.95) -> kept 45
- Why only the training set: (so test information can't influence which features the model sees)

**Scaling**
- StandardScaler fitted on train only, saved to models/scaler.joblib
- Needed for Logistic Regression and the anomaly detectors, not for tree models

**Leakage rule I follow**
- Anything that learns from data (feature selection, scaler, SMOTE later) is fitted on train only and then applied to test

**Problems I hit and how I fixed them**
- Created files in the wrong folder (nested src/notebooks folders) -> moved them to the right place and checked the path in the breadcrumb.

jk


