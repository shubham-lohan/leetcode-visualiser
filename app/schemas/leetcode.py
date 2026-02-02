from typing import Any, List, Optional

from pydantic import BaseModel


class DifficultyCount(BaseModel):
    difficulty: str
    count: int
    submissions: Optional[int] = None


class SubmitStats(BaseModel):
    acSubmissionNum: List[DifficultyCount]


class UserProfileProfile(BaseModel):
    reputation: Optional[int] = 0
    ranking: Optional[int] = 0
    realName: Optional[str] = ""
    userAvatar: Optional[str] = ""
    countryName: Optional[str] = ""
    company: Optional[str] = ""
    jobTitle: Optional[str] = ""
    aboutMe: Optional[str] = ""


class TagProblemCount(BaseModel):
    tagName: str
    problemsSolved: int


class TagProblemCounts(BaseModel):
    advanced: List[TagProblemCount]
    intermediate: List[TagProblemCount]
    fundamental: List[TagProblemCount]


class ContestRanking(BaseModel):
    attendedContestsCount: int
    rating: float
    globalRanking: int
    totalParticipants: int
    topPercentage: float
    badge: Optional[dict] = None


class ContestHistory(BaseModel):
    attended: bool
    problemsSolved: int
    ranking: int
    contest: dict


class ServiceResponse(BaseModel):
    """Generic wrapper for service responses"""

    valid: bool
    message: Optional[str] = None
    data: Optional[Any] = None


# API Response Models
class MatchedUser(BaseModel):
    username: Optional[str] = None
    profile: Optional[UserProfileProfile] = None
    submitStats: Optional[SubmitStats] = None
    tagProblemCounts: Optional[TagProblemCounts] = None


class UserData(BaseModel):
    allQuestionsCount: Optional[List[DifficultyCount]] = None
    matchedUser: Optional[MatchedUser] = None
    userContestRanking: Optional[ContestRanking] = None
    userContestRankingHistory: Optional[List[ContestHistory]] = None
