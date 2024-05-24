{
    'name': 'Estate account',
    'version': '1',
    'description': "Este es un modulo de pruebas.", 
    'application': True,
    'depends': ['estate', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_account_views.xml',
        'views/estate_account_menu.xml'
    ]
}