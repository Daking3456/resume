from .heading_extractor import*


def parse_resume(input_text):
    resume_text = input_text
    sent_lines = resume_text.splitlines()
    # index of last line of the resume
    end_index = len(sent_lines)
    sliced_text = {}
    unique_index_heading_title = unique_index_headings(resume_text)

    #     list of indices of heading titles, will be used for slicing of resume text
    list_of_title_indices = list(unique_index_heading_title)

    # add last index of sentence splited resume to slice the last section of resume
    list_of_title_indices.append(end_index)
    # i=0 initialization is required to slice resume text from index-0 to first heading index of resume
    # which is in most cases, the personal information of the candidate
    i = 0
    for key, value in unique_index_heading_title.items():
        #         for i in range(len(list_of_title_indices)-1):
        sliced_text["profile information"] = sent_lines[0:list_of_title_indices[0]]
        sliced = sent_lines[list_of_title_indices[i] + 1:list_of_title_indices[i + 1]]
        sliced_text[value] = sliced
        #         sliced_text.append(value: sliced)
        i += 1
    return sliced_text


def formated_parsed_information(text):
    Profile = []
    Objectives = []
    Experiences = []
    Skills = []
    Projects = []
    Educations = []
    Rewards = []
    Languages = []
    References = []

    pharsed_info =parse_resume(text)

    for k, v in pharsed_info.items():
        if set(personal_info).intersection(set(k.lower().split(' '))):
            Profile.extend(v)
        elif k.lower() in objective:
            Objectives.extend(v)
        elif set(experiences).intersection(set(k.lower().split(' '))):
            Experiences.extend(v)
        elif set(skills).intersection(set(k.lower().split(' '))):
            Skills.extend(v)
        elif set(projects).intersection(set(k.lower().split(' '))):
            Projects.extend(v)
        elif set(academics).intersection(set(k.lower().split(' '))):
            Educations.extend(v)
        elif set(rewards).intersection(set(k.lower().split(' '))):
            Rewards.extend(v)
        elif set(languages).intersection(set(k.lower().split(' '))):
            Languages.extend(v)
        elif set(references).intersection(set(k.lower().split(' '))):
            References.extend(v)
        else:
            pass

    resume_info_extracted = {'profile': Profile,
                             'objectives': Objectives,
                             'experiences': Experiences,
                             'skills': Skills,
                             'projects': Projects,
                             'academics': Educations,
                             'rewards': Rewards,
                             'languages': Languages,
                             'references': References}

    return resume_info_extracted
