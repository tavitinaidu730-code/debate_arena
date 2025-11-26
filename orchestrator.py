from agents import Agent
from llm import LLMClient
from rag import simple_retrieve
import re

class Orchestrator:
    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()

    # ---------- NEW LOGIC: detect comparison topics ----------
    def detect_comparison(self, topic: str):
        topic = topic.lower()

        # Detect "A vs B"
        if " vs " in topic or " versus " in topic:
            parts = re.split(r" vs | versus ", topic)
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()

        # Detect "A and B"
        if " and " in topic:
            parts = topic.split(" and ")
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()

        # Detect "A or B"
        if " or " in topic:
            parts = topic.split(" or ")
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()

        # No comparison found
        return None, None

    def run_debate(self, topic: str, num_agents: int = 2, rounds: int = 2):

        # ---------- NEW: apply comparison logic ----------
        sideA, sideB = self.detect_comparison(topic)

        if sideA and sideB:
            # Use fixed roles for side-based debate
            agent_profiles = [
                {"name": sideA.title(), "focus": sideA, "persona_hint": f"advocate of {sideA}", "style": "support"},
                {"name": sideB.title(), "focus": sideB, "persona_hint": f"advocate of {sideB}", "style": "support"}
            ]
        else:
            # default Pro vs Con
            agent_profiles = [
                {"name": "Agent A", "focus": "positive", "persona_hint": "optimistic, supportive", "style": "pro"},
                {"name": "Agent B", "focus": "negative", "persona_hint": "critical, skeptical", "style": "con"},
                {"name": "Agent C", "focus": "positive", "persona_hint": "optimistic, supportive", "style": "pro"},
                {"name": "Agent D", "focus": "negative", "persona_hint": "critical, skeptical", "style": "con"}
            ]

        # Create agents based on count
        agents = []
        for i in range(num_agents):
            p = agent_profiles[i % len(agent_profiles)]
            agents.append(Agent(name=p['name'], persona=p['persona_hint'], style=p['style'], focus=p['focus'], llm=self.llm))

        transcript = {"topic": topic, "agents": [{"name": a.name, "turns": []} for a in agents]}

        # ------------- Opening Statements ----------------
        for idx, agent in enumerate(agents):
            prompt = f"""
            Opening statement on: {topic}
            Your assigned side: {agent.focus}
            Persona: {agent.persona}
            """
            text = agent.respond(prompt)
            transcript['agents'][idx]['turns'].append({"round": 1, "text": text})

        # ------------- Rebuttal Rounds -------------------
        for r in range(2, rounds):
            for idx, agent in enumerate(agents):
                context = self._collect_recent_claims(transcript, last_n=3)
                evidence = simple_retrieve(topic, agent.focus)

                prompt = f"""
                Round {r} rebuttal.
                Topic: {topic}
                You are representing: {agent.focus}
                Context from previous turns: {context}
                Evidence hints: {evidence}
                Persona: {agent.persona}
                Instruction: Counter the opposing side and strengthen your own side.
                """

                text = agent.respond(prompt)
                transcript['agents'][idx]['turns'].append({"round": r, "text": text})

        # ------------- Closing Statements -------------------
        for idx, agent in enumerate(agents):
            context = self._collect_recent_claims(transcript, last_n=5)
            prompt = f"""
            Closing statement.
            Topic: {topic}
            Your assigned side: {agent.focus}
            Context summary: {context}
            Persona: {agent.persona}
            Summarize why your side is stronger.
            """
            text = agent.respond(prompt)
            transcript['agents'][idx]['turns'].append({"round": rounds, "text": text})

        summary = self._moderator_summarize(transcript)
        return transcript, summary

    def _collect_recent_claims(self, transcript, last_n=3):
        parts = []
        for a in transcript['agents']:
            turns = a['turns'][-last_n:]
            for t in turns:
                parts.append(t['text'])
        return " ||| ".join(parts)

    def _moderator_summarize(self, transcript):
        closing_texts = [a['turns'][-1]['text'] for a in transcript['agents']]
        combined = " ".join(closing_texts)
        prompt = f"Summarize debate and provide 3 insights: {combined}"
        summary_text = self.llm.call(prompt)
        insights = [x.strip() for x in summary_text.split('.') if x.strip()][:3]
        return {"summary_text": summary_text, "insights": insights}
