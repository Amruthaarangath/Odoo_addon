{
    'name': "Hospital",
    'description': "Hospital management",
    'application': True,
    'depends': ['base','hr'],

    'data': [
           'security/ir.model.access.csv',
           'views/patient_view.xml',
           'views/doctor_view.xml',
           'views/op_view.xml',
           'data/op_sequence.xml',
           'views/op_view.xml'
],
}