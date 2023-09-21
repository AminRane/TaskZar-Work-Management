from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
from .models import Employee


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(due_date__day=day)
        d = ''
        for event in events_per_day:
            div_for_row = ''

            if event.status == 'Done':
                css_class = 'done'
                div_for_row = ' class="col-sm-auto title"'
                icon_div = '<div class = "col-sm-auto icon"><i class="bi bi-check"></i></div>'

            elif event.status == 'In Progress':
                css_class = 'in_progress'
                icon_div = '<div class = "col-sm-auto icon"></div>'
                if event.due_date - date.today() <= timedelta(days=2):
                    div_for_row = ' class="col-sm-auto"'
                    css_class = 'due-date'
                    icon_div = '<div class = "col-sm-auto icon"><i class="bi bi-clock-fill"></i></div>'
                if event.due_date < date.today():
                    div_for_row = ' class="col-sm-auto"'
                    css_class = 'past-due'
                    icon_div = '<div class = "col-sm-auto icon"><i class="material-icons">warning</i></div>'

            elif event.status == 'To Do':
                css_class = 'to_do'
                icon_div = '<div class = "col-sm-auto icon"></div>'
                if event.due_date - date.today() <= timedelta(days=2):
                    div_for_row = ' class="col-sm-auto"'
                    css_class = 'due-date'
                    icon_div = f'<div class = "col-sm-auto icon"><i class="bi bi-clock-fill"></i></div>'
                if event.due_date < date.today():
                    div_for_row = ' class="col-sm-auto"'
                    css_class = 'past-due'
                    icon_div = '<div class = "col-sm-auto icon"><i class="material-icons">warning</i></div>'

            else:
                css_class = ''
                icon_div = ''

            d += f'<li class="event {css_class}"><div class="row event-list"><div {div_for_row} data-bs-placement="auto" ' \
                 f'data-bs-container="body" ' \
                 f'data-bs-toggle="popover" data-bs-trigger="hover" data-bs-title="{event.title}" ' \
                 f'data-bs-content="Assignee: {event.assignee.full_name()}</br>Priority: {event.priority}" ' \
                 f'data-bs-html="true">{event.title[:9]}...' \
                 f'</div>{icon_div}</div></li>'

        if day != 0:
            # if day == date.today().strftime('%d'):
            #     return f"<td style='background-color:#f8f9fa;text-align:center'><span class='date' " \
            #   f"style='border-radius:16px;font-family:Roboto;font-style:bold;color:white;background-color:#6c757d'>" \
            #            f"{day}{day}</span><ul style='margin-top:5px'> {d} </ul></td>"
            # else:
            return f"<td style='background-color:#f8f9fa;text-align:center'><span class='date' " \
                f"style='font-family:Roboto;font-style:bold'>{day}" \
                f"</span><ul style='margin-top:5px'> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, employee, withyear=True):
        events = employee.task_set.filter(due_date__year=self.year, due_date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="table calendar">\n'
        cal += f'<thead class="table-light calendar" style="background-color:#212529">' \
               f'{self.formatmonthname(self.year, self.month, withyear=withyear)}</thead>\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
