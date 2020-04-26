import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


# -----=====***** Party leaders *****=====-----

# -- f u n c t i o n s -- #

def transform_date_string_to_datetime_object(entry):
    '''
    :param string: format 'YYYY-MM-DD'
    :return: datetime
    '''
    if isinstance(entry, str):
        return datetime.strptime(entry, '%Y-%m-%d')
    else:
        return entry

# -------- d a t a   p r e p a r a t i o n -------- #

# loading data
party_leaders = pd.read_csv('swedish_party_leaders.csv', header=0)
# filling empty dates with todays date (death dates, left office dates)
party_leaders[['death_date',
               'assumed_office',
               'left_office']] = party_leaders[['death_date',
                                                'assumed_office',
                                                'left_office']].fillna(datetime.today())
# transforming date strings to datetime objects
party_leaders['birth_date'] = party_leaders.apply(lambda row: \
                              transform_date_string_to_datetime_object(row['birth_date']), axis = 1)
party_leaders['death_date'] = party_leaders.apply(lambda row: \
                              transform_date_string_to_datetime_object(row['death_date']), axis = 1)
party_leaders['left_office'] = party_leaders.apply(lambda row: \
                              transform_date_string_to_datetime_object(row['left_office']), axis = 1)
party_leaders['assumed_office'] = party_leaders.apply(lambda row: \
                              transform_date_string_to_datetime_object(row['assumed_office']), axis = 1)
# calculating age when party leader assumed office and time in office in years
party_leaders['age_when_assumed_office'] = party_leaders.apply(lambda row: \
                                           relativedelta(row['assumed_office'],
                                                         row['birth_date']).years,
                                           axis = 1)
party_leaders['years_in_office'] = party_leaders.apply(lambda row: \
                                          np.round((relativedelta(row['left_office'],
                                                         row['assumed_office']).years * 12 + \
                                           relativedelta(row['left_office'],
                                                         row['assumed_office']).months) / 12, 2),
                                           axis = 1)
# concatenate first name and surname
party_leaders['full_name'] = party_leaders.apply(lambda row: row['name'] + ' ' + row['surname'],
                                                 axis = 1)

# concatenate full name and years in office
party_leaders['full_name_years_in_office'] = party_leaders.apply(\
                                            lambda row: row['full_name'] + \
                                                        ' (' + str(row['assumed_office'].year) + \
                                                         ' - ' + str(row['left_office'].year) + ')' ,
                                                 axis = 1)

# order by political affiliation (left-wing to right-wing)
party_leaders['party_abr'] = pd.Categorical(party_leaders['party_abr'],
                                            ['V', 'S', 'Mp', 'C', 'L', 'M', 'Kd', 'Sd' ])
party_leaders.sort_values('party_abr', inplace = True)

# --- p l o t t i n g --- #
fig = px.scatter(party_leaders,
                 title='Svenska partiledare genom århundradena',
                 x='age_when_assumed_office',
                 y='years_in_office',
                 hover_name='full_name_years_in_office',
                 color='party_abr',
                 color_discrete_map={'L': '#99ccff',
                                     'M': '#0066ff',
                                     'S': '#ff3300',
                                     'Mp': '#408000',
                                     'Kd': '#000099',
                                     'C': '#8cff66',
                                     'V': '#990000',
                                     'Sd' : '#ffff00'
                                     },
                 #symbol='sex',
                 #symbol_map={'m':'circle',
                 #            'k':'diamond'},
                 labels={'age_when_assumed_office':u'Ålder vid tillträde',
                         'years_in_office':'Antal år i ämbetet',
                         'party_abr':'Parti'}
                 )
fig.update_traces(marker=dict(size=15,
                              symbol= 'circle',
                              line=dict(width=2,
                                        color='DarkSlateGrey'),
                              opacity = 0.95),
                  selector=dict(mode='markers')
                  )

fig.show()