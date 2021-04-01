{'name': 'My Hotel Company',
'summary': 'Management of an hotel ',
'description': '''All modules for the management like crm, contacts, hr''',
'author':'Maud Leleux',
'website': 'Nothing now',
"category" : "Marketing",
"version": "14.0.0",
"depends": ['base','account','website'],
"data": [
    "data/data.xml",
    "data/demo.xml",
    "security/groups.xml",
    "security/marketing_security.xml",
    "security/ir.model.access.csv",
    "views/bedroom.xml",
    "views/room.xml",
    "views/bedroom_category.xml",
    "views/account.xml",
    "views/clients.xml",
    "views/web/hotel_web.xml",
    "views/hotel.xml",
    "views/web/templates.xml"
    ],
"demo": ["demo.xml"],
"images": "my_hotel_company/static/description/icon.png"
}

