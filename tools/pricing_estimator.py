rate_table = {
    "ai_consulting": {"low": 5000, "medium": 10000, "high": 15000},
    "digital_marketing": {"low": 2000, "medium": 6000, "high": 10000},
    "web_development": {"low": 4000, "medium": 8000, "high": 12000},
    "cloud_devops": {"low": 3500, "medium": 7000, "high": 10000},
}
complexity_multiplier = {
    "low": 0.8,
    "medium": 1.0,
    "high": 1.5,
}

def estimate_price(project_type, duration, complexity="medium"):
    """Estimate the price of a project.
    
    Args:
        project_type: The type of service.
        duration: The project duration in months.
        complexity: Project complexity level (low, medium, high).
        
    Returns:
        dict with pricing details or error information.
    """
    try:
        duration = int(duration)
    except (ValueError, TypeError):
        return {
            "error": f"Invalid duration: '{duration}'. Duration must be a valid number of months (e.g., 3)."
        }

    if duration <= 0:
        return {
            "error": f"Invalid duration: {duration}. Duration must be a positive number of months."
        }

    project_type = str(project_type).strip().lower()
    complexity = str(complexity).strip().lower()

    if project_type not in rate_table:
        return {
            "error": f"Unknown service: '{project_type}'. Available services: {list(rate_table.keys())}"
        }

    base_price = rate_table[project_type][complexity]
    adjusted_price = base_price * complexity_multiplier[complexity] * duration
    return {
        "project_type": project_type,
        "duration_months": duration,
        "complexity": complexity,
        "estimated_price_usd": adjusted_price,
        "notes": "This is an estimated price. Final pricing may vary based on specific requirements."
    }
