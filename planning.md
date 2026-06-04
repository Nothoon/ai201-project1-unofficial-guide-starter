# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

**Off Campus Housing Expieriences for SDSU** 

There are no official channels regarding best and worse places to get housing off campus near SDSU. Since Juniors and Seniors are unable to live on campus this is a frequently searched for domain.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |SDSU Reddit Thread|A thread talking about off campus housing|https://www.reddit.com/r/SDSU/comments/1rd1srd/off_campus_housing|
| 2 |SDSU Reddit Thread|A thread talking about off campus housing as a transfer|https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/|
| 3 |SDSU Reddit Thread|A thread talking about where to live off-campus|https://www.reddit.com/r/SDSU/comments/1jjml66/where_to_live_offcampus/|
| 4 |SDSU Reddit Thread|A thread asking where to house off-campus as a transfer student|https://www.reddit.com/r/SDSU/comments/1s3vvzl/i_got_accepted_housing/|
| 5 |SDSU Reddit Thread|A thread asking about off campus living expenses|https://www.reddit.com/r/SDSU/comments/1r63ttx/off_campus_living/|
| 6 |SDSU Facebook Group|A Facebook group regarding SDSU off-campus housing search|https://www.facebook.com/groups/sandiegostateuniversitysdsuhousingsublet/|
| 7 |Rive Apartments Yelp|A commonly rented apartment complex's Yelp Page|https://www.yelp.com/biz/the-rive-san-diego-4?dd_referrer=https%3A%2F%2Fwww.google.com%2F|
| 8 |Union Grantville Apartments Yelp |A commonly rented apartment complex's Yelp Page|https://www.yelp.com/biz/union-grantville-san-diego |
| 9 |5025 Apartments Yelp|A commonly rented apartment complex's Yelp Page|https://www.yelp.com/biz/fifty-twenty-five-san-diego-4|
| 10 |Unishack Article|An article about the best campus student housing|https://www.unishack.com/blog/top-5-best-apartments-near-sdsu-for-off-campus-student-housing|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
800 characters

**Overlap:**
150

**Reasoning:**
800 is a good midrange for short and longer texts. I have reddit posts but also yelp reviews that may be longer. 150 overlap is less than a fourth of the chunk size to reduce repition but still include fuller ideas.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
sentence-transformers (all-MiniLM-L6-v2)

**Top-k:**
6 Chunks

**Production tradeoff reflection:**
For context length, a short context model would be good for short reddit comments, short reviews, and facebook posts. Which would be better in my situation because most of my documents are just short comments/reviews/suggestions.

Multilingual support wouldn't be too beneficial as the main speaking language is English are there are more English supported resources such as the SDSU subreddit, many yelp reviews, and facebook groups.

Having a model tuned for specifically housing language would be very beneficial even though it may require some more fine-tuning.

A faster embedding model would probably be better than a slow one so that someone researching could be cross-checking an AI's answer with other resources they have. Though the trade-off is worse accuracy.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |What are the most rented apartment complexes|Rive, 5025, Grantville|
| 2 |How is the maintenence at 5025|Slow and unresponsive|
| 3 |What is the average pricing for an apartment|$1000-$2000|
| 4 |How are the amenties at the Rive|Includes a full gym, pool, and shuttle bus to school|
| 5 |What do students say about the parking situation at Union Grantville|Expensive and not worth it|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. I anticipate that it will retrieve maybe irrelevent information based on the specifity of the question if its not mentioned anywhere in the reviews.

2. I anticipate it may have bad chunking just because of the varying size of reviews and etc.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                     SDSU OFF-CAMPUS HOUSING RAG PIPELINE                         ║
╚══════════════════════════════════════════════════════════════════════════════════╝

 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  STAGE 1: DOCUMENT INGESTION                                                │
 │                                                                             │
 │  Sources (manual copy/paste → .txt files)                                   │
 │                                                                             │
 │  [Reddit Threads] [Yelp Reviews] [Facebook Group] [Unishack Article]        │
 │       5 posts          3 pages        1 group           1 article           │
 │                                                                             │
 │                         raw .txt files                                      │
 └───────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  STAGE 2: CHUNKING                                                          │
 │                                                                             │
 │  Tool: Python (custom chunk_text())                                         │
 │                                                                             │
 │  chunk size: 800 chars  │  overlap: 150 chars                               │
 │                                                                             │
 │  "The Rive has a gym..."─┐                                                  │
 │  "...gym, pool, and   ───┼──► [chunk 1] [chunk 2] [chunk 3] ...             │
 │   shuttle to SDSU..."    ┘         overlapping text segments                │
 └───────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  STAGE 3: EMBEDDING + VECTOR STORE                                          │
 │                                                                             │
 │  Embedding Model: sentence-transformers (all-MiniLM-L6-v2)                  │
 │  Vector Store:    ChromaDB                                                  │
 │                                                                             │
 │  [chunk 1] ──► [0.24, 0.87, ...]  ──► ┌─────────────┐                       │
 │  [chunk 2] ──► [0.11, 0.52, ...]  ──► │   ChromaDB  │                       │
 │  [chunk 3] ──► [0.76, 0.33, ...]  ──► │  (on disk)  │                       │
 │     ...                           ──► └─────────────┘                       │
 └───────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                       ┌─────────┘
                       │   At query time:
                       ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  STAGE 4: RETRIEVAL                                                         │
 │                                                                             │
 │  User Query: "What are amenities like at The Rive?"                         │
 │       │                                                                     │
 │       ▼                                                                     │
 │  all-MiniLM-L6-v2 ──► query vector                                          │
 │       │                                                                     │
 │       ▼                                                                     │
 │  ChromaDB cosine similarity search  ──► top-k = 6 chunks returned           │
 └───────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  STAGE 5: GENERATION                                                        │
 │                                                                             │
 │  LLM: llama-3.3-70b-versatile                                               │
 │                                                                             │
 │  prompt = system instructions                                               │
 │          + [6 retrieved chunks as context]                                  │
 │          + user question                                                    │
 │                │                                                            │
 │                ▼                                                            │
 │         Groq LLM response                                                   │
 │                │                                                            │
 │                ▼                                                            │
 │  "Based on student reviews, The Rive includes a gym, pool..."               │
 └─────────────────────────────────────────────────────────────────────────────┘
```
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec
     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Document Ingestion**

AI Tool: ChatGPT

Input: URLS

Output Expectations: text quotes

Verification: Check relevance to the domain

For document ingestion the plan is to manually copy/paste reviews, comments, and articles into .txt files with the help of ChatGPT scraping relevant info.

**Chunking**

AI Tool: Claude Code

Input: planning.md Chunking section

Output Expectations: Python code with explanation

Verification: Debug the function by printing out its chunk production

For chunking the plan is to prompt Claude Code with planning.md's Chunking section. I will verify its code by using various printing statements to ensure its working and the correct chunking spec

**Embedding + Vector Store**

AI Tool: Claude Code

Input: Embedding tech stack (ChromaDB and sentence-transformers (all-MiniLM-L6-v2))

Output Expectations: Code that will embed the chunks and store it in ChromaDB

Verification: Check the embedding and print chunks stored in ChromaDB

For embedding and vector store the plan is to prompt Claude Code with the embedding tech stack. Letting it know that we will be processing text chunks. The expectation of output is code that will correctly embed and store into ChromaDB. I will verify by using print statements and seeing if ChromaDB is able to retrieve anything.

**RETRIEVAL**

AI Tool: Claude Code

Input: Retrival section of planning.md

Output Expectations: Code that will correctly embed the query and cosine similarity search ChromaDB and return top-k

Verification: Check returned chunks and its relevance to the query

For the retrieval part the plan is to prompt Claude Code with the retrieval section of planning.md so that it knows the specs. I expect code that correctly does a cosine similarity search and gives top-k chunks. I will verify by checking the textual content of the returned chunks and checking the cosine similarity scores of the returned chunks.

**Generation**

AI Tool: Claude Code

Input: Organize chunks and prompt LLM with grounding prompt

Output Expectations: Code the correctly uses API and gives all the relevant chunks and system prompting (grounding)

Verification: Check the returned response and its accuracy.

For the generation part the plan is to prompt Claude Code to correctly format the returned chunks and getting a grounding prompt. The expectation is for it to generate code that will sucessfully generate a response from the LLM. I will verify by checking the questions in the evaluation plan and seeing if it matches with the LLM's responses

