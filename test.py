# input
Raw_Data = """
008
Intro to CS is the best course ever
2021-09-01

Ponce,Marcelo
Tafliovich,Anya Y.

We present clear evidence that Introduction to
Computer Science is the best course.
END
031
Calculus is the best course ever

2021-09-02
Breuss,Nataliya

We discuss the reasons why Calculus I
is the best course.
END
067
Discrete Mathematics is the best course ever
2021-09-02
2021-10-01
Pancer,Richard
Bretscher,Anna

We explain why Discrete Mathematics is the best course of all times.
END
827
University of Toronto is the best university
2021-08-20
2021-10-02
Ponce,Marcelo
Bretscher,Anna
Tafliovich,Anya Y.

We show a formal proof that the University of
Toronto is the best university.
END
042

2021-05-04
2021-05-05

This is a very strange article with no title
and no authors.
END
"""

EXAMPLE_ARXIV = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}

output = {'008': {'identifier': '008', 'title': 'Intro to CS is the best course ever', 'created': '2021-09-01',
                  'modified': None, 'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
                  'abstract': ' We present clear evidence that Introduction to Computer Science is the best course.'},
          '031': {'identifier': '031', 'title': 'Calculus is the best course ever', 'created': None,
                  'modified': '2021-09-02', 'authors': ['Breuss', 'Nataliya'],
                  'abstract': ' We discuss the reasons why Calculus I is the best course.'},
          '067': {'identifier': '067', 'title': 'Discrete Mathematics is the best course ever', 'created': '2021-09-02',
                  'modified': '2021-10-01', 'authors': [('Pancer', 'Richard'), ('Bretscher', 'Anna')],
                  'abstract': '  We explain why Discrete Mathematics is the best course of all times.'},
          '827': {'identifier': '827', 'title': 'University of Toronto is the best university', 'created': '2021-08-20',
                  'modified': '2021-10-02',
                  'authors': [('Ponce', 'Marcelo'), ('Bretscher', 'Anna'), ('Tafliovich', 'Anya Y.')],
                  'abstract': ' We show a formal proof that the University of Toronto is the best university.'},
          '042': {'identifier': '042', 'title': None, 'created': '2021-05-04', 'modified': '2021-05-05', 'authors': [],
                  'abstract': ' This is a very strange article with no title and no authors.'}}


def return_none(text):
    if text == '':
        return None
    else:
        return text


def listToString(s):
    str1 = ""
    for ele in s:
        str1 = str1 + ' ' + ele
    return str1


def authors_tuple_list(list):
    temp_auth = [i for i in list if i]
    authors = []
    for i in temp_auth:
        if len(temp_auth) >= 2:
            auth_list = [x for x in i.split(',') if x]
            authors.append(tuple(i for i in auth_list))
        else:
            authors = (i.split(','))
    return authors


def read_arxiv_file(TextIO):
    temp_list = TextIO.split('END')
    ARXIV = {}
    for char in temp_list:
        if char == '\n':
            continue
        temp_char = char.split('\n')
        ARXIV[temp_char[1]] = {
            'identifier': return_none(temp_char[1]),
            'title': return_none(temp_char[2]),
            'created': return_none(temp_char[3]),
            'modified': return_none(temp_char[4]),
            'authors': authors_tuple_list(temp_char[5:-3]),
            'abstract': return_none(listToString(temp_char[-3:-1]))}
    if EXAMPLE_ARXIV == ARXIV:
        print('ok')
    return ARXIV


print(read_arxiv_file(Raw_Data))
# read_arxiv_file(Raw_Data)
