import random

class Agent:
    def __init__(self, name: str, persona: str = "", style: str = "neutral", focus: str = "", llm=None):
        self.name = name
        self.persona = persona
        self.style = style
        self.focus = focus
        self.llm = llm

    def respond(self, prompt: str) -> str:
        # If an LLM client is provided, use it; otherwise use local fallback generator
        instruction = f"[Agent: {self.name} | Persona: {self.persona} | Focus: {self.focus}]\n{prompt}"
        if self.llm:
            return self.llm.call(instruction)
        else:
            return self._local_fallback(instruction)

    def _local_fallback(self, instruction: str) -> str:
        # deterministic but varied local responses for offline testing
        templates = [
            "I argue that {topic}. My key point is that {point}.",
            "From my perspective, {topic} raises concerns about {point}. We should consider {consideration}.",
            "Consider this: {topic} may lead to {point}. Evidence suggests {suggestion}.",
            "While there are benefits, we must not ignore {point} and the following risk: {consideration}."
        ]
        # extract topic crudely
        topic = "the topic"
        if "Topic:" in instruction:
            try:
                topic = instruction.split("Topic:")[1].split("\n")[0].strip()
            except Exception:
                topic = "the topic"
        point = random.choice(["economic impact", "ethical concerns", "scalability issues", "educational outcomes"])
        consideration = random.choice(["long-term effects", "edge cases", "costs", "social acceptance"])
        suggestion = random.choice(["further study", "pilot programs", "controlled trials", "stakeholder consultation"])
        t = random.choice(templates)
        return t.format(topic=topic, point=point, consideration=consideration, suggestion=suggestion)
