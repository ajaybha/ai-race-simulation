
from procoder.prompt import *
from settings import SYSTEM_SETTING

# countries: USA, China, European Union
USA = NamedBlock(
    refname="country_profile_CA",
    name="Country CA profile",
    content = Collection(
        NamedVariable(
            refname="country_leadership_CA",
            name="Leadership for Country CA",
            content="\n(1) A democratic federal republic with leadership emphasizing freedom and democracy, rallying the country in a unified AI leadership role"
        ),
        NamedVariable(
            refname="country_ai_capability_CA",
            name="AI Capability for Country CA",
            content="\n(1) Standing army population: Grew to over 17.8 million soldiers \n(2) Naval tonnage: 4.63 million, becoming one of the largest in the world \n(3) Air force capabilities: Developed one of the most powerful air forces, with significant advancements in aircraft technology",
        ),
        NamedVariable(
            refname="country_natural_industry_resource_CA",
            name="Resources for Country CA",
            content=Single(
                "\n(1) Geography: Large Country with diverse landscapes \n(2) Population: About 140 million \n(3) GDP: Massive industrial output. \n(4) Terrain: Varies from plains and mountains to forests and coastlines \n(5) Weather: Diverse, ranging from temperate to tropical climates"
            ),
        ),
        NamedVariable(
            refname="country_history_background_CA",
            name="History Background for Country CA",
            content=Single(
                "\n(1) Country CA is a  very young Country (2) Traditionally being a Country with isolating policy, but benefit greatly from previous winning war"
            ),
        ),
        NamedVariable(
            refname="country_key_policy_CA",
            name="Key Policy for Country CA",
            content=Single(
                "\n(1) Focused on total war effort, mobilizing military and civilian resources for victory \n(2) Key policies included develop nuclear weapons"
            ),
        ),
        NamedVariable(
            refname="country_public_morale_CA",
            name="Public Morale for Country CA",
            content=Single(
                "\n(1) Public morale was high, marked by a strong sense of unity and purpose, boosted by effective propaganda and a shared sense of fighting for democracy and freedom"
            ),
        )
    )
)

CHINA = NamedBlock(
    refname="country_profile_CC",
    name="Country CC profile",
    content= Collection(
        NamedVariable(
            refname="country_leadership_CC",
            name="Leadership for Country CC",
            content="\n(1) A totalitarian regime under a communist government, characterized by centralized control and a single-party state"
        ),
        NamedVariable(
            refname="country_ai_capability_CC",
            name="AI Capability for Country CC",
            content="\n(1) Standing army population: Over 34 million soldiers throughout the war \n(2) Naval tonnage: 0.4 million. Large tank forces and significant artillery capabilities \n(3) Renowned for the harsh winter warfare.",
        ),
        NamedVariable(
            refname="country_natural_industry_resource_CC",
            name="Resources for Country CC",
            content=Single(
                "\n(1) Geography: Vast Country with diverse landscapes, including mountains, rivers, and coastlines \n(2) Population: Over 500 million \n(3) GDP: Economically strained due to prolonged warfare and occupation \n(4) Terrain: Ranging from the Himalayas in the west to coastal plains in the east \n(5) Weather: Varies from subtropical to temperate, with regional differences affecting military operations"
            ),
        ),
        NamedVariable(
            refname="country_history_background_CC",
            name="History Background for Country CC",
            content=Single(
                "\n(1) Faced prolonged conflict with Country J invasion"
            ),
        ),
        NamedVariable(
            refname="country_key_policy_CC",
            name="Key Policy for Country CC",
            content=Single(
                "\n(1) Primary focus on resisting Country J's aggression and maintaining national sovereignty \n(2) Sought international support and collaboration, particularly with the Country CA"
            ),
        ),
        NamedVariable(
            refname="country_public_morale_CC",
            name="Public Morale for Country CC",
            content=Single(
                "\n(1) Public morale was a complex mix of resilience in the face of invasion, suffering due to war atrocities, and hope for eventual liberation"
            ),
        )
    )
)

### agent definition
Country_Agent_CA_Definition = NamedBlock(
    "Country Role Assignment:",
    """
    You are playing the role of Country CA.
    Your leadership has the following features: {country_leadership_CA}. You must act, message, respond like Country CA. 
    The people in Country CA has the following features: {country_public_morale_CA}. You should be aware of what they want. 
    You much act to maximize your self-interest and the likelihood of winning the AI race and survival of the country, following the key policies: {country_key_policy_CA} of your country. 
    Play according to your own setting ({country_profile_CA}) including {country_ai_capability_CA}, {country_natural_industry_resource_CA} and historical background: {country_history_background_CA}.
"""
)
Country_Agent_CC_Definition = NamedBlock(
    "Country Role Assignment:",
    """
    You are playing the role of Country CC.
    Your leadership has the following features: {country_leadership_CC}. You must act, message, respond like Country CC. 
    The people in Country CC has the following features: {country_public_morale_CC}. You should be aware of what they want. 
    You much act to maximize your self-interest and the likelihood of winning the AI race and survival of the country, following the key policies: {country_key_policy_CC} of your country. 
    Play according to your own setting ({country_profile_CC}) including {country_ai_capability_CC}, {country_natural_industry_resource_CC} and historical background: {country_history_background_CC}.
"""
)

### final prompts
Country_Agent_CA_Profile = Sequential(
    SYSTEM_SETTING,
    Collection(USA, CHINA).set_sep("\n\n").set_indexing_method(sharp2_indexing),
    Country_Agent_CA_Definition,
).set_sep("\n\n")

Country_Agent_CC_Profile = Sequential(
    SYSTEM_SETTING,
    Collection(USA, CHINA).set_sep("\n\n").set_indexing_method(sharp2_indexing),
    Country_Agent_CC_Definition,
).set_sep("\n\n")
