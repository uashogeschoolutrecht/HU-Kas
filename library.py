HUKAS_TABLES = {
    'BehandelendePartijs': [
        'Files'
    ],
    'Casess': [
        'File',
        'RequesterType'
    ],
    'Decisions': [
        'File',
        'StatusChanges'
    ],
    'RequesterTypes': [
        'Casess',
        'StatusChanges'
    ],
    'Files': [
        'Cases',
        'Decisions',
        'Status',
        'BehandelendePartij',
        'StatusChanges',
        'Behandelaar'
    ],
    'StatusChanges': [
        'File',
        'Decision',
        'Status from',
        'Status_to'
    ],
    'Statuss': [
        'Files',
        'StatusChanges',
        'StatusChanges_2'
    ],
}
