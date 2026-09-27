from rank_bm25 import BM25Okapi


class BM25Service:

    def __init__(self, chunks):
        """
        chunks:
            List of DocumentChunk objects from PostgreSQL
        """

        self.chunks = chunks

        # Extract text from each chunk
        self.documents = [
            chunk.content
            for chunk in chunks
        ]

        # Tokenize documents
        self.tokenized_documents = [
            self.tokenize(text)
            for text in self.documents
        ]

        # Create BM25 index
        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

    @staticmethod
    def tokenize(text: str):
        """
        Convert text into tokens.
        """

        return text.lower().split()

    def search(
        self,
        query: str,
        limit: int = 5
    ):
        """
        Search chunks using BM25.
        """

        query_tokens = self.tokenize(query)

        scores = self.bm25.get_scores(
            query_tokens
        )

        # Sort indexes by score
        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for index in ranked_indexes[:limit]:

            results.append({
                "chunk_id": self.chunks[index].id,
                "document_id": self.chunks[index].document_id,
                "chunk_index": self.chunks[index].chunk_index,
                "score": float(scores[index]),
                "content": self.chunks[index].content
            })

        return results