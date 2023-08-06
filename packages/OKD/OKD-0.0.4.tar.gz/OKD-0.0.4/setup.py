import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
	name = 'OKD',
	version = '0.0.4',
	author = 'Harish Sita',
	author_email = 'hsista@stevens.edu',
	description = 'Online Knee Detection Model',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/harish2sista/OKD',
	project_urls = {
		'Bug Tracker': 'https://github.com/harish2sista/OKD/issues'
	},
	license = 'BSD 3-Clause License',
	packages = ['OKD'],
	install_requires = ['numpy', 'joblib', 'sklearn', 'scikit-spatial']
	)