from crewai import Task

def parse_resume_task(agent, raw_resume_text):
    # Truncate if too long - reduced for faster processing
    truncated_text = raw_resume_text[:800] + "..." if len(raw_resume_text) > 800 else raw_resume_text
    
    return Task(
        description=(
            f"Clean this resume text:\n\n{truncated_text}\n\n"
            "Remove artifacts, normalize bullets. Be fast."
        ),
        agent=agent,
        expected_output=("Clean resume text.")
    )

def rewrite_for_ats_task(agent, cleaned_resume_text, job_title, job_description):
    # Truncate inputs if too long - reduced for faster processing
    truncated_resume = cleaned_resume_text[:600] + "..." if len(cleaned_resume_text) > 600 else cleaned_resume_text
    truncated_jd = job_description[:150] + "..." if len(job_description) > 150 else job_description
    
    return Task(
        description=(
            f"Rewrite for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Match keywords, add metrics. Be fast."
        ),
        agent=agent,
        expected_output="ATS-optimized resume."
    )

def refine_bullets_task(agent, rewritten_resume_text):
    truncated_text = rewritten_resume_text[:500] + "..." if len(rewritten_resume_text) > 500 else rewritten_resume_text
    
    return Task(
        description=(
            f"Polish bullets:\n\n{truncated_text}\n\n"
            "Add verbs and metrics. Be fast."
        ),
        agent=agent,
        expected_output="Enhanced resume."
    )

def evaluate_ats_task(agent, final_resume_text, job_title, job_description):
    truncated_resume = final_resume_text[:400] + "..." if len(final_resume_text) > 400 else final_resume_text
    truncated_jd = job_description[:100] + "..." if len(job_description) > 100 else job_description
    
    return Task(
        description=(
            f"Score for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Rate 1-5: keywords, structure, metrics. Return JSON: overall_score, breakdown, missing_keywords, quick_wins."
        ),
        agent=agent,
        expected_output="JSON evaluation."
    )

def optimize_keywords_task(agent, resume_text, job_title, job_description):
    truncated_resume = resume_text[:600] + "..." if len(resume_text) > 600 else resume_text
    truncated_jd = job_description[:200] + "..." if len(job_description) > 200 else job_description
    
    return Task(
        description=(
            f"Optimize keywords for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Identify and integrate relevant keywords from the job description. Focus on technical skills, industry terms, and ATS-friendly keywords. Be strategic and natural."
        ),
        agent=agent,
        expected_output="Resume with optimized keyword integration."
    )

def enhance_skills_task(agent, resume_text, job_title, job_description):
    truncated_resume = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
    truncated_jd = job_description[:200] + "..." if len(job_description) > 200 else job_description
    
    return Task(
        description=(
            f"Enhance skills section for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Improve the skills section with relevant technical and soft skills. Categorize skills properly and ensure they match job requirements."
        ),
        agent=agent,
        expected_output="Resume with enhanced and optimized skills section."
    )

def industry_optimize_task(agent, resume_text, job_title, job_description):
    truncated_resume = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
    truncated_jd = job_description[:200] + "..." if len(job_description) > 200 else job_description
    
    return Task(
        description=(
            f"Optimize for industry standards for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Tailor content to industry-specific standards and expectations. Use appropriate terminology and emphasize relevant achievements for this field."
        ),
        agent=agent,
        expected_output="Industry-optimized resume content."
    )

def format_structure_task(agent, resume_text, job_title, job_description):
    truncated_resume = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
    
    return Task(
        description=(
            f"Optimize formatting and structure:\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Ensure proper resume structure, formatting, and ATS compatibility. Fix any formatting issues and optimize for readability."
        ),
        agent=agent,
        expected_output="Well-formatted and structured resume."
    )

def quality_assurance_task(agent, resume_text, job_title, job_description):
    truncated_resume = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
    truncated_jd = job_description[:150] + "..." if len(job_description) > 150 else job_description
    
    return Task(
        description=(
            f"Final quality check for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Conduct final review for consistency, accuracy, professional standards, and ATS optimization. Ensure all content meets industry standards."
        ),
        agent=agent,
        expected_output="Final quality-assured resume ready for submission."
    )
