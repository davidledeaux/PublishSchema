import datetime
import requests
from operator import itemgetter

# Variables to set
#########################
user=''
password=''
workspace_oid = 
include_custom_fields = True
##########################

css = """
table,tr,th,td { border: 1px solid; border-collapse: collapse; }
td,th { padding: 5px; }
tr:nth-child(even) { background-color: #dddddd; }
.sidenav {
  height: 100%; /* Full-height: remove this if you want "auto" height */
  width: 160px; /* Set the width of the sidebar */
  position: fixed; /* Fixed Sidebar (stay in place on scroll) */
  z-index: 1; /* Stay on top */
  top: 0; /* Stay at the top */
  left: 0;
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 20px;
}
.sidenav a {
  text-decoration: none;
  display: block;
}
.sidenav a:hover {
  color: #212121;
}
.main {
  margin-left: 160px; /* Same as the width of the sidebar */
  padding: 0px 10px;
}
@media screen and (max-height: 450px) {
  .sidenav {padding-top: 15px;}
  .sidenav a {font-size: 18px;}
}
"""

print("[{timestamp}] Starting run".format(timestamp=datetime.datetime.now()))

session = requests.session()

results = session.get('https://rally1.rallydev.com/slm/schema/v2.0/workspace/{workspace_oid}'.format(workspace_oid=workspace_oid), auth=(user,password)).json()
schema = sorted(results['QueryResult']['Results'], key=itemgetter('Name'))
nav = ''
tables = ''
table_row = ''

for object_type in schema:
    nav = nav + '<a href="#{object_name}">{object_name}</a><br>'.format(object_name=object_type['ElementName'])
    table_rows = ''

    if object_type['Abstract']:
        continue

    attributes = sorted(object_type['Attributes'], key=itemgetter('ElementName'))

    for attrib in attributes:
        if attrib['Custom'] and not include_custom_fields:
            continue

        schema_type = attrib['SchemaType']
        if attrib['AttributeType'] == 'OBJECT':
            schema_type = '<a href="#{object_name}">{schema_type}</a>'.format(object_name=attrib['SchemaType'],schema_type=attrib['SchemaType'])
        elif (attrib['RealType'] == 'MULTI_VALUE' and attrib['Custom'] == False) or (attrib['AttributeType'] == 'COLLECTION' and attrib['RealType'] == 'COLLECTION'):
            schema_type = '<a href="#{object_name}">{schema_type}</a>'.format(object_name=attrib['AllowedValueType']['_refObjectName'],schema_type=attrib['SchemaType'])

        attribute_type = attrib['AttributeType']
        if 'RealType' in attrib and attrib['RealType'] != 'COLLECTION':
            attribute_type = attrib['RealType']

        table_row = '<tr><td>{element_name}</td><td>{attribute_type}</td><td>{schema_type}</td><td>{max_length}</td><td>{max_fractional_digits}</td><td>{filterable}</td><td>{read_only}</td><td>{required}</td><td>{sortable}</td><td><a href="{ref}" target="_blank">Schema Details</a></td></tr>\n' \
            .format(element_name=attrib['ElementName'],attribute_type=attribute_type,schema_type=schema_type,max_length=attrib['MaxLength'],max_fractional_digits=attrib['MaxFractionalDigits'],filterable=attrib['Filterable'],read_only=attrib['ReadOnly'],required=attrib['Required'],sortable=attrib['Sortable'],ref=attrib['_ref'])
        table_rows = table_rows + table_row

    tables = tables + '<h2 id="{element_name}">{object_name}</h2>\n<table>\n<tr><th>Element Name</th><th>Attribute Type</th><th>Schema Type</th><th>Max Length</th><th>Max Fractional Digits</th><th>Filterable</th><th>Read Only</th><th>Required</th><th>Sortable</th><th>Details</th></tr>\n{table_rows}</table>\n\n'.format(element_name=object_type['ElementName'],object_name=object_type['Name'],table_rows=table_rows)

html = '<html><head><style>\n{css}\n</style></head><body><div class="sidenav">{nav}</div><div class=main>\n{tables}\n</div></body></html>'.format(css=css,nav=nav,tables=tables)
with open('field_defs.html', 'w') as f:
    f.write(html)

print(tables)

print("[{timestamp}] Wrote file field_defs.html".format(timestamp=datetime.datetime.now()))
print("[{timestamp}] Finished run".format(timestamp=datetime.datetime.now()))
