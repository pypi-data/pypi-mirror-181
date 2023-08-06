# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['customer_segmentation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'customer-segmentation',
    'version': '0.0.1',
    'description': 'The goal of the project is to group consumers into clusters using the elbow approach.',
    'long_description': "#### Purpose of the Package\n\n# Customer-Segmentation-for-for-Mall\nThe goal of the project is to group consumers into clusters using the elbow approach. The project also includes scatter plots to show the relationships between the variables and dataset's columns. Customer Segmentation is the subdivision of a marketplace into discrete client agencies that proportion comparable characteristics. Customer Segmentation may be a effective method to perceive unhappy client needs. Using the above statistics groups can then outperform the opposition through growing uniquely attractive merchandise and services. K method clustering is one of the maximum famous clustering algorithms and normally the primary component practitioners practice while fixing clustering duties to get an concept of the shape of the dataset. The purpose of K method is to organization statistics factors into wonderful non-overlapping subgroups. One of the important software of K method clustering is segmentation of clients to get a higher information of them which in flip may be used to growth the sales of the company.\n\n#### Tools used\nK-means clustering\nElbow method\nLibraries- Pandas, Matplotlib, Numpy, Seaborn, Skleran libraries\n\n#### Getting started\nThe package can be installed using pip\n```bash\npip install customer_segmentation\n```\n### Where can be used\nThe most common ways companies segment their customer base are:\n1) Demographic information such as gender, age, marital and marital status, income, education and occupation;\n2) Geographic Information. It depends on the scale of your business. For localized businesses, this information may relate to a specific city or county. For large companies, this may mean the customer's city, state or even country of residence;\n3) Psychographic data such as social class, lifestyle, and personality traits; \n4) Behavioral data such as spending and consumption habits, product/service usage and desired benefits.\n\n#### Usage\nThis package can be used for the \n-Determine the right price for the product.\n-Create individualized marketing initiatives.\n-Create the best distribution plan possible.\n-Select particular product features for implementation.\n-Set new product development activities as a priority.\n\n### Data\nThe data was taken from Kaggle competition datasets\n\n\n",
    'author': 'Bella Martirosyan',
    'author_email': 'bella.martirosyan2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bellamartirosyan/Customer-Segmentation-for-for-Mall',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
