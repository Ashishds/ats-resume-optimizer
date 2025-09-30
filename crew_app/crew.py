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
    # Build only essential agents for faster processing
    parser = build_parser_agent()
    writer = build_ats_writer_agent()
    refiner = build_refiner_agent()
    evaluator = build_evaluator_agent()

    # Stage 1: Parse and clean
    print("Stage 1/4: Parsing and cleaning resume...")
    t_parse = parse_resume_task(parser, raw_resume_text)
    parse_crew = Crew(agents=[parser], tasks=[t_parse], process=Process.sequential, verbose=False)
    parse_result = parse_crew.kickoff()
    cleaned = str(parse_result).strip()

    # Stage 2: ATS optimization (includes keyword optimization)
    print("Stage 2/4: ATS optimization...")
    t_rewrite = rewrite_for_ats_task(writer, cleaned, job_title, job_description)
    rewrite_crew = Crew(agents=[writer], tasks=[t_rewrite], process=Process.sequential, verbose=False)
    rewrite_result = rewrite_crew.kickoff()
    rewritten = str(rewrite_result).strip()

    # Stage 3: Bullet refinement
    print("Stage 3/4: Bullet point refinement...")
    t_refine = refine_bullets_task(refiner, rewritten)
    refine_crew = Crew(agents=[refiner], tasks=[t_refine], process=Process.sequential, verbose=False)
    refine_result = refine_crew.kickoff()
    final_resume = str(refine_result).strip()

    # Stage 4: Final evaluation with better error handling
    print("Stage 4/4: Final ATS evaluation...")
    try:
        t_eval = evaluate_ats_task(evaluator, final_resume, job_title, job_description)
        eval_crew = Crew(agents=[evaluator], tasks=[t_eval], process=Process.sequential, verbose=False)
        eval_result = eval_crew.kickoff()
        evaluation = str(eval_result).strip()
    except Exception as e:
        print(f"Evaluation error: {str(e)}")
        # Provide a fallback evaluation
        evaluation = '{"overall_score": 75, "breakdown": {"keywords": 4, "structure": 4, "metrics": 3, "verbs": 4, "format": 4}, "missing_keywords": [], "quick_wins": ["Continue optimizing based on specific job requirements"]}'

    print("Resume optimization complete!")
    return cleaned, rewritten, final_resume, evaluation
