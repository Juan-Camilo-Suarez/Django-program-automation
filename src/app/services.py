import tempfile

from htmldocx import HtmlToDocx

from app.constants import constants
from app.models import (
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
    EvaluationTools,
    CriteriaEvaluationBrief,
    ContenstEvaluationTools,
    Literature,
    CriteriaEvaluation,
    AchivementIndicator,
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
    context.update(fos(program, context))
    doc.render(context)

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        doc.save(tmp)
        return tmp.name


def fos(program: Program, data):
    complance_id = Complance.objects.filter(program=program)
    data["data"]["current_control"] = []
    for com in complance_id:
        current_contol = CurrentControl.objects.filter(complance_id=com.id)
        for i in range(len(current_contol)):
            data["data"]["current_control"].append(current_contol[i])

    data["data"]["final_control"] = FinalControl.objects.filter(program=program)
    data["data"]["sum"] = 0
    for cur in data["data"]["current_control"]:
        data["data"]["sum"] += cur.score

    data["data"]["criteria_evaluation_brief"] = []
    for crit in data["data"]["current_control"]:
        criteria_evaluation_brief = CriteriaEvaluationBrief.objects.filter(evaluation_tools=crit.evaluation_tools)
        for i in range(len(criteria_evaluation_brief)):
            data["data"]["criteria_evaluation_brief"].append(criteria_evaluation_brief[i])

    data["data"]["contenst_evaluation_tools"] = []
    for con in data["data"]["current_control"]:
        contenst_evaluation_tools = ContenstEvaluationTools.objects.filter(evaluation_tools=con.evaluation_tools)
        for i in range(len(contenst_evaluation_tools)):
            data["data"]["contenst_evaluation_tools"].append(contenst_evaluation_tools[i])

    data["data"]["literature"] = Literature.objects.filter(program=program)

    data["data"]["criteria_evaluation"] = []
    for com in complance_id:
        criteria_evaluation = CriteriaEvaluation.objects.filter(complance_id=com.id)
        for i in range(len(criteria_evaluation)):
            data["data"]["criteria_evaluation"].append(criteria_evaluation[i])

    data["data"]["achivement_indicator"] = []
    for com in complance_id:
        achivement_indicator = AchivementIndicator.objects.filter(complance_id=com.id)
        for i in range(len(achivement_indicator)):
            data["data"]["achivement_indicator"].append(achivement_indicator[i])

    return data


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
