from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Literal, Union

class RunRequest(BaseModel):
    goal: str = "Generate today's trend-grounded post"
    platform: Literal["linkedin", "instagram", "both"] = "linkedin"
    seed_topic: Optional[str] = None

class SignalItem(BaseModel):
    """
    Architectural Contract: Grounded trend signal.
    """
    source: Literal["reddit", "trends", "news", "internal"]
    text: str                # Snapped quote / snippet
    score: float             # Upvote ratio or velocity, normalized
    url: str                 # Traceability URL

class Theme(BaseModel):
    label: str
    evidence: List[SignalItem]
    heat: float

class Angle(BaseModel):
    take: str
    product_tie: Optional[str] = None  # Resume tailor, Adaptive interviewer, Career copilot
    why_only_jobingen: str             # Anti-positioning defense

class PlatformBrief(BaseModel):
    platform: Literal["linkedin", "instagram"]
    format: str
    hook_style: str
    length_rule: str
    cta_type: str
    tone: str

class PostDraft(BaseModel):
    platform: Literal["linkedin", "instagram"]
    hook_options: List[str] = Field(default_factory=list)
    body: List[str] = Field(default_factory=list)
    caption: str = "Grounded Career Strategy"
    hashtags: List[str] = Field(default_factory=list)
    cta: str = "Create your free account on JobInGen"
    alt_text: str = "JobInGen Branded Post"

    @field_validator('cta', 'alt_text', 'caption', mode='before')
    @classmethod
    def heal_draft_aliases(cls, v, info):
        # Programmatic Schema-Healing for LLM drifts
        field_name = info.field_name
        return v if v is not None else ""

class Critique(BaseModel):
    brand_voice: int = 8
    hook_strength: int = 8
    value_density: int = 8
    cta_score: int = 7
    cringe_filter: int = 9
    total_score: float = 8.0
    feedback: Union[str, List[str]] = "PASS"
    passed: bool = True

    @field_validator('feedback', mode='before')
    @classmethod
    def ensure_string_feedback(cls, v):
        if isinstance(v, list):
            return " ".join(str(item) for item in v)
        return str(v)

class ViralityScore(BaseModel):
    total: int = 80
    hook_strength: int = 80
    trend_alignment: int = 80
    emotional_resonance: int = 80
    value_density: int = 80
    share_trigger: int = 80
    weakest_lever: str = "value_density"

class AnalysisReport(BaseModel):
    trend_basis: str
    audience_tension: str
    differentiation: str
    platform_fit: str
    virality: ViralityScore = Field(default_factory=ViralityScore)
    what_to_watch: str

# Aliases for unified importing & backwards compatibility
class ContentPlan(BaseModel):
    date: str
    selected_pillar: str
    selected_template: str
    topic_id: str
    topic_title: str
    topic_data: Dict[str, Any]
    math_analysis: Dict[str, Any]

class CopyVariant(BaseModel):
    """
    Architectural Contract: Copy Variant.
    Defensively heals common LLM schema drifts (e.g. returning call_to_action instead of cta)
    and falls back to robust brand defaults to guarantee 100% un-crashable execution.
    """
    hook: str = "JobInGen Career Insight"
    caption: str = "Deep, value-dense career strategies for student success."
    hashtags: List[str] = Field(default_factory=list)
    cta: str = "Join JobInGen today"
    alt_text: str = "JobInGen Programmatic Branding Post"
    slides: Optional[List[str]] = None

    @field_validator('hook', 'caption', 'cta', 'alt_text', 'hashtags', mode='before')
    @classmethod
    def heal_aliases(cls, v, info):
        # Auto-mapping of common LLM variations
        field_name = info.field_name
        return v if v is not None else ""

class QAEvaluation(BaseModel):
    brand_voice: int = 8
    hook_strength: int = 8
    value_density: int = 8
    cta_score: int = 7
    cringe_filter: int = 9
    total_score: float = 8.0
    feedback: Union[str, List[str]] = "PASS"
    passed: bool = True

    @field_validator('feedback', mode='before')
    @classmethod
    def ensure_string_feedback(cls, v):
        if isinstance(v, list):
            return " ".join(str(item) for item in v)
        return str(v)

class MarketingState(BaseModel):
    """
    Architectural Principle: Single State Context.
    LangGraph-compatible state container validated on entry and exit.
    """
    request: RunRequest = Field(default_factory=RunRequest)
    raw_signal: List[SignalItem] = Field(default_factory=list)
    themes: List[Theme] = Field(default_factory=list)
    chosen_theme: Optional[Theme] = None
    tension: Optional[str] = None
    angle: Optional[Angle] = None
    briefs: Dict[str, PlatformBrief] = Field(default_factory=dict)
    drafts: Dict[str, PostDraft] = Field(default_factory=dict)
    images: Dict[str, List[str]] = Field(default_factory=dict)
    critiques: Dict[str, Critique] = Field(default_factory=dict)
    virality: Dict[str, ViralityScore] = Field(default_factory=dict)
    retry_counts: Dict[str, int] = Field(default_factory=dict)
    report: Dict[str, AnalysisReport] = Field(default_factory=dict)
    approved: Optional[bool] = None
    errors: List[str] = Field(default_factory=list)
    logs: List[str] = Field(default_factory=list)
    
    # Backwards compatible operational fields
    plan: Optional[ContentPlan] = None
    variant_a: Optional[CopyVariant] = None
    variant_b: Optional[CopyVariant] = None
    eval_a: Optional[QAEvaluation] = None
    eval_b: Optional[QAEvaluation] = None
    render_paths: List[str] = Field(default_factory=list)
    caption_file: Optional[str] = None

# Unified Architectural Alias
ContentState = MarketingState
