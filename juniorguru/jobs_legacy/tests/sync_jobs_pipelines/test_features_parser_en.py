import pytest

from juniorguru.jobs.legacy_jobs.pipelines.features_parser import parse_from_sentence


def get_rule_ids(parse_results):
    return {rule_id for rule_id, match, pattern in parse_results}


@pytest.mark.parametrize('sentence', [
    'have Computing Degree',
    'You have a degree in Computer Science, Mathematics, Physics or Business Administration.',
    'After your studies in mathematics, computer science, engineering, business or comparable studies',
    'Completed technical education (college or university level)',
    'Bachelor’s degree or higher (min A- average for under-graduate, first class for post-graduate).',
    'Bachelorâ€™s degree or higher in Computer Science or related field.',
    'exceptional master\'s degree in computer science or even a doctorate',
    'Profound completed education in the field of IT/software-development',
    'Good academic record',
    'Completed education in computer science',
    'B.Sc. in computer science or related field',
    'Technical Engineering Degree',
    'Completed education in informatics',
    'B.S. in Computer Science or related area of study (M.S. preferred)',
    'BS in a technical discipline. MS desirable.',
    'University degree in Computer Sciences or a comparable education',
])
def test_parse_from_sentence_en_tech_degree_required(sentence):
    assert 'TECH_DEGREE_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'A completed degree in a suitable field of study',
    'BS in Computer Science/Engineering or equivalent industry experience.',
    'BS or MS in software engineering or equivalent experience',
    'completed training in computer science / electrical engineering',
    'World-class technical training within Teradata University',
    'Do you want to combine university and work? Are you doing your PhD?',
    'You are a high school graduate with a focus on IT or a interested person in programming',
    'University degree in Computer Science or Economics/Finance or equivalent professional qualification or experience',
])
def test_parse_from_sentence_en_tech_degree_required_not(sentence):
    assert 'TECH_DEGREE_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    '10+ experience with architecting',
    'At least 5 years’ experience as an iOS mobile developer.',
    'Two or more years of hands-on experience',
    'Strong experience (5+ years) in Java',
    'At least five years experience as an iOS mobile developer.',
    'Must have 3+ years of proven track record as a ServiceNow Admin/Developer',
    'Multiple years of experience in software development.',
    'Several years experience of Java development',
    'Successfully developed web applications in a professional working environment (minimum 1 year)',
])
def test_parse_from_sentence_en_years_experience_required(sentence):
    assert 'YEARS_EXPERIENCE_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Ability to determine which data could provide value and insights towards improving user experience',
    'We are willing to offer a higher salary depending on your professional experience and qualification',  # bug/regression
])
def test_parse_from_sentence_en_years_experience_required_not(sentence):
    assert 'YEARS_EXPERIENCE_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    '10+ experience with architecting',
    'developer with strong technical background',
    'engineer with a thorough understanding',
    'strong Java development background',
    'working experience in (software) development',
    'Excellent analytical and problem-solving skills',
    'Solid technical background',
    'Proven commercial experience working with Java',
    'sound knowledge of HTML',
    'previous experience in C++',
    'significant technical background',
    'very solid know-how on how to write C++',
    'take responsibility for good architecture and software design',
    'you have gained professional experience',
    'Very good programming skills and practical experience',
    'experience in building very complex applications',
    'Excellent SQL know how',
    'You have HTML 5 superpowers',
    'experience with React, HTML, CSS, JavaScript, JS, Bootstrap and everything else',
    'Willingness to take end-to-end ownership on the whole control function',
    'Manage your own project priorities, deadlines and deliverables',
    'Proficiency in C# / C++ , object oriented programming, and component oriented architecture.',
    'Experience as a software engineer in cloud-based software solutions',
    'with a deeper understanding of ServiceNow development best practices',
    'Must have hands-on implementation experience of ServiceNow',
    'Must have hands-on experience with customizations',
    'Strong coding skills in Python, Java or C++',
    'Proficient in a scripting language like Bash or Groovy',
    'Experience of deploying components',
    'Are you fluent in C++?',
    'Architecture knowledge, such as DevOps desired',
    'Extensive experience with Swift as well as software architecture',
    'Well-versed in HTTP, Web services, RESTful API design principles, scalability and security concerns',
    'Proficient understanding of code versioning tools, such as Stash/Git',
    'Superior analytical and problem-solving abilities.',
    'you consider yourself as a healthy mix between a machine learning expert, a software engineer, a researcher, and a hacker',
    'Efficiently translate customer business needs into end-to-end technical solutions',
    'provable relevant industry experience',
    'Advanced scripting skills including bash and python.',
    'You have extensive experience in Software Engineering',
    'You gained profound experience with Spring, REST',
    'Fluency in Agile and Scrum',
    'Working proficiency with',
    'Business analysis and/or requirements engineering experience',
    'Detailed knowledge of MS SQL Server',
    'Experience working with a variety of databases',
    'Extensive knowledge of modern HTML and CSS',
    'Java 8 Development experience within a professional / commercial setting',
    'Notable C# object oriented programming skills, .NET framework knowledge',
    'intermediate SQL developer - enterprise projects',
    'medior SQL developer - enterprise projects',
    'C# or C++developer (intermediate/senior) - Prague',
    'Extended knowledge in React or a similar UI library (e.g., Vue)',
])
def test_parse_from_sentence_en_advanced_required(sentence):
    assert 'ADVANCED_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Good english communication skills',
    'Practical experience with C# and .NET or other OOP language',
    'Some experience in software development',
    'On-the-job training for professional and technical background of our products',
    'We are willing to offer a higher salary depending on your professional experience and qualification',
    'Ideally, you already have practical experience in the areas of IT consulting or logistics',
    'you are also proficient with MS Office and ideally have previous experience with JIRA and Confluence',
    'Professional growth and development through certified training programs and knowledge sharing',
    'No prior work experience necessary',
    'Integration of services to maximize ad revenues and maintain strong user experience.',
    'Excellent communications skills',
    'good knowledge of Microsoft Office',
    'good knowledge of MS Office',
    'Opportunity to develop solid cross functional network',
    'chance to develop key soft skills and management',
    'advantage - practical experience with web frameworks',
    'We welcome knowledge of ITIL and previous experience in test automation.',
    'If you are interested, please send us an overview of your skills and previous experience.',
    'You are experienced with one or the other communication protocol',
    'These are the professional requirements and personal skills we are looking for:',
    'So if you like the sound of the above and your CV has some of the aforementioned key skills then why not apply.',
    'Augmented Analytics automates work of human analysts by developing software intelligence that autonomously produces key business insights',
    'Extensive library / knowledge base',
    'At Ubiq we work on enabling a seamless last mile experience by delivering',
    'Work alongside machine learning engineers to optimize visualizations and product experience',
    'You can also take advantage of targeted professional development opportunities',
    'We take full ownership of our projects - from technical scope',
    'As a Frontend Engineer at Perseus, you will work with a small team of highly skilled developers delivering experience',
    '・ We are hungry craftspeople, we have grit, we are honest, we take ownership',
    'First professional experience in software development',
    'with excellent test coverage and world-class processes including great code reviews and cross-team knowledge-sharing.',
    'You are routinely working with modern technologies and practices on a high quality Swift codebase, allowing you to grow fast and gain experience efficiently.',
    'You are fluent in at least one programming language.',
    'This future state platform will seamlessly and uniquely deliver a revolutionized learning experience through innovation, continuous delivery, and architectural integration.',
    'love working in a diverse team with different backgrounds and different knowledge levels',
    'Required Technical and Professional Expertise',
    'Proficiency with Mac OS and Windows operating systems.',
    'Flat hierarchies strengthen the initiative and the willingness of our employees to take on responsibility independently.',
    'Solid presentation skills',
])
def test_parse_from_sentence_en_advanced_required_not(sentence):
    assert 'ADVANCED_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'We are looking for a seasoned engineer',
    'experienced Java developer',
    'As a senior developer your will',
    'senior developers shall demonstrate very good understanding of C#',
    'As a senior developer your will focus',
    'They are now looking for an experienced Senior Java developer to join their collaborative team',
    'The Specialist Software Engineer will be responsible for the software design, development, and operation of these SaMD.',
])
def test_parse_from_sentence_en_explicitly_senior(sentence):
    assert 'EXPLICITLY_SENIOR' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Team 8-10 junior-senior',
    'love working in a diverse team with seniors and juniors.',
    'we are open to all levels of seniority from junior to team leaders',
    'C# Software Developer - Jnr, Mid and Senior Opportunties Available',
    'Support, learn, and collaborate with Senior and Lead Developers',
    'guided by a senior software engineer.',
    'Excellent communication skills and the ability to work effectively with senior traders and other developers',
])
def test_parse_from_sentence_en_explicitly_senior_not(sentence):
    assert 'EXPLICITLY_SENIOR' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'You are a native German speaker',
    'In addition to solid German and English skills',
    'Strong communication skills with good command of German and English',
    'German language is desired.',
    'good language skills in German and English',
    'German spoken and written is indispensable',
    'You have good German and very good English language skills',
    'Proficient in English, desirable: german',
    'Basic communication in German',
])
def test_parse_from_sentence_en_german_required(sentence):
    assert 'GERMAN_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'communication skills in German, speaking and writing, would be a benefit',
    'demonstrate ability to communicate in English (B1-B2), German language is an advantage',
    'Language courses (Czech, German)',
    'Languages: Fluent English (a must), other (German, Russian, Spanish - an advantage)',
    'Fluent English skills with German as a plus',
    'English language / german language (nice to have)',
    'Fluent in English, German is a plus',
    'German as a plus- B2 level daily communication with a client',
    'Free German classes with people from all over the world!',
    'Fluency in German or Russian is a plus; English is required',
    'Strong verbal and written English skills (English is the working language, German is not required)',
])
def test_parse_from_sentence_en_german_required_not(sentence):
    assert 'GERMAN_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Experience leading a team',
    'Lead a growing team',
    'experience as a Technical Leader',
    'leadership skills',
    'Leadership experience',
    'Capable of working cross functionally, leading by example',
    'You lead courses at the customer’s premises',
    'you will also get the chance to mentor junior developers in the team',
    'Mentor junior members in the team by relentlessly guarding code quality through pull requests and code reviews',
    'delegate tasks to others on team',
    'technical leadership and mentoring skills',
])
def test_parse_from_sentence_en_leadership_required(sentence):
    assert 'LEADERSHIP_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'we are open to all levels of seniority from junior to team leaders',
    'A leading organisation within the financial services industry are looking for a several Java Developers to join their team.',
    'called out appropriately to the developer community, and where they lead to...',
    'Mentoring, learning by doing, gaining valuable experience from relevant people',
])
def test_parse_from_sentence_en_leadership_required_not(sentence):
    assert 'LEADERSHIP_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Czech/Slovak language knowledge/possibly is essential',
    'Although team language is Czech - basic English knowledge is required',
    'Fluent English + Czech or Slovak',
])
def test_parse_from_sentence_en_czech_required(sentence):
    assert 'CZECH_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Language courses (Czech, German)',
    'English on advanced level is mandatory, Czech is optional',
    'Czech as a plus - B2 level daily communication with the team',
    'Workshops and meetings with various experts from the Czech market, internal trainings, language courses',
])
def test_parse_from_sentence_en_czech_required_not(sentence):
    assert 'CZECH_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Czech/Slovak language knowledge/possibly is essential',
    'Fluent English + Czech or Slovak',
])
def test_parse_from_sentence_en_slovak_required(sentence):
    assert 'SLOVAK_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'execute tasks independently',
    'with little supervision and under pressure',
    'Able to work with minimal supervision',
    'work independently on given tasks',
    'work autonomously on given tasks',
    'Independent working ability',
    'Independent, self-directing working style.',
    'with minimal outside supervision',
    'Self-motivated and able to operate independently',
    'Being able to work autonomous and take ownership',
    'As an engineer, you are self sufficient and well organised',
    'be self-motivated and comfortable solving problems independently',
])
def test_parse_from_sentence_en_independence_preferred(sentence):
    assert 'INDEPENDENCE_PREFERRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    "We operate Germany's largest independent payment infrastructure",
    'Augmented Analytics automates work of human analysts by developing software intelligence that autonomously produces key business insights',
    'leading the pace in autonomous driving and novel connected car applications',
])
def test_parse_from_sentence_en_independence_preferred_not(sentence):
    assert 'INDEPENDENCE_PREFERRED' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Javascript junior developer',
    'As a Junior Software Engineer you will have the following responsibilities',
    'Padawan tester',
    'Internship: JAVA DEVELOPER ',
    'Point Cloud Data Science Intern (Aug/Sept 2020 intake)',
    'Trainee E-shop Admin, students welcome',
])
def test_parse_from_sentence_en_explicitly_junior(sentence):
    assert 'EXPLICITLY_JUNIOR' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'Team 8-10 junior-senior',
    'love working in a diverse team with seniors and juniors.',
    'you will also get the chance to mentor junior developers in the team',
    'C# Software Developer - Jnr, Mid and Senior Opportunties Available',
])
def test_parse_from_sentence_en_explicitly_junior_not(sentence):
    assert 'EXPLICITLY_JUNIOR' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'It doesn’t matter that you don’t have any experiences.',
    'you’ll find a challenging entry-level position',
    'Learn a ton, whether you know a lot, or nothing about system software',
    'If you are missing some qualifications, but you are motivated.',
    'No prior work experience necessary',
    'Would you like to start your career with one of the world market leaders in medical technology',
    'experience with the development of own or school projects',
    'development under the guidance of experienced developers',
    'looking for programmers who do not necessarily have experience in professional game development',
    'We are open to applications from recent college graduates for a junior position',
    'It would be awesome, if you have already worked with these two languages but in case you have not, that is also no big deal.',
    'Doesn’t matter if you don’t know all of them – general overview and right motivation will be enough!',
    'Work or educational experience in software development',
    'guided by a senior software engineer.',
    'You are fluent in at least one programming language.',
    'Mentoring, learning by doing, gaining valuable experience from relevant people',
])
def test_parse_from_sentence_en_junior_friendly(sentence):
    assert 'JUNIOR_FRIENDLY' in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'With just a few clicks, you can apply online and start the sunny side of your career.',
])
def test_parse_from_sentence_en_junior_friendly_not(sentence):
    assert 'JUNIOR_FRIENDLY' not in get_rule_ids(parse_from_sentence(sentence, 'en'))


@pytest.mark.parametrize('sentence', [
    'from junior developer candidates we expect willingness to learn',
    'or a willingness to learn new technologies',
    'Ability and will to quickly learn new technologies and new products.',
])
def test_parse_from_sentence_en_learning_required(sentence):
    assert 'LEARNING_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'en'))
