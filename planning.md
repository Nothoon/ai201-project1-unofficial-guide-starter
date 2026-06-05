# Project 1 Planning: The Unofficial Guide

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

**Off-Campus Housing Experiences for SDSU Students** 

This domain is valuable because SDSU students often rely on informal sources like Reddit, Yelp, and Facebook to learn about rent, parking, maintenance, amenities, safety, and management quality. Official housing pages may list options, but they usually do not capture student experiences or complaints.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

I will collect original text from posts, comments, reviews, and articles, preserving source URLs and date accessed. Each source will be saved as a separate .txt file with metadata at the top.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |SDSU Reddit Thread|A thread talking about off campus housing|https://www.reddit.com/r/SDSU/comments/1rd1srd/off_campus_housing|
| 2 |SDSU Reddit Thread|A thread talking about off campus housing as a transfer|https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/|
| 3 |SDSU Reddit Thread|A thread talking about where to live off-campus|https://www.reddit.com/r/SDSU/comments/1jjml66/where_to_live_offcampus/|
| 4 |SDSU Reddit Thread|A thread asking where to house off-campus as a transfer student|https://www.reddit.com/r/SDSU/comments/1s3vvzl/i_got_accepted_housing/|
| 5 |SDSU Reddit Thread|A thread asking about off campus living expenses|https://www.reddit.com/r/SDSU/comments/1r63ttx/off_campus_living/|
| 6 |SDSU Reddit Thread|A thread asking for last minute housing|https://www.reddit.com/r/SDSU/comments/1lq9pjr/im_panicking/|
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
I will first split sources by natural units such as Reddit comments, Yelp reviews, and article paragraphs. Items longer than 800 characters will be split into overlapping chunks with 150 characters of overlap. This keeps most short reviews intact while preventing long reviews or articles from exceeding the context size. The overlap helps preserve apartment names and complaints that may appear near chunk boundaries.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->
ChromaDB will store each chunk with metadata including source URL, platform, apartment name, and chunk ID. Retrieval will use cosine similarity and return the top 6 chunks.

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
| 1 |Which apartment complexes appear most often in the collected SDSU housing sources?|The answer should identify frequently mentioned complexes such as The Rive, 5025, and Union Grantville if supported by retrieved sources.|
| 2 |What do students/reviewers say about maintenance at 5025?| The answer should mention slow or unresponsive maintenance only if retrieved reviews support it, and should cite the relevant source chunks.|
| 3 |What rent range do students mention for off-campus housing near SDSU?|The answer should give the range found in the sources and clarify whether it is per person or per unit when possible.|
| 4 |What amenities are mentioned for The Rive?|The answer should mention amenities such as gym, pool, and shuttle only if those appear in the collected sources.|
| 5 |What complaints do students/reviewers make about parking at Union Grantville?|The answer should mention cost/value concerns if supported and distinguish between one review and repeated complaints.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. I anticipate that it will retrieve irrelevent information based on the specifity of the question if its not mentioned anywhere in the reviews.

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

AI Tool: None

Input: N/A

Output Expectations: N/A

Verification: N/A

Document ingestion will be done manually. Reviews, comments, and articles will be pasted into a .txt document and seperated accordingly.

**Chunking**

AI Tool: Claude Code

Input: `planning.md Chunking Strategy` Explain and produce a function that seperates .txt files into spec and labels them.

Output Expectations: A function what when called will be able to seperate a .txt file to spec and label it with a dictionary or similar structure.

Verification: Check the elements of the dictionary/similar structure.

**Embedding + Vector Store**

AI Tool: Claude Code

Input: Using `ChromaDB` and `sentence-transformers (all-MiniLM-L6-v2)` create a function that will correctly embed text chunks and store it into ChromaDB.

Output Expectations: A function that correctly embeds chunks with all the correct information and calls the ChromaDB API to store it.

Verification: Check ChromaDB for any recieved chunks

**RETRIEVAL**

AI Tool: Claude Code

Input: `planning.md Retrieval Approach` Using this spec, write a function that will retrieve the 6 most related chunks to the query from ChromaDB.

Output Expectations: A function that will correctly embed the query then compare it to the chunks in ChromaDB. It should return the 6 most related chunks.

Verification: Check the 6 returned chunks and their similarity to the query.

**Generation**

AI Tool: Claude Code

Input: Create a grounding prompt for the LLM to only use information that it is given. Then create a function that will correctly call the LLM API with the grounding prompt, 6 most relevant chunks, and the query. Finally, return the response from the LLM.

Output Expectations: A function that correctly prompts the LLM and returns a response.

Verification: Check for any returned response and its accuracy answering the query.

