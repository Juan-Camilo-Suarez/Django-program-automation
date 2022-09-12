from docx2txt import process
from docx import Document

from re import DOTALL, findall
from src.app.models import *

from datetime import date


def get_date(text: str):
    data = findall(r'"..."..............20... г.', text)
    return data[0] if data else None


def get_program(text: str):
    data = findall(r"Программа дисциплины.*\n\n(.*)\n", text)
    return data[0] if data else None


def get_direction(text: str):
    data = findall(r"Направление подготовки.*: (.*)\n", text)[0].split(" - ")

    return data if data else None


def get_profile(text: str):
    data = findall(r"рофиль.* подготовки: (.*)\n", text)
    return data[0] if data else None


def get_student_qualification(text: str):
    data = findall(r"Квалификация выпускника: (.*)\n", text)
    return data[0] if data else None


def get_study_form(text: str):
    data = findall(r"Форма обучения: (.*)\n", text)
    return data[0] if data else None


def get_language(text: str):
    data = findall(r"Язык обучения: (.*)\n", text)
    return data[0] if data else None


def get_year(text: str):
    data = findall(r"Год начала обучения по образовательной программе: (\d{4})", text)
    return data[0] if data else None


def get_author(text: str):
    result_data = {}
    data = findall(r"Программу дисциплины.* разработал.(.*)\n", text)[0]
    email = findall(r"[a-z]*@[a-z]*\.[a-z]*", data)[0]

    position = findall(r"([а-я]*) ", data)[0]
    fullname = findall(r"([А-Я][а-я]* [А-Я]\.[А-Я]\.)", data)[0]
    academic_degree = findall(r"([а-я]\.[а-я]\.)", data)  # might be empty

    cath_inst = findall(r" \((.*?), (Институт.*\))", data)
    if cath_inst:
        result_data["cathedra"] = cath_inst[0][0]
        result_data["institute"] = cath_inst[0][1]
    else:
        result_data["institute"] = findall(r"\((.*)\)", data)[0]
    result_data["fullname"] = fullname
    result_data["email"] = email
    result_data["academic_degree"] = academic_degree[0] if academic_degree else None
    result_data["raw"] = data
    return result_data


def get_competences(text: str):
    data = findall(r"(\w\w-\d.?)\n\n([^\t].*)", text)
    return data


def get_discipline_knowledge(text: str):
    data = findall(r"олжен знать: (.*)олжен уметь:(.*)олжен владеть:(.*)2\. Место дисциплины", text, DOTALL)
    return data[0] if data else None


def discipline_and_time(text: str):
    data = findall(r"Данная .* включена в раздел (.*)\n\nОсваивается на (.*)", text)[0]
    return data


def get_lessons_hours(text: str):
    data = findall(
        r"Общая трудоемкость.*составляет .*\n\nКонтактная работа - (\d+) .* лекции - (\d+).* занятия - (\d+).*? работы - (\d+).* работы - (\d+)",
        text,
    )
    return data[0]


def get_themes(text: str):
    data = findall(r"((\d+)\.\n\n(.*)\n\n(\d+)\n\n(\d+)\n\n(\d+)\n\n(\d+)\n\n(\d+))", text)
    return data[0]


def get_theme_description(text: str):
    data = findall(r"(Тема \d\..*\n\n[^\d].*)", text)
    return data


def get_data_from_table(table):
    data = []
    for i, row in enumerate(table.rows):
        if i == 0 or i == 1:
            continue
        text = list(cell.text for cell in row.cells)
        data.append(text)
    return data


def get_theme_data(data: list):
    for i in range(len(data) - 1):
        row = data[i]
        yield row[1][row[1].index(".") + 2 :], row[2], row[3], row[4], row[5], row[6]


def process_file(filename: str):
    text = process(filename)
    pr_name = ProgramName.objects.create(name=get_program(text))
    number, name = get_direction(text)
    direction = Direction.objects.create(
        name=name,
        qualification=Direction.QualificationProgramme.BACHELOR
        if get_student_qualification(text).strip() == "бакалавр"
        else Direction.QualificationProgramme.MASTER,
        number=number,
    )
    profile = Profile.objects.create(name=get_profile(text), direction=direction)
    competences = []
    for competence in get_competences(text):
        c = Competence.objects.create(name=competence[1], cipher=competence[0])
        c.program_name.set([pr_name])
        competences.append(c)
    language = Program.LanguageChoices.russian if get_language(text) == "русский" else Program.LanguageChoices.english
    form_training = Program.FormTraining.full_time if get_study_form(text) else Program.FormTraining.distance
    d = date(year=int(get_year(text)), day=1, month=1)
    program = Program.objects.create(
        program_name=pr_name,
        release_date=d,
        profile=profile,
        form_training=form_training,
        language_choices=language,
        type_discipline=Program.TypeDiscipline.basic,
    )
    raw_author = get_author(text)

    if raw_author.get("academic_degree") == "к.н.":
        academic_degree = Author.AcademicDegree.k_n
    else:
        academic_degree = Author.AcademicDegree.d_n

    if "аспирант" in raw_author["raw"]:
        position = Author.Position.graduate
    elif "преподаватель" in raw_author["raw"]:
        position = Author.Position.teacher
    elif "доцент" in raw_author["raw"]:
        position = Author.Position.docent
    elif "профессор" in raw_author["raw"]:
        position = Author.Position.professor
    else:
        position = ""

    if position == Author.Position.professor:
        academic_tittle = Author.AcademicTitle.docent
    elif position == Author.Position.professor:
        academic_tittle = Author.AcademicTitle.professor
    else:
        academic_tittle = ""

    first_name = raw_author["fullname"].split()[0]
    last_name = raw_author["fullname"].split()[1].split(".")[0]
    patronymic_name = raw_author["fullname"].split()[1].split(".")[1]

    author = Author(
        academic_degree=academic_degree,
        academic_position=position,
        first_name=first_name,
        last_name=last_name,
        patronymic_name=patronymic_name,
        email=raw_author["email"],
        program=program,
        # institute=raw_author['institute'],
        cathedra=raw_author.get("cathedra") if raw_author.get("cathedra") is not None else "",
        academic_tittle=academic_tittle,
    )
    author.save()

    data = get_discipline_knowledge(text)

    if data:
        for knowledge_text in findall(r"-(.*)\n", data[0]):
            StudentMust.objects.create(program=program, text=knowledge_text, must_choices=StudentMust.MustChoices.know)
        for knowledge_text in findall(r"-(.*)\n", data[1]):
            StudentMust.objects.create(program=program, text=knowledge_text, must_choices=StudentMust.MustChoices.can)
        for knowledge_text in findall(r"-(.*)\n", data[2]):
            StudentMust.objects.create(program=program, text=knowledge_text, must_choices=StudentMust.MustChoices.own)

    f = open(filename, "rb")
    document = Document(f)
    f.close()

    table = document.tables[1]
    data = get_data_from_table(table)
    for row in get_theme_data(data):
        thematic_plan = ThematicPlan.objects.create(
            theme=row[0],
            semester_number=row[1],
            program=program,
        )
        ThematicPlanFormLesson.objects.create(
            count=row[2], thematic_plan=thematic_plan, lesson_form=LessonForm.objects.create(name="Лекции")
        )

        ThematicPlanFormLesson.objects.create(
            count=row[3],
            thematic_plan=thematic_plan,
            lesson_form=LessonForm.objects.create(name="Практические занятия"),
        )

        ThematicPlanFormLesson.objects.create(
            count=row[4], thematic_plan=thematic_plan, lesson_form=LessonForm.objects.create(name="Лабораторные работы")
        )

        ThematicPlanFormLesson.objects.create(
            count=row[5],
            thematic_plan=thematic_plan,
            lesson_form=LessonForm.objects.create(name="Самостоятаельная работа"),
        )
