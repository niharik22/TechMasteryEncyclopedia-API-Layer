import logging
from typing import Dict, List
from main.services.qualified_service import QualifiedService

class DataProcessor:
    def __init__(self, qualified_service: QualifiedService):
        """
        Initializes the DataProcessor with an instance of QualifiedService.

        Args:
            qualified_service (QualifiedService): An instance of QualifiedService to fetch and process data.
        """
        self.qualified_service = qualified_service

    def process_place_of_work_data(self, country: str, state: str, role: str) -> List[Dict]:
        """
        Processes the place of work data and prepares it in the desired percentage format,
        considering only the counts for 'Hybrid', 'On-Site', and 'Remote'.
        If any of the categories are missing or have zero counts, 1 is added to each category
        to balance the data and calculate percentages.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list of dictionaries with the 'id', 'label', and 'value' (percentage) of each place of work.
        """
        # Call the QualifiedService method to get raw data
        raw_data = self.qualified_service.get_place_of_work_count_grouped_by_role_and_state(country, state, role)

        # Convert the raw data to a dictionary for easier access
        place_of_work_counts = {entry["_id"]: entry["count"] for entry in raw_data}

        # Define the desired place of work labels
        desired_labels = ["Hybrid", "On-Site", "Remote"]

        # Initialize counts, adding 1 to each category to balance the data
        balanced_counts = {label: place_of_work_counts.get(label, 0) + 1 for label in desired_labels}

        # Calculate the total count after adding 1 to each category
        total_count = sum(balanced_counts.values())

        # Process the data to form percentages and match the desired format
        processed_data = []
        for label in desired_labels:
            count = balanced_counts[label]
            percentage = (count / total_count * 100) if total_count > 0 else 0
            processed_data.append({
                "id": label,
                "label": label,
                "value": round(percentage, 2)  # Round to 2 decimal places
            })

        logging.info(f"Processed place of work data for country: {country}, state: {state}, role: {role}")
        return processed_data

    def process_tools_data(self, country: str, state: str, role: str) -> List[Dict]:
        """
        Processes the tools data by extracting 1-grams from bigrams, accumulating scores,
        and calculating percentages. Special handling for 'power' + 'bi' -> 'powerbi',
        Microsoft-related combinations, 'google' partnering with its bigram partner,
        and ignoring specific 1-grams.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list of tools with their percentages.
        """
        raw_tools_data = self.qualified_service.get_bigram_details_by_country_state_role(country, state, role).get(
            'tools', [])
        tools_scores = {}

        # Define 1-grams to ignore
        ignored_1grams = {"like"}  # Add more words to ignore as needed

        for item in raw_tools_data:
            bigram = item['bigram']
            score = item['score']

            # Check for special case: "power" + "bi" -> "powerbi"
            if "power" in bigram and "bi" in bigram:
                tools_scores["powerbi"] = tools_scores.get("powerbi", 0) + score
            else:
                for word in bigram:
                    if word.lower() in ignored_1grams:
                        # Skip words that are in the ignored set
                        continue
                    elif word.lower() == "microsoft":
                        # Combine 'Microsoft' with the other word in the bigram
                        combined_tool = f"microsoft {bigram[1] if bigram[0].lower() == 'microsoft' else bigram[0]}"
                        tools_scores[combined_tool.lower()] = tools_scores.get(combined_tool.lower(), 0) + score
                    elif word.lower() == "google":
                        # Combine 'Google' with its partner word in the bigram
                        combined_tool = f"google {bigram[1] if bigram[0].lower() == 'google' else bigram[0]}"
                        tools_scores[combined_tool.lower()] = tools_scores.get(combined_tool.lower(), 0) + score
                    else:
                        tools_scores[word.lower()] = tools_scores.get(word.lower(), 0) + score

        # Calculate total score and convert to percentages
        total_score = sum(tools_scores.values())
        tools_data = [
            {"tool": tool, "percentage": round((score / total_score * 100), 2) if total_score > 0 else 0}
            for tool, score in tools_scores.items()
        ]

        # Sort and return the top 5
        tools_data.sort(key=lambda x: x["percentage"], reverse=True)
        return tools_data[:5]

    def process_skills_data(self, country: str, state: str, role: str) -> List[Dict]:
        """
        Processes the skills data by extracting bigrams, accumulating scores, and calculating percentages.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list of skills with their percentages.
        """
        raw_skills_data = self.qualified_service.get_bigram_details_by_country_state_role(country, state, role).get('skills', [])
        skills_scores = {}

        for item in raw_skills_data:
            bigram = " ".join(item['bigram'])  # Join bigram with a space
            score = item['score']
            skills_scores[bigram] = skills_scores.get(bigram, 0) + score

        # Calculate total score and convert to percentages
        total_score = sum(skills_scores.values())
        skills_data = [
            {"skill": skill, "percentage": round((score / total_score * 100), 2) if total_score > 0 else 0}
            for skill, score in skills_scores.items()
        ]

        # Sort and return the top 5
        skills_data.sort(key=lambda x: x["percentage"], reverse=True)
        return skills_data[:5]

    def process_languages_data(self, country: str, state: str, role: str) -> List[Dict]:
        """
        Processes the languages data by extracting 1-grams, accumulating scores, and calculating percentages.
        Ignores specific 1-grams and handles renaming "net" to ".net".

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list of languages with their percentages.
        """
        raw_languages_data = self.qualified_service.get_bigram_details_by_country_state_role(country, state, role).get(
            'languages', []
        )
        languages_scores = {}

        # Define 1-grams to ignore
        ignored_1grams = {"data", "server"}  # Add any other 1-grams you want to ignore

        for item in raw_languages_data:
            # Ensure 'bigram' is not None and is a list before processing
            bigram = item.get('bigram', [])
            if not bigram or not isinstance(bigram, list):
                continue

            score = item.get('score', 0)
            for word in bigram:
                if word and word.lower() not in ignored_1grams:  # Check if the word is not None and not in the ignored list
                    # Rename "net" to ".net"
                    if word.lower() == "net":
                        word = ".net"
                    languages_scores[word.lower()] = languages_scores.get(word.lower(), 0) + score

        # Calculate total score and convert to percentages
        total_score = sum(languages_scores.values())
        languages_data = [
            {"language": language, "percentage": round((score / total_score * 100), 2) if total_score > 0 else 0}
            for language, score in languages_scores.items()
        ]

        # Sort and return the top 5
        languages_data.sort(key=lambda x: x["percentage"], reverse=True)
        return languages_data[:5]

    def process_libraries_data(self, country: str, state: str, role: str) -> List[Dict]:
        """
        Processes the libraries data by extracting 1-grams, accumulating scores, and calculating percentages.
        Special handling for "spring" + "boot" -> "spring boot", "apache" + "kafka" -> "apache kafka",
        combining "framework" with its bigram partner, and combining "js" with its bigram partner.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list of libraries with their percentages.
        """
        raw_libraries_data = self.qualified_service.get_bigram_details_by_country_state_role(country, state, role).get(
            'libraries', []
        )
        libraries_scores = {}

        for item in raw_libraries_data:
            bigram = item['bigram']
            score = item['score']

            # Check for special cases: "spring" + "boot" -> "spring boot" and "apache" + "kafka" -> "apache kafka"
            if "spring" in bigram and "boot" in bigram:
                libraries_scores["spring boot"] = libraries_scores.get("spring boot", 0) + score
            elif "apache" in bigram and "kafka" in bigram:
                libraries_scores["apache kafka"] = libraries_scores.get("apache kafka", 0) + score
            elif "framework" in bigram:
                # Combine "framework" with its bigram partner
                combined_library = f"{bigram[1] if bigram[0].lower() == 'framework' else bigram[0]} framework"
                libraries_scores[combined_library.lower()] = libraries_scores.get(combined_library.lower(), 0) + score
            elif "js" in bigram:
                # Combine "js" with its bigram partner to form "partner.js"
                combined_library = f"{bigram[1] if bigram[0].lower() == 'js' else bigram[0]}.js"
                libraries_scores[combined_library.lower()] = libraries_scores.get(combined_library.lower(), 0) + score
            else:
                for word in bigram:
                    libraries_scores[word.lower()] = libraries_scores.get(word.lower(), 0) + score

        # Calculate total score and convert to percentages
        total_score = sum(libraries_scores.values())
        libraries_data = [
            {"library": library, "percentage": round((score / total_score * 100), 2) if total_score > 0 else 0}
            for library, score in libraries_scores.items()
        ]

        # Sort and return the top 5
        libraries_data.sort(key=lambda x: x["percentage"], reverse=True)
        return libraries_data[:5]

    def process_bigram_data(self, country: str, state: str, role: str) -> Dict[str, List[Dict]]:
        """
        Calls all four processing methods and formats the data into the desired structure.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            Dict[str, List[Dict]]: A dictionary containing processed data for skills, tools, libraries, and languages.
        """
        # Call each method to get the processed data
        skills_data = self.process_skills_data(country, state, role)
        tools_data = self.process_tools_data(country, state, role)
        libraries_data = self.process_libraries_data(country, state, role)
        languages_data = self.process_languages_data(country, state, role)

        # Format the data into the desired structure
        data = {
            "skills": [{"skill": item["skill"], "percentage": item["percentage"]} for item in skills_data],
            "tools": [{"tool": item["tool"], "percentage": item["percentage"]} for item in tools_data],
            "libraries": [{"library": item["library"], "percentage": item["percentage"]} for item in libraries_data],
            "languages": [{"language": item["language"], "percentage": item["percentage"]} for item in languages_data]
        }

        logging.info(f"Processed bigram data for country: {country}, state: {state}, role: {role}")
        return data

    def process_education_data(self, country: str, state: str, role: str) -> List[Dict]:
        """
        Processes the education data to prepare it in a list of dictionaries format.
        Groups the 1-grams from bigrams (ignoring specific words) and sums the scores,
        then converts the scores to percentages and returns the top 3.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list of dictionaries containing 'id', 'label', and 'value' for the top 4 1-grams.
        """
        # Set of 1-grams to ignore
        ignored_1grams = {"degree", "jobrelated"}

        # Call the QualifiedService method to get raw education data
        raw_education_data = self.qualified_service.get_education_data_by_country_state_role(country, state, role)

        # Dictionary to accumulate scores for each 1-gram
        education_scores = {}

        # Process the raw data to extract and accumulate scores
        for item in raw_education_data:
            bigram = item.get("bigram", [])
            score = item.get("score", 0)

            for word in bigram:
                if word.lower() not in ignored_1grams:  # Ignore words in the set
                    if word.lower() in education_scores:
                        education_scores[word.lower()] += score
                    else:
                        education_scores[word.lower()] = score

        # Calculate the total score for all 1-grams
        total_score = sum(education_scores.values())

        # Convert accumulated scores into percentages and format as required
        data = [
            {
                "id": word.capitalize(),
                "label": word.capitalize(),  # Capitalize for label formatting
                "value": round((score / total_score * 100), 2) if total_score > 0 else 0  # Calculate percentage
            }
            for word, score in education_scores.items()
        ]

        # Sort the data by percentage in descending order and select the top 4
        data.sort(key=lambda x: x["value"], reverse=True)
        top_3_data = data[:3]  # Get only the top 4 entries

        logging.info(f"Processed education data for country: {country}, state: {state}, role: {role}")
        return top_3_data

    def process_state_frequency_data(self, country: str) -> List[Dict]:
        """
        Processes the state frequency data and prepares it in the desired percentage format.

        Args:
            country (str): The country to filter by.

        Returns:
            List[Dict]: A list of dictionaries with the 'state' and 'percentage' for each state.
        """
        # Call the QualifiedService method to get raw state frequency data
        raw_state_data = self.qualified_service.get_freq_grouped_by_state(country)

        state_counts = {}
        for entry in raw_state_data:
            state = entry["state"]
            count = entry["count"]

            if state in state_counts:
                state_counts[state] += count
            else:
                state_counts[state] = count

        # Calculate the total count of all state records
        total_count = sum(state_counts.values())

        # Process the data to form percentages and match the desired format
        processed_data = []
        for state, count in state_counts.items():
            percentage = (count / total_count * 100) if total_count > 0 else 0
            processed_data.append({
                "state": state,
                "percentage": round(percentage, 2)  # Round to 2 decimal places
            })

        # Sort the data by state for consistency
        processed_data.sort(key=lambda x: x["state"])

        logging.info(f"Processed state frequency data for country: {country}")
        return processed_data

    def fetch_distinct_roles(self, country: str) -> List[str]:
        """
        Fetches distinct roles for the given country using the QualifiedService.

        Args:
            country (str): The country to filter by.

        Returns:
            List[str]: A list of distinct roles available in the specified country.
        """
        try:
            roles = self.qualified_service.get_roles_by_country_and_state(country)
            logging.info(f"Fetched distinct roles for country: {country}")
            return roles
        except Exception as e:
            logging.exception(f"Error fetching distinct roles for country: {country}")
            return []

