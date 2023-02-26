from django.contrib import admin
from django.http import FileResponse
from nested_admin.nested import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from . import forms

from .models import (
    Program,
    Direction,
    Profile,
    ProgramName,
    Competence,
    StudentMust,
    ThematicPlanFormLesson,
    ThematicPlan,
    InternetResource,
    Curriculum,
    LessonForm,
    CurriculumLessonForm,
    Author,
    AchivementIndicator,
    Complance,
    CriteriaEvaluation,
    CurrentControl,
    FinalControl,
    EvaluationTools,
    ContenstEvaluationTools,
    CriteriaEvaluationBrief,
    Literature,
)
from .services import generate_doc_file


# @admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")
    list_display = (
        "last_name",
        "first_name",
        "cathedra",
        "institute",
        "email",
        "academic_degree",
        "academic_position",
        "academic_tittle",
    )
    list_filter = (
        "cathedra",
        "institute",
        "academic_tittle",
    )

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class InternetResourceAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "link",
    )

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class DirectionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "number",
        "qualification",
    )
    list_filter = (
        "number",
        "qualification",
    )

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class CompetenceInline(admin.TabularInline):
    model = Competence

    extra = 0


class ProgramNameAdmin(admin.ModelAdmin):
    # inlines = [CompetenceInline]
    search_fields = ("name",)
    list_display = ("name",)


class CompetenceAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "cipher",
    )
    list_display = (
        "name",
        "cipher",
    )
    list_filter = ("cipher",)

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class StudentMustAdmin(admin.ModelAdmin):
    search_fields = ("text_choices",)
    list_display = (
        "text",
        "text_choices",
    )
    list_filter = ("text_choices",)

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class InlineCurriculumLessonForm(NestedTabularInline):
    model = CurriculumLessonForm

    extra = 0


class InlineContenstEvaluationTools(NestedTabularInline):
    model = CurriculumLessonForm

    extra = 0


class InlineCurriculum(NestedStackedInline):
    model = Curriculum
    inlines = [
        InlineCurriculumLessonForm,
    ]
    show_change_link = True

    extra = 0


class ProfileAdmin(NestedModelAdmin):
    inlines = [InlineCurriculum]
    search_fields = ("name", "direction")
    list_display = (
        "name",
        "direction",
    )
    list_filter = ("direction",)

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class ThematicPlanFormLessonAdmin(admin.ModelAdmin):
    list_display = ("count",)
    list_filter = ("count",)

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class LessonFormAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "text",
    )
    list_filter = ("name",)

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class CurriculumLessonFormAdmin(admin.ModelAdmin):
    search_fields = ("lesson_form",)
    list_display = (
        "count",
        "lesson_form",
    )

    list_filter = ("lesson_form",)

    class Media:
        css = {"all": ("/templates/css/admin-extra.css ",)}


class CurriculumAdmin(admin.ModelAdmin):
    form = forms.CurricilumForm


class InlineProgramName(NestedStackedInline):
    model = ProgramName

    extra = 0


class InlineInternetResource(NestedStackedInline):
    model = InternetResource

    extra = 0


class InlineStudentMust(NestedTabularInline):
    model = StudentMust

    extra = 0


class InlineAuthor(NestedStackedInline):
    model = Author

    extra = 0


class InlineThematicPlanFormLesson(NestedTabularInline):
    model = ThematicPlanFormLesson
    show_change_link = True

    extra = 0


class InlineThematicPlan(NestedStackedInline):
    model = ThematicPlan
    inlines = [
        InlineThematicPlanFormLesson,
    ]
    show_change_link = True

    extra = 0


class InlineAchivementIndicator(NestedStackedInline):
    model = AchivementIndicator

    extra = 0


class InlineCriteriaEvaluation(NestedStackedInline):
    model = CriteriaEvaluation

    extra = 0


class InlineCurrentControl(NestedTabularInline):
    model = CurrentControl
    extra = 0


class InlineFinalControl(NestedTabularInline):
    model = FinalControl
    extra = 0


class ThematicPlanAdmin(NestedModelAdmin):
    inlines = [InlineThematicPlanFormLesson]
    search_fields = ("theme", "semester_number")
    list_display = ("theme", "semester_number")
    list_filter = ("semester_number",)

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class ProgramAdmin(NestedModelAdmin):
    inlines = [InlineThematicPlan, InlineAuthor, InlineStudentMust, InlineInternetResource]
    search_fields = ("program_name",)
    list_display = (
        "program_name",
        "release_date",
        "profile",
        "capabilities",
        "language_choices",
        "type_discipline",
    )
    list_filter = (
        "program_name",
        "release_date",
        "profile",
        "capabilities",
        "language_choices",
        "type_discipline",
    )
    change_form_template = "web/admin/site_edit.html"

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if "_print_site" in request.POST:
            program = Program.objects.get(id=object_id)
            a = generate_doc_file(program)
            return FileResponse(open(a, "rb"), filename="program.docx", content_type="application/msword")

        return super(ProgramAdmin, self).changeform_view(
            request,
            object_id,
            form_url,
            extra_context,
        )

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class AchivementIndicatorAdmin(admin.ModelAdmin):
    # inlines = [CompetenceInline]
    search_fields = ("text",)
    list_display = ("complance", "text", "achivement_choices")


class ComplanceAdmin(admin.ModelAdmin):
    fields = ("program", "competence")


class CriteriaEvaluationAdmin(NestedModelAdmin):
    # inlines = [InlineThematicPlan, InlineAuthor, InlineStudentMust, InlineInternetResource]
    search_fields = ("program_name",)
    list_display = (
        "complance",
        "level_choices",
        "text",
        "type",
    )
    list_filter = (
        "complance",
        "level_choices",
        "text",
        "type",
    )
    change_form_template = "web/admin/site_edit.html"

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class EvaluationToolsAdmin(admin.ModelAdmin):
    search_fields = ("order_conduct",)
    list_display = ("order_conduct",)
    list_filter = ("order_conduct",)

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class CurrentControlAdmin(admin.ModelAdmin):
    search_fields = ("evaluation_tools",)
    list_display = (
        "name",
        "score",
        "evaluation_tools",
    )

    list_filter = ("evaluation_tools",)

    class Media:
        css = {"all": ("/templates/css/admin-extra.css ",)}


class FinalControlAdmin(admin.ModelAdmin):
    search_fields = ("evaluation_tools",)
    list_display = (
        "program",
        "text",
        "semester",
    )

    list_filter = ("evaluation_tools",)

    class Media:
        css = {"all": ("/templates/css/admin-extra.css ",)}


class ContenstEvaluationToolsAdmin(admin.ModelAdmin):
    search_fields = ("evaluation_tools",)
    list_display = (
        "text",
        "image",
        "evaluation_tools",
    )

    list_filter = ("evaluation_tools",)

    class Media:
        css = {"all": ("/templates/css/admin-extra.css ",)}


class CriteriaEvaluationBriefAdmin(admin.ModelAdmin):
    search_fields = ("text",)
    list_display = (
        "text",
        "evaluation_tools",
        "level_type",
    )
    list_filter = (
        "evaluation_tools",
        "level_type",
    )

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


class LiteratureAdmin(admin.ModelAdmin):
    search_fields = ("text",)
    list_display = (
        "text",
        "program",
        "literature_type",
    )
    list_filter = (
        "program",
        "literature_type",
    )

    class Media:
        css = {"all": ("/static/css/admin-extra.css ",)}


admin.site.register(Curriculum, CurriculumAdmin)

admin.site.register(Literature, LiteratureAdmin)
admin.site.register(CriteriaEvaluationBrief, CriteriaEvaluationBriefAdmin)
admin.site.register(ContenstEvaluationTools, ContenstEvaluationToolsAdmin)
admin.site.register(FinalControl, FinalControlAdmin)
admin.site.register(CurrentControl, CurrentControlAdmin)
admin.site.register(CriteriaEvaluation, CriteriaEvaluationAdmin)
admin.site.register(EvaluationTools, EvaluationToolsAdmin)
admin.site.register(Complance, ComplanceAdmin)
admin.site.register(AchivementIndicator, AchivementIndicatorAdmin)

# admin.site.register(Author, AuthorAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProgramName, ProgramNameAdmin)
admin.site.register(Competence, CompetenceAdmin)
# admin.site.register(StudentMust, StudentMustAdmin)
# admin.site.register(ThematicPlanFormLesson, ThematicPlanFormLessonAdmin)
# admin.site.register(ThematicPlan, ThematicPlanAdmin)
# admin.site.register(InternetResource, InternetResourceAdmin)
admin.site.register(LessonForm, LessonFormAdmin)
admin.site.register(CurriculumLessonForm, CurriculumLessonFormAdmin)
admin.site.register(Program, ProgramAdmin)
