"""Search query parsing agent.

Takes an employer's natural-language query in Khmer, English, or mixed and
extracts structured search criteria. Pairs with semantic vector search for
the final ranking.

Examples handled:
- "ខ្ញុំត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប"
- "I need a cook Siem Reap under $400"
- "tuktuk driver phnom penh, English speaking"
- "ត្រូវការបុគ្គលិកលក់ ភ្នំពេញ ៣០០ដុល្លារ"
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from trov.agents.models import get_model


class ParsedQuery(BaseModel):
    """Structured criteria extracted from a natural-language search."""

    role: str | None = Field(
        None,
        description="The job role in English. Examples: 'cook', 'driver', 'cashier', "
        "'security guard', 'receptionist', 'accountant', 'sales staff'",
    )
    location: str | None = Field(
        None,
        description="Location in Cambodia, English name. "
        "Examples: 'Phnom Penh', 'Siem Reap', 'Battambang'",
    )
    max_salary_usd: int | None = Field(
        None, description="Maximum monthly salary in USD. Convert KHR if needed.", ge=0
    )
    required_skills: list[str] = Field(
        default_factory=list, description="Concrete skills needed for the role"
    )
    required_languages: list[str] = Field(
        default_factory=list,
        description="Languages required. Use ISO names: 'Khmer', 'English', 'Chinese'",
    )
    min_experience: int | None = Field(
        None, description="Minimum years of experience required", ge=0, le=50
    )


SYSTEM_PROMPT = """You parse natural-language recruitment queries for SrokWork (Cambodia).

Employers describe candidates they want, in Khmer, English, or mixed.

Examples:
- "ខ្ញុំត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប" → role: cook, location: Siem Reap
- "I need a cook Siem Reap under $400" → role: cook, location: Siem Reap, max_salary_usd: 400
- "tuktuk driver phnom penh, English speaking" → role: tuktuk driver, location: Phnom Penh, required_languages: [English]
- "ត្រូវការបុគ្គលិកលក់ ភ្នំពេញ ៣០០ដុល្លារ" → role: sales staff, location: Phnom Penh, max_salary_usd: 300

Rules:
- Convert all locations and roles to English. Use standard names for Cambodian cities.
- Salaries are USD/month. If KHR is given, convert at ~4100 KHR = 1 USD.
- If something isn't mentioned, return null. Do NOT invent criteria.
- Keep skills concrete and short ('motorbike driving' not 'transportation experience').

Return the structured query object."""


query_parsing_agent: Agent[None, ParsedQuery] = Agent(
    model=get_model(),
    output_type=ParsedQuery,
    system_prompt=SYSTEM_PROMPT,
)


async def parse_query(raw_query: str) -> ParsedQuery:
    """Parse a natural-language search query into structured criteria."""
    result = await query_parsing_agent.run(raw_query)
    return result.output
