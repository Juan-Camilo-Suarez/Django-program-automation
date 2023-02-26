from django.db import models


class Direction(models.Model):
    """
    Направление. Например: програмная инженерия
    """

    class QualificationProgramme(models.TextChoices):
        BACHELOR = "Бакалавриат", "BACHELOR"
        MASTER = "Магистратура", "MASTER"

    name = models.CharField(max_length=120, verbose_name="название")
    number = models.CharField(max_length=20, verbose_name="номер")
    qualification = models.CharField(
        max_length=20,
        choices=QualificationProgramme.choices,
        verbose_name="квалификация",
    )

    class Meta:
        verbose_name = "направление"
        verbose_name_plural = "направления"

    def __str__(self):
        return self.name + "-" + self.number + "-" + self.qualification


class Profile(models.Model):
    """
    Направленность (профиль) подготовки / специализация
    """

    name = models.CharField(max_length=120, verbose_name="название")
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="направления")

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return self.name


class ProgramName(models.Model):
    """
    Название програмы там где Программа дисциплины (модуля)
    """

    name = models.CharField(max_length=120, verbose_name="название")

    class Meta:
        verbose_name = "название программы"
        verbose_name_plural = "названия программ"

    def __str__(self):
        return self.name


class Competence(models.Model):
    """
    1. Перечень планируемых результатов обучения по дисциплине (модулю),
    соотнесенных с планируемыми результатами освоения ОПОП ВО
    """

    name = models.CharField(max_length=300, verbose_name="название")  # расшифровка
    cipher = models.CharField(max_length=5, verbose_name="шифр")
    program_name = models.ManyToManyField(ProgramName)

    class Meta:
        verbose_name = "компетенция"
        verbose_name_plural = "компетенции"

    def __str__(self):
        return self.name + "-" + self.cipher


class Program(models.Model):
    class LanguageChoices(models.TextChoices):
        russian = "русский", "русский"
        english = "англиский", "англиский"

    class TypeDiscipline(models.TextChoices):
        basic = "базовая", "базовая"
        variant = "вариативная", "вариативная"
        selective = "курс по выбору", "курс по выбору"

    class FormTraining(models.TextChoices):
        full_time = "очное", "очное"
        distance = "заочное", "заочное"

    release_date = models.DateField(verbose_name="дата создания")
    program_name = models.ForeignKey(ProgramName, on_delete=models.CASCADE, verbose_name="название программы")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=" профиль")
    capabilities = models.TextField(null=True, verbose_name="возможности")
    form_training = models.CharField(max_length=20, choices=FormTraining.choices, verbose_name="форма обучения")
    language_choices = models.CharField(max_length=20, choices=LanguageChoices.choices, verbose_name="язык")
    type_discipline = models.CharField(max_length=20, choices=TypeDiscipline.choices, verbose_name="тип дисциплина")
    accounting_methodological_support = models.TextField(
        null=True, verbose_name="методическое обеспечение бухгалтерского учета"
    )
    material_technical_base = models.TextField(verbose_name="материально-техническая база")

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return str(self.release_date) + "-" + self.program_name.name


class Author(models.Model):
    """
    Авторы
    """

    class AcademicDegree(models.TextChoices):
        k_n = "К.Н", "К.Н"
        d_n = "Д.Н", "Д.Н"

    class Position(models.TextChoices):
        graduate = "аспирант", "аспирант"
        teacher = "преподаватель", "преподаватель"
        docent = "доцент", "доцент"
        professor = "профессор", "профессор"

    class AcademicTitle(models.TextChoices):
        docent = "доцент", "доцент"
        professor = "профессор", "профессор"

    last_name = models.CharField(max_length=120, verbose_name="фамилия")
    first_name = models.CharField(max_length=120, verbose_name="имя")
    patronymic_name = models.CharField(max_length=120, null=True, verbose_name="отчество")
    cathedra = models.CharField(max_length=120, verbose_name="кафедра")
    institute = models.CharField(max_length=120, verbose_name="институт")
    email = models.EmailField(max_length=120, verbose_name="почта")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="программа")
    academic_degree = models.CharField(
        max_length=8,
        choices=AcademicDegree.choices,
        verbose_name="ученная степень",
    )
    academic_position = models.CharField(
        max_length=15,
        choices=Position.choices,
        verbose_name="должность",
    )
    academic_tittle = models.CharField(
        max_length=15,
        choices=AcademicTitle.choices,
        verbose_name="ученое звание",
    )

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"

    @property
    def author_initials(self):
        self.first_name = self.first_name[:1:]
        self.patronymic_name = self.patronymic_name[:1:]

        return self.first_name, self.patronymic_name

    def __str__(self):
        return self.first_name + "-" + self.patronymic_name + "-" + self.institute


class StudentMust(models.Model):
    """
    Должен знать, уметь, владеть
    """

    class MustChoices(models.TextChoices):
        know = "знать", "знать"
        can = "уметь", "уметь"
        own = "владеть", "владеть"

    text = models.TextField(verbose_name="текст")
    must_choices = models.CharField(max_length=8, choices=MustChoices.choices, verbose_name="тип текста")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="программа")

    class Meta:
        verbose_name = "Обучающийся должен"
        verbose_name_plural = "Обучающийся должен"

    def __str__(self):
        return self.must_choices


class InternetResource(models.Model):
    """
    Пункт 8. Перечень ресурсов информационно-телекоммуникационной сети "Интернет",
    необходимых для освоения дисциплины (модуля)
    """

    name = models.CharField(max_length=120, verbose_name="название")
    link = models.URLField(max_length=120, verbose_name="ссылка")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="программа")

    class Meta:
        verbose_name = "интернет ресурc"
        verbose_name_plural = "интернет ресурcы"

    def __str__(self):
        return self.name


class ThematicPlan(models.Model):
    """
    4.1 Структура и тематический план контактной и самостоятельной работы по дисциплинe (модулю) и
    4.2 Содержание дисциплины (модуля)
    """

    theme = models.CharField(max_length=120, verbose_name="тема")
    semester_number = models.IntegerField(verbose_name="семестер")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="программа")
    text = models.TextField(verbose_name="текст")

    class Meta:
        verbose_name = "тематический план"
        verbose_name_plural = "тематические планы"

    def __str__(self):
        return self.theme + "-" + str(self.semester_number)


class LessonForm(models.Model):
    """
    Форма занятия: лекции, лабораторные и т.д.
    Пункт 9. Методические указания для обучающихся по освоению дисциплины (модуля)
    """

    name = models.CharField(max_length=120, verbose_name="название")
    text = models.TextField(verbose_name="текст")

    class Meta:
        verbose_name = "форма занятия"
        verbose_name_plural = "форма занятий"

    def __str__(self):
        return self.name


class ThematicPlanFormLesson(models.Model):
    """
    4.1 Структура и тематический план контактной и самостоятельной работы по дисциплинe (модулю)
    Количество часов по теме для определенного вида занятия
    """

    count = models.IntegerField(verbose_name="количество часов")
    thematic_plan = models.ForeignKey(ThematicPlan, on_delete=models.CASCADE, verbose_name="тематический план")
    lesson_form = models.ForeignKey(LessonForm, on_delete=models.CASCADE, verbose_name="форма занятия")

    class Meta:
        verbose_name = "количество часов по темам"
        verbose_name_plural = "количество часов по темам"

    def __str__(self):
        return str(self.count)


class Curriculum(models.Model):
    """
    В каком семестре идет курс, какой тип экзамена
    """

    program_name = models.ForeignKey(ProgramName, on_delete=models.CASCADE, verbose_name="названия программа")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="профиль")
    semester_number = models.JSONField(default=list, verbose_name="семестр")
    exam = models.BooleanField(default=False, verbose_name="экзамен")
    test = models.BooleanField(default=False, verbose_name="тест")

    class Meta:
        verbose_name = "учебный план"
        verbose_name_plural = "учебные планы"

    def __str__(self):
        return self.program_name.name + "-" + self.profile.name


class CurriculumLessonForm(models.Model):
    """
    3. Объем дисциплины (модуля) в зачетных единицах с указанием количества часов,
    выделенных на контактную работу обучающихся с преподавателем (по видам учебных занятий) \
    и на самостоятельную работу обучающихся
    """

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, verbose_name="учебный план")
    count = models.IntegerField(verbose_name="количество")
    lesson_form = models.ForeignKey(LessonForm, on_delete=models.CASCADE, verbose_name="форма занятия")

    class Meta:
        verbose_name = "количество часов занятия"
        verbose_name_plural = "количество часов занятий"


class Complance(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="программа")
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, verbose_name="компетенция")

    class Meta:
        verbose_name = "Компетенция - соответствие компетенции"
        verbose_name_plural = "Компетенции - соответствие компетенциям"

    def __str__(self):
        return str(self.competence.cipher)


class AchivementIndicator(models.Model):
    class AchivementChoices(models.TextChoices):
        know = "знать", "знать"
        can = "уметь", "уметь"
        own = "владеть", "владеть"

    achivement_choices = models.CharField(
        max_length=8, choices=AchivementChoices.choices, verbose_name="Индикаторы достижения компетенции"
    )
    text = models.TextField(verbose_name="текст")
    complance = models.ForeignKey(Complance, on_delete=models.CASCADE, verbose_name="Соответствие компетенций")

    class Meta:
        verbose_name = "Компетенция - индикатор достижения компетенции"
        verbose_name_plural = "Компетенции - индикаторы достижения компетенций"

    def __str__(self):
        return str(self.text)


class CriteriaEvaluation(models.Model):
    class LevelChoices(models.TextChoices):
        excelent = "отлично", "отлично"
        fine = "хорошо", "хорошо"
        satisfactory = "удовлетворительно", "удовлетворительно"
        unsatisfactory = "неудовлетворительно", "неудовлетворительно"

    class AchivementChoices(models.TextChoices):
        know = "знать", "знать"
        can = "уметь", "уметь"
        own = "владеть", "владеть"

    class Meta:
        verbose_name = "Компетенция - критерий оценивания"
        verbose_name_plural = "Компетенции - критерии оценивания"

    complance = models.ForeignKey(Complance, on_delete=models.CASCADE, verbose_name="Соответствие компетенций")
    level_choices = models.CharField(max_length=19, choices=LevelChoices.choices, verbose_name="Оценка")
    text = models.TextField(verbose_name="текст")
    type = models.CharField(
        max_length=19, choices=AchivementChoices.choices, verbose_name="Индикаторы достижения компетенции"
    )


class EvaluationTools(models.Model):
    order_conduct = models.TextField(verbose_name="порядок проведения")

    class Meta:
        verbose_name = "Оценочное средство - порядок проведения"
        verbose_name_plural = "Оценочное средство - порядки проведения"

    def __str__(self):
        return str(self.order_conduct)


class CurrentControl(models.Model):
    complance = models.ForeignKey(Complance, on_delete=models.CASCADE, verbose_name="Соответствие компетенций")
    name = models.CharField(max_length=120, verbose_name="название")
    score = models.IntegerField(verbose_name="количество баллов")
    evaluation_tools = models.ForeignKey(EvaluationTools, on_delete=models.CASCADE, verbose_name="порядок проведения")

    class Meta:
        verbose_name = "Оценочное средство - текущий контроль"
        verbose_name_plural = "Оценочное средство - текущие контроли"

    def __str__(self):
        return str(self.name)


class FinalControl(models.Model):
    class ExamChoices(models.TextChoices):
        exam = "экзамен", "экзамен"
        test = "зачет", "зачет"

    exam_choices = models.CharField(max_length=8, choices=ExamChoices.choices, verbose_name="тип экзамена")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="программа")
    text = models.TextField(verbose_name="текст")
    semester = models.IntegerField(verbose_name="номер семестра")
    evaluation_tools = models.ForeignKey(EvaluationTools, on_delete=models.CASCADE, verbose_name="порядок проведения")

    class Meta:
        verbose_name = "Оценочное средство - промежуточная аттестация"
        verbose_name_plural = "Оценочное средство - промежуточная аттестация"

    def __str__(self):
        return str(self.program.program_name) + " - " + str(self.exam_choices) + " - " + str(self.semester)


class ContenstEvaluationTools(models.Model):
    text = models.TextField(verbose_name="текст")
    image = models.ImageField(null=True, verbose_name="картинка")
    evaluation_tools = models.ForeignKey(EvaluationTools, on_delete=models.CASCADE, verbose_name="порядок проведения")

    class Meta:
        verbose_name = "Оценочное средство - содержание оценочного средства"
        verbose_name_plural = "Оценочные средства - содержание оценочного средства"

    def __str__(self):
        return str(self.text)


class CriteriaEvaluationBrief(models.Model):
    class LevelChoices(models.TextChoices):
        excelent = "отлично", "отлично"
        fine = "хорошо", "хорошо"
        satisfactory = "удовлетворительно", "удовлетворительно"
        unsatisfactory = "неудовлетворительно", "неудовлетворительно"

    text = models.TextField(verbose_name="текст")
    evaluation_tools = models.ForeignKey(EvaluationTools, on_delete=models.CASCADE, verbose_name="порядок проведения")
    level_type = models.CharField(max_length=19, choices=LevelChoices.choices, verbose_name="оценка")

    class Meta:
        verbose_name = "Оценочное средство - критерий оценивания"
        verbose_name_plural = "Оценочные средства - критерии оценивания"

    def __str__(self):
        return str(self.text)


class Literature(models.Model):
    class LiterChoices(models.TextChoices):
        base = "основная", "основная"
        additional = "дополнительная", "дополнительная"

    text = models.TextField(verbose_name="текст")
    literature_type = models.CharField(max_length=14, choices=LiterChoices.choices, verbose_name="литература")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="программа")

    class Meta:
        verbose_name = "литература"
        verbose_name_plural = "литература"

    def __str__(self):
        return str(self.text)
