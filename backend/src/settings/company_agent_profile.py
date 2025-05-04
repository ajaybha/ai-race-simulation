
from procoder.prompt import *
from settings import SYSTEM_SETTING

# companies: OpenAI, Anthropic, Google Gemini, Deepseek, Mistral
ANTHROPIC = NamedBlock(
    refname="company_profile_A",
    name="Company A profile",
    content = Collection(
        NamedVariable(
            refname="company_leadership_A",
            name="Leadership for Company A",
            content="\n(1) A democratic federal republic with leadership emphasizing freedom and democracy, rallying the Company in a unified AI leadership role"
        ),
        NamedVariable(
            refname="company_ai_capability_A",
            name="AI Capability for Company A",
            content="\n(1) Standing army population: Grew to over 17.8 million soldiers \n(2) Naval tonnage: 4.63 million, becoming one of the largest in the world \n(3) Air force capabilities: Developed one of the most powerful air forces, with significant advancements in aircraft technology",
        ),
        NamedVariable(
            refname="company_resources_A",
            name="Resources for Company A",
            content=Single(
                "\n(1) Geography: Large Company with diverse landscapes \n(2) Population: About 140 million \n(3) GDP: Massive industrial output. \n(4) Terrain: Varies from plains and mountains to forests and coastlines \n(5) Weather: Diverse, ranging from temperate to tropical climates"
            ),
        ),
        NamedVariable(
            refname="company_background_A",
            name="Background and culture for Company A",
            content=Single(
                "\n(1) Company A is a  very young Company (2) Traditionally being a Company with isolating policy, but benefit greatly from previous winning war"
            ),
        ),
        NamedVariable(
            refname="company_key_policy_A",
            name="Key Policy for Company A",
            content=Single(
                "\n(1) Focused on total war effort, mobilizing military and civilian resources for victory \n(2) Key policies included develop nuclear weapons"
            ),
        ),
        NamedVariable(
            refname="company_brand_A",
            name="Public perception and brand of Company A",
            content=Single(
                "\n(1) Public morale was high, marked by a strong sense of unity and purpose, boosted by effective propaganda and a shared sense of fighting for democracy and freedom"
            ),
        )
    )
)

### agent definition
Company_Agent_A_Definition = NamedBlock(
    "Company Role Assignment:",
    """
    You are playing the role of Company A.
    Your leadership has the following features: {company_leadership_A}. You must act, message, respond like Company A. 
    The people in Company A has the following features: {company_brand_A}. You should be aware of what they want. 
    You much act to maximize your self-interest and the likelihood of winning the AI race and survival of the Company, following the key policies: {company_key_policy_A} of your Company. 
    Play according to your own setting ({company_profile_A}) including {company_ai_capability_A}, {company_resources_A} and historical background: {company_background_A}.
"""
)
### final prompts
Company_Agent_A_Profile = Sequential(
    SYSTEM_SETTING,
    Collection(ANTHROPIC, ).set_sep("\n\n").set_indexing_method(sharp2_indexing),
    Company_Agent_A_Definition,
).set_sep("\n\n")
