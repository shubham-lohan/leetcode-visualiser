import requests

queries = {
    "getUserProfile": "query getUserProfile($username: String!) { allQuestionsCount {difficulty count} matchedUser(username: $username) { contributions {points questionCount testcaseCount} profile {reputation ranking} submitStats {acSubmissionNum {difficulty count submissions}} } }",
    "skillStats": "query skillStats($username: String!) { matchedUser(username: $username) { tagProblemCounts { advanced {tagName problemsSolved} intermediate {tagName problemsSolved} fundamental {tagName problemsSolved} } } }",
    "userProfile": "query userProfile($username: String!) { matchedUser(username: $username) { username profile {ranking userAvatar realName} } }",
    "userContestRankingInfo": "query userContestRankingInfo($username: String!) { userContestRanking(username: $username) { attendedContestsCount rating globalRanking totalParticipants topPercentage badge {name} } userContestRankingHistory(username: $username) { attended problemsSolved ranking contest {title startTime} } }",
    "userPublicProfile": "query userPublicProfile($username: String!) { matchedUser(username: $username) { username profile { ranking userAvatar realName aboutMe countryName company jobTitle reputation } } }",
}

def get_result(username, operation_name):
    query = queries[operation_name]
    payload = {
        "operationName": operation_name,
        "variables": {"username": username},
        "query": query
    }
    headers = {
        "Referer": f"https://leetcode.com/{username}",
        "Content-type": "application/json"
    }
    try:
        response = requests.post(
            url="https://leetcode.com/graphql", json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
