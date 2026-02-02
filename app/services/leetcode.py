import asyncio
from typing import Any, Dict, List, Optional

import httpx


class LeetCodeDataService:
    QUERIES = {
        "getUserProfile": "query getUserProfile($username: String!) { allQuestionsCount {difficulty count} matchedUser(username: $username) { contributions {points questionCount testcaseCount} profile {reputation ranking} submitStats {acSubmissionNum {difficulty count submissions}} submissionCalendar languageProblemCount {languageName problemsSolved} } }",
        "skillStats": "query skillStats($username: String!) { matchedUser(username: $username) { tagProblemCounts { advanced {tagName problemsSolved} intermediate {tagName problemsSolved} fundamental {tagName problemsSolved} } } }",
        "userProfile": "query userProfile($username: String!) { matchedUser(username: $username) { username profile {ranking userAvatar realName} } }",
        "userContestRankingInfo": "query userContestRankingInfo($username: String!) { userContestRanking(username: $username) { attendedContestsCount rating globalRanking totalParticipants topPercentage badge {name} } userContestRankingHistory(username: $username) { attended problemsSolved ranking rating contest {title startTime} } }",
        "userPublicProfile": "query userPublicProfile($username: String!) { matchedUser(username: $username) { username profile { ranking userAvatar realName aboutMe countryName company jobTitle reputation } } }",
    }

    @staticmethod
    async def _get_result(
        client: httpx.AsyncClient, username: str, operation_name: str
    ) -> Optional[Dict[str, Any]]:
        """Make API request to LeetCode GraphQL API"""
        query = LeetCodeDataService.QUERIES[operation_name]
        payload = {
            "operationName": operation_name,
            "variables": {"username": username},
            "query": query,
        }
        headers = {
            "Referer": f"https://leetcode.com/{username}",
            "Content-type": "application/json",
        }
        try:
            response = await client.post(
                url="https://leetcode.com/graphql", json=payload, headers=headers
            )
            response.raise_for_status()
            data = response.json().get("data", {})
            return data
        except httpx.RequestError as e:
            print(f"Error fetching data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    @staticmethod
    async def fetch_all_user_data(usernames: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Fetch all data for multiple users in parallel
        """
        operations = [
            "userPublicProfile",
            "getUserProfile",
            "skillStats",
            "userProfile",
            "userContestRankingInfo",
        ]

        all_results = {}

        async with httpx.AsyncClient() as client:
            tasks = []
            for username in usernames:
                for op in operations:
                    tasks.append(LeetCodeDataService._get_result(client, username, op))

            # Execute all tasks
            results = await asyncio.gather(*tasks)

            # Reassemble results
            # The order of results matches the order of tasks
            task_idx = 0
            for username in usernames:
                all_results[username] = {}
                for op in operations:
                    all_results[username][op] = results[task_idx]
                    task_idx += 1

        return all_results

    @staticmethod
    async def validate_user(username: str) -> Dict[str, Any]:
        """Check if user exists and return validation result"""
        async with httpx.AsyncClient() as client:
            data = await LeetCodeDataService._get_result(
                client, username, "userPublicProfile"
            )

        if not data or "matchedUser" not in data or data["matchedUser"] is None:
            return {
                "valid": False,
                "message": f"User '{username}' does not exist on LeetCode or could not be found.",
            }
        return {"valid": True, "message": "User found", "data": data["matchedUser"]}
