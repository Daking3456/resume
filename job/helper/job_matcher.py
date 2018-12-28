
def job_matcher():
    matching_skills = []
    job_match_percent = []

    for i in range(0, len(python_jobs)):
        if profile['skills'] != 0:
            common_skills = tuple(set(profile['skills'].keys()) & set(python_jobs.iloc[i, 4]))
            matching_skills.append([common_skills, len(common_skills)])
        else:
            common_skills = ()
            matching_skills.append([common_skills])

        if profile['undergrad_degree'] == True and python_jobs.iloc[i, 6] == True or profile['graduate_degree'] == True and \
                python_jobs.iloc[i, 6] == True or \
                profile['undergrad_degree'] == True and python_jobs.iloc[i, 6] == False or profile[
            'graduate_degree'] == True and python_jobs.iloc[i, 6] == False or \
                profile['graduate_degree'] == True and python_jobs.iloc[i, 7] == True or profile[
            'graduate_degree'] == True and python_jobs.iloc[i, 7] == False:
            education_match = 1
        else:
            education_match = 0

        if profile['total_experience'] >= float(python_jobs.iloc[i, -1]):
            experience_match = 1
        else:
            experience_match = 0

        # Applying algorithm
        job_match_percent.append((((0.4 * len(common_skills)) / len(
            python_jobs.iloc[i, 4])) + 0.25 * education_match + 0.35 * experience_match) * 100)

    result = pd.DataFrame()
    result['company_name'] = python_jobs['company_name']
    result['location'] = python_jobs['location']
    result['position'] = python_jobs['position']
    result['required_skills'] = python_jobs['required_skills']
    result['matching_skills'] = matching_skills
    result['job_match_percent'] = job_match_percent