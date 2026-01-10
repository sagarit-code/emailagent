from langchain_groq import ChatGroq

from langgraph.graph import StateGraph,END,START
from typing import TypedDict,List
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()  
model = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


class AgentState(TypedDict):
    from_mail: str
    to_mail: str
    subject: str
    prompt: str
    message: str
    final_message: str
    status: str
    




def write_email(state: AgentState) -> dict:
    prompt = f"""
You are a world-class professional email writer with 15+ years of experience.

Write a professional email about:
{state["prompt"]}

Rules:
- Include a clear SUBJECT LINE at the top
- Then the email body
- No markdown
- No explanations

Format EXACTLY like this:

Subject: <subject here>

<email body>
"""

    result = model.invoke(prompt)
    text = result.content.strip()

    subject, body = text.split("\n", 1)
    subject = subject.replace("Subject:", "").strip()

    return {
        "subject": subject,
        "message": body.strip()
    }

def checks_email(state:AgentState) -> dict:
    llm_first_message=state["message"]
    promptt=f"""You are an Email Quality Assurance Agent.

    here is the email drafts {llm_first_message}

Your job is NOT to rewrite the email immediately.
Your job is to evaluate the draft like a strict but smart reviewer.

Analyze the email across these dimensions:

1. CLARITY
- Is the purpose obvious within the first 2–3 lines?
- Is anything vague, confusing, or unnecessary?

2. TONE & INTENT
- Is the tone appropriate for the recipient (professional, polite, confident)?
- Does it sound respectful without being submissive or awkward?

3. STRUCTURE
- Is there a clear opening, body, and closing?
- Are paragraphs too long or messy?

4. IMPACT
- Does the email clearly state what action is expected from the recipient?
- Would a busy person understand and respond quickly?

5. RISK FLAGS
- Any grammar or spelling issues?
- Any lines that sound unprofessional, desperate, or careless?
- Any ambiguity that could be misinterpreted?

---

### OUTPUT FORMAT (STRICT)

Return a structured review in the following format:

Email Verdict: PASS / NEEDS IMPROVEMENT / FAIL

Strengths:
- Bullet list (short, honest)

Issues:
- Bullet list (be direct, no sugarcoating)

Suggested Improvements:
- Bullet list of actionable suggestions (not a full rewrite)

Rewrite Needed?: YES / NO

If Rewrite Needed = YES:
Briefly explain *why* a rewrite is necessary.

---

### IMPORTANT RULES
- Do NOT rewrite the email unless explicitly asked.
- Be concise but sharp.
- Think like the recipient, not the sender.
- Prioritize effectiveness over politeness.

"""
    response=model.invoke(promptt)
    textt = response.content.strip()


    subjectt, bodyy = textt.split("\n", 1)
    subjectt = subjectt.replace("Subject:", "").strip()

    return {
        "subject": subjectt,
        "final_message": bodyy.strip()
    }

def send_email(state: AgentState) -> dict:
    msg = MIMEMultipart()
    msg["From"] = state["from_mail"]
    msg["To"] = state["to_mail"]
    msg["Subject"] = state["subject"]

    msg.attach(MIMEText(state["final_message"], "plain"))

    try:
        server = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.send_message(msg)
        server.quit()

        return {"status": "sent"}

    except Exception as e:
        return {"status": f"failed: {str(e)}"}

graph = StateGraph(AgentState)

graph.add_node("write_email", write_email)
graph.add_node("checking_email", checks_email)
graph.add_node("send_email", send_email)

graph.add_edge(START, "write_email")
graph.add_edge("write_email", "checking_email")
graph.add_edge("checking_email","send_email")
graph.add_edge("send_email", END)

app = graph.compile()

initial_state = {
    "from_mail": "founder.evidora@gmail.com",
    "to_mail": "digiance.sagarit@gmail.com",
    "prompt": "my name is sagarit and recievers name is abc write that Reschedule today's 2pm meeting to 5pm due to urgent code bugs",
}

result = app.invoke(initial_state)

print("STATUS:", result["status"])
