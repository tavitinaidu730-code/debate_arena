# Simple RAG stub — returns simulated 'evidence' snippets for the topic.
# Replace with a real retriever (FAISS/Weaviate) for production.
def simple_retrieve(topic: str, focus: str = ""):
    hints = {
        "benefits": ["Study A shows productivity increases.", "Case study: City X reduced costs."],
        "risks": ["Report B notes privacy concerns.", "Study C highlights inequality effects."],
        "data": ["Dataset D indicates mixed outcomes.", "Survey E reports public opinion split."],
        "edge-cases": ["Edge-case: small communities may be left out.", "Rare failure mode observed in pilot projects."]
    }
    key = focus if focus in hints else "data"
    return hints.get(key, hints["data"])    
