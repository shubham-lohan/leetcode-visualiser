from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.helpers.comparison import (
    compare_contests_from_data,
    compare_problem_counts_from_data,
    compare_skills_from_data,
)
from app.services.helpers.profile import get_profile_details_from_data
from app.services.leetcode import LeetCodeDataService

router = APIRouter(prefix="/compare")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def comparison_form(request: Request):
    """Display form to compare two LeetCode profiles"""
    return templates.TemplateResponse(request=request, name="compare.html")


@router.post("/", response_class=HTMLResponse)
async def submit_comparison(
    request: Request, username1: str = Form(...), username2: str = Form(...)
):
    """Handle comparison form submission"""
    return RedirectResponse(url=f"/compare/{username1}/{username2}", status_code=303)


@router.get("/{username1}/{username2}", response_class=HTMLResponse)
async def comparison_detail(request: Request, username1: str, username2: str):
    """Display detailed comparison between two specific LeetCode profiles"""

    # Validation logic
    # We validate sequentially here, or could do parallel if we improve validate_user to take list
    # For now, let's keep it simple as per original
    validation1 = await LeetCodeDataService.validate_user(username1)
    validation2 = await LeetCodeDataService.validate_user(username2)

    if not validation1["valid"] or not validation2["valid"]:
        error_messages = []
        if not validation1["valid"]:
            error_messages.append(validation1["message"])
        if not validation2["valid"]:
            error_messages.append(validation2["message"])

        error_html = '<div class="alert alert-warning" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>'
        error_html += "<br>".join(error_messages)
        error_html += "</div>"

        return templates.TemplateResponse(
            request=request, name="compare.html", context={"error": error_html}
        )

    # Fetch all data for both users
    user_data = await LeetCodeDataService.fetch_all_user_data([username1, username2])
    user1_data = user_data.get(username1)
    user2_data = user_data.get(username2)

    # Generate user profiles
    user1_details = get_profile_details_from_data(user1_data)
    user2_details = get_profile_details_from_data(user2_data)
    users = [user1_details, user2_details]

    # Generate comparison visualizations
    problem_type_count = compare_problem_counts_from_data(
        user1_data, user2_data, username1, username2
    )
    skills_comparison = compare_skills_from_data(
        user1_data, user2_data, username1, username2
    )
    contest_comparison = compare_contests_from_data(
        user1_data, user2_data, username1, username2
    )

    plots = [problem_type_count, skills_comparison, contest_comparison]

    context = {
        "users": users,
        "plots": plots,
        "username1": username1,
        "username2": username2,
        "og_title": f"Compare {username1} vs {username2}",
        "og_description": f"See who's better: {username1} vs {username2}. Compare their LeetCode problem solving stats, contest ratings, and skills side-by-side.",
        "og_image": user1_details.get("img") or user2_details.get("img"),
    }
    return templates.TemplateResponse(
        request=request, name="compare.html", context=context
    )
