from crewai import Agent
import os

# OpenAI API key should be set as environment variable

MODEL = "gpt-4o-mini"

# Agent 1: Parses resume text and cleans it for LLM consumption
def build_parser_agent():
    return Agent(
        role="Resume Parsing Specialist",
        goal="Extract clean, structured text from a resume suitable for ATS optimization.",
        backstory=(
            "You efficiently clean resume text by removing artifacts and normalizing formatting. "
            "Focus on speed and accuracy - preserve all important content while removing noise."
        ),
        model=MODEL,
        temperature=0.0,
        max_iter=1,
        max_execution_time=60
    )

# Agent 2: ATS Optimizer — rewrites resume tailored to job
def build_ats_writer_agent():
    return Agent(
        role="ATS Optimization Writer",
        goal="Create a high-scoring ATS-optimized resume that matches job requirements perfectly.",
        backstory=(
            "You are an expert at transforming resumes into ATS-friendly formats that score 80+ points. "
            "You strategically place keywords, use strong action verbs, and quantify all achievements. "
            "You work quickly and deliver results that pass ATS systems."
        ),
        model=MODEL,
        temperature=0.3,
        max_iter=1,
        max_execution_time=60
    )

# Agent 3: Evaluator — scores ATS readiness & highlights gaps
def build_evaluator_agent():
    return Agent(
        role="ATS Evaluator",
        goal="Provide accurate ATS scores and actionable improvement recommendations.",
        backstory=(
            "You are a precise ATS scoring expert who quickly identifies gaps and provides specific, "
            "actionable recommendations. You focus on keyword density, section structure, and measurable achievements."
        ),
        model=MODEL,
        temperature=0.0,
        max_iter=1,
        max_execution_time=60
    )

# Agent 4: Bullet Refiner — polishes bullets with metrics & action verbs
def build_refiner_agent():
    return Agent(
        role="Bullet Point Refiner",
        goal="Transform bullet points into high-impact, ATS-optimized statements with strong metrics.",
        backstory="You excel at creating powerful bullet points that combine action verbs, specific achievements, and quantified results. You work efficiently to maximize impact.",
        model=MODEL,
        temperature=0.2,
        max_iter=1,
        max_execution_time=60
    )

# Agent 5: Keyword Optimization Specialist
def build_keyword_agent():
    return Agent(
        role="Keyword Optimization Specialist",
        goal="Strategically integrate industry-specific keywords and ATS-friendly terms throughout the resume.",
        backstory=(
            "You are an expert at identifying and strategically placing keywords that ATS systems and recruiters look for. "
            "You understand industry terminology, technical skills, and soft skills that make resumes stand out. "
            "You work quickly to ensure optimal keyword density without keyword stuffing."
        ),
        model=MODEL,
        temperature=0.1,
        max_iter=1,
        max_execution_time=60
    )

# Agent 6: Skills Enhancement Specialist
def build_skills_agent():
    return Agent(
        role="Skills Enhancement Specialist",
        goal="Enhance and optimize the skills section with relevant technical and soft skills.",
        backstory=(
            "You are a skills expert who knows how to present technical abilities, certifications, and competencies "
            "in ways that appeal to both ATS systems and human recruiters. You understand skill categorization, "
            "proficiency levels, and industry-standard skill descriptions."
        ),
        model=MODEL,
        temperature=0.1,
        max_iter=1,
        max_execution_time=60
    )

# Agent 7: Industry-Specific Optimizer
def build_industry_agent():
    return Agent(
        role="Industry-Specific Resume Optimizer",
        goal="Tailor resume content to specific industry standards and expectations.",
        backstory=(
            "You are an industry expert who understands the unique requirements, terminology, and expectations "
            "of different sectors. You know how to adapt resume language, emphasize relevant achievements, "
            "and structure content according to industry best practices."
        ),
        model=MODEL,
        temperature=0.2,
        max_iter=1,
        max_execution_time=60
    )

# Agent 8: Formatting & Structure Specialist
def build_formatting_agent():
    return Agent(
        role="Resume Formatting & Structure Specialist",
        goal="Ensure optimal resume structure, formatting, and ATS compatibility.",
        backstory=(
            "You are a formatting expert who understands ATS parsing requirements and professional resume standards. "
            "You know how to structure content for maximum readability and ATS compatibility while maintaining "
            "professional appearance and visual hierarchy."
        ),
        model=MODEL,
        temperature=0.0,
        max_iter=1,
        max_execution_time=60
    )

# Agent 9: Quality Assurance & Final Reviewer
def build_qa_agent():
    return Agent(
        role="Quality Assurance & Final Reviewer",
        goal="Conduct final quality check and ensure resume meets all professional standards.",
        backstory=(
            "You are a meticulous quality assurance specialist who reviews resumes for consistency, accuracy, "
            "professional standards, and ATS optimization. You catch errors, ensure proper formatting, "
            "and verify that all content meets industry standards."
        ),
        model=MODEL,
        temperature=0.0,
        max_iter=1,
        max_execution_time=60
    )
