This will output an HTML file that effectively contains field definitions using the Rally schema

# Installation
Install requests:

`pip install requests`

# Configuration
Set username and password in lines 7 and 8 

Set your workspace object ID in line 9 (use this page to find workspace OID https://knowledge.broadcom.com/external/article/47763/rally-find-object-ids-of-current-worksp.html)

Set whether you want to include custom fields in the output or not in line 10



# Execution
Run the script:

`python publish_schema.py`

Output will be field_def.html


# Sample Output
![Screenshot](https://github.com/davidledeaux/PublishSchema/blob/main/ScreenShot.png?raw=true)


# Misc
This script is provided without warranty or support.
