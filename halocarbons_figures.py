#! /usr/bin/env python

import pandas as pd
import altair as alt


class HATS_figures:

    def mf_units(self, gas):
        units = '(ppb)' if gas == 'N2O' else '(ppt)'
        return units

    def multi_station_figure(self, prog_df, errorbars=True):
        """ Creates an interactive figure with data from all sample locations
            for a measurement program. prog_df is a pandas dataframe. """

        # upper and lower sd values for error bands
        df = prog_df.reset_index().copy()
        gas = prog_df.attrs['gas']
        prog = prog_df.attrs['program']

        if errorbars:
            df.loc[:, 'lower'] = df.mf - df.sd
            df.loc[:, 'upper'] = df.mf + df.sd

        color_scheme = 'turbo'
        selection = alt.selection_multi(encodings=['color'])

        # main figure
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('date:T',
                    axis=alt.Axis(title='Date',
                                  labelAngle=-60, format=("%b %Y"),
                                  labelFontSize=12, titleFontSize=16)),
            y=alt.Y('mf', scale=alt.Scale(zero=False),
                    title=f'mole fraction {self.mf_units(gas)}',
                    axis=alt.Axis(labelFontSize=12, titleFontSize=16)),
            color=alt.Color('site:O',
                            sort=alt.EncodingSortField('lat', op='mean', order='descending'),
                            legend=None,
                            scale=alt.Scale(scheme=color_scheme)),
            tooltip=['mf:Q', 'sd:Q', 'site:N'],
            opacity=alt.condition(selection, alt.value(1.0), alt.value(0.0))
        ).properties(
            height=400, width=600,
            title=f'{prog} {gas}'
        ).add_selection(
            selection
        ).interactive()

        # error bar bands
        eb = alt.Chart(df).mark_area(
            opacity=0.2
        ).encode(
            x=alt.X('date'),
            y=alt.Y('lower'),
            y2=alt.Y2('upper'),
            color=alt.Color('site:O',
                            sort=alt.EncodingSortField('lat', op='mean', order='descending'),
                            legend=None,
                            scale=alt.Scale(scheme=color_scheme)),
            opacity=alt.condition(selection, alt.value(0.3), alt.value(0.0))
        )

        # Clickable legend
        clickable_legend = alt.Chart(df).mark_circle(size=150).encode(
            y=alt.Y('site:O', title='Site Code',
                    axis=alt.Axis(labelFontSize=12, titleFontSize=16),
                    sort=alt.EncodingSortField('lat', op='mean', order='descending')),
            color=alt.condition(selection, 'site:O', alt.value('lightgray'),
                                legend=None,
                                sort=alt.EncodingSortField('lat', op='mean', order='descending'),
                                scale=alt.Scale(scheme=color_scheme))
        ).add_selection(selection)

        if errorbars:
            ((chart + eb) | clickable_legend).display()
        else:
            ((chart) | clickable_legend).display()

    def multi_program_figure(self, site, prog_df, errorbars=True):
        """ Creates an interactive figure with data from all sampling programs
            at a single station (site). prog_df is a pandas dataframe. """

        # upper and lower sd values for error bands
        site = site.lower()
        gas = prog_df.attrs['gas']
        df = prog_df.loc[prog_df.site == site].reset_index()

        if errorbars:
            df.loc[:, 'lower'] = df.mf - df.sd
            df.loc[:, 'upper'] = df.mf + df.sd

        palette = alt.Scale(domain=['msd', 'cats', 'otto', 'pr1'],
                      range=['teal', 'darkred', 'orange', 'darkslategray', 'black'])
        selection = alt.selection_multi(encodings=['color'])

        # main figure
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('date:T',
                    axis=alt.Axis(title='Date',
                        labelAngle=-60, format=("%b %Y"),
                        labelFontSize=12, titleFontSize=16)),
            y=alt.Y('mf', scale=alt.Scale(zero=False),
                    title=f'{gas} mole fraction {self.mf_units(gas)}',
                    axis=alt.Axis(labelFontSize=12, titleFontSize=16)),
            color=alt.Color('prog:O',
                            legend=None,
                            scale=palette),
            tooltip=['mf:Q', 'sd:Q', 'prog:N'],
            opacity=alt.condition(selection, alt.value(1.0), alt.value(0.0))
        ).properties(
            height=400, width=600,
            title=f'{site.upper()} {gas}'
        ).add_selection(
            selection
        ).interactive()

        # error bar bands
        eb = alt.Chart(df).mark_area(
            opacity=0.3
        ).encode(
            x=alt.X('date'),
            y=alt.Y('lower'),
            y2=alt.Y2('upper'),
            color=alt.Color('prog:O',
                            legend=None,
                            scale=palette),
            opacity=alt.condition(selection, alt.value(0.3), alt.value(0.0))
        )

        # Clickable legend
        clickable_legend = alt.Chart(df).mark_circle(size=150).encode(
            y=alt.Y('prog:O', title='Program',
                    axis=alt.Axis(labelFontSize=12, titleFontSize=16)),
            color=alt.condition(selection, 'prog:O', alt.value('lightgray'),
                                legend=None,
                                scale=palette)
        ).add_selection(selection)

        if errorbars:
            ((chart + eb) | clickable_legend).display()
        else:
            ((chart) | clickable_legend).display()
