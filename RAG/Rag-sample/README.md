RAG :
Ingestion pipeline -> document -> Load -> split -> embedding -> storevdb
Query pipeline -> question -> embedding -> query vdb(retriver) -> prompt builder (context + query) llm  -> output

Problem statment:
I have a math book where i have to load the pdf file of first chapter using python libaries and get the data w.r.t questions or images.

First Ingestion Pipeline :
1. load the document -> check the type of document and use respective libaries to laod the file.
2. split -> here we get the chunking. before chunkong understand the file/document what we used to laod and search patterns how effectient we can chunk the data.
3. Embedding -> convert the text data into vector. Use the model that suits your llm to embbed the data formed in chuncks. here i'm using ollama(nomic-embed-text)
4. Vector DB -> Then load the data into database that suits the reqirement . here i'm using chromadb

Query Pipeline:
1. Question: user ask question through input
2. Question Embeddings :  A vectordb can't under the question/english directly , it understand only vectors. so before searching convert to vector.
3. Query search : vector question search for vector answer using cosine similarity based on the similarity 
4. Prompt builder: based on the prompt we have something called system,human,context. It combines all 3 parts before sending to LLM
5. LLM: Here it convert vextor to nlp using model. Use the prefred model to get the data (here i'm using llama3)
6. Output: You will recieve the output  for the requested based on knowledge feeded. 




LLMs have a context window.

Llama3 = 8K tokens
After loading document may conatin 120,000 tokens It simply won't fit.so we need chunking here. 

chunk: Chunking solves this.
If we laod a doc with 100 pages -> 500,000 characters
If we don't chunk then your vector database will contain one embedding.
Everything is mixed together. Retrieval quality becomes very poor.

chunk_overlap:
Chunk overlap is the number of characters (or tokens, depending on the splitter) that are copied from the end of one chunk to the beginning of the next chunk.

if we don't use overlap The semantic meaning is broken.

Step Size = Chunk Size − Chunk Overlap
Next Chunk Start = Previous Chunk Start + Step Size
example:
Chunk Size = 500
Overlap = 50

500 − 50 = 450

Chunk 1
0 → 499

Chunk 2
450 → 949

Chunk 3
900 → 1399

overlap is 
450–499 appears in both Chunk 1 and Chunk 2.

In General a production grade chunking uses between 10-20% (i.e: 10,15,20)

If overlaps larger than 10-20% below problems my occur
Storage doubles because of duplicated content.
Embedding generation takes longer.
Vector database size increases.
Retriever may return multiple nearly identical chunks, reducing answer diversity.


Embedding: This converts the splittext data (NLP) to vector where llm can understand the data.



Prompt Builder:
It combines the retrieved context, the system prompt (instructions that define the AI's behavior), and the human prompt (the user's question) into a single prompt that is sent to the LLM. It ensures the model answers using the retrieved context while following the system instructions instead of relying solely on its pretrained knowledge.

Example:
System:
You are a helpful AI assistant. Answer only from the provided context.
If the answer is not present, say "I don't know."

Context:
About addition summing of multiple values.

Human:
What is addition?

 
Large Language Model (LLM) :
The Vector Database retrieves information, but it does not understand or generate natural language. The LLM reads the retrieved context, understands the user's question, reasons over the information, and generates a coherent, human-readable answer.
Understands context, reasons, and generates the final answser




Structutred aware chunking
Heading - split()
        section->    sub-split()
            paragraph-> sub-split()
                sentence -> sub-split()
                    token -> sub-suplit()


Add metadata for each chunk


parent-child + sliding window approch

smaller chuks good for embedding

every small (child) chunk is assosciated with parent chunk

sematic chunking + propostions approch

This is high scematic match but more costlier


How do you know chunk is good ..??
A/B testing - 2/5 2 out of 5 cunks matching
MRR (mean reciprocal rag )
Answer Faithufullness - chunks retrived 5 llm answer from this .but not from hallucination
Answer Relevance- how relavent is your answer (llm address user question)
content precison - what fraction of 
