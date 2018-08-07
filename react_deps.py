#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 10:09:55 2018

@author: keenanszulik
"""

"""
react deps

"""

import pandas as pd

proj = pd.read_csv('/Users/keenanszulik/Documents/libraries_2/projects_2.csv')
npm = proj.loc[proj['Platform'] == 'NPM']

deps = pd.read_csv('/Users/keenanszulik/Documents/react_deps.csv')

deps = deps[['packages']]

d_final = []
for d in deps['packages']:
    if '@' in d:
        char = d.find('@')
        d_final.append(d[:char])
    else:
        d_final.append(d)
        
deps['Project'] = d_final

deps = deps.merge(right = npm[['Name','Homepage URL','Repository URL']], left_on = 'Project', right_on = 'Name', how = 'inner')

counter = 0
for url in deps['Repository URL']:
    try:
        if 'facebook' in url:
            counter +=1
        else:
            pass
    except TypeError:
        pass

deps_fb = deps.dropna()
fb = deps_fb[deps_fb['Repository URL'].str.contains('facebook')]
deps_fb['Repo Name'] = [i.replace('https://github.com/','') for i in deps_fb['Repository URL']]

deps_export = deps_fb[['Repo Name']]
deps_export = deps_export.drop_duplicates().reset_index(drop=True)

deps_export.to_csv('/Users/keenanszulik/Documents/bigquery_react_deps.csv')

lics = proj[['Name','Platform','Licenses','Dependent Repositories Count']].dropna()
agpl = lics[lics['Licenses'].str.contains('AGPL')]
agpl = agpl.sort_values('Dependent Repositories Count', ascending = False)