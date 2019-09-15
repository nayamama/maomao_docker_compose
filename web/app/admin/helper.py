import psutil
from bokeh.models import HoverTool, FactorRange
from bokeh.plotting import figure
from bokeh.models.sources import ColumnDataSource
import datetime

from ..models import Log
from .. import db

 
def get_system_info():
    used_cpu_percent = psutil.cpu_percent() / 100
    used_disk_percent = psutil.disk_usage('/').percent / 100
    free_disk_size = psutil.disk_usage('/').free 

    return used_cpu_percent, used_disk_percent, free_disk_size


def create_line_chart(df, title, width=800, height=300):
    """
    Create a line and circle chart with name of x axis, y axis and hover tool.
    """
    # convert date object to string and factorize the month as x_axis lable
    df.date = df.date.apply(lambda x: datetime.datetime.strftime(x, '%Y-%m'))
    xdr = FactorRange(factors=df.date)

    source = ColumnDataSource(df)
    plot = figure(title=title, x_range=xdr, plot_width=800, plot_height=300)

    plot.line(x="date", y="salary", source=source, line_width=2)
    #plot.circle(x="date", y="salary", source=source, fill_color="white", size=8)
    plot.vbar(x="date", top="salary", source=source, width=0.5)

    plot.toolbar.logo = None
    plot.xaxis.axis_label = "月份"
    plot.yaxis.axis_label = "工资"

    hover = HoverTool()
    hover.tooltips=[
        ('日期', '@date'),
        ('工资', '@salary{0.00}'),
    ]

    plot.add_tools(hover)

    return plot


def add_log(user, action, target_id=None, target_table=None, status='S'):
    log = Log(date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
              action = action, 
              target_id = target_id,
              target_table = target_table,
              user = user, 
              status = status)
    try:
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
