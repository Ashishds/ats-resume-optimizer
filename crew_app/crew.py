import os
from crewai import Crew, Process
from .agents import (
    build_parser_agent, build_ats_writer_agent,
    build_evaluator_agent, build_refiner_agent,
    build_keyword_agent, build_skills_agent,
    build_industry_agent, build_formatting_agent,
    build_qa_agent
)
from .tasks import (
    parse_resume_task, rewrite_for_ats_task,
    evaluate_ats_task, refine_bullets_task,
    optimize_keywords_task, enhance_skills_task,
    industry_optimize_task, format_structure_task,
    quality_assurance_task
)

def build_crew(raw_resume_text: str, job_title: str, job_description: str):
    parser = build_parser_agent()
    writer = build_ats_writer_agent()
    refiner = build_refiner_agent()
    evaluator = build_evaluator_agent()

    t_parse = parse_resume_task(parser, raw_resume_text)
    # these are placeholders; we'll stitch later after parse result is known
    t_rewrite = rewrite_for_ats_task(writer, "{CLEANED_RESUME}", job_title, job_description)
    t_refine = refine_bullets_task(refiner, "{REWRITTEN_RESUME}")
    t_eval = evaluate_ats_task(evaluator, "{FINAL_RESUME}", job_title, job_description)

    crew = Crew(
        agents=[parser, writer, refiner, evaluator],
        tasks=[t_parse, t_rewrite, t_refine, t_eval],
        process=Process.sequential,
        verbose=True
    )
    return crew

def run_pipeline(raw_resume_text: str, job_title: str, job_description: str):
    # Build all agents
    parser = build_parser_agent()
    writer = build_ats_writer_agent()
    refiner = build_refiner_agent()
    keyword_agent = build_keyword_agent()
    skills_agent = build_skills_agent()
    industry_agent = build_industry_agent()
    formatting_agent = build_formatting_agent()
    qa_agent = build_qa_agent()
    evaluator = build_evaluator_agent()

    # Stage 1: Parse and clean
    print("🔍 Stage 1: Parsing and cleaning resume...")
    t_parse = parse_resume_task(parser, raw_resume_text)
    parse_crew = Crew(agents=[parser], tasks=[t_parse], process=Process.sequential, verbose=True)
    parse_result = parse_crew.kickoff()
    cleaned = str(parse_result).strip()

    # Stage 2: ATS optimization
    print("📝 Stage 2: ATS optimization...")
    t_rewrite = rewrite_for_ats_task(writer, cleaned, job_title, job_description)
    rewrite_crew = Crew(agents=[writer], tasks=[t_rewrite], process=Process.sequential, verbose=True)
    rewrite_result = rewrite_crew.kickoff()
    rewritten = str(rewrite_result).strip()

    # Stage 3: Keyword optimization
    print("🔑 Stage 3: Keyword optimization...")
    t_keywords = optimize_keywords_task(keyword_agent, rewritten, job_title, job_description)
    keyword_crew = Crew(agents=[keyword_agent], tasks=[t_keywords], process=Process.sequential, verbose=True)
    keyword_result = keyword_crew.kickoff()
    keyword_optimized = str(keyword_result).strip()

    # Stage 4: Skills enhancement
    print("🛠️ Stage 4: Skills enhancement...")
    t_skills = enhance_skills_task(skills_agent, keyword_optimized, job_title, job_description)
    skills_crew = Crew(agents=[skills_agent], tasks=[t_skills], process=Process.sequential, verbose=True)
    skills_result = skills_crew.kickoff()
    skills_enhanced = str(skills_result).strip()

    # Stage 5: Industry-specific optimization
    print("🏭 Stage 5: Industry-specific optimization...")
    t_industry = industry_optimize_task(industry_agent, skills_enhanced, job_title, job_description)
    industry_crew = Crew(agents=[industry_agent], tasks=[t_industry], process=Process.sequential, verbose=True)
    industry_result = industry_crew.kickoff()
    industry_optimized = str(industry_result).strip()

    # Stage 6: Bullet refinement
    print("✨ Stage 6: Bullet point refinement...")
    t_refine = refine_bullets_task(refiner, industry_optimized)
    refine_crew = Crew(agents=[refiner], tasks=[t_refine], process=Process.sequential, verbose=True)
    refine_result = refine_crew.kickoff()
    refined = str(refine_result).strip()

    # Stage 7: Formatting and structure
    print("📋 Stage 7: Formatting and structure optimization...")
    t_format = format_structure_task(formatting_agent, refined, job_title, job_description)
    format_crew = Crew(agents=[formatting_agent], tasks=[t_format], process=Process.sequential, verbose=True)
    format_result = format_crew.kickoff()
    formatted = str(format_result).strip()

    # Stage 8: Quality assurance
    print("✅ Stage 8: Quality assurance and final review...")
    t_qa = quality_assurance_task(qa_agent, formatted, job_title, job_description)
    qa_crew = Crew(agents=[qa_agent], tasks=[t_qa], process=Process.sequential, verbose=True)
    qa_result = qa_crew.kickoff()
    final_resume = str(qa_result).strip()

    # Stage 9: Final evaluation
    print("📊 Stage 9: Final ATS evaluation...")
    t_eval = evaluate_ats_task(evaluator, final_resume, job_title, job_description)
    eval_crew = Crew(agents=[evaluator], tasks=[t_eval], process=Process.sequential, verbose=True)
    eval_result = eval_crew.kickoff()
    evaluation = str(eval_result).strip()

    print("🎉 Resume optimization complete!")
    return cleaned, rewritten, final_resume, evaluation
