# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_fossy']

package_data = \
{'': ['*']}

install_requires = \
['certifi==2021.10.8',
 'charset-normalizer==2.0.7',
 'idna==3.3',
 'pydantic==1.8.2',
 'requests-toolbelt==0.9.1',
 'requests==2.26.0',
 'typing-extensions==3.10.0.2',
 'urllib3==1.26.7']

entry_points = \
{'console_scripts': ['easy_fossy = easy_fossy:easy_fossy']}

setup_kwargs = {
    'name': 'easy-fossy',
    'version': '2.0.5',
    'description': 'fossology API wrapper in python 3.10',
    'long_description': '# easy_fossy\n\n[![Snake fonts](https://see.fontimg.com/api/renderfont4/mLZ3a/eyJyIjoiZnMiLCJoIjoxNzEsInciOjI2MjUsImZzIjo2NSwiZmdjIjoiIzAwMDAwMCIsImJnYyI6IiNGRkZGRkYiLCJ0IjoxfQ/ZWFzeV9mb3NzeQ/terasong.png)](https://www.fontspace.com/category/snake) For Font credit Refer <1>\n\nAccessing fossy api is made easier (requires python 3.10)\n\n[Production Index Registry](https://pypi.org/project/easy-fossy/)\n\n[Test Index Registry](https://test.pypi.org/project/easy-fossy/)\n\n```\npip install easy-fossy\n```\n\nRequires\n\n```\n#### 1. python 3.10\n```\n\n(uses latest structural matching case patterms)\n\n```\n#### 2. pip install easy-fossy\n\n```\n\n```\n#### 3. configure your server in config.ini\n```\n\n(config.ini file with below contents is essential & effortless kickstart)\n\n```\n[test]\nurl = http://fossology-test.com:port/repo/api/v1/\nuname =\npwd =\naccess = write\nbearer_token = Bearer OHNSUFaI6OtoFNz\ntoken_valdity_days = 365\ntoken_expire = 2022-10-29\nreports_location = reports/\ngroup_name = fossy\n\n[prod]\nurl = http://fossology.com:port/repo/api/v1/\nuname =\npwd =\naccess = write\nbearer_token = Bearer OHNSUFaI6OtoFNz\ntoken_valdity_days = 365\ntoken_expire = 2022-10-29\nreports_location = reports/\ngroup_name = fossy\n```\n\n```\n#### 4.  Kickstart straight away with example.py\n```\n\n[example.py](https://github.com/dineshr93/easy_fossy/blob/master/example.py)\n\n```\nUseful functions to import and try\n\n    from easy_fossy import easy_fossy as fossy\n\n\nTo set the location of config.ini file and get the instance to access all the methods use below code\n\n\n    use_fossy_to=fossy(\'location/config.ini\',\'test\')\n\n\n    use_fossy_to=fossy(\'location/config.ini\',\'prod\')\n\n\n1. use_fossy_to.delete_uploads_by_upload_id(upload_id=7)\n\n2. use_fossy_to.trigger_analysis_for_git_upload_package(\n    git_url=\'https://github.com/dineshr93/pageres\', branch_name=\'master\', folder_id=1)\nAvoids duplicate uploads\n\n3. use_fossy_to.trigger_analysis_for_url_upload_package(\n    file_download_url=\'https://github.com/dineshr93/pageres/archive/refs/heads/master.zip\',\n    file_name=\'pageres.zip\', branch_name=\'\', folder_id=1)\nAvoids duplicate uploads\n\n4. use_fossy_to.trigger_analysis_for_upload_package(\n    file_path=\'uploads/commons-lang3-3.12.0-src.zip\', folder_id=1)\nAvoids duplicate uploads\n\n5. use_fossy_to.trigger_analysis_for_upload_id(\n    upload_id=4, folder_id=1)\n\n6. use_fossy_to.get_upload_id_by_giturl_package_upload(git_url=\'https://github.com/dineshr93/pageres\',\n                                        branch_name=\'master\', upload_name=\'\',\n                                       folder_id=1, upload_desc=\'\', visibility=Public.public)\n\n7. use_fossy_to.get_upload_id_by_download_url_package_upload(\n    file_download_url=\'https://github.com/dineshr93/pageres/archive/refs/heads/master.zip\',\n    file_name=\'pageres\', folder_id=1, upload_desc=\'commons-io-2.11.0\', visibility=Public.public)\n\n\n8. use_fossy_to.get_upload_id_by_local_package_upload(\n    file_path=\'uploads/commons-io-2.11.0-src.zip\', folder_id=1, upload_desc=\'commons-io-2.11.0\',\n    visibility=Public.public)\n\n9. use_fossy_to.get_licenses_found_by_agents_for_uploadid\n        (upload_id=2, show_directories=True, agents=[\n                Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name,\n                Agent.reportImport.name,\n                Agent.reso.name])\n\n\n10. use_fossy_to.get_all_uploads_based_on(folder_id=1, is_recursive=True,\n                         search_pattern_key=\'\', upload_status=ClearingStatus.Open,\n                         assignee=\'\', since_yyyy_mm_dd=\'\', page=1, limit=1000)\n\n\n11. use_fossy_to.get_upload_summary_for_uploadid(upload_id=2)\n\n\n12. use_fossy_to.apply_action_to_folderid(actions=Action.move, folder_id=6, parent_folder_id=2)\n\n13. use_fossy_to.delete_folder_by_id(folder_id=3)\n\n14. use_fossy_to.get_all_folders()\n\n\n15. use_fossy_to.create_folder_under_parent_folder_id(\n    parent_folder_id=1, folder_name=\'test\')\n\n16. use_fossy_to.change_folder_name_or_desc(folder_id=3, new_folder_name=\'\', new_folder_desc=\'\')\n\n17. use_fossy_to.get_folder_info_by_id(folder_id=11)\n\n18. use_fossy_to.get_all_folders()\n\n19. use_fossy_to.generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)\n\n20. use_fossy_to.get_job_info_by_id(job_id=3)\n\n\n21. use_fossy_to.get_job_info_by_upload_id(job_id=3)\n\n22. use_fossy_to.get_all_jobs()\n\nFrom 1.0.6\n23. use_fossy_to.get_all_license_based_on(is_active=\'true\', license_kind=Kind.main, page=1, limit=1)\n\n24. sns = use_fossy_to.get_all_license_short_names_based_on(\n        is_active=\'true\', license_kind=Kind.main, contains_key=\'gp\', page=1, limit=10000)\n    for i, sn in enumerate(sns, start=1):\n        print(f\'{i}. {sn}\')\n\nFrom 1.0.9\n25. use_fossy_to.get_license_by_short_name(short_name=\'AGPL-1.0\')\n\n26. use_fossy_to.add_new_license(unique_short_name=\'\', new_full_name=\'\', new_license_text=\'\',\n                new_url=\'\', new_risk=2, isCandidate=True, merge_request=False)\n\n27. use_fossy_to.update_license_info_by_short_name(short_name=\'\', new_full_name=\'\', new_license_text=\'\', new_url=\'\', new_risk=2)\n\n28. use_fossy_to.search_files_based_on(self, filename_wildcard: str, searchType: SearchType, uploadId: int, tag: str, filesizemin_bytes: int, filesizemax_bytes: int, license: str, copyright: str) -> List[SearchResults] | Info:\n--- give SearchType.Directory and filename_wildcard = \'draw%\' (for draPaintIO.zip)\n\n29 use_fossy_to.get_file_by_any_one_of_sha1_or_md5_or_sha256(self, sha1: str = \'\', md5: str = \'\', sha256: str = \'\') -> str | List[File]:\n--- give only one hash of any of 3 format sha1 or sha256 or md5\n--- returns list if even only data is there else it will return \'not found\' string.\n\n```\n\n### =====================================================================\n\n### License: MIT\n\n```\nMIT License\n\nCopyright (c) 2021 Dinesh Ravi\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n```\n\n<1>\nFont by Tehisa by Sealoung\nhttps://www.fontspace.com/category/snake\nLicense: Personal Use Free\n',
    'author': 'dinesh_ravi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
