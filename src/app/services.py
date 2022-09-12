import tempfile

from .constants import constants
from .models import (
    Program,
    Author,
    StudentMust,
    Curriculum,
    ThematicPlan,
    InternetResource,
    ThematicPlanFormLesson,
    Competence,
    CurrentControl,
    Complance,
    FinalControl,
    CriteriaEvaluationBrief,
    ContenstEvaluationTools,
    Literature,
)

from docxtpl import DocxTemplate


months_in_rus = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августф",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


def get_doc_context(program: Program):
    data = {}
    result = {"lectures": 0, "workshops": 0, "laboratory": 0, "independent_work": 0, "exam": 0}
    data["result"] = result
    data["program"] = program
    data["program"].material_technical_base = data["program"].material_technical_base.split(".")[:-1:]
    data["month"] = months_in_rus[data["program"].release_date.month]
    data["author"] = Author.objects.filter(program=program)
    split_authors_name(data)
    data["len_author"] = len(data["author"])
    data["student_must"] = StudentMust.objects.filter(program=program)
    split_student_must(data, data["student_must"])
    program_name_id = data["program"].program_name.id
    data["competence"] = Competence.objects.filter(program_name=program_name_id)
    data["curriculum"] = Curriculum.objects.filter(program_name=program_name_id).first()
    data["thematic_plan"] = ThematicPlan.objects.filter(program=program)
    data["internet_resource"] = InternetResource.objects.filter(program=program)
    data["thematic_plan_form_lesson"] = []
    for plan in data["thematic_plan"]:
        id_thematic_plan = plan.id
        thematic_plan_form_lesson = ThematicPlanFormLesson.objects.filter(thematic_plan=id_thematic_plan)
        data["thematic_plan_form_lesson"].append(thematic_plan_form_lesson)
        for form in thematic_plan_form_lesson:
            if form.lesson_form.name == "лекции":
                data["result"]["lectures"] += form.count
            if form.lesson_form.name == "практические занятия":
                data["result"]["workshops"] += form.count
            if form.lesson_form.name == "лабораторные работы":
                data["result"]["laboratory"] += form.count
            if form.lesson_form.name == "самостоятельная работа":
                data["result"]["independent_work"] += form.count
            if form.lesson_form.name == "экзамен":
                data["result"]["exam"] += form.count
        data["result"]["all_hours"] = (
            data["result"]["lectures"]
            + data["result"]["workshops"]
            + data["result"]["laboratory"]
            + data["result"]["independent_work"]
            + data["result"]["exam"]
        )
        data["result"]["contact_work"] = data["result"]["lectures"] + data["result"]["workshops"]
    data["constants"] = constants
    return {"data": data}


def generate_doc_file(program: Program):
    doc = DocxTemplate("app/templates/word/program.docx")
    context = get_doc_context(program)
    context["fos"] = fos(program)
    doc.render(context)

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        doc.save(tmp)
        return tmp.name


def fos(program: Program):
    data = {}

    complance_id = Complance.objects.filter(program=program)
    data["current_control"] = []
    for com in complance_id:
        current_contol = CurrentControl.objects.filter(complance_id=complance_id.id)
        data["current_control"].append(current_contol)

    data["final_control"] = FinalControl.objects.filter(program=program)
    data["sum"] = 0
    for score in data["current_control"]:
        data["sum"] += score.score
    data["criteria_evaluation_brief"] = []
    for crit in data["current_control"]:
        criteria_evaluation_brief = CriteriaEvaluationBrief.objects.filter(evaluation_tools=crit.evaluation_tools)
        data["criteria_evaluation_brief"].append(criteria_evaluation_brief)
    data["contenst_evaluation_tools"] = []
    for content in data["contenst_evaluation_tools"]:
        contenst_evaluation_tools = ContenstEvaluationTools.objects.filter(evaluation_tools=content.evaluation_tools)
        data["contenst_evaluation_tools"].append(contenst_evaluation_tools)

    literature = Literature.objects.filter(program=program)


# def get_fos_doc_context(fos: Fos):
#   data = {}
#     return {"data": {fos: fos}}
#


def split_student_must(data, student_must):
    data["student_must_know"] = []
    data["student_must_able"] = []
    data["student_must_master"] = []
    for must in student_must:
        if must.must_choices == StudentMust.MustChoices.know:
            data["student_must_know"].append(must)
        elif must.must_choices == StudentMust.MustChoices.can:
            data["student_must_able"].append(must)
        elif must.must_choices == StudentMust.MustChoices.own:
            data["student_must_master"].append(must)


def split_authors_name(data):
    for author in data["author"]:
        first_name, patronymic_name = author.author_initials
