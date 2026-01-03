from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.leetcode import LeetCodeDataService
from app.services.helpers import (
    get_accepted_problems_count_from_data,
    get_skills_stats_from_data,
    get_profile_details_from_data,
    get_contest_ranking_from_data
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Landing page"""
    return templates.TemplateResponse(request=request, name="index.html")

@router.post("/", response_class=HTMLResponse)
async def search_profile(request: Request, username: str = Form(...)):
    """Handle search form submission"""
    return RedirectResponse(url=f"/profiles/{username}", status_code=303)

@router.get("/profiles/{username}", response_class=HTMLResponse)
async def profile_detail(request: Request, username: str):
    """Display detailed visualization for a specific user profile"""
    
    # Check if user exists
    validation = await LeetCodeDataService.validate_user(username)
    if not validation['valid']:
        error_message = f'<div class="alert alert-warning" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>{validation["message"]}</div>'
        return templates.TemplateResponse(request=request, name="index.html", context={"error": error_message})

    # Fetch all data
    # Note: fetch_all_user_data expects a list of usernames
    user_data_map = await LeetCodeDataService.fetch_all_user_data([username])
    user_data = user_data_map.get(username)

    if not user_data:
         # Should ideally not happen if validation passed, but good to handle
         error_message = "Failed to fetch user data."
         return templates.TemplateResponse(request=request, name="index.html", context={"error": error_message})

    # Generate visualizations
    accepted_problem_count = get_accepted_problems_count_from_data(user_data)
    advanced_problem_count = get_skills_stats_from_data(user_data)
    user_details = get_profile_details_from_data(user_data)
    attended_contest_history = get_contest_ranking_from_data(user_data)

    context = {
        "plots": [accepted_problem_count, attended_contest_history, advanced_problem_count],
        "users": [user_details],
        "username": username
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
