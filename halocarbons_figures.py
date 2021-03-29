#! /usr/bin/env python

import pandas as pd
import altair as alt


class HATS_Figures:

    def multi_instrument_dataframe(self, list_dfs):
        """ Create a synced dataframe from a list of measurement program
            dataframs, list_dfs """

        dfs = []

        # iterate through program dataframes for mf and sd
        for df in list_dfs:
            if df is None:
                print('Blank dataframe in list. Skipping.')
                continue
            if df.shape[0] == 0:
                print('Blank dataframe in list. Skipping.')
                continue
            df = df.reset_index()
            df = df[['date', 'site', 'mf', 'sd', 'lat', 'lon', 'elev']]
            df['prog'] = df.attrs['program']
            dfs.append(df)

        # combine into one dataframe
        df = pd.concat(dfs)
        df = df.set_index('date').sort_index()

        # use attrs for meta data. In this case the gas name.
        df.attrs['gas'] = list_dfs[0].attrs['gas']

        return df

    def mf_units(self, gas):
        units = '(ppb)' if gas == 'N2O' else '(ppt)'
        return units

    def multi_station_figure(self, prog_df, errorbars=True):
        """ Creates an interactive figure with data from all sample locations
            for a measurement program. prog_df is a pandas dataframe. """

        # return if dataframe is empty
        if prog_df is None:
            return
        if prog_df.shape[0] == 0:
            return

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

        # return if dataframe is empty
        if prog_df is None:
            return
        if prog_df.shape[0] == 0:
            return

        # upper and lower sd values for error bands
        site = site.lower()
        gas = prog_df.attrs['gas']
        df = prog_df.loc[prog_df.site == site].reset_index()

        # no data for site
        if df.shape[0] == 0:
            return

        if errorbars:
            df.loc[:, 'lower'] = df.mf - df.sd
            df.loc[:, 'upper'] = df.mf + df.sd

        palette = alt.Scale(domain=['msd', 'cats', 'otto', 'pr1'],
                      range=['teal', 'darkred', 'orange', 'black', '#33a02c'])
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
            color=alt.Color('prog:O', scale=palette),
            opacity=alt.condition(selection, alt.value(0.3), alt.value(0.0))
        )

        # Clickable legend
        clickable_legend = alt.Chart(df).mark_circle(size=150).encode(
            y=alt.Y('prog:O', title='Program',
                    axis=alt.Axis(labelFontSize=12, titleFontSize=16)),
            color=alt.condition(selection, 'prog:O', alt.value('lightgray'),
                                scale=palette)
        ).add_selection(selection)

        if errorbars:
            ((chart + eb) | clickable_legend).display()
        else:
            ((chart) | clickable_legend).display()

    def return_ratios(self, df_org, prog0, prog1):
        """ Returns a long data from of ratios between prog0 and prog1.
            df_org is a multi_instrument_dataframe
            prog0 and prog1 are strings that match the prog column in df_org """

        # find the sites that are in common to both prog0 and prog1
        s0 = df_org.loc[df_org.prog == prog0].site.unique()
        s1 = df_org.loc[df_org.prog == prog1].site.unique()
        common_sites = set(s0) & set(s1)

        dfs = []
        for site in common_sites:
            sdf = df_org.loc[df_org.site == site].copy()
            sdf['ratio'] = sdf.loc[sdf.prog == prog0].mf / sdf.loc[sdf.prog == prog1].mf
            sdf.drop(['mf', 'sd', 'lat', 'lon', 'elev', 'prog'], axis=1, inplace=True)
            dfs.append(sdf)

        # no common_sites found, return an empty dataframe
        if len(dfs) == 0:
            return pd.DataFrame()

        sdf = pd.concat(dfs).dropna()
        return sdf

    def site_ratios_figure(self, df0, df1):
        """ Generates a figure of ratios for each site.
            df0 and df1 are Pandas data frames returned from the halocarbons_loader
            method. """

        if df0 is None or df1 is None:
            return

        gas = df0.attrs['gas']
        prog0 = df0.attrs['program']
        prog1 = df1.attrs['program']

        measurements = self.multi_instrument_dataframe([df0, df1])
        df = self.return_ratios(measurements, prog0, prog1)
        mm = df.groupby('date').mean()

        line = alt.Chart(df.reset_index()).mark_line().encode(
            x=alt.X('date:T',
                    axis=alt.Axis(title='Date',
                                  labelAngle=-60, format=("%b %Y"),
                                  labelFontSize=12, titleFontSize=16)),
            y=alt.Y('ratio', scale=alt.Scale(zero=False),
                    axis=alt.Axis(title=f'{gas} {prog0} / {prog1} Ratio',
                                  labelFontSize=12, titleFontSize=16)),
            color=alt.Color('site', legend=None),
            tooltip=['ratio:Q', 'site:N']
        )

        mm_line = alt.Chart(mm.reset_index()).mark_line(size=5).encode(
            x='date:T',
            y='ratio'
        )

        points = line.mark_point(filled=True, size=100).encode(
            color='site',
            shape='site',
        )

        alt.layer(
            line,
            mm_line,
            points
        ).resolve_scale(
            color='independent',
            shape='independent'
        ).properties(
            height=400, width=700
        ).interactive().display()
