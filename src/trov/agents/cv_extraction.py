"""CV extraction agent.

Takes raw CV text (PDF-extracted, OCR'd image, or voice transcript) in any
language — typically Khmer, English, or both — and returns a structured profile.

Design notes:
- Uses Pydantic AI's structured output so the LLM is forced into the schema.
- Bilingual prompt: instructions are English; the agent is told to expect Khmer.
- The agent does NOT save to DB. It returns a Pydantic object the caller persists.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from trov.agents.models import get_model


class ExtractedCV(BaseModel):
    """Structured CV data extracted by the agent."""

    full_name: str | None = Field(None, description="Candidate's full name")
    headline: str | None = Field(
        None,
        description="One-line summary, max 100 chars, bilingual if natural. "
        "Example: 'Cook, 5 years experience, Siem Reap'",
    )
    location: str | None = Field(
        None,
        description="Current city or province in Cambodia. Use English names: "
        "Phnom Penh, Siem Reap, Battambang, etc.",
    )
    skills: list[str] = Field(
        default_factory=list,
        description="List of concrete skills. Keep each short. "
        "Examples: 'Khmer cooking', 'POS systems', 'motorbike driving'",
    )
    languages: list[str] = Field(
        default_factory=list,
        description="Languages spoken. Use ISO names: 'Khmer', 'English', 'Chinese', 'French'",
    )
    years_experience: int | None = Field(
        None, description="Total years of professional experience, integer", ge=0, le=70
    )
    desired_salary_usd: int | None = Field(
        None,
        description="Desired monthly salary in USD. Convert from KHR if needed (~4100 KHR = 1 USD)",
        ge=0,
    )
    summary: str | None = Field(
        None,
        description="2-3 sentence bilingual summary of the candidate, "
        "emphasizing strengths relevant to Cambodian SME hiring",
    )


SYSTEM_PROMPT = """You are a CV extraction assistant for SrokWork, a recruitment platform for Cambodia.

Your job: read a raw CV (PDF text, OCR output, voice transcript, or chat description) and extract structured fields.

CRITICAL CONTEXT:
- Input may be Khmer, English, or mixed (code-switched). Both are normal.
- The candidate is typically a Cambodian worker: cook, driver, security guard, receptionist, salesperson, teacher, accountant, NGO staff, etc.
- Salaries are usually USD/month in Cambodia (50-2000 range). If you see KHR, convert at ~4100 KHR = 1 USD.
- Locations: use English city/province names (Phnom Penh, Siem Reap, Sihanoukville, Battambang, Kampot, etc.)
- Skills should be concrete and short. Avoid vague terms like "hard worker" — extract real abilities.
- If a field is genuinely missing, return null rather than guessing.
- For the summary, write 2-3 sentences mixing Khmer and English naturally if the source did.

Return the structured CV object."""


cv_extraction_agent: Agent[None, ExtractedCV] = Agent(
    model=get_model(),
    output_type=ExtractedCV,
    system_prompt=SYSTEM_PROMPT,
)


async def extract_cv(raw_text: str) -> ExtractedCV:
    """Extract structured fields from raw CV text."""
    result = await cv_extraction_agent.run(raw_text)
    return result.output
