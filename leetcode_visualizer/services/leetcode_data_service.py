import pandas as pd
import requests
import concurrent.futures


class LeetCodeDataService:
    QUERIES = {
        "getUserProfile": "query getUserProfile($username: String!) { allQuestionsCount {difficulty count} matchedUser(username: $username) { contributions {points questionCount testcaseCount} profile {reputation ranking} submitStats {acSubmissionNum {difficulty count submissions}} } }",
        "skillStats": "query skillStats($username: String!) { matchedUser(username: $username) { tagProblemCounts { advanced {tagName problemsSolved} intermediate {tagName problemsSolved} fundamental {tagName problemsSolved} } } }",
        "userProfile": "query userProfile($username: String!) { matchedUser(username: $username) { username profile {ranking userAvatar realName} } }",
        "userContestRankingInfo": "query userContestRankingInfo($username: String!) { userContestRanking(username: $username) { attendedContestsCount rating globalRanking totalParticipants topPercentage badge {name} } userContestRankingHistory(username: $username) { attended problemsSolved ranking contest {title startTime} } }",
        "userPublicProfile": "query userPublicProfile($username: String!) { matchedUser(username: $username) { username profile { ranking userAvatar realName aboutMe countryName company jobTitle reputation } } }",
    }

    @staticmethod
    def _get_result(username, operation_name):
        """Make API request to LeetCode GraphQL API without caching"""
        query = LeetCodeDataService.QUERIES[operation_name]
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
            data = response.json().get("data", {})
            return data
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    @staticmethod
    def fetch_all_user_data(usernames):
        """
        Fetch all data for multiple users in parallel

        Args:
            usernames: List of usernames to fetch data for

        Returns:
            Dictionary mapping usernames to their results
        """
        operations = ['userPublicProfile', 'getUserProfile',
                      'skillStats', 'userProfile', 'userContestRankingInfo']

        all_results = {}

        # Use thread pool to fetch data in parallel for all users and operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Create a dictionary mapping futures to (username, operation) tuples
            future_to_data = {}
            for username in usernames:
                for op in operations:
                    future = executor.submit(
                        LeetCodeDataService._get_result, username, op)
                    future_to_data[future] = (username, op)

            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_data):
                username, operation = future_to_data[future]

                # Initialize result dictionary for this username if needed
                if username not in all_results:
                    all_results[username] = {}

                try:
                    result = future.result()
                    all_results[username][operation] = result
                except Exception as e:
                    print(f"Error fetching {operation} for {username}: {e}")
                    all_results[username][operation] = None

        return all_results

    @staticmethod
    def validate_user(username):
        """Check if user exists and return validation result"""
        data = LeetCodeDataService._get_result(username, "userPublicProfile")

        if not data or 'matchedUser' not in data or data['matchedUser'] is None:
            return {
                'valid': False,
                'message': f"User '{username}' does not exist on LeetCode or could not be found."
            }
        return {
            'valid': True,
            'message': "User found",
            'data': data['matchedUser']
        }

    @staticmethod
    def get_profile_details(username):
        """Get user profile details"""
        data = LeetCodeDataService._get_result(
            username, operation_name='userProfile')
        data = data['matchedUser']
        return {
            "username": data['username'],
            "realname": data['profile']['realName'],
            'img': data['profile']['userAvatar']
        }

    @staticmethod
    def get_solved_problems_data(username):
        """Get data about solved problems by difficulty"""
        data = LeetCodeDataService._get_result(
            username, operation_name='getUserProfile')
        d1 = data['allQuestionsCount'][1:]
        d2 = data['matchedUser']['submitStats']['acSubmissionNum'][1:]

        if data['matchedUser']['submitStats']['acSubmissionNum'][0]['count'] == 0:
            return pd.DataFrame()

        difficulty = ['Easy', 'Medium', 'Hard']
        total_ques_count = [problem_count['count'] for problem_count in d1]
        accepted_ques_count = [problem_count['count'] for problem_count in d2]

        return pd.DataFrame({
            "difficulty": difficulty,
            "total": total_ques_count,
            "accepted": accepted_ques_count
        })

    @staticmethod
    def get_skills_data(username):
        """Get data about skills/tags"""
        data = LeetCodeDataService._get_result(
            username, operation_name='skillStats')
        return data['matchedUser']['tagProblemCounts']

    @staticmethod
    def get_contest_data(username):
        """Get contest ranking data"""
        data = LeetCodeDataService._get_result(
            username, "userContestRankingInfo")
        if 'userContestRankingHistory' not in data:
            return pd.DataFrame()

        all_contest_history = pd.DataFrame(data['userContestRankingHistory'])

        if len(all_contest_history) == 0:
            return pd.DataFrame()

        attended_contest = all_contest_history[all_contest_history['attended'] != False]
        attended_contest.reset_index(drop=True, inplace=True)

        for i in range(len(attended_contest)):
            attended_contest.iloc[i, -
                                  1] = attended_contest.iloc[i, -1]['title']

        return attended_contest
