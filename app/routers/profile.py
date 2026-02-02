from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.helpers.profile import (
    get_accepted_problems_count_from_data,
    get_contest_ranking_from_data,
    get_language_stats_from_data,
    get_profile_details_from_data,
    get_skills_stats_from_data,
)
from app.services.leetcode import LeetCodeDataService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Landing page"""
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/", response_class=HTMLResponse)
async def search_profile(request: Request, username: str = Form(...)):
    """Handle search form submission"""
    return RedirectResponse(url=f"/profile/{username}", status_code=303)


@router.get("/profile/{username}", response_class=HTMLResponse)
async def profile_detail(request: Request, username: str):
    """Display detailed visualization for a specific user profile"""

    validation = await LeetCodeDataService.validate_user(username)
    if not validation["valid"]:
        error_message = f'<div class="alert alert-warning" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>{validation["message"]}</div>'
        return templates.TemplateResponse(
            request=request, name="index.html", context={"error": error_message}
        )

    user_data_map = await LeetCodeDataService.fetch_all_user_data([username])
    user_data = user_data_map.get(username)

    if not user_data:

        error_message = "Failed to fetch user data."
        return templates.TemplateResponse(
            request=request, name="index.html", context={"error": error_message}
        )

    accepted_problem_count = get_accepted_problems_count_from_data(user_data)
    advanced_problem_count = get_skills_stats_from_data(user_data)
    user_details = get_profile_details_from_data(user_data)
    attended_contest_history = get_contest_ranking_from_data(user_data)
    language_stats = get_language_stats_from_data(user_data)

    context = {
        "problems_chart": accepted_problem_count,
        "languages_chart": language_stats,
        "contest_history": attended_contest_history,
        "skills_stats": advanced_problem_count,
        "users": [user_details],
        "username": username,
        "og_title": f"{username}'s LeetCode Stats",
        "og_description": f"Check out {username}'s LeetCode stats: {user_details['realname']} has solved problems and attended contests. View their detailed progress!",
        "og_image": user_details["img"],
    }
    return templates.TemplateResponse(
        request=request, name="index.html", context=context
    )
