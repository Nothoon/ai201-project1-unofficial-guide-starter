# The Unofficial Guide — Project 1

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

**Off-Campus Housing Experiences for San Diego State University (SDSU) Students** 

This domain is valuable because SDSU students often rely on informal sources like Reddit, Yelp, and Facebook to learn about rent, parking, maintenance, amenities, safety, and management quality. Official housing pages may list options, but they usually do not capture student experiences or complaints.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
500 characters if the comment/review is longer than 500 characters. However, if the comment/review is smaller than 500 it is processed as its own chunk.

**Overlap:**
100 characters

**Why these choices fit your documents:**
Even though some Reddit and Yelp reviews were lengthy I decided to go with a 500 character chunk size because the reviews would be mentioning different aspects of a apartment complex or housing expierience. The full review wouldn't be needed in a chunk because not all of the information in a full length review would be required to answer a query. I chose a 100 overlap to keep most ideas intact but keep repeat text to a minimum.

**Final chunk count:**
My final chunk count is 723 chunks.

**Sample Chunks:**
| # | Chunk Text | Source |
|---|------------|--------|
|1|I just signed my lease and was accepted! Big thanks to Shiloh for giving me an amazing tour, she answered any and all questions I had including helping me fill out my application, and Armiena for helping me when I was having some issues with the approval! From what I can tell, 5025 really cares about its residents and I've had some amazing support from the staff, beyond my expectations. The process took 2 days, so quick and if you have any issues or questions the staff get back to you quickly! I|5025_Yelp_Reviews.txt|
|2|ve a real maintenance team just college kids. I sent in a request for my stovetop to get fixed and they came twice and never solved the issue. Same thing happened because my window wouldn't open so I requested maintenance and they didn't fix it. Overall decent experience because I never had a bug issue here but wish staff was more helpful.|5025_Yelp_Reviews.txt|
|3|One thing I really appreciate is how the staff organizes events for residents. Events like wine nights and charm bracelet making have been a lot of fun. They create a great opportunity to build a community and meet new friends.|5025_Yelp_Reviews.txt|
|4|s took 2 days, so quick and if you have any issues or questions the staff get back to you quickly! I was worried when an issue came up about my lease but Armiena was an absolute angel and saved the day.|5025_Yelp_Reviews.txt|
|5|My awful experience with 5025 started off before I moved in. They had to resend my lease twice before they corrected the information. Thankfully I made sure to check it before signing. When I get to my studio I notice that the apartment wasn't actually cleaned. I would think they would double check the apartments and clean them before the next people moving in. As far as maintenance, they don't have a real maintenance team just college kids. I sent in a request for my stovetop to get fixed and t|5025_Yelp_Reviews.txt|

---


## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
The embedding model and vector database used is sentence-transforers (all-MiniLM-L6-v2) and ChromDB.

**Production tradeoff reflection:**
For context length, a shorter-context embedding model fits my project because most of my documents are short Reddit comments, Yelp reviews, and Facebook posts. This works well for my situation because the majority of the sources are brief comments, with only occasional longer reviews.

Multilingual support would not be very important for this project because the main language of the sources is English. Most of the available resources, such as the SDSU subreddit, Yelp reviews, and Facebook groups, are also primarily in English.

A model tuned specifically for housing-related language would be very beneficial because it could better understand terms related to rent, parking, maintenance, amenities, safety, and management quality. However, this might require additional fine-tuning or a more specialized dataset.

A faster embedding model would also be useful because it would allow users to search and cross-check the AI’s answers more quickly. The main tradeoff is that a faster model may be less accurate than a larger or more specialized model.

**Retrieval Test Results:**

Query One: What amenities are mentioned for The Rive?
|#|Chunk Text|
|-|----------|
|1|The Rive is honestly amazing, the apartments are in good condition with new furniture and appliances, the price is affordable and it's a 5 minute drive to campus, 20 min walk or you can take the free shuttle. The pool area is so pretty and I also love the fire places around the property. My favorite amenity is the communal area where you can study or place pool or even watch the huge tv!!|
|2|treet parking as well. also, the rive is close enough to a bunch of food places and vons that you can walk to it. their amenities are much nicer, the apartments updated better, and just overall seem to take care of their residents a LOT better than 5025. i have a few friends who live at the rive and i am so envious of them|
|3|The Rive (shuttle/parking under), but further away|
|4|I have loved living at the Rive! The amenities are great, it comes fully furnished which is ideal and they have good roommate matching. My room was very clean upon move in and I was very pleased with the new appliances in the apartment as well. The shuttle transport has also been reliable to getting to SDSU campus.|
|5|Edit: lived in the rive|
|6|i enjoy living at the rive because of all the amenities and how close it is to everything! The staff is very attentive and responsive for lots of things! This is the best student apartment living !|

Explanation: The returned chunks are relevant because they mention amenities such as the shuttle, pool, fireplace, and communal area.

Query Two: What do reviewers say about maintenance at 5025?
|#|Chunk Text|
|-|----------|
|1|My awful experience with 5025 started off before I moved in. They had to resend my lease twice before they corrected the information. Thankfully I made sure to check it before signing. When I get to my studio I notice that the apartment wasn't actually cleaned. I would think they would double check the apartments and clean them before the next people moving in. As far as maintenance, they don't have a real maintenance team just college kids. I sent in a request for my stovetop to get fixed and t|
|2|how is 5025|
|3|I can't believe I've moved out months ago and am STILL having problems with 5025.|
|4| I moved into 5025 in August, and so far, I love it here. Amenities are great, especially the 24-hour gym that I've never seen packed. Our apartment was pretty nice moving in, and if there's ever any issues, maintenance requests usually get taken care of very fast. I don't really have any complaints for this apartment!! It's been great so far!!|
|5|update: i live at 5025 and ive had a good experience so far. just depends on what unit you get|
|6|Here's my 5-day experience with 5025. This happened in 2020, but this situation will always be traumatic for me.|

Explanation: The returned chunks are relevant because they talk about people's experience at 5025. Most are bad however some are good which is good so that someone deciding can have an unbiased review.

Query Three: What is the average rent for off-campus housing around SDSU?
|#|Chunk Text|
|-|----------|
|1|Here is a link for off-campus housing at SDSU with some information, but the results near the College Area are rather limited.|
|2|Go on Facebook and search SDSU off-campus housing. They have a lot of rentals and sublets|
|3|SDSU website has a couple options for off-campus school associated options. I had a difficult time when I tried since a lot of the buildings near campus don’t seem to be listed on Zillow or apartments.com. I would try to look up apartment complexes around the school and just go directly to their websites. I’ve seen most studios around $1800-1900+ per month, one beds for like $2200-2500+ and 2bed 2bath for $3000+|
|4|$750 for a bedroom near SDSU|
|5|Other Recommended Apartments For additional options in off-campus housing near SDSU, consider checking out the following apartments:|
|6|feels just right for your needs. For those searching for the best off-campus housing near SDSU, these apartments are a great starting point. Remember, the perfect apartment won’t last long, so act fast!|

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are the Unofficial Guide to off-campus housing for SDSU students. You
answer questions using ONLY the retrieved context provided below, which is
drawn from student posts, reviews, and articles.

Rules you must follow:
1. Answer ONLY using information found in the retrieved context. Do not use
outside knowledge, and do not guess or infer beyond what the context says.
2. If the retrieved context does not contain enough information to answer the
question, respond with exactly: "I don't have enough information to answer
that." Do not try to fill the gap.
3. Attribute your claims. When you state something, indicate which source it
came from (apartment name and/or platform).
4. Distinguish between a single review and a repeated pattern when the context
supports it.
5. After your answer, include a "Sources:" section listing the distinct \
sources you used, formatted as: "- <apartment or platform> (<source_url>)".
Only list sources you actually drew from.

Keep the answer concise and grounded in the evidence.

**How source attribution is surfaced in the response:**
Source attribution is built into the text of the response itself and embedded into the elements of the interface. A drop down button appears when answering a valid question with links and the specific text in which the answer was derived from.

**Example Outputs**
|#|Response Text|
|-|-------------|
|1|The Rive has several amenities mentioned, including a pool area, fire places around the property, a communal area for studying, playing pool, or watching a huge TV, fully furnished apartments, new appliances, and a free shuttle to SDSU campus. Sources: The Rive (https://www.yelp.com/biz/the-rive-san-diego-4)|
|2|According to reviews on Yelp, maintenance at 5025 is a mixed experience. One reviewer (Source 2) states that "maintenance requests usually get taken care of very fast." However, another reviewer (Source 1) mentions that they don't have a "real maintenance team just college kids" and had issues with getting their stovetop fixed. Additionally, a third reviewer (Source 6) notes that maintenance requests often fall to a student worker at the front desk who lacks the training or authority to address issues, leading to delayed resolutions.Sources: 5025 (https://www.yelp.com/biz/fifty-twenty-five-san-diego-4)|

**Out of Scope Query**
Query: What's the average rent on a house near SDSU?

Response: ```I don't have enough information to answer that.```

Explanation: The system only includes apartment complexes under its term housing. I did not include any resources regarding renting houses only apartment complexes.

---

## Query Interface

The interface consists of a text box for the query, an ask button to submit your query, sample questions you can ask, and finally a sources drop down menu.

Sample uses could be:

1. Click "What amenities are mentioned for the Rive?"
2. See generated response: 
```
   The Rive has several amenities mentioned, including a pool area, fire places around the property, a communal area for studying, playing pool, or watching a huge TV, fully furnished apartments, new appliances, and a free shuttle to SDSU campus (Source 1: The Rive | Yelp, Source 4: The Rive | Yelp). Additionally, it's mentioned that the amenities are great and that they have good roommate matching (Source 4: The Rive | Yelp). Sources:The Rive (https://www.yelp.com/biz/the-rive-san-diego-4)
```

3. Click the sources drop down at the bottom of the page to read the sources: 
```
Retrieved context (6 chunks)
[1] The Rive · Yelp · similarity 0.65
https://www.yelp.com/biz/the-rive-san-diego-4

The Rive is honestly amazing, the apartments are in good condition with new furniture and appliances, the price is affordable and it's a 5 minute drive to campus, 20 min walk or you can take the free shuttle. The pool area is so pretty and I also love the fire places around the property. My favorite amenity is the communal area where you can study or place pool or even watch the huge tv!!

[2] General · Reddit · similarity 0.64
https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/

treet parking as well. also, the rive is close enough to a bunch of food places and vons that you can walk to it. their amenities are much nicer, the apartments updated better, and just overall seem to take care of their residents a LOT better than 5025. i have a few friends who live at the rive and i am so envious of them

[3] General · Reddit · similarity 0.64
https://www.reddit.com/r/SDSU/comments/1s3vvzl/i_got_accepted_housing/

The Rive (shuttle/parking under), but further away

[4] The Rive · Yelp · similarity 0.62
https://www.yelp.com/biz/the-rive-san-diego-4

I have loved living at the Rive! The amenities are great, it comes fully furnished which is ideal and they have good roommate matching. My room was very clean upon move in and I was very pleased with the new appliances in the apartment as well. The shuttle transport has also been reliable to getting to SDSU campus.

[5] General · Reddit · similarity 0.60
https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/

Edit: lived in the rive

[6] The Rive · Yelp · similarity 0.60
https://www.yelp.com/biz/the-rive-san-diego-4

i enjoy living at the rive because of all the amenities and how close it is to everything! The staff is very attentive and responsive for lots of things! This is the best student apartment living !
```

Or:
1. Use the text box to query any question regarding off-campus housing around the SDSU area. For example ```"Is it better to live at the Rive or 5025?"```
2. Click the ask button to submit your query.
3. See generated response:
```
According to the posts, one user on Reddit strongly dislikes 5025, stating "I HATE THIS PLACE WITH ALL OF MY BEING" and recommends living at the Rive instead (Source 1). Another user mentions that the Rive has nicer amenities, updated apartments, and takes better care of its residents compared to 5025 (Source 6). However, other users have positive experiences with 5025, with one user on Yelp stating it's a great place to live with friendly and helpful people (Source 4), and another user on Yelp mentioning it's affordable and has convenient amenities like a washing machine and dryer in the unit (Source 5). Additionally, a user on Reddit notes that a friend likes living at 5025 and that utilities are included in the rent (Source 3).

Sources:

Reddit (https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/)
Reddit (https://www.reddit.com/r/SDSU/comments/1lq9pjr/im_panicking/)
Yelp (https://www.yelp.com/biz/fifty-twenty-five-san-diego-4)
```
4. Click the sources drop down at the bottom of the page to read the sources.
```
Retrieved context (6 chunks)
[1] General · Reddit · similarity 0.74
https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/

LIVE AT THE RIVE. NOT 5025. I HATE THIS PLACE WITH ALL OF MY BEING

[2] General · Reddit · similarity 0.64
https://www.reddit.com/r/SDSU/comments/1lq9pjr/im_panicking/

5025 is like the Rive. They also have shuttle service. Apparently their rent includes utilities already, rive is a separate bill for it.

[3] General · Reddit · similarity 0.61
https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/

Ya! So a friend lives in 5025 and he likes it. I learned that when he was living there the utilities is included in the rent already, Rive is like 850 + whatever for the utilities, and 5025 was like 850 (including thr utilities alread)

[4] 5025 · Yelp · similarity 0.61
https://www.yelp.com/biz/fifty-twenty-five-san-diego-4

5025 is a great place to live at! Everyone is so friendly, nice, and helpful! You should definitely come here!

[5] 5025 · Yelp · similarity 0.60
https://www.yelp.com/biz/fifty-twenty-five-san-diego-4

5025 is a better alternative to living on campus if you have the opportunity. It is worth your money and is affordable compared to the other apartments in the area. I live in a double and the rooms are spacious. The kitchen is well equipped with many storage spaces. Not only is it affordable, but it comes with its own washing machine and dryer in the unit, which is extremely convenient.

[6] General · Reddit · similarity 0.58
https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/

treet parking as well. also, the rive is close enough to a bunch of food places and vons that you can walk to it. their amenities are much nicer, the apartments updated better, and just overall seem to take care of their residents a LOT better than 5025. i have a few friends who live at the rive and i am so envious of them
```

---


## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |Which apartment complexes are the most commonly mentioned?|The answer should identify frequently mentioned complexes such as The Rive, 5025, and Union Grantville.|The apartment complex "5025" (also known as Fifty-Twenty-Five) is the most commonly mentioned, with 3 reviews on Yelp (Source 4, Source 5, Source 6). Other sources do not mention specific apartment complex names.|Relevant|Partially Accurate|
| 2 |What do students/reviewers say about maintenance at 5025?|The answer should mention slow or unresponsive maintenance.|According to reviews on Yelp, maintenance at 5025 is a mixed experience. One reviewer (Source 2) states that "maintenance requests usually get taken care of very fast." However, another reviewer (Source 1) mentions that they don't have a "real maintenance team just college kids" and had issues with getting their stovetop fixed. Additionally, a third reviewer (Source 6) notes that maintenance requests often fall to a student worker at the front desk who lacks the training or authority to address issues, leading to delayed resolutions. |Relevant|Accurate|
| 3 |What rent range do students mention for off-campus housing near SDSU?|he answer should range between $1000-$3000|According to a post on Reddit (https://www.reddit.com/r/SDSU/comments/1r63ttx/off_campus_living/), students mention the following rent range for off-campus housing near SDSU: studios around $1800-1900+ per month, one beds for $2200-2500+, and 2bed 2bath for $3000+.|Relevant|Accurate|
| 4 |What amenities are mentioned for The Rive?|The answer should mention amenities such as gym, pool, and shuttle.|The Rive has several amenities, including a pool area, fire places, a communal area for studying, playing pool, or watching TV, and a free shuttle to SDSU campus. Additionally, the apartments are fully furnished and have new appliances (Source 1: The Rive \| Yelp, Source 4: The Rive \| Yelp).|Relevant|Accurate|
| 5 |What complaints do students/reviewers make about parking at Union Grantville?|The answer should mention cost/value concerns.|Students/reviewers at Union Grantville complain about the parking situation, stating that it is "horrendous" and not guaranteed (Source 1: Union Grantville \| Yelp \| https://www.yelp.com/biz/union-grantville-san-diego). They also mention that the complex sold parking spots to MTS, leaving residents with no option but street parking, which can be unsafe, especially for unaccompanied women (Source 5: Union Grantville \| Yelp \| https://www.yelp.com/biz/union-grantville-san-diego). Additionally, reviewers express frustration about being towed without clear warning or notification, with one reviewer stating that they had to pay $365 to retrieve their car (Source 6: Union Grantville \| Yelp \| https://www.yelp.com/biz/union-grantville-san-diego).|Relevant|Partially Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which apartment complexes are mentioned most often?

**What the system returned:**
The apartment complex "5025" (also known as Fifty-Twenty-Five) is mentioned most often, with 3 sources discussing it (Source 4, Source 5, Source 6, all from Yelp).

**Root cause (tied to a specific pipeline stage):**
The failure is that it mentions the document with the most reviews. While 5025 is a common apartment complex near SDSU it isn't the only one. The system fails to retrieve all of the apartment complexes.

**What you would change to fix it:**
I think there are two ways to go about fixing this. One is returning more chunks to the LLM so it has more information to go off or to cut some of the information in the 5025 Yelp reviews document as it is the largest one and probably returns the most information. I would need to work on making all documents similar size so that one document isn't favored more in the AI's generation.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
One of the big things that planning.md helped me with is visualizing how everything worked and went together. I think having an understanding of how your system works is key in a accurate and efficient implementation. Also, being able to write the specific specs beforehand made prompting the AI a much easier process that figuring out all of the information I need to give to it before it can start building. It also helped with error checking the system. Because of the test questions that were written I was able to quickly test if the system worked correctly or not especially the generation section.

**One way your implementation diverged from the spec, and why:**
One aspect of the spec I diverged from was the chunk size. I originally chose a chunk size of 800 characters however after testing the generation I realized that maybe too much info for the LLM at once to answer one specific question. I then reduced the chunk size to 500 characters because even while some Yelp reviews spanned more than 1000 characters not all of the information mentioned in that Yelp review would be relevant in answering the query.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**
- *What I gave the AI:* I used Claude Code to implement the interface and generation at the same time.
- *What it produced:* It produced a well written interface and the generation worked correctly.
- *What I changed or overrode:* However, event though everything worked correctly the source attribution wasn't exactly how I envisioned it to be. That may be partly due to the lack of mention of how the source attribution should be implemented so I then prompted it to be more specific in its source attribution and use the metadata given to give out specific links and the chunk text. I also prompted it to make a seperate section on the interface that would be dedicated to source attribution. There the user could specifically read a review that the generation based it's response on.

**Instance 2**
- *What I gave the AI:* I gave it the chunking section of planning.md to create the ingestion and chunking part of the pipeline.
- *What it produced:* It produced code the chunked the information.
- *What I changed or overrode:* Though it produced correct code that chunked the information to the chunk spec there was no metadata given. The source attribution would be less accurate without it. So I then prompted the AI with the sources list so it could correctly label the metadata of each chunk with the link of the source for better source attribution.

## Demo Video

[Watch the demo video](./demo.mkv)
